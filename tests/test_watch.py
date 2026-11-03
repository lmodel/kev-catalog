"""Checks the upstream watch's decisions against stubbed answers.

scripts/check_upstream_release.py asks the GitHub API about cisagov/kev-data and
reads the copy of the JSON schema CISA serves. These tests replace its one
network call, `_get`, with a table of answers, so they run offline. They show
what the report says in each case the watch knows: a changed or dropped file, a
changed copy at CISA, a moved branch, a refusal, and a check that could not
finish.
"""

import hashlib
import http.client
import importlib.util
import json
import urllib.error
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
SCRIPT = ROOT / "scripts" / "check_upstream_release.py"
SCHEMA_COPY = ROOT / "tests" / "upstream" / "known_exploited_vulnerabilities_schema.json"

NEW_COMMIT = "1" * 40
OTHER_BLOB = "b" * 40


@pytest.fixture
def watch():
    """A fresh copy of the script, so no test sees another's stub."""
    spec = importlib.util.spec_from_file_location("watch_under_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _tree(files):
    return {
        "truncated": False,
        "tree": [{"path": p, "type": "blob", "sha": s} for p, s in files.items()],
    }


def _answers(watch, head=None, branch="develop", latest_files=None, pinned_files=None):
    """The answers of an unchanged upstream, with the parts a test changes."""
    head = head or watch.PINNED_COMMIT
    pinned_files = (
        dict(watch.PINNED_BLOBS, **{"README.md": "a" * 40})
        if pinned_files is None
        else pinned_files
    )
    answers = {
        watch.CISA_SCHEMA: SCHEMA_COPY.read_bytes(),
        watch.API: {"default_branch": branch},
        f"{watch.API}/commits/{branch}": {"sha": head},
        f"{watch.API}/git/trees/{watch.PINNED_COMMIT}?recursive=1": _tree(pinned_files),
    }
    if head != watch.PINNED_COMMIT:
        files = pinned_files if latest_files is None else latest_files
        answers[f"{watch.API}/git/trees/{head}?recursive=1"] = _tree(files)
    return answers


def _newest(watch, answers, sha=NEW_COMMIT, date="2027-01-15T10:00:00Z", branch="develop"):
    """Add the answer to the question of which commit last touched the schema."""
    query = f"path={watch.SCHEMA_FILE}&sha={branch}&per_page=1"
    answers[f"{watch.API}/commits?{query}"] = [
        {"sha": sha, "commit": {"committer": {"date": date}}}
    ]
    return answers


def _stub(watch, answers):
    """Make `_get` answer from the table: an exception is raised, a pair is
    the address that answered and its body, bytes are a file at the address
    asked, and anything else is JSON."""

    def get(url):
        answer = answers[url]
        if isinstance(answer, Exception):
            raise answer
        if isinstance(answer, tuple):
            return answer
        if isinstance(answer, bytes):
            return url, answer
        return url, json.dumps(answer).encode()

    watch._get = get


def _run(watch, tmp_path):
    report = tmp_path / "report.md"
    code = watch.main(["--report", str(report)])
    return code, report.read_text(encoding="utf-8")


def _forbidden():
    return urllib.error.HTTPError("https://www.cisa.gov/x", 403, "Forbidden", None, None)


def test_nothing_changed(watch, tmp_path):
    """With the pinned files at the pinned commit, the watch exits 0."""
    _stub(watch, _answers(watch))
    code, text = _run(watch, tmp_path)
    assert code == 0, text
    assert "Pinned edition: 2026-09-17" in text
    assert "leaves the JSON schema and the licence unchanged." in text
    assert "The JSON schema CISA serves is the pinned edition" in text


def test_a_new_commit_with_the_same_files_is_for_information(watch, tmp_path):
    """The catalogue changes most weekdays, and that is no finding."""
    _stub(watch, _answers(watch, head=NEW_COMMIT))
    code, text = _run(watch, tmp_path)
    assert code == 0, text
    assert (
        "`develop` at commit `111111111111` leaves the JSON schema and the licence"
        in text
    )


def test_the_schema_changed(watch, tmp_path):
    """A new blob for the JSON schema at the branch's head needs attention, and
    the report names the date a new edition would take."""
    files = {
        "known_exploited_vulnerabilities_schema.json": OTHER_BLOB,
        "LICENSE": "bd3f969029f08512e9a67348be9d744b2eb81a7a",
    }
    answers = _answers(watch, head=NEW_COMMIT, latest_files=files)
    _stub(watch, _newest(watch, answers))
    code, text = _run(watch, tmp_path)
    assert code == 1
    assert (
        "**`known_exploited_vulnerabilities_schema.json` changed at commit "
        "`111111111111` of `2027-01-15` on `develop`; the schema renders 2026-09-17.**"
        in text
    )
    assert "leaves the JSON schema" not in text


def test_the_schema_is_gone(watch, tmp_path):
    """A head without the JSON schema needs attention."""
    files = {"LICENSE": "bd3f969029f08512e9a67348be9d744b2eb81a7a"}
    _stub(watch, _answers(watch, head=NEW_COMMIT, latest_files=files))
    code, text = _run(watch, tmp_path)
    assert code == 1
    assert (
        "**`known_exploited_vulnerabilities_schema.json` is gone from `develop` at "
        "commit `111111111111`.**" in text
    )


def test_the_licence_changed(watch, tmp_path):
    """A new blob for LICENSE needs attention, since NOTICE rests on it."""
    files = dict(watch.PINNED_BLOBS, LICENSE=OTHER_BLOB)
    _stub(watch, _answers(watch, head=NEW_COMMIT, latest_files=files))
    code, text = _run(watch, tmp_path)
    assert code == 1
    assert "**`LICENSE` changed on `develop` at commit `111111111111`.**" in text
    assert "update NOTICE" in text


def test_the_licence_is_gone(watch, tmp_path):
    """A head without LICENSE needs attention."""
    files = {watch.SCHEMA_FILE: watch.PINNED_BLOBS[watch.SCHEMA_FILE]}
    _stub(watch, _answers(watch, head=NEW_COMMIT, latest_files=files))
    code, text = _run(watch, tmp_path)
    assert code == 1
    assert "**`LICENSE` is gone from `develop` at commit `111111111111`.**" in text


def test_the_pinned_commit_lost_a_file(watch, tmp_path):
    """A pinned commit that no longer holds a pinned blob needs attention."""
    answers = _answers(
        watch,
        pinned_files={},
        head=NEW_COMMIT,
        latest_files=dict(watch.PINNED_BLOBS),
    )
    _stub(watch, answers)
    code, text = _run(watch, tmp_path)
    assert code == 1
    assert (
        "**The pinned commit no longer holds "
        "`known_exploited_vulnerabilities_schema.json`" in text
    )
    assert "**The pinned commit no longer holds `LICENSE`" in text


def test_another_branch_and_an_added_schema_are_for_information(watch, tmp_path):
    """Another default branch, and a new file with schema in its name, are
    reported and leave the exit code at 0."""
    files = dict(watch.PINNED_BLOBS, **{"schema-v2.json": "c" * 40})
    answers = _answers(watch, head=NEW_COMMIT, branch="main", latest_files=files)
    _stub(watch, answers)
    code, text = _run(watch, tmp_path)
    assert code == 0, text
    assert "the mirror's default branch is `main`, not `develop`." in text
    assert "the mirror also holds `schema-v2.json`." in text


def test_the_copy_at_cisa_differs(watch, tmp_path):
    """Bytes at CISA other than the pinned ones need attention."""
    answers = _answers(watch)
    answers[watch.CISA_SCHEMA] = b"{}"
    _stub(watch, answers)
    code, text = _run(watch, tmp_path)
    assert code == 1
    shown = hashlib.sha256(b"{}").hexdigest()
    assert f"**The JSON schema CISA serves has SHA-256 `{shown}`" in text


def test_a_403_from_cisa_is_for_information(watch, tmp_path):
    """CISA's site refuses some clients. The watch says so and leaves it closed,
    and the mirror's check stands."""
    answers = _answers(watch)
    answers[watch.CISA_SCHEMA] = _forbidden()
    _stub(watch, answers)
    code, text = _run(watch, tmp_path)
    assert code == 0, text
    assert "answered 403, so its copy was not compared." in text


def test_a_redirect_at_cisa_is_reported_and_quoted(watch, tmp_path):
    """The address that answered is named, as code, when it is not the one
    asked, and a backtick in it cannot end the quotation."""
    answers = _answers(watch)
    answers[watch.CISA_SCHEMA] = (
        "https://www.cisa.gov/@someone`x",
        SCHEMA_COPY.read_bytes(),
    )
    _stub(watch, answers)
    code, text = _run(watch, tmp_path)
    assert code == 0, text
    assert "redirected to `https://www.cisa.gov/@someone'x`." in text


@pytest.mark.parametrize(
    ("failure", "shown"),
    [
        (
            urllib.error.HTTPError("https://x", 500, "Server Error", None, None),
            "`HTTP Error 500",
        ),
        (urllib.error.URLError("Connection refused"), "`<urlopen error"),
        (http.client.IncompleteRead(b"<html>"), "`IncompleteRead"),
        (http.client.RemoteDisconnected("closed"), "`closed`"),
        (EOFError("cut"), "`cut`"),
        (LookupError("unknown encoding: x-bogus"), "`unknown encoding"),
        (
            ValueError("the answer is larger than 5000000 bytes"),
            "`the answer is larger",
        ),
    ],
)
def test_a_check_that_could_not_finish(watch, tmp_path, failure, shown):
    """A refused, failed, cut-off or oversized answer stops one check, says
    so, and leaves the other check to run and the report to be written."""
    answers = _answers(watch)
    answers[watch.CISA_SCHEMA] = failure
    _stub(watch, answers)
    code, text = _run(watch, tmp_path)
    assert code == 1
    assert f"**The CISA copy check could not finish: {shown}" in text
    assert "leaves the JSON schema and the licence unchanged." in text


def test_json_of_another_shape_could_not_finish(watch, tmp_path):
    """An API answer without the keys the watch reads is a check that could
    not finish, not a crash."""
    answers = _answers(watch)
    answers[watch.API] = {"message": "moved"}
    _stub(watch, answers)
    code, text = _run(watch, tmp_path)
    assert code == 1
    assert "**The mirror check could not finish: `'default_branch'`.**" in text
    assert "The JSON schema CISA serves is the pinned edition" in text


def test_a_json_list_where_an_object_belongs_could_not_finish(watch, tmp_path):
    """An API answer that is a list, where the watch reads an object's key,
    raises a TypeError, which is a check that could not finish."""
    answers = _answers(watch)
    answers[watch.API] = (watch.API, b'["develop"]')
    _stub(watch, answers)
    code, text = _run(watch, tmp_path)
    assert code == 1
    assert "**The mirror check could not finish: `list indices" in text


def test_an_empty_history_could_not_finish(watch, tmp_path):
    """A commit list with nothing in it, where the watch reads the first, is a
    check that could not finish."""
    files = dict(watch.PINNED_BLOBS, **{watch.SCHEMA_FILE: OTHER_BLOB})
    answers = _answers(watch, head=NEW_COMMIT, latest_files=files)
    query = f"path={watch.SCHEMA_FILE}&sha=develop&per_page=1"
    answers[f"{watch.API}/commits?{query}"] = []
    _stub(watch, answers)
    code, text = _run(watch, tmp_path)
    assert code == 1
    assert "**The mirror check could not finish: `list index" in text


def test_a_truncated_tree_could_not_finish(watch, tmp_path):
    """A file listing GitHub cut short cannot show the files are unchanged, so
    the check says it could not finish."""
    answers = _answers(watch)
    answers[f"{watch.API}/git/trees/{watch.PINNED_COMMIT}?recursive=1"] = {
        "truncated": True,
        "tree": [],
    }
    _stub(watch, answers)
    code, text = _run(watch, tmp_path)
    assert code == 1
    assert "**The mirror check could not finish: `the tree at" in text
    assert "too large for one listing`.**" in text


def test_a_commit_the_mirror_does_not_hold_is_an_empty_tree(watch, tmp_path):
    """A 404 on the pinned commit means the mirror lost it, so each pinned file
    is reported missing there."""
    answers = _answers(watch, head=NEW_COMMIT, latest_files=None)
    answers[f"{watch.API}/git/trees/{NEW_COMMIT}?recursive=1"] = _tree(
        dict(watch.PINNED_BLOBS)
    )
    answers[f"{watch.API}/git/trees/{watch.PINNED_COMMIT}?recursive=1"] = (
        urllib.error.HTTPError("https://x", 404, "Not Found", None, None)
    )
    _stub(watch, answers)
    code, text = _run(watch, tmp_path)
    assert code == 1
    assert "**The pinned commit no longer holds `LICENSE`" in text


class _Answer:
    def __init__(self, url):
        self.url = url

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def geturl(self):
        return self.url

    def read(self, size):
        return b"{}"


def test_the_token_goes_to_the_api_alone(watch, monkeypatch):
    """The token travels in an unredirected header to api.github.com, and
    never to CISA."""
    monkeypatch.setenv("GITHUB_TOKEN", "not-to-leak")
    sent = {}

    def urlopen(req, timeout):
        sent[req.full_url] = (dict(req.header_items()), dict(req.unredirected_hdrs))
        return _Answer(req.full_url)

    monkeypatch.setattr(watch, "_open", urlopen)
    watch._get(watch.API)
    watch._get(watch.CISA_SCHEMA)
    headers, unredirected = sent[watch.API]
    assert unredirected["Authorization"] == "Bearer not-to-leak"
    assert headers["User-agent"] == "lmodel-kev-catalog-watch"
    cisa_headers, cisa_unredirected = sent[watch.CISA_SCHEMA]
    assert "Authorization" not in cisa_headers and not cisa_unredirected
    assert set(cisa_headers) == {"User-agent"}


def test_a_plain_client_is_all_the_watch_claims_to_be(watch):
    """The watch names itself. It sets no browser's user agent."""
    assert "Mozilla" not in watch.USER_AGENT
    assert watch.USER_AGENT == "lmodel-kev-catalog-watch"


def test_an_answer_over_the_cap_is_refused(watch, monkeypatch):
    """An answer larger than MAX_BYTES raises rather than being read whole."""

    class Big(_Answer):
        def read(self, size):
            return b"x" * size

    monkeypatch.setattr(watch, "_open", lambda req, timeout: Big(req.full_url))
    assert watch.MAX_BYTES == 5_000_000
    with pytest.raises(ValueError, match="larger than"):
        watch._get(watch.CISA_SCHEMA)


def test_server_text_stays_on_one_line(watch, tmp_path):
    """A branch name with a blank line and a mention in it stays inside its
    code span, so the issue mentions no one."""
    branch = "main\n\n@someone `x`"
    answers = _answers(watch, branch=branch)
    _stub(watch, answers)
    code, text = _run(watch, tmp_path)
    assert code == 0, text
    assert "default branch is `main @someone 'x'`, not `develop`." in text


def test_a_redirect_off_the_expected_hosts_is_refused(watch):
    """A redirect is followed to CISA's and the GitHub API's hosts over https,
    and to no other address."""
    handlers = watch._open.__self__.handlers
    assert any(isinstance(h, watch._ExpectedHostRedirect) for h in handlers)
    handler = watch._ExpectedHostRedirect()
    req = watch.urllib.request.Request(watch.CISA_SCHEMA)
    for newurl in (
        "https://example.org/feeds/x.json",
        "http://www.cisa.gov/feeds/x.json",
        "https://www.cisa.gov.example.org/feeds/x.json",
        "https://raw.githubusercontent.com/cisagov/kev-data/develop/LICENSE",
    ):
        with pytest.raises(ValueError, match="leads off the expected hosts"):
            handler.redirect_request(req, None, 302, "Found", {}, newurl)
    for moved in (
        "https://www.cisa.gov/feeds/x.json",
        "https://api.github.com/repositories/1/git/trees/x",
    ):
        assert (
            handler.redirect_request(req, None, 301, "Moved", {}, moved).full_url
            == moved
        )


def test_a_refused_redirect_could_not_finish(watch, tmp_path):
    """A redirect the watch refuses stops that check, and the report quotes
    the address it was sent to."""
    answers = _answers(watch)
    answers[watch.CISA_SCHEMA] = ValueError(
        "a redirect leads off the expected hosts, to https://example.org/@someone"
    )
    _stub(watch, answers)
    code, text = _run(watch, tmp_path)
    assert code == 1
    assert (
        "**The CISA copy check could not finish: `a redirect leads off the expected "
        "hosts, to https://example.org/@someone`.**" in text
    )
