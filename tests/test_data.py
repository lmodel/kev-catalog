"""Checks the example data against the schema and its generated models.

Every valid example must load and validate, and every counter-example must fail
at the place its first line names. The JSON Schema the validator generates is
the check that applies every constraint the schema states, so each example is
held to it and to the committed project/jsonschema file. tests/kev_rules.py
holds the rules no generated validator states.

The examples under tests/data/problem/valid/ are valid data that the generated
dataclasses refuse under LinkML 1.12.1: a required multivalued slot treats an
empty list as missing, though CISA's JSON schema and the JSON Schema generated
here accept one. They are validated and loaded through the Pydantic model, but
not through the dataclasses or the example runner. tests/data/README.md says the
same.
"""

import json
from pathlib import Path

import jsonschema
import pytest
import yaml
from linkml.validator import validate
from linkml_runtime.loaders import yaml_loader

import kev_catalog.datamodel.kev_catalog
import kev_catalog.datamodel.kev_catalog_pydantic
from tests.kev_rules import catalogue_faults

ROOT = Path(__file__).parent.parent
DATA = Path(__file__).parent / "data"
SCHEMA = ROOT / "src" / "kev_catalog" / "schema" / "kev_catalog.yaml"
COMMITTED_JSON_SCHEMA = ROOT / "project" / "jsonschema" / "kev_catalog.schema.json"
EXTRACT = DATA / "kev-data" / "extract" / "known_exploited_vulnerabilities.json"

LOADABLE = sorted((DATA / "valid").glob("*.yaml"))
DATACLASSES_REFUSE = sorted((DATA / "problem" / "valid").glob("*.yaml"))
VALID = LOADABLE + DATACLASSES_REFUSE
INVALID = sorted((DATA / "invalid").glob("*.yaml"))


def test_the_example_folders_hold_examples():
    """Each folder the tests below read holds examples, so that no parametrized
    test passes by running over nothing."""
    assert LOADABLE and DATACLASSES_REFUSE and INVALID
    assert json.loads(EXTRACT.read_text(encoding="utf-8"))


def _class(path):
    return path.stem.split("-")[0]


def _load(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("path", LOADABLE, ids=lambda p: p.name)
def test_valid_examples_load_as_dataclasses(path):
    """An example loads into the generated dataclass its file name names."""
    target = getattr(kev_catalog.datamodel.kev_catalog, _class(path))
    assert yaml_loader.load(str(path), target_class=target)


@pytest.mark.parametrize("path", VALID, ids=lambda p: p.name)
def test_valid_examples_load_as_pydantic(path):
    """An example loads into the generated Pydantic class."""
    target = getattr(kev_catalog.datamodel.kev_catalog_pydantic, _class(path))
    assert target.model_validate(_load(path))


@pytest.mark.parametrize("path", VALID, ids=lambda p: p.name)
def test_valid_examples_validate(path):
    """Every valid example passes the validator."""
    report = validate(_load(path), str(SCHEMA), _class(path))
    assert not report.results, [r.message for r in report.results]


def _fails_at(path):
    first = path.read_text(encoding="utf-8").splitlines()[0]
    assert first.startswith("# Fails at: "), (
        f"{path.name}: the first line names where it fails, as # Fails at: /key"
    )
    return first.removeprefix("# Fails at: ").strip()


@pytest.mark.parametrize("path", INVALID, ids=lambda p: p.name)
def test_counter_examples_fail_where_they_say(path):
    """Every counter-example fails the validator at the place its first line
    names, as `# Fails at: <JSON pointer>`, and nowhere else, so a file that
    starts failing for another reason fails this test."""
    pointer = _fails_at(path)
    report = validate(_load(path), str(SCHEMA), _class(path))
    messages = [r.message for r in report.results]
    assert messages, f"{path.name} passed the validator"
    assert all(m.endswith(f" in {pointer}") for m in messages), messages


def _committed_errors(instance, class_name):
    """What the committed project/jsonschema file finds wrong with a record of
    one class, under the draft the file names."""
    schema = json.loads(COMMITTED_JSON_SCHEMA.read_text(encoding="utf-8"))
    root = {
        "$schema": schema["$schema"],
        "$ref": f"#/$defs/{class_name}",
        "$defs": schema["$defs"],
    }
    validator = jsonschema.validators.validator_for(schema)(
        root, format_checker=jsonschema.FormatChecker()
    )
    return list(validator.iter_errors(instance))


def test_the_committed_json_schema_is_read_under_its_own_draft():
    """The draft the committed file names is the one its records are checked
    under, not the newest the jsonschema package knows."""
    schema = json.loads(COMMITTED_JSON_SCHEMA.read_text(encoding="utf-8"))
    validator = jsonschema.validators.validator_for(schema, default=None)
    assert validator is not None, schema.get("$schema")
    assert validator.META_SCHEMA["$id"].rstrip("#") == schema["$schema"].rstrip("#")


@pytest.mark.parametrize("path", VALID, ids=lambda p: p.name)
def test_valid_examples_pass_the_committed_json_schema(path):
    """The committed project/jsonschema file accepts every valid example, so it
    is the schema's current rendering."""
    assert not _committed_errors(_load(path), _class(path))


def _pointer(error):
    return "/" + "/".join(str(part) for part in error.absolute_path)


@pytest.mark.parametrize("path", INVALID, ids=lambda p: p.name)
def test_counter_examples_fail_the_committed_json_schema(path):
    """The committed project/jsonschema file refuses every counter-example at
    the place its first line names, as the validator does."""
    errors = _committed_errors(_load(path), _class(path))
    assert errors, f"{path.name} passed the committed JSON Schema"
    assert {_pointer(e) for e in errors} == {_fails_at(path)}, [
        e.message for e in errors
    ]


def test_every_class_has_an_example():
    """Each class has a valid example, since a concept may name either as its
    type."""
    classes = set(yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))["classes"])
    assert classes <= {_class(p) for p in VALID}


