---
type: GlossaryTerm
id: https://w3id.org/lmodel/kev-catalog/knowledge/glossary/forensic-triage
title: Forensic triage (forensicTriage)
description: "The KEV key `forensicTriage`: `Yes` when BOD 26-04 calls for forensic triage of a vulnerability and `No` when it does not. CISA types it as a string and names the two values in its description, and the schema makes them an enum."
definedBy:
  - https://w3id.org/lmodel/kev-catalog/knowledge/references/cisa-kev-json-schema
sources:
  - id: kev_catalog.yaml
    resource: src/kev_catalog/schema/kev_catalog.yaml
    title: the forensicTriage slot and the KevForensicTriage enum
  - id: index.md
    resource: docs/index.md
    title: the Validating data section
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# Forensic triage (forensicTriage)

`forensicTriage` says whether BOD 26-04 calls for forensic triage of the vulnerability. Its values are `Yes` and `No`. CISA types the key as a string, and names the two values in its description, so the schema's `KevForensicTriage` enum takes its values from that sentence. The key is optional in CISA's JSON schema.[^kev_catalog.yaml]

In YAML, quote the values: unquoted, YAML reads them as booleans, and they fail. CISA's JSON does not have this problem.[^index.md]

[^kev_catalog.yaml]: src/kev_catalog/schema/kev_catalog.yaml, the forensicTriage slot and the KevForensicTriage enum
[^index.md]: docs/index.md, the Validating data section
