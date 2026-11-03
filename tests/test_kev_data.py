"""Validates the full pinned KEV catalogue, unchanged.

The catalogue changes most weekdays, so tests/data/kev-data/manifest.json pins
one dated file. `just fetch-kev-data` downloads it into tmp/kev-data/ and checks
its hashes, and `just test-kev-data` runs these tests with KEV_DATA=1, as the
kev-data job of main.yaml does. Without that variable they skip, so `just test`
stays quick and offline; with it, a missing file fails them.
"""

import hashlib
import json
import os
from collections import Counter
from functools import cache
from pathlib import Path

import jsonschema
import pytest
from linkml.validator import validate
from linkml_runtime.loaders import json_loader

import kev_catalog.datamodel.kev_catalog
import kev_catalog.datamodel.kev_catalog_pydantic
from tests.kev_rules import catalogue_faults

ROOT = Path(__file__).parent.parent
DATA = Path(os.environ.get("KEV_DATA_DIR", ROOT / "tmp" / "kev-data"))
TESTS = ROOT / "tests"
MANIFEST = json.loads(
    (TESTS / "data" / "kev-data" / "manifest.json").read_text(encoding="utf-8")
)
NAME = "known_exploited_vulnerabilities.json"
EXTRACT = TESTS / "data" / "kev-data" / "extract" / NAME
SCHEMA = ROOT / "src" / "kev_catalog" / "schema" / "kev_catalog.yaml"
COMMITTED_JSON_SCHEMA = ROOT / "project" / "jsonschema" / "kev_catalog.schema.json"
UPSTREAM_SCHEMA = TESTS / "upstream" / "known_exploited_vulnerabilities_schema.json"

pytestmark = pytest.mark.skipif(
    os.environ.get("KEV_DATA") != "1",
    reason="the full catalogue is tested by `just test-kev-data`",
)

# Where the pinned catalogue goes beyond CISA's JSON schema, with the number of
# places. The file's `title` is not among the schema's properties, and the
# upstream's objects are open, so the upstream accepts it; this schema names it.
KNOWN_DATA_DEPARTURES = {"title, a key the upstream's JSON schema does not list": 1}

# What the pinned catalogue holds, so that a moved pin says what moved. A key
# that the upstream's JSON schema leaves optional is on every entry here.
PROFILE = {
    "entries": 1766,
    "knownRansomwareCampaignUse": {"Known": 361, "Unknown": 1405},
    "forensicTriage": {"No": 1670, "Yes": 96},
    "cwes empty": 175,
    "cve number over four digits": 1055,
}


@cache
def _catalogue():
    path = DATA / NAME
    if not path.is_file():
        pytest.fail(f"{path} is missing; run `just fetch-kev-data`")
    return json.loads(path.read_text(encoding="utf-8"))


def test_the_file_is_the_pinned_one():
    """The file's size and hashes are the manifest's, and it is the edition the
    manifest names."""
    data = (DATA / NAME).read_bytes()
    pin = MANIFEST["fetched"][NAME]
    assert len(data) == pin["size"]
    assert hashlib.sha256(data).hexdigest() == pin["sha256"]
    assert hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest() == pin["git_blob"]
    assert _catalogue()["catalogVersion"] == MANIFEST["catalogVersion"]


def test_the_upstream_accepts_its_own_file():
    """CISA's JSON schema, read under the draft it declares, accepts the file, so
    a failure below is this schema's and not the data's."""
    schema = json.loads(UPSTREAM_SCHEMA.read_text(encoding="utf-8"))
    validator = jsonschema.validators.validator_for(schema)(
        schema, format_checker=jsonschema.FormatChecker()
    )
    assert not list(validator.iter_errors(_catalogue()))


def test_the_validator_accepts_the_file_unchanged():
    """Every entry passes the LinkML validator; the first 20 failures are shown."""
    report = validate(_catalogue(), str(SCHEMA), "KevCatalog")
    assert not report.results, [r.message[:200] for r in report.results[:20]]


def test_the_committed_json_schema_accepts_the_file_unchanged():
    """The committed project/jsonschema file accepts the file, under the draft it
    declares."""
    schema = json.loads(COMMITTED_JSON_SCHEMA.read_text(encoding="utf-8"))
    validator = jsonschema.validators.validator_for(schema)(
        schema, format_checker=jsonschema.FormatChecker()
    )
    errors = list(validator.iter_errors(_catalogue()))
    assert not errors, [e.message[:200] for e in errors[:20]]


def test_the_generated_models_load_the_file():
    """Both generated models load every entry."""
    catalogue = _catalogue()
    pydantic = kev_catalog.datamodel.kev_catalog_pydantic.KevCatalog.model_validate(
        catalogue
    )
    assert len(pydantic.vulnerabilities) == len(catalogue["vulnerabilities"])
    dataclass = json_loader.loads(
        json.dumps(catalogue),
        target_class=kev_catalog.datamodel.kev_catalog.KevCatalog,
    )
    assert len(dataclass.vulnerabilities) == len(catalogue["vulnerabilities"])


def test_the_count_is_the_list_and_no_cve_repeats():
    """CISA describes `count` as the total. This holds the real file to that,
    and to one entry per CVE."""
    assert not catalogue_faults(_catalogue())


def test_the_departures_are_the_known_ones():
    """A pin that moves to a file with another key beyond the upstream's JSON
    schema fails here until KNOWN_DATA_DEPARTURES follows it."""
    catalogue = _catalogue()
    schema = json.loads(UPSTREAM_SCHEMA.read_text(encoding="utf-8"))
    extra = set(catalogue) - set(schema["properties"])
    entry_keys = set(schema["$defs"]["vulnerability"]["properties"])
    extra_on_entries = {k for e in catalogue["vulnerabilities"] for k in e} - entry_keys
    assert extra == {"title"}
    assert not extra_on_entries
    assert KNOWN_DATA_DEPARTURES == {
        "title, a key the upstream's JSON schema does not list": len(extra)
    }


def test_the_file_holds_the_profile():
    """The numbers the hand-over and the bundle report are the file's."""
    entries = _catalogue()["vulnerabilities"]
    found = {
        "entries": len(entries),
        "knownRansomwareCampaignUse": dict(
            Counter(e["knownRansomwareCampaignUse"] for e in entries)
        ),
        "forensicTriage": dict(Counter(e["forensicTriage"] for e in entries)),
        "cwes empty": sum(not e["cwes"] for e in entries),
        "cve number over four digits": sum(
            len(e["cveID"].split("-")[2]) > 4 for e in entries
        ),
    }
    assert found == PROFILE


def test_the_extract_is_copied_unchanged():
    """Each entry of the committed extract is the entry of that CVE in the file."""
    by_id = {e["cveID"]: e for e in _catalogue()["vulnerabilities"]}
    for entry in json.loads(EXTRACT.read_text(encoding="utf-8")):
        assert entry == by_id[entry["cveID"]], entry["cveID"]
