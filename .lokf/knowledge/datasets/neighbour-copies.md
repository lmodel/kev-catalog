---
type: Dataset
id: https://w3id.org/lmodel/kev-catalog/knowledge/datasets/neighbour-copies
title: Neighbours' adapt copies
description: The adapt copies of other lmodel repositories under `tests/neighbours/`, each pinned by its SHA-256 in `tests/test_schema_rules.py`. The test holds this repository's copy apart from them and from LOKF, so that a new shared name fails.
genre: reference
resource: tests/neighbours
relatedTo:
  - https://w3id.org/lmodel/kev-catalog/knowledge/glossary/adapt-copy
sources:
  - id: test_schema_rules.py
    resource: tests/test_schema_rules.py
    title: the neighbours and the shared keys
  - id: test_mappings.py
    resource: tests/test_mappings.py
    title: the neighbour check
  - resource: tests/neighbours
generated:
  by: process:ktl-librarian
  at: "2026-11-04T21:49:33Z"
status: draft
---

# Neighbours' adapt copies

`tests/neighbours/` holds each neighbour's schema release asset, pinned by SHA-256 in `tests/test_schema_rules.py`, which names the release of each. The test keeps the adapt copy's names apart from LOKF's and the neighbours'. No class, enum or type is shared. lmodel/stix's copy shares the keys `count` and `product`, and lmodel/cve's shares `product`. Each has another IRI in the neighbour's copy. They are shared because they are CISA's own keys.[^test_schema_rules.py]

`tests/test_mappings.py` also reads these copies: a mapping to a term of lmodel/cve, lmodel/stix or lmodel/spdx must name a term the copy declares.[^test_mappings.py]

[^test_schema_rules.py]: tests/test_schema_rules.py, the neighbours and the shared keys
[^test_mappings.py]: tests/test_mappings.py, the neighbour check
