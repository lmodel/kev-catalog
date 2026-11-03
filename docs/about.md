# About kev-catalog

This page is for anyone reading the [LinkML](https://linkml.io) schema's elements:
it says what the classes are and what the model leaves out.

The KEV catalog is one JSON file that CISA republishes when an entry is added or
changed. `KevCatalog` is one release of that file, and `KevVulnerability` is one
entry of it, identified by its CVE identifier. The keys are CISA's own, such as
`cveID` and `vendorProject`, and so are the values, such as `Known` and `Yes`.

The schema follows CISA's JSON schema, which `tests/upstream/` copies exactly. It
departs from that file in three ways, and `tests/test_upstream.py` lists each with
its reason:

- it names `title`, which every real file carries though the JSON schema lists no
  such property;
- it makes `knownRansomwareCampaignUse` and `forensicTriage` enums, since CISA types
  them as strings but names their values in their descriptions;
- its classes are closed, so a key it does not name fails, where CISA's open objects
  would accept it.

## What is left out

- Any rule CISA does not state. No slot relates `dueDate` to `dateAdded`, and no
  pattern is set on `catalogVersion`.
- The contents of `notes`, which stays one string. It often holds addresses
  separated by ` ; `, but CISA states no form for it.
- The terms of the directives behind the catalog, and any contact address, date or
  count from them. They belong at their source: CISA's
  [directives](https://www.cisa.gov/directives) page, which answered a plain client
  with 403 on 2026-11-03.
- The CSV form of the catalog, which holds the same keys as the JSON.
