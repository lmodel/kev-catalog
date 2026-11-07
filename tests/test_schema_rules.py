"""Checks that the adapt copy can sit beside LOKF and the neighbours' copies."""

import hashlib
import keyword
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent

# What a host may import beside this schema's adapt copy: LOKF's schema, pinned by
# the sidecar, and the adapt copies other lmodel repositories release. Each
# neighbour but cve is the schema asset of the newest release that carries one,
# downloaded and checked against the release's .sha256 and its build-provenance
# attestation on 2026-11-03, and pinned here by that checksum.
SOURCE = ROOT / "src" / "kev_catalog" / "schema" / "kev_catalog.yaml"
COPY = ROOT / ".lokf" / "schema" / "kev-catalog.yaml"
LOKF = ROOT / ".lokf" / "schema" / "lokf.yaml"
NEIGHBOURS = {
    # lmodel/slsa v0.10.0, schema-v0.10.0-slsa.yaml
    "slsa.yaml": "9eeb68decc918565886794fe4eb6e32e1fee0620688cc699961c227242a2f4c2",
    # lmodel/github-actions v0.5.0, schema-v0.5.0-github-actions.yaml
    "github-actions.yaml": "375794f7343936ae8c555e8c060c2790346661e7d81fa84d15a761fd5a329969",
    # lmodel/in-toto v0.3.0, schema-v0.3.0-in-toto.yaml
    "in-toto.yaml": "b1d15be557adfbcd538ab75ec9d43f558027d4bcbd150d72d370e83c9602f25b",
    # lmodel/oscal v0.1.2, schema-v0.1.2-oscal.yaml
    "oscal.yaml": "4eb56d7d1106463ed0a2255a29af14b8d619741acc29863d1e86eb3f8923c710",
    # lmodel/spdx v0.1.1, schema-v0.1.1-spdx.yaml
    "spdx.yaml": "3411cf5d19b1955f0362988c542984e4c817417c7b7b7892647aba1adf1ddd4a",
    # lmodel/stix v0.1.0, schema-v0.1.0-stix.yaml
    "stix.yaml": "3837d097c0cd48e0d2a98d118003c099d1290333f5b973aee85a7017bae344c9",
    # lmodel/cve v0.1.0, schema-v0.1.0-cve.yaml
    "cve.yaml": "33e6086a81ac8e4cdc1e6143598cfcc961cbc1864ad9268773da9e863c652a73",
    # lmodel/uco v0.3.0, schema-v0.3.0-uco.yaml
    "uco.yaml": "78bc3a266fa463ba380da7290adcbdfb1b8e1b7cef1ceb992bf8b1bed9b7b758",
}
NEIGHBOUR_DIR = ROOT / "tests" / "neighbours"
ELEMENT_KINDS = ("classes", "enums", "types", "subsets")

# Keys the copy shares with a neighbour, each under another IRI there. LinkML keeps
# one namespace, and the JSON-LD context gives each key one IRI across a composite,
# so in a host that imports both copies one of them projects under the other's IRI.
# These are CISA's own keys, which must stay as they are for a real file to validate;
# lokf issue #169 asks `lokf adapt` for a --beside option that would rename them in
# the copy. A new overlap fails this test. No class, enum or type is shared.
SHARED_WITH_NEIGHBOURS = {name: set() for name in NEIGHBOURS} | {
    "cve.yaml": {"product"},
    "stix.yaml": {"count", "product"},
}

# The classes `just lokf-adapt` re-roots on Concept, which the README lists for the
# plugins' Known LOKF types setting.
ROOTS = {"KevCatalog", "KevVulnerability"}

# What the copy renames because LOKF defines the name, keeping the IRI the source
# gives it, and the identifier it drops for LOKF's `id`.
RENAMED = {"title": "kev_title"}
DROPPED = {"cveID"}

MAPPING_KEYS = (
    "mappings",
    "exact_mappings",
    "close_mappings",
    "related_mappings",
    "narrow_mappings",
    "broad_mappings",
)


