---
type: Playbook
id: https://w3id.org/lmodel/kev-catalog/knowledge/playbooks/move-the-upstream-pins
title: Move the upstream pins
description: "What to do when the upstream watch reports a change: the pins for the JSON schema and the licence in `scripts/check_upstream_release.py`, the copies in `tests/upstream/`, the schema header, and separately the catalogue's pin in `tests/data/kev-data/manifest.json`."
genre: how-to
dependsOn:
  - https://w3id.org/lmodel/kev-catalog/knowledge/datasets/upstream-copies
references:
  - https://w3id.org/lmodel/kev-catalog/knowledge/workflows/upstream-watch
  - https://w3id.org/lmodel/kev-catalog/knowledge/datasets/pinned-kev-catalogue-release
sources:
  - id: check_upstream_release.py
    resource: scripts/check_upstream_release.py
    title: the docstring and the pins
  - id: test_upstream.py
    resource: tests/test_upstream.py
    title: the header and copy tests
  - id: tests-data-kev-data-readme.md
    resource: tests/data/kev-data/README.md
    title: the last paragraph
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# Move the upstream pins

**The JSON schema or the licence.** The upstream watch opens an issue when either changes.[^check_upstream_release.py]

1. Read what changed, and decide whether the schema moves to it.
2. Replace the copy under `tests/upstream/`, and move `PINNED_EDITION`, `PINNED_COMMIT`, `PINNED_BLOBS` and `PINNED_SHA256` in `scripts/check_upstream_release.py`.
3. Move the schema header's `version`, `source` and annotations. `tests/test_upstream.py` checks that these equal the pins, and reports any part of the new file with no element.[^test_upstream.py]
4. When the licence changed, read what it allows, and update NOTICE.

**The catalogue.** The watch does not report new data. To move the pin, change the commit, size and hashes in `tests/data/kev-data/manifest.json` together, then read what `tests/test_kev_data.py` reports: its `PROFILE` and `KNOWN_DATA_DEPARTURES` say what the file holds.[^tests-data-kev-data-readme.md]

[^check_upstream_release.py]: scripts/check_upstream_release.py, the docstring and the pins
[^test_upstream.py]: tests/test_upstream.py, the header and copy tests
[^tests-data-kev-data-readme.md]: tests/data/kev-data/README.md, the last paragraph
