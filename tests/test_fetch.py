"""Checks the catalogue fetcher's refusals offline, with no download at all.

scripts/fetch_kev_data.py reads addresses from the manifest alone, takes the file
from raw.githubusercontent.com alone, and keeps a download only when its size and
both hashes match. These tests replace its download with a stub.
"""

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
SCRIPT = ROOT / "scripts" / "fetch_kev_data.py"
MANIFEST = json.loads(
    (ROOT / "tests" / "data" / "kev-data" / "manifest.json").read_text(encoding="utf-8")
)
BODY = b'{"count": 0}'
URL = "https://raw.githubusercontent.com/cisagov/kev-data/abc/file.json"


@pytest.fixture
def fetcher():
    """A fresh copy of the script, so no test sees another's stub."""
    spec = importlib.util.spec_from_file_location("fetch_under_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _pin(body=BODY, url=URL):
    return {
        "url": url,
        "size": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
        "git_blob": hashlib.sha1(b"blob %d\0" % len(body) + body).hexdigest(),
    }


def _stub_download(fetcher, monkeypatch, body):
    def download(url, part, size):
        part.write_bytes(body[: size + 1])

    monkeypatch.setattr(fetcher, "_download", download)


def test_the_manifest_pins_the_catalogue_at_a_commit():
    """The address names the pinned commit, on the one host the fetcher accepts,
    and the file is the one the tests read."""
    pin = MANIFEST["fetched"]["known_exploited_vulnerabilities.json"]
    assert pin["url"].startswith(
        "https://raw.githubusercontent.com/cisagov/kev-data/" + MANIFEST["commit"] + "/"
    )
    assert pin["url"].endswith("/known_exploited_vulnerabilities.json")
    assert len(MANIFEST["commit"]) == 40
    assert len(pin["git_blob"]) == 40
    assert len(pin["sha256"]) == 64


def test_a_matching_download_is_kept(fetcher, monkeypatch, tmp_path):
    """A download of the pinned size and hashes moves into place."""
    _stub_download(fetcher, monkeypatch, BODY)
    assert not fetcher.fetch(tmp_path, {"fetched": {"file.json": _pin()}})
    assert (tmp_path / "file.json").read_bytes() == BODY


def test_a_copy_already_there_is_not_fetched_again(fetcher, monkeypatch, tmp_path):
    """A file that matches its pins stays, with no download."""
    (tmp_path / "file.json").write_bytes(BODY)

    def refuse(url, part, size):
        raise AssertionError("no download should start")

    monkeypatch.setattr(fetcher, "_download", refuse)
    assert not fetcher.fetch(tmp_path, {"fetched": {"file.json": _pin()}})


@pytest.mark.parametrize(
    "body", [b'{"count": 1}', BODY + b" ", BODY[:-1]], ids=["other", "long", "short"]
)
def test_a_download_that_differs_is_deleted(fetcher, monkeypatch, tmp_path, body):
    """A download of another size or hash is deleted and reported, and nothing
    arrives at the file's place."""
    _stub_download(fetcher, monkeypatch, body)
    problems = fetcher.fetch(tmp_path, {"fetched": {"file.json": _pin()}})
    assert problems == [
        "file.json: the download does not match its pinned size and hashes"
    ]
    assert not list(tmp_path.iterdir())


def test_a_name_that_leaves_the_destination_is_refused(fetcher, monkeypatch, tmp_path):
    """A manifest name cannot write outside the destination."""
    _stub_download(fetcher, monkeypatch, BODY)
    dest = tmp_path / "dest"
    dest.mkdir()
    problems = fetcher.fetch(dest, {"fetched": {"../outside.json": _pin()}})
    assert "would be written outside" in problems[0]
    assert not (tmp_path / "outside.json").exists()


@pytest.mark.parametrize(
    "address",
    [
        "http://raw.githubusercontent.com/cisagov/kev-data/abc/file.json",
        "https://www.cisa.gov/sites/default/files/feeds/file.json",
        "https://raw.githubusercontent.com.example.org/file.json",
        "https://github.com/cisagov/kev-data/raw/abc/file.json",
    ],
)
def test_an_address_off_the_pinned_host_is_refused(fetcher, address):
    """Only https on raw.githubusercontent.com is fetched."""
    with pytest.raises(ValueError, match="is not an https address"):
        fetcher._check_address(address)


def test_a_redirect_off_the_pinned_host_is_refused(fetcher):
    """A redirect is followed to the pinned host over https, and to nothing else."""
    handlers = fetcher._open.__self__.handlers
    assert any(isinstance(h, fetcher._PinnedHostRedirect) for h in handlers)
    handler = fetcher._PinnedHostRedirect()
    req = fetcher.urllib.request.Request(URL)
    with pytest.raises(ValueError, match="is not an https address"):
        handler.redirect_request(req, None, 302, "Found", {}, "https://example.org/x")
    moved = "https://raw.githubusercontent.com/cisagov/kev-data/def/file.json"
    assert (
        handler.redirect_request(req, None, 301, "Moved", {}, moved).full_url == moved
    )


def test_a_failed_download_is_reported_and_leaves_nothing(
    fetcher, monkeypatch, tmp_path
):
    """A failure stops that file, says so, and leaves no partial file behind."""

    def fail(url, part, size):
        part.write_bytes(b"partial")
        raise OSError("connection reset")

    monkeypatch.setattr(fetcher, "_download", fail)
    problems = fetcher.fetch(tmp_path, {"fetched": {"file.json": _pin()}})
    assert problems == ["file.json: the download failed: connection reset"]
    assert not list(tmp_path.iterdir())


def test_the_cut_short_answer_is_not_read_past_the_pin(fetcher, monkeypatch, tmp_path):
    """The download stops one byte past the pinned size, so a huge answer fails
    without filling the disk."""

    class Big:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def read(self, size):
            return b"x" * size

    monkeypatch.setattr(fetcher, "_open", lambda req, timeout: Big())
    part = tmp_path / "file.part"
    fetcher._download(URL, part, 10)
    assert part.stat().st_size == 11
