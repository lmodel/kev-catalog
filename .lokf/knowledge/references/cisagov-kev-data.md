---
type: Reference
id: https://w3id.org/lmodel/kev-catalog/knowledge/references/cisagov-kev-data
title: cisagov/kev-data
description: "The official GitHub mirror of CISA's KEV data files, at `https://github.com/cisagov/kev-data`, default branch `develop`: the JSON and CSV catalogue, the JSON schema, and a CC0 licence. This project pins the schema and one dated catalogue from it."
genre: reference
resource: https://github.com/cisagov/kev-data
sources:
  - id: license
    resource: tests/upstream/LICENSE
    title: the first paragraph
  - id: fetch_kev_data.py
    resource: scripts/fetch_kev_data.py
    title: the docstring
  - resource: https://github.com/cisagov/kev-data
    title: the repository and its README
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# cisagov/kev-data

`cisagov/kev-data` mirrors the data files CISA serves, updated shortly after the source. Its default branch is `develop`. It holds the catalogue as JSON and CSV, the JSON schema and a LICENSE file. The LICENSE file opens with CISA's statement of the terms and goes on with CC0 1.0.[^license]

`scripts/check_upstream_release.py` watches the JSON schema and the licence there, and `scripts/fetch_kev_data.py` fetches the pinned catalogue from `raw.githubusercontent.com` alone.[^fetch_kev_data.py]

[^license]: tests/upstream/LICENSE, the first paragraph
[^fetch_kev_data.py]: scripts/fetch_kev_data.py, the docstring
