---
type: Explanation
id: https://w3id.org/lmodel/kev-catalog/knowledge/explanations/keys-edition-and-departures
title: Keys, edition and departures
description: "Why the schema keeps CISA's keys and values, why its version is a date, and where it departs from CISA's JSON schema: the `title` key, two enums, closed classes and null on an optional key. It also says why nothing imports `lmodel/vulnerability-core`."
genre: explanation
about:
  - https://w3id.org/lmodel/kev-catalog/knowledge/datasets/kev-catalog-linkml-schema
sources:
  - id: linkmllint
    resource: .linkmllint.yaml
    title: the comment
  - id: kev_catalog.yaml
    resource: src/kev_catalog/schema/kev_catalog.yaml
    title: the header's comments
  - id: changelog
    resource: CHANGELOG.md
    title: the Changed and Removed sections
  - id: test_upstream.py
    resource: tests/test_upstream.py
    title: the departures
  - id: about.md
    resource: docs/about.md
    title: What is left out
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# Keys, edition and departures

A real KEV file must validate unchanged, so slots and permissible values keep CISA's spelling, such as `cveID` and `Known`. `.linkmllint.yaml` fits the naming rule to them and says why. Class and enum names keep the usual form, with a `Kev` prefix.[^linkmllint]

CISA's JSON schema states no version, so the header's `version` is the date of the commit that last changed the file.[^kev_catalog.yaml]

The schema imports only `linkml:types`. Its `KevVulnerability` has no base class, so an entry carries only the keys CISA's format has.[^changelog]

`tests/test_upstream.py` lists every departure from CISA's JSON schema with its reason:[^test_upstream.py]

- `title` is named, since every real file carries it, though the JSON schema lists no such property.
- `knownRansomwareCampaignUse` and `forensicTriage` are enums, since CISA names their values in their descriptions.
- Classes are closed, so an unnamed key fails here and passes upstream.
- An optional key may be null in the generated JSON Schema, which CISA's string types refuse. No generator option changes that, and the real file holds no null.

The schema states no rule of its own. Nothing relates `dueDate` to `dateAdded`, since CISA does not.[^about.md]

[^linkmllint]: .linkmllint.yaml, the comment
[^kev_catalog.yaml]: src/kev_catalog/schema/kev_catalog.yaml, the header's comments
[^changelog]: CHANGELOG.md, the Changed and Removed sections
[^test_upstream.py]: tests/test_upstream.py, the departures
[^about.md]: docs/about.md, What is left out