def _extract():
    return json.loads(EXTRACT.read_text(encoding="utf-8"))


def test_the_extract_validates_entry_by_entry():
    """Each real entry of the extract, copied unchanged from the pinned
    catalogue, validates as an entry."""
    for entry in _extract():
        assert not _committed_errors(entry, "KevVulnerability"), entry["cveID"]
        report = validate(entry, str(SCHEMA), "KevVulnerability")
        assert not report.results, (entry["cveID"], [r.message for r in report.results])


def test_the_extract_loads_as_a_catalogue():
    """The extract's entries load together through both generated models,
    in a catalogue whose head is the real file's."""
    entries = _extract()
    record = {
        "title": "CISA Catalog of Known Exploited Vulnerabilities",
        "catalogVersion": "2026.10.30",
        "dateReleased": "2026-10-30T17:02:45.3665Z",
        "count": len(entries),
        "vulnerabilities": entries,
    }
    assert not _committed_errors(record, "KevCatalog")
    assert not catalogue_faults(record)
    assert kev_catalog.datamodel.kev_catalog_pydantic.KevCatalog.model_validate(record)
    loaded = kev_catalog.datamodel.kev_catalog.KevCatalog(**record)
    assert [v.cveID for v in loaded.vulnerabilities] == [e["cveID"] for e in entries]


def test_the_extract_covers_what_the_format_varies():
    """The extract holds each value and each shape the real file shows, so it
    is worth validating."""
    entries = _extract()
    assert {e["knownRansomwareCampaignUse"] for e in entries} == {"Known", "Unknown"}
    assert {e["forensicTriage"] for e in entries} == {"Yes", "No"}
    assert any(not e["cwes"] for e in entries)
    assert any(len(e["cwes"]) > 1 for e in entries)
    assert any(len(e["cveID"].split("-")[2]) == 4 for e in entries)
    assert any(len(e["cveID"].split("-")[2]) > 5 for e in entries)
    assert any(e["product"] != e["product"].strip() for e in entries)
    assert any(
        e["vulnerabilityName"] != e["vulnerabilityName"].strip() for e in entries
    )
    assert any(" ; " in e["notes"] for e in entries)


@pytest.mark.parametrize(
    "path",
    [p for p in VALID if _class(p) == "KevCatalog"],
    ids=lambda p: p.name,
)
def test_valid_catalogues_keep_the_rules_no_validator_states(path):
    """Each valid catalogue's count is its list's length, with no CVE twice."""
    assert not catalogue_faults(_load(path))


ENTRY = {
    "cveID": "CVE-2021-44228",
    "vendorProject": "Apache",
    "product": "Log4j2",
    "vulnerabilityName": "A name",
    "dateAdded": "2021-12-10",
    "shortDescription": "A description.",
    "requiredAction": "An action.",
    "dueDate": "2021-12-24",
}
HEAD = {"catalogVersion": "2026.10.30", "dateReleased": "2026-10-30T17:02:45.3665Z"}


@pytest.mark.parametrize(
    ("record", "fault"),
    [
        (
            {**HEAD, "count": 2, "vulnerabilities": [ENTRY]},
            "count says 2, the list holds 1",
        ),
        (
            {**HEAD, "count": 0, "vulnerabilities": [ENTRY]},
            "count says 0, the list holds 1",
        ),
        (
            {**HEAD, "count": 2, "vulnerabilities": [ENTRY, ENTRY]},
            "repeats CVE-2021-44228",
        ),
    ],
)
def test_the_rules_find_what_the_validator_passes(record, fault):
    """Each record passes the validator and the committed JSON Schema, and only
    the Python rule refuses it, at its one stated fault."""
    assert not validate(record, str(SCHEMA), "KevCatalog").results
    assert not _committed_errors(record, "KevCatalog")
    assert catalogue_faults(record) == [fault]


def test_the_dataclasses_refuse_an_empty_list():
    """This is why the empty-list example sits under tests/data/problem/valid/.
    When a LinkML release lets the dataclasses take an empty list, this fails, and
    the example moves back."""
    record = {**HEAD, "count": 0, "vulnerabilities": []}
    assert not validate(record, str(SCHEMA), "KevCatalog").results
    with pytest.raises(ValueError, match="vulnerabilities must be supplied"):
        kev_catalog.datamodel.kev_catalog.KevCatalog(**record)


def test_a_date_is_read_as_a_date_by_every_model():
    """The real file's four-digit fraction of a second loads through both
    generated models as well as the validator."""
    record = {**HEAD, "count": 1, "vulnerabilities": [ENTRY]}
    pydantic = kev_catalog.datamodel.kev_catalog_pydantic.KevCatalog.model_validate(
        record
    )
    assert pydantic.dateReleased.year == 2026
    dataclass = kev_catalog.datamodel.kev_catalog.KevCatalog(**record)
    assert str(dataclass.dateReleased).startswith("2026-10-30T17:02:45")
