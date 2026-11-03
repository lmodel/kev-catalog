# kev-catalog

This project is a LinkML model of the JSON format of the Known Exploited
Vulnerabilities (KEV) catalog that the Cybersecurity and Infrastructure Security
Agency (CISA) publishes. It follows CISA's JSON schema at its edition of
17 September 2026. CISA's keys and values are the schema's, so a real KEV file
validates unchanged.

- [Schema documentation](elements/index.md), generated from the schema
- [About](about.md): what the classes are and what the model leaves out
- [`kev_catalog.yaml`](schema/kev_catalog.yaml): the schema

## Validating data

`linkml-validate -s src/kev_catalog/schema/kev_catalog.yaml -C KevCatalog known_exploited_vulnerabilities.json`
checks a file against the JSON Schema generated from the schema, and
`tests/test_data.py` holds every example to it. The validator checks:

- that a catalog has its version, its release date and time, its count and its
  list of entries, and that an entry has the eight keys CISA requires;
- that `cveID` and each code in `cwes` have the form CISA states;
- that `dateAdded` and `dueDate` are dates, and `dateReleased` a date and time;
- that `knownRansomwareCampaignUse` is `Known` or `Unknown`, and `forensicTriage`
  is `Yes` or `No`;
- that an object has no key the schema does not name.

Two rules are out of the validator's reach, and `tests/kev_rules.py` checks them in
Python, over the examples and the pinned catalogue: `count` is the length of the
list, and no two entries name one CVE.

In YAML, quote `"Yes"` and `"No"`. Unquoted, YAML reads them as booleans, and they
fail. CISA's JSON has no such trap.

## The real file

`just test-kev-data` fetches one dated catalogue, pinned by its git object hash in
`tests/data/kev-data/manifest.json`, and validates it in full, unchanged. Twelve of
its entries sit under `tests/data/kev-data/extract/`, and `just test` checks those
offline.
