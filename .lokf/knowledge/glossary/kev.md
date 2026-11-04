---
type: GlossaryTerm
id: https://w3id.org/lmodel/kev-catalog/knowledge/glossary/kev
title: Known Exploited Vulnerabilities (KEV)
description: "The Known Exploited Vulnerabilities (KEV) catalog: the list of CVEs that the Cybersecurity and Infrastructure Security Agency (CISA) publishes as a JSON and a CSV file, each entry naming the action it asks for and a due date."
definedBy:
  - https://w3id.org/lmodel/kev-catalog/knowledge/references/cisa-kev-json-schema
sources:
  - id: about.md
    resource: docs/about.md
    title: the opening paragraphs
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# Known Exploited Vulnerabilities (KEV)

The Known Exploited Vulnerabilities (KEV) catalog is a list that the Cybersecurity and Infrastructure Security Agency (CISA) publishes. Each entry names a CVE, the vendor and product, the action CISA asks for and the day it is due. CISA publishes it as one JSON file and one CSV file, and republishes them when an entry is added or changed.[^about.md]

In this schema a release of the file is a `KevCatalog`, and an entry is a `KevVulnerability`.

[^about.md]: docs/about.md, the opening paragraphs