def _load(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _expander(doc):
    """A function that expands a CURIE by the prefixes a schema file binds."""
    prefixes = doc.get("prefixes") or {}

    def expand(curie):
        prefix, _, local = curie.partition(":")
        return prefixes[prefix] + local if prefix in prefixes else curie

    return expand


def _names(path):
    """Each kind of element a schema file declares, and every slot and attribute
    name with the IRI it expands to."""
    doc = _load(path)
    expand = _expander(doc)
    default = doc.get("default_prefix")
    elements = {kind: set(doc.get(kind) or {}) for kind in ELEMENT_KINDS}
    slots = {}
    owners = [doc.get("slots") or {}]
    owners += [
        (cls or {}).get("attributes") or {}
        for cls in (doc.get("classes") or {}).values()
    ]
    for owner in owners:
        for name, slot in owner.items():
            uri = (slot or {}).get("slot_uri") or f"{default}:{name}"
            slots.setdefault(name, set()).add(expand(uri))
    return elements, slots


def _mappings(node):
    """Every mapping value anywhere in a parsed schema file."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key in MAPPING_KEYS:
                yield from value if isinstance(value, list) else [value]
            else:
                yield from _mappings(value)
    elif isinstance(node, list):
        for item in node:
            yield from _mappings(item)


def test_neighbours_are_the_pinned_files():
    """Each neighbour copy is byte for byte the asset its release published, and
    no copy sits there unpinned."""
    assert {p.name for p in NEIGHBOUR_DIR.iterdir()} == set(NEIGHBOURS)
    for name, sha256 in NEIGHBOURS.items():
        digest = hashlib.sha256((NEIGHBOUR_DIR / name).read_bytes()).hexdigest()
        assert digest == sha256, name


def test_names_apart_from_lokf():
    """No class, enum, type or subset name of the copy is LOKF's, and a slot name
    the two share carries LOKF's IRI."""
    elements, slots = _names(COPY)
    their_elements, their_slots = _names(LOKF)
    for kind in ELEMENT_KINDS:
        assert not elements[kind] & their_elements[kind], kind
    for name in slots.keys() & their_slots.keys():
        assert slots[name] == their_slots[name], name


def test_names_apart_from_neighbours():
    """A class, enum, type or subset name is the copy's alone, and the only keys it
    shares with a neighbour are the listed ones."""
    elements, slots = _names(COPY)
    for name in NEIGHBOURS:
        their_elements, their_slots = _names(NEIGHBOUR_DIR / name)
        for kind in ELEMENT_KINDS:
            assert not elements[kind] & their_elements[kind], (name, kind)
        assert slots.keys() & their_slots.keys() == SHARED_WITH_NEIGHBOURS[name], name


def test_the_copy_renames_what_lokf_defines_and_keeps_the_iris():
    """Each name the copy takes from LOKF's way is renamed with its source IRI, the
    identifier gives way to LOKF's `id`, and nothing else is renamed."""
    source, copy = _load(SOURCE), _load(COPY)
    expand_source, expand_copy = _expander(source), _expander(copy)
    for old, new in RENAMED.items():
        assert new in copy["slots"] and old not in copy["slots"], old
        assert expand_copy(copy["slots"][new]["slot_uri"]) == expand_source(
            source["slots"][old]["slot_uri"]
        ), old
    assert set(copy["slots"]) == (set(source["slots"]) - set(RENAMED) - DROPPED) | set(
        RENAMED.values()
    )
    assert set(copy["classes"]) == set(source["classes"])
    assert set(copy["enums"]) == set(source["enums"])


def test_copy_roots_the_concept_classes():
    """The copy re-roots exactly the two classes on Concept, and imports nothing but
    the LinkML types and LOKF."""
    doc = _load(COPY)
    rooted = {
        name for name, cls in doc["classes"].items() if cls.get("is_a") == "Concept"
    }
    assert rooted == ROOTS
    assert doc["imports"] == ["linkml:types", "lokf"]


def test_the_copy_keeps_the_enum_values_as_strings():
    """YAML reads an unquoted Yes or No as a boolean, so this holds the copy's
    values to CISA's spelling, as a string, after adapt has rewritten the file."""
    values = _load(COPY)["enums"]["KevForensicTriage"]["permissible_values"]
    assert set(values) == {"Yes", "No"}
    values = _load(SOURCE)["enums"]["KevForensicTriage"]["permissible_values"]
    assert set(values) == {"Yes", "No"}


def test_mappings_use_a_bound_prefix():
    """Every mapping in the copy is a CURIE whose prefix the copy binds. A full
    address that no prefix covers makes every `lokf convert --schema` over the copy
    warn that it has no namespace."""
    doc = _load(COPY)
    prefixes = doc.get("prefixes") or {}
    mappings = list(_mappings(doc))
    assert mappings
    for mapping in mappings:
        prefix, sep, _ = mapping.partition(":")
        assert sep and prefix in prefixes, mapping


def test_names_are_safe_for_every_generator():
    """No slot is a Python keyword, which breaks the dataclasses, or `index`, whose
    page would overwrite the docs index, and no two names differ only by case, which
    collide on a case-insensitive filesystem."""
    doc = _load(SOURCE)
    slots = set(doc["slots"])
    assert not {s for s in slots if keyword.iskeyword(s)}
    assert "index" not in slots
    names = slots | set(doc["classes"]) | set(doc["enums"]) | {doc["name"]}
    lowered = Counter(name.lower() for name in names)
    assert not [name for name, n in lowered.items() if n > 1]


def test_prefixes_agree_with_lokf_and_the_neighbours():
    """A prefix the copy shares with LOKF or a neighbour binds the same namespace,
    so a composite that imports them does not bind one prefix twice."""
    mine = _load(COPY)["prefixes"]
    others = [LOKF, *(NEIGHBOUR_DIR / name for name in NEIGHBOURS)]
    for path in others:
        theirs = _load(path).get("prefixes") or {}
        for prefix in mine.keys() & theirs.keys():
            assert mine[prefix] == theirs[prefix], (path.name, prefix)
