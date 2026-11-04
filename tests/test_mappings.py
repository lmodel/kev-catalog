"""Checks the schema's mappings: each prefix bound, each lmodel target real.

The schema's mappings are the one home for what it crosses to. Every mapping names
a CURIE whose prefix the schema binds, so a projection raises no warning. Every
target in a namespace a neighbour's adapt copy holds must be a term of that copy
under tests/neighbours/, so a rename there fails here. The table below is the list
the README gives: a mapping added or dropped fails until both follow.
"""

from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
SCHEMA = ROOT / "src" / "kev_catalog" / "schema" / "kev_catalog.yaml"
NEIGHBOUR_DIR = ROOT / "tests" / "neighbours"
DOC = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))

KINDS = (
    "exact_mappings",
    "close_mappings",
    "related_mappings",
    "narrow_mappings",
    "broad_mappings",
)

# Every mapping, by element and kind. Each target was read at its source on
# 2026-11-03: DCAT 3, schema.org, Dublin Core, SKOS, Wikidata's items Q631425 and
# Q125498394 and properties P3587 and P3624, SPDX 3.0.1's model pages, SEPSES's CVE
# ontology, and the neighbours' copies.
MAPPINGS = {
    "KevCatalog": {
        "broad_mappings": {"dcat:Dataset", "schema:Dataset"},
        "related_mappings": {
            "dcat:Catalog",
            "wd:Q125498394",
            "spdx3:Security/ExploitCatalogType/kev",
        },
    },
    "KevVulnerability": {
        "close_mappings": {"spdx3:Security/ExploitCatalogVulnAssessmentRelationship"},
        "related_mappings": {
            "wd:Q631425",
            "stix:StixVulnerability",
            "spdx3:Security/Vulnerability",
            "sepses_cve:CVE",
            "dcat:CatalogRecord",
            "cve:CveRecord",
        },
    },
    "title": {"exact_mappings": {"dcterms:title"}},
    "catalogVersion": {
        "exact_mappings": {"dcat:version"},
        "close_mappings": {"schema:version"},
    },
    "dateReleased": {"close_mappings": {"dcterms:issued", "schema:datePublished"}},
    "count": {"related_mappings": {"schema:numberOfItems"}},
    "vulnerabilities": {"broad_mappings": {"dcterms:hasPart"}},
    "cveID": {"exact_mappings": {"cve:cveId", "wdt:P3587"}},
    "vendorProject": {"close_mappings": {"cve:vendor"}},
    "product": {"close_mappings": {"cve:product"}},
    "vulnerabilityName": {"related_mappings": {"cve:title"}},
    "dateAdded": {"close_mappings": {"dcterms:issued"}},
    "shortDescription": {"related_mappings": {"cve:descriptions"}},
    "requiredAction": {"related_mappings": {"cve:solutions"}},
    "notes": {"close_mappings": {"skos:note"}},
    "cwes": {
        "close_mappings": {"cve:cweId", "wdt:P3624"},
        "related_mappings": {"sepses_cve:hasCWE"},
    },
}

# The neighbour copy that holds each target's namespace. SPDX's terms live at
# spdx.org, and lmodel/spdx's copy names them by those IRIs.
NEIGHBOUR_OF_PREFIX = {"stix": "stix.yaml", "spdx3": "spdx.yaml", "cve": "cve.yaml"}


def _elements():
    for kind in ("classes", "slots", "enums"):
        yield from (DOC.get(kind) or {}).items()


def _found():
    return {
        name: {k: set(element[k]) for k in KINDS if element.get(k)}
        for name, element in _elements()
        if any(element.get(k) for k in KINDS)
    }


def _targets():
    return sorted(
        {
            t
            for kinds in MAPPINGS.values()
            for targets in kinds.values()
            for t in targets
        }
    )


def _expand(curie, prefixes):
    prefix, _, local = curie.partition(":")
    return prefixes[prefix] + local


def _terms(path):
    """The IRI of every class, slot, attribute and enum a schema file declares, and
    of every permissible value whose meaning it names."""
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    prefixes = doc.get("prefixes") or {}
    default = doc.get("default_prefix")
    terms = set()
    for kind, key in (
        ("classes", "class_uri"),
        ("slots", "slot_uri"),
        ("enums", "enum_uri"),
    ):
        for name, element in (doc.get(kind) or {}).items():
            curie = (element or {}).get(key) or f"{default}:{name}"
            terms.add(_expand(curie, prefixes))
            for value in ((element or {}).get("permissible_values") or {}).values():
                if (value or {}).get("meaning"):
                    terms.add(_expand(value["meaning"], prefixes))
    for cls in (doc.get("classes") or {}).values():
        for name, slot in ((cls or {}).get("attributes") or {}).items():
            curie = (slot or {}).get("slot_uri") or f"{default}:{name}"
            terms.add(_expand(curie, prefixes))
    return terms


def test_the_table_is_the_schema():
    """The schema's mappings are the listed ones, element by element, kind by kind."""
    assert _found() == MAPPINGS


@pytest.mark.parametrize("target", _targets())
def test_every_mapping_has_a_bound_prefix(target):
    """A mapping is a CURIE whose prefix the schema binds."""
    prefix, sep, local = target.partition(":")
    assert sep and local and prefix in DOC["prefixes"], target


def test_no_mapping_uses_a_prefix_lokf_binds_to_another_namespace():
    """LOKF binds `spdx:` to SPDX 2, so SPDX 3.0.1's terms never go under it."""
    assert "spdx" not in DOC["prefixes"]
    assert DOC["prefixes"]["spdx3"] == "https://spdx.org/rdf/3.0.1/terms/"


def test_every_bound_prefix_is_used():
    """Every prefix binding but the schema's own and LinkML's serves a mapping, so
    no binding outlives its use."""
    used = {t.partition(":")[0] for t in _targets()}
    assert set(DOC["prefixes"]) - used == {"kev_catalog", "linkml"}


def test_no_element_maps_to_vulnerability_core():
    """vulnerability-core is being folded in and archived, so nothing here names it."""
    text = SCHEMA.read_text(encoding="utf-8")
    assert "vulnerability_core" not in text
    assert "vulnerability-core" not in text


@pytest.mark.parametrize(
    "target",
    [t for t in _targets() if t.partition(":")[0] in NEIGHBOUR_OF_PREFIX],
)
def test_every_lmodel_target_is_in_its_neighbour_copy(target):
    """A target in a neighbour's namespace is a term that neighbour's adapt copy
    declares, by IRI, so a rename there fails here."""
    prefix = target.partition(":")[0]
    path = NEIGHBOUR_DIR / NEIGHBOUR_OF_PREFIX[prefix]
    assert path.is_file(), path
    assert _expand(target, DOC["prefixes"]) in _terms(path), target


def test_the_one_direction_holds():
    """Mappings across the family point downstream to upstream. This schema may
    map to cve, and it imports nothing of any family member."""
    assert DOC["imports"] == ["linkml:types"]
    assert "nist_nvd" not in DOC["prefixes"]
