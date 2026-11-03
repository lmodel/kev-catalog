"""Checks that the schema renders the edition of CISA's JSON schema the pins name.

tests/upstream/ holds exact copies of CISA's JSON schema and the licence of its
mirror, which their CC0 terms allow. These tests read them offline. They hold the
copies to their pins, the schema header to the pins, and walk the copy: every
definition, property, required-list member, cardinality, type, format and pattern
must have its element here, and every keyword must be one this walk reads, so a
new edition with a rule it cannot yet state fails here. Each departure is listed
below with its reason.
"""

import hashlib
import importlib.util
import json
import re
from pathlib import Path

import jsonschema
import pytest
import yaml
from linkml_runtime import SchemaView

ROOT = Path(__file__).parent.parent
SCHEMA = ROOT / "src" / "kev_catalog" / "schema" / "kev_catalog.yaml"
UPSTREAM_DIR = Path(__file__).parent / "upstream"
COPY = UPSTREAM_DIR / "known_exploited_vulnerabilities_schema.json"
LICENCE = UPSTREAM_DIR / "LICENSE"


def _load(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


WATCH = _load("watch_pins", ROOT / "scripts" / "check_upstream_release.py")
SV = SchemaView(str(SCHEMA))
HEADER = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
UPSTREAM = json.loads(COPY.read_text(encoding="utf-8"))

# Each object the upstream defines, by JSON pointer, and the class that renders it.
CLASS_FOR = {"#": "KevCatalog", "#/$defs/vulnerability": "KevVulnerability"}

# Every departure from CISA's JSON schema, each with its reason. The walk below
# applies each one, so an entry here that stops being true fails, and a departure
# not listed fails.
#
# Keys the file carries that the JSON schema does not list. The upstream's objects
# are open, so CISA's schema accepts them, and this schema's classes are closed.
EXTRA_KEYS = {
    "KevCatalog": {
        "title": "Every KEV file carries it, and a real file must validate unchanged.",
    },
}
# Keys typed as a plain string upstream whose values the upstream names only in the
# key's description. An enum says what the sentence says, and the real file agrees.
ENUMS_FROM_THE_DESCRIPTION = {
    "knownRansomwareCampaignUse": "KevRansomwareCampaignUse",
    "forensicTriage": "KevForensicTriage",
}
# What holds everywhere, and so has no element to compare.
GENERAL_DEPARTURES = {
    "closed classes": (
        "The upstream's objects are open, since it does not set additionalProperties. "
        "LinkML closes every class, so an unnamed key fails here and passes upstream. "
        "A new key in a real file should be read before it is admitted."
    ),
    "null on an optional key": (
        "gen-json-schema lets an optional slot be null, which the upstream's string "
        "types refuse. No generator option changes it, and the real file holds no null."
    ),
    "a closed list of keywords": (
        "The JSON schema's own title, description and url describe the file, not a "
        "record, so they map to the schema's header and not to an element."
    ),
}

# The keywords this walk knows how to compare, and those that only describe. A
# keyword outside both (oneOf, anyOf, if, then, enum, minItems,
# additionalProperties and so on) is a rule the schema does not yet state.
READ_KEYWORDS = {
    "$defs",
    "$ref",
    "format",
    "items",
    "pattern",
    "properties",
    "required",
    "type",
}
DESCRIBING_KEYWORDS = {"$schema", "description", "title", "url"}

RANGE_FOR_FORMAT = {"date": "date", "date-time": "datetime"}
RANGE_FOR_TYPE = {"string": "string", "integer": "integer"}


def _objects():
    """Each object the upstream defines, with its pointer and its class."""
    for pointer, class_name in CLASS_FOR.items():
        node = UPSTREAM
        for part in pointer.lstrip("#/").split("/"):
            if part:
                node = node[part]
        yield pointer, class_name, node


def _properties():
    """Each property of each object, with its class and whether it is required."""
    for pointer, class_name, node in _objects():
        for name, prop in node["properties"].items():
            yield pointer, class_name, name, prop


PROPERTIES = list(_properties())
PROPERTY_IDS = [f"{c}.{n}" for _, c, n, _ in PROPERTIES]


def _resolve(pointer):
    """The node of the copy a `#/a/b` pointer names."""
    node = UPSTREAM
    for part in pointer.lstrip("#").strip("/").split("/"):
        if part:
            node = node[part]
    return node


def _keywords(node, property_names=False):
    """Every JSON Schema keyword in the copy. Under `properties` and `$defs`, the
    keys are names and not keywords."""
    if isinstance(node, dict):
        for key, value in node.items():
            if not property_names:
                yield key
            yield from _keywords(value, property_names=key in ("properties", "$defs"))
    elif isinstance(node, list):
        for item in node:
            yield from _keywords(item)


def test_the_copy_is_the_pinned_file():
    """The copy of the JSON schema has the pinned hashes."""
    data = COPY.read_bytes()
    assert hashlib.sha256(data).hexdigest() == WATCH.PINNED_SHA256
    blob = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    assert blob == WATCH.PINNED_BLOBS[WATCH.SCHEMA_FILE]


def test_the_licence_copy_is_the_pinned_file():
    """The copy of the licence is the file the watch pins, and it opens with what
    NOTICE says it opens with."""
    data = LICENCE.read_bytes()
    blob = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    assert blob == WATCH.PINNED_BLOBS[WATCH.LICENCE_FILE]
    text = data.decode("utf-8")
    assert "CISA Logo or DHS Seal" in text.splitlines()[0]
    assert "CC0 1.0 Universal" in text


def test_the_notice_states_the_upstream_terms():
    """NOTICE names the licence, the logo and seal, and no endorsement."""
    notice = (ROOT / "NOTICE").read_text(encoding="utf-8")
    flat = " ".join(notice.split())
    for phrase in (
        "Creative Commons Zero 1.0 Universal",
        "CISA Logo or the DHS Seal",
        "implies no endorsement",
        f"{WATCH.PINNED_EDITION} (commit {WATCH.PINNED_COMMIT[:12]})",
    ):
        assert phrase in flat, phrase


def test_the_header_names_the_pinned_edition():
    """The schema's header and the watch name one edition, one commit, one blob."""
    assert HEADER["version"] == WATCH.PINNED_EDITION
    assert HEADER["source"] == WATCH.PINNED_SOURCE
    annotations = HEADER["annotations"]
    assert annotations["upstream_schema_commit"] == WATCH.PINNED_COMMIT
    assert annotations["upstream_schema_blob"] == WATCH.PINNED_BLOBS[WATCH.SCHEMA_FILE]
    assert annotations["upstream_schema_sha256"] == WATCH.PINNED_SHA256
    assert annotations["upstream_schema_draft"] == UPSTREAM["$schema"]


def test_the_header_keeps_the_family_form():
    """Licence, identifier and name are the family's, and the source is an address
    at the edition, not at a moving branch."""
    assert HEADER["license"] == "Apache-2.0"
    assert HEADER["id"] == "https://w3id.org/lmodel/kev-catalog"
    assert HEADER["name"] == "kev_catalog"
    assert WATCH.PINNED_COMMIT in HEADER["source"]
    assert HEADER["imports"] == ["linkml:types"]


def test_the_copy_is_read_under_the_draft_it_declares():
    """The draft the copy names is the one it is read under, and the copy is valid
    under that draft."""
    validator = jsonschema.validators.validator_for(UPSTREAM, default=None)
    assert validator is not None, UPSTREAM.get("$schema")
    assert validator.META_SCHEMA["$id"].rstrip("#") == UPSTREAM["$schema"].rstrip("#")
    validator.check_schema(UPSTREAM)


def test_every_keyword_of_the_copy_is_one_the_walk_reads():
    """A keyword the walk does not read is a rule it does not compare. A new edition
    with oneOf, if, enum or additionalProperties fails here until the schema states
    the rule, or a departure lists it."""
    found = set(_keywords(UPSTREAM))
    assert found <= READ_KEYWORDS | DESCRIBING_KEYWORDS, sorted(
        found - READ_KEYWORDS - DESCRIBING_KEYWORDS
    )


def test_every_definition_has_a_class():
    """The root and each `$defs` entry have a class, and every class renders one."""
    defined = {"#"} | {f"#/$defs/{name}" for name in UPSTREAM["$defs"]}
    assert defined == set(CLASS_FOR)
    assert set(CLASS_FOR.values()) == set(SV.all_classes())


@pytest.mark.parametrize(
    ("pointer", "class_name", "name", "prop"), PROPERTIES, ids=PROPERTY_IDS
)
def test_every_property_has_its_slot(pointer, class_name, name, prop):
    """Each upstream property is a slot of its class, under its own name."""
    assert name in SV.class_slots(class_name), (class_name, name)


@pytest.mark.parametrize(
    ("pointer", "class_name", "name", "prop"), PROPERTIES, ids=PROPERTY_IDS
)
def test_cardinality_matches(pointer, class_name, name, prop):
    """An upstream array is a multivalued slot, and anything else a single value."""
    slot = SV.induced_slot(name, class_name)
    assert bool(slot.multivalued) == (prop.get("type") == "array"), (class_name, name)


@pytest.mark.parametrize(
    ("pointer", "class_name", "name", "prop"), PROPERTIES, ids=PROPERTY_IDS
)
def test_range_matches(pointer, class_name, name, prop):
    """A string, date, date-time or integer has its range, and a reference or an
    array of them has the class or the type of its items. The enums are the listed
    departures."""
    slot = SV.induced_slot(name, class_name)
    item = prop.get("items", prop)
    if name in ENUMS_FROM_THE_DESCRIPTION:
        assert item["type"] == "string"
        assert slot.range == ENUMS_FROM_THE_DESCRIPTION[name]
    elif "$ref" in item:
        assert slot.range == CLASS_FOR[item["$ref"]]
    elif "format" in item:
        assert slot.range == RANGE_FOR_FORMAT[item["format"]]
    else:
        assert slot.range == RANGE_FOR_TYPE[item["type"]]


@pytest.mark.parametrize(
    ("pointer", "class_name", "name", "prop"), PROPERTIES, ids=PROPERTY_IDS
)
def test_pattern_matches(pointer, class_name, name, prop):
    """A pattern is written as the upstream writes it, anchors and all, on the value
    or on each item, and nowhere else."""
    slot = SV.induced_slot(name, class_name)
    assert slot.pattern == prop.get("items", prop).get("pattern"), (class_name, name)


@pytest.mark.parametrize(
    ("pointer", "class_name", "node"),
    [o for o in _objects()],
    ids=lambda v: v if isinstance(v, str) else "",
)
def test_required_matches(pointer, class_name, node):
    """The class's required slots are exactly the upstream's required list."""
    required = {
        s for s in SV.class_slots(class_name) if SV.induced_slot(s, class_name).required
    }
    assert required == set(node["required"]), class_name


@pytest.mark.parametrize(
    ("pointer", "class_name", "node"),
    [o for o in _objects()],
    ids=lambda v: v if isinstance(v, str) else "",
)
def test_no_slot_goes_beyond_the_upstream_but_the_listed_ones(
    pointer, class_name, node
):
    """A class's slots are the upstream's properties and the listed extra keys."""
    expected = set(node["properties"]) | set(EXTRA_KEYS.get(class_name, {}))
    assert set(SV.class_slots(class_name)) == expected, class_name


@pytest.mark.parametrize("name", sorted(ENUMS_FROM_THE_DESCRIPTION))
def test_an_enum_holds_the_values_its_description_names(name):
    """Each value the upstream's sentence names in single quotes is a permissible
    value, spelled as it spells it, and the enum has no other."""
    described = _resolve(f"#/$defs/vulnerability/properties/{name}")["description"]
    named = set(re.findall(r"'(\w+)'", described))
    assert named, name
    enum = SV.get_enum(ENUMS_FROM_THE_DESCRIPTION[name])
    assert set(enum.permissible_values) == named


def test_every_element_is_described_and_its_path_resolves():
    """Each class, slot and enum has a description, and each `upstream_path`
    annotation names a node of the copy. A key from the file alone says so."""
    elements = [
        *SV.all_classes().values(),
        *SV.all_slots().values(),
        *SV.all_enums().values(),
    ]
    for element in elements:
        assert element.description, element.name
        annotations = element.annotations or {}
        if "upstream_path" in annotations:
            _resolve(annotations["upstream_path"].value)
        else:
            assert element.name in EXTRA_KEYS["KevCatalog"], element.name
            assert annotations["upstream_file_key"].value == element.name


def test_each_enum_value_has_its_own_description():
    """Every permissible value says what it means, in this project's words."""
    for enum in SV.all_enums().values():
        for value in enum.permissible_values.values():
            assert value.description, (enum.name, value.text)


def _words(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def _upstream_descriptions(node):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "description" and isinstance(value, str):
                yield value
            else:
                yield from _upstream_descriptions(value)


def test_no_description_pastes_the_upstream():
    """No description here shares a run of five words with one of CISA's, so they
    stay this project's own, as the AI covenant asks."""
    runs = set()
    for text in _upstream_descriptions(UPSTREAM):
        words = _words(text)
        runs |= {tuple(words[i : i + 5]) for i in range(len(words) - 4)}
    mine = [
        (e.name, e.description)
        for e in [
            *SV.all_classes().values(),
            *SV.all_slots().values(),
            *SV.all_enums().values(),
        ]
    ]
    for enum in SV.all_enums().values():
        mine += [(v.text, v.description) for v in enum.permissible_values.values()]
    for name, text in mine:
        words = _words(text)
        shared = {tuple(words[i : i + 5]) for i in range(len(words) - 4)} & runs
        assert not shared, (name, shared)


def test_each_departure_says_why():
    """No departure is listed without a reason."""
    reasons = [*GENERAL_DEPARTURES.values(), *EXTRA_KEYS["KevCatalog"].values()]
    assert all(len(reason.split()) > 5 for reason in reasons)
