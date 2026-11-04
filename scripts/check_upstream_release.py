#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Check CISA's KEV JSON schema and its licence against the pinned edition.

The schema renders the JSON schema of the Known Exploited Vulnerabilities (KEV)
catalog. The Cybersecurity and Infrastructure Security Agency (CISA) serves that
file from www.cisa.gov, and cisagov/kev-data, the data's official mirror on
GitHub, holds the same bytes. The file states no version, so the edition is the
date of the commit that last changed it in kev-data. tests/upstream/ copies the
file and the mirror's licence, as their CC0 terms allow.

Three things can change without any change in this repository:

- CISA changes the JSON schema, so a new edition is out;
- the mirror's LICENSE file changes, so NOTICE may no longer hold;
- the copy CISA serves differs from the mirror's.

The script asks the GitHub API for the mirror's default branch, the commit it
is at, and the file tree at that commit and at the pinned one, and compares
both files with their pins by git object hash. It reads the copy CISA serves
and compares its SHA-256. The catalogue itself changes most weekdays, and that
is no finding here: tests/data/kev-data/manifest.json pins a dated catalogue
for the tests.

It prints a Markdown report, and exits 1 when:

- the JSON schema or the licence changed on the default branch, or is gone;
- the pinned commit no longer holds a pinned file;
- the copy CISA serves differs from the pinned bytes;
- a check could not finish, such as a refused, failed or cut-off request,
  or an answer larger than the script reads.

A new commit that leaves both files unchanged, another default branch, a new
file with "schema" in its name, and a 403 from CISA are reported for information
only. CISA's site refuses some clients, and the watch does not try to get round
that: the mirror holds the same facts.

Text a server chose, such as an address, a file name or an error message,
is quoted as code on one line in the report, so the issue the workflow
opens from it cannot mention anyone. A redirect is followed only to an
https address on www.cisa.gov or api.github.com. Set ``GITHUB_TOKEN`` to
raise the API rate limit. The token goes to api.github.com alone, never to
CISA and never on to a redirect. Usage::

    python scripts/check_upstream_release.py [--report FILE]
