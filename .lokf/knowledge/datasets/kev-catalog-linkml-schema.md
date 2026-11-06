---
type: Dataset
id: https://w3id.org/lmodel/kev-catalog/knowledge/datasets/kev-catalog-linkml-schema
title: kev-catalog LinkML schema
description: "The LinkML schema of the JSON format of the Known Exploited Vulnerabilities (KEV) catalog, `src/kev_catalog/schema/kev_catalog.yaml` (schema id `https://w3id.org/lmodel/kev-catalog`, version 2026-09-17): the classes `KevCatalog` and `KevVulnerability`, CISA's keys as its slots, and two enums. Its `lokf adapt` copy `.lokf/schema/kev-catalog.yaml` is the bundle's domain schema."
genre: reference
resource: src/kev_catalog/schema/kev_catalog.yaml
version: "2026-09-17"
license: Apache-2.0
derivedFrom:
  - https://w3id.org/lmodel/kev-catalog/knowledge/references/cisa-kev-json-schema
sources:
  - id: kev_catalog.yaml
    resource: src/kev_catalog/schema/kev_catalog.yaml
    title: the header, the classes, the slots and the enums
  - id: project.justfile
    resource: project.justfile
    title: the lokf-adapt recipes and their roots
  - resource: .lokf/schema/kev-catalog.yaml
    title: the copy lokf adapt wrote
  - resource: .lokf/justfile
    title: the schema line
  - resource: .lokf/pyproject.toml
    title: the tool.lokf table
generated:
  by: process:ktl-librarian
  at: "2026-11-06T21:21:49Z"
status: draft
---

# kev-catalog LinkML schema

`src/kev_catalog/schema/kev_catalog.yaml` is the schema. Its header gives `version: "2026-09-17"`, the date of the commit that last changed CISA's JSON schema in `cisagov/kev-data`, and `source`, that file's address at that commit. Its licence is Apache-2.0, and it imports only `linkml:types`.[^kev_catalog.yaml]

## Classes and slots

- **`KevCatalog`** is one published release of the catalog. It is the tree root. It holds `catalogVersion`, `dateReleased`, `count` and `vulnerabilities`, all four required, and an optional `title`.
- **`KevVulnerability`** is one entry. `cveID` identifies it. It requires `vendorProject`, `product`, `vulnerabilityName`, `dateAdded`, `shortDescription`, `requiredAction` and `dueDate`, and it may hold `knownRansomwareCampaignUse`, `forensicTriage`, `notes` and `cwes`.

`dateReleased` is a date and time, and `dateAdded` and `dueDate` are dates. `cveID` and each item of `cwes` carry the patterns CISA states. Two enums, `KevRansomwareCampaignUse` and `KevForensicTriage`, hold CISA's values. Each element cites its place in CISA's JSON schema in an `upstream_path` annotation.[^kev_catalog.yaml]

## As the bundle's domain schema

`just lokf-adapt` writes `.lokf/schema/kev-catalog.yaml`, rooted on both classes with `--prefix kev`. In the copy, LOKF's `id` replaces `cveID`, and `title` becomes `kev_title` with its IRI kept. `.lokf/justfile` names the copy on its `schema :=` line, and `.lokf/pyproject.toml` names it under `tool.lokf`.[^project.justfile]

[^kev_catalog.yaml]: src/kev_catalog/schema/kev_catalog.yaml, the header, the classes, the slots and the enums
[^project.justfile]: project.justfile, the lokf-adapt recipes and their roots
