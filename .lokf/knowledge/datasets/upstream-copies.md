---
type: Dataset
id: https://w3id.org/lmodel/kev-catalog/knowledge/datasets/upstream-copies
title: Upstream copies
description: "The exact copies of CISA's files under `tests/upstream/`: the JSON schema and the licence of the mirror, each held to its pin by `tests/test_upstream.py`. The test walks the JSON schema, and fails on any part with no element in the LinkML schema."
genre: reference
resource: tests/upstream
derivedFrom:
  - https://w3id.org/lmodel/kev-catalog/knowledge/references/cisa-kev-json-schema
  - https://w3id.org/lmodel/kev-catalog/knowledge/references/cisagov-kev-data
sources:
  - id: notice
    resource: NOTICE
    title: the Known Exploited Vulnerabilities section
  - id: test_upstream.py
    resource: tests/test_upstream.py
    title: the walk and the departures
  - resource: tests/upstream
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# Upstream copies

`tests/upstream/known_exploited_vulnerabilities_schema.json` and `tests/upstream/LICENSE` are byte-for-byte copies, which CC0 1.0 allows.[^notice]

`tests/test_upstream.py` compares each with the hashes in `scripts/check_upstream_release.py`. It then walks the JSON schema. Each definition, property, required key, cardinality, type, format and pattern must have its element in the LinkML schema, and each enum value must be named in its property's description. The walk fails on a JSON Schema keyword it does not read. So a new edition with `oneOf`, `if` or `additionalProperties` fails until the schema states the rule or a departure lists it.[^test_upstream.py]

[^notice]: NOTICE, the Known Exploited Vulnerabilities section
[^test_upstream.py]: tests/test_upstream.py, the walk and the departures