"""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from functools import cache
from pathlib import Path

USER_AGENT = "lmodel-kev-catalog-watch"
API_HOST = "https://api.github.com/"
# The hosts a redirect may lead to: CISA's, which serves the JSON schema, and
# the GitHub API's.
HOSTS = frozenset({"www.cisa.gov", "api.github.com"})
API = f"{API_HOST}repos/cisagov/kev-data"

# The most the script reads of one answer. The largest, the mirror's file tree,
# is about 3 kB, and the JSON schema under 4 kB.
MAX_BYTES = 5_000_000

SCHEMA_FILE = "known_exploited_vulnerabilities_schema.json"
LICENCE_FILE = "LICENSE"

# The edition the schema renders, as the date of the commit that last changed
# the file, and that commit. The schema header's `version` and `source` name
# them, and tests/test_upstream.py holds the header, the copies and these pins
# equal. Move them together when the schema moves to another edition.
PINNED_EDITION = "2026-09-17"
PINNED_COMMIT = "d98075f22b11ca60ede428f4397966d3523dc692"
PINNED_SOURCE = (
    f"https://github.com/cisagov/kev-data/blob/{PINNED_COMMIT}/{SCHEMA_FILE}"
)

# The git object hash of each file at that commit.
PINNED_BLOBS = {
    SCHEMA_FILE: "ec422845b354f58250d2e99cdfcce17a18659423",
    LICENCE_FILE: "bd3f969029f08512e9a67348be9d744b2eb81a7a",
}

# The address CISA serves the JSON schema from, and the SHA-256 of its bytes.
CISA_SCHEMA = f"https://www.cisa.gov/sites/default/files/feeds/{SCHEMA_FILE}"
PINNED_SHA256 = "0d5865c98694c5bfba2c78a26caf814f406b3fce8bfb81bef79e99c7f288b0e7"

# The mirror's default branch when the pins were read.
PINNED_BRANCH = "develop"


class _ExpectedHostRedirect(urllib.request.HTTPRedirectHandler):
    """Follow a redirect only to an https address on one of HOSTS."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parts = urllib.parse.urlsplit(newurl)
        if parts.scheme != "https" or parts.hostname not in HOSTS:
            raise ValueError(f"a redirect leads off the expected hosts, to {newurl}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


# An opener in place of urlopen's, whose redirect handler follows any address.
_open = urllib.request.build_opener(_ExpectedHostRedirect).open


def _get(url: str) -> tuple[str, bytes]:
    """The address that answered, after any redirect, and the answer's body."""
    headers = {"User-Agent": USER_AGENT}
    if url.startswith(API_HOST):
        headers["Accept"] = "application/vnd.github+json"
    req = urllib.request.Request(url, headers=headers)
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith(API_HOST):
        # urllib copies ordinary headers onto a redirect, so the token goes in
        # an unredirected one and reaches api.github.com alone.
        req.add_unredirected_header("Authorization", f"Bearer {token}")
    with _open(req, timeout=60) as resp:
        body = resp.read(MAX_BYTES + 1)
        answered = resp.geturl()
    if len(body) > MAX_BYTES:
        raise ValueError(f"the answer from {url} is larger than {MAX_BYTES} bytes")
    return answered, body


def _json(url: str):
    return json.loads(_get(url)[1])


def _code(text: object) -> str:
    """Text a server chose, such as an address or a file name, as a code
    span on one line, so it cannot mention a person or add a link in the
    issue. A blank line would end the span, so every run of spaces and line
    breaks is one space."""
    return "`" + " ".join(str(text).replace("`", "'").split()) + "`"


@cache
def _tree(ref: str) -> dict[str, str]:
    """Every file of the mirror at a ref, by path, with its object hash. A ref
    the repository does not hold gives an empty mapping. Each tree is asked for
    once, and no caller changes what it returns."""
    try:
        body = _json(f"{API}/git/trees/{ref}?recursive=1")
    except urllib.error.HTTPError as err:
        if err.code in (404, 422):
            return {}
        raise
    if body.get("truncated"):
        raise OSError(f"the tree at {ref} is too large for one listing")
    return {e["path"]: e["sha"] for e in body.get("tree", []) if e["type"] == "blob"}


def _head() -> tuple[str, str]:
    """The mirror's default branch and the commit it is at."""
    branch = _json(API)["default_branch"]
    commit = _json(f"{API}/commits/{branch}")["sha"]
    return branch, commit


def _newest_change(branch: str) -> tuple[str, str]:
    """The newest commit on a branch that touched the JSON schema, and its date,
    which is what the next edition would be called."""
    query = urllib.parse.urlencode({"path": SCHEMA_FILE, "sha": branch, "per_page": 1})
    newest = _json(f"{API}/commits?{query}")[0]
    return newest["sha"], newest["commit"]["committer"]["date"][:10]


def check_mirror() -> tuple[list[str], bool]:
    """Report whether the pinned commit still holds the pinned files, and
    whether the mirror's default branch has changed or dropped either."""
    report = [
        f"- Pinned edition: {PINNED_EDITION}, `{SCHEMA_FILE}` in cisagov/kev-data "
        f"at commit `{PINNED_COMMIT[:12]}`, copied into `tests/upstream/`."
    ]
    attention = False
    pinned_tree = _tree(PINNED_COMMIT)
    for name, sha in sorted(PINNED_BLOBS.items()):
        if pinned_tree.get(name) != sha:
            attention = True
            report.append(
                f"- **The pinned commit no longer holds `{name}` as the pinned blob.** "
                "Find out what happened to the mirror's history before trusting the pins."
            )

    branch, commit = _head()
    if branch != PINNED_BRANCH:
        report.append(
            f"- For information, the mirror's default branch is {_code(branch)}, "
            f"not `{PINNED_BRANCH}`."
        )
    latest_tree = pinned_tree if commit == PINNED_COMMIT else _tree(commit)
    where = f"{_code(branch)} at commit {_code(commit[:12])}"

    if SCHEMA_FILE not in latest_tree:
        attention = True
        report.append(
            f"- **`{SCHEMA_FILE}` is gone from {where}.** Find where CISA now keeps "
            "the JSON schema, and move the pins."
        )
    elif latest_tree[SCHEMA_FILE] != PINNED_BLOBS[SCHEMA_FILE]:
        attention = True
        changed, date = _newest_change(branch)
        report.append(
            f"- **`{SCHEMA_FILE}` changed at commit {_code(changed[:12])} of "
            f"{_code(date)} on {_code(branch)}; the schema renders {PINNED_EDITION}.** "
            "Read what changed, decide whether the schema moves to it, and move the "
            "pins here, the copy under `tests/upstream/` and the schema header."
        )
    if LICENCE_FILE not in latest_tree:
        attention = True
        report.append(
            f"- **`{LICENCE_FILE}` is gone from {where}.** Read what terms now apply "
            "and update NOTICE."
        )
    elif latest_tree[LICENCE_FILE] != PINNED_BLOBS[LICENCE_FILE]:
        attention = True
        report.append(
            f"- **`{LICENCE_FILE}` changed on {where}.** Read what the new terms allow, "
            "update NOTICE and the copy under `tests/upstream/`, and move the pin."
        )

    added = sorted(
        path
        for path in latest_tree
        if "schema" in path.lower() and path not in PINNED_BLOBS
    )
    if added:
        report.append(
            "- For information, the mirror also holds "
            + ", ".join(_code(n) for n in added)
            + "."
        )
    if not attention:
        report.append(
            f"- For information, {where} leaves the JSON schema and the licence "
            "unchanged."
        )
    return report, attention


def check_cisa() -> tuple[list[str], bool]:
    """Report whether the copy CISA serves is still the pinned bytes. A 403 is
    for information: the site refuses some clients, and the mirror check holds
    the same facts."""
    try:
        answered, body = _get(CISA_SCHEMA)
    except urllib.error.HTTPError as err:
        if err.code != 403:
            raise
        return [
            f"- For information, {CISA_SCHEMA} answered 403, so its copy was not "
            "compared. The mirror's check above stands."
        ], False
    report = []
    if answered != CISA_SCHEMA:
        report.append(f"- {CISA_SCHEMA} redirected to {_code(answered)}.")
    digest = hashlib.sha256(body).hexdigest()
    if digest != PINNED_SHA256:
        report.append(
            f"- **The JSON schema CISA serves has SHA-256 {_code(digest)}, not the "
            f"pinned `{PINNED_SHA256}`.** The mirror may be about to follow, or the "
            "two may differ: read both before moving the pins."
        )
        return report, True
    report.append(
        f"- The JSON schema CISA serves is the pinned edition, {CISA_SCHEMA}."
    )
    return report, False


# Each check, by the name the report gives it when it cannot finish.
CHECKS = (
    ("mirror", check_mirror),
    ("CISA copy", check_cisa),
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--report", type=Path, help="Also write the Markdown report to this file"
    )
    args = parser.parse_args(argv)
    lines: list[str] = []
    attention = False
    for label, check in CHECKS:
        try:
            found, needs = check()
        # OSError covers a refused or failed request and a timeout,
        # HTTPException and EOFError a connection cut off mid-answer,
        # ValueError an answer that is not JSON or is too large, and
        # LookupError, TypeError and AttributeError JSON of another shape.
        except (
            OSError,
            http.client.HTTPException,
            EOFError,
            ValueError,
            LookupError,
            TypeError,
            AttributeError,
        ) as err:
            found = [f"- **The {label} check could not finish: {_code(err)}.**"]
            needs = True
        lines += found
        attention = attention or needs
    text = "\n".join(lines) + "\n"
    print(text, end="")
    if args.report:
        args.report.write_text(text, encoding="utf-8")
    return 1 if attention else 0


if __name__ == "__main__":
    sys.exit(main())
