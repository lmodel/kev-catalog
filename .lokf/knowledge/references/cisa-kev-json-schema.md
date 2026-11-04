---
type: Reference
id: https://w3id.org/lmodel/kev-catalog/knowledge/references/cisa-kev-json-schema
title: CISA's KEV JSON schema
description: CISA's JSON schema for the KEV catalog, draft-07, the file this project renders, at the edition of 2026-09-17. It states no version of its own. CISA serves it from `www.cisa.gov`, and `cisagov/kev-data` holds the same bytes.
genre: reference
resource: tests/upstream/known_exploited_vulnerabilities_schema.json
version: "2026-09-17"
isPartOf:
  - https://w3id.org/lmodel/kev-catalog/knowledge/references/cisagov-kev-data
sources:
  - id: check_upstream_release.py
    resource: scripts/check_upstream_release.py
    title: the pins
  - id: known_exploited_vulnerabilities_schema.json
    resource: tests/upstream/known_exploited_vulnerabilities_schema.json
    title: the whole file
  - resource: https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities_schema.json
    title: the copy CISA serves
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# CISA's KEV JSON schema

CISA serves `known_exploited_vulnerabilities_schema.json` from `www.cisa.gov`, and `cisagov/kev-data` holds the same bytes, git object `ec422845`. The file declares JSON Schema draft-07 and states no version. Its history in the mirror has two commits, of 2025-01-27 and 2026-09-17, so this project names the edition `2026-09-17`.[^check_upstream_release.py]

The file names a root object with four required keys and one definition, `vulnerability`, which has twelve keys, eight of them required. It sets no `additionalProperties`, so its objects are open.[^known_exploited_vulnerabilities_schema.json]

[^check_upstream_release.py]: scripts/check_upstream_release.py, the pins
[^known_exploited_vulnerabilities_schema.json]: tests/upstream/known_exploited_vulnerabilities_schema.json, the whole file
