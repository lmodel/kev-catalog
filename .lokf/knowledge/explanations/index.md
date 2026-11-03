# Explanations

* [Keys, edition and departures](keys-edition-and-departures.md) - Why the schema keeps CISA's keys and values, why its version is a date, and where it departs from CISA's JSON schema: the `title` key, two enums, closed classes and null on an optional key. It also says why nothing imports `lmodel/vulnerability-core`.
* [Mappings and how each kind was chosen](mappings.md) - What the schema maps to and why each mapping has its kind: DCAT, schema.org, Dublin Core, SKOS, Wikidata, SPDX 3.0.1, SEPSES, lmodel/stix and lmodel/cve, with the sample of 120 entries that decided the kinds toward CVE. The schema's mappings are the one home for mappings, and `tests/test_mappings.py` holds each.
