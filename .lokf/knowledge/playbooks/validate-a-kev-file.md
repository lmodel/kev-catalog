---
type: Playbook
id: https://w3id.org/lmodel/kev-catalog/knowledge/playbooks/validate-a-kev-file
title: Validate a KEV file
description: "How to validate a real KEV file with `linkml-validate` against `KevCatalog`, what the validator checks, and the two rules only `tests/kev_rules.py` checks: the count and a repeated CVE."
genre: how-to
dependsOn:
  - https://w3id.org/lmodel/kev-catalog/knowledge/datasets/kev-catalog-linkml-schema
references:
  - https://w3id.org/lmodel/kev-catalog/knowledge/datasets/pinned-kev-catalogue-release
sources:
  - id: index.md
    resource: docs/index.md
    title: the Validating data section
  - id: kev_rules.py
    resource: tests/kev_rules.py
    title: the catalogue rules
  - id: project.justfile
    resource: project.justfile
    title: the test-kev-data recipe
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# Validate a KEV file

Run `linkml-validate -s src/kev_catalog/schema/kev_catalog.yaml -C KevCatalog known_exploited_vulnerabilities.json`. The validator checks the required keys, the form of `cveID` and each code in `cwes`, the dates, the two enums, and that no object has a key the schema does not name.[^index.md]

Two rules are out of its reach. `tests/kev_rules.py` checks that `count` is the length of the list and that no two entries name one CVE.[^kev_rules.py]

To validate the pinned catalogue, run `just test-kev-data`.[^project.justfile]

[^index.md]: docs/index.md, the Validating data section
[^kev_rules.py]: tests/kev_rules.py, the catalogue rules
[^project.justfile]: project.justfile, the test-kev-data recipe
