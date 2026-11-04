---
type: KevCatalog
id: https://w3id.org/lmodel/kev-catalog/knowledge/datasets/pinned-kev-catalogue-release
title: The pinned KEV catalogue release
description: "The release of the KEV catalog that the tests pin: `catalogVersion` 2026.10.30, released 2026-10-30, with a count of 1,766 entries, fetched from `cisagov/kev-data` at commit `7ccba8e1223c` and validated in full by `just test-kev-data`. This concept lists no entries inline."
genre: reference
resource: tests/data/kev-data/manifest.json
derivedFrom:
  - https://w3id.org/lmodel/kev-catalog/knowledge/references/cisagov-kev-data
kev_title: CISA Catalog of Known Exploited Vulnerabilities
catalogVersion: 2026.10.30
dateReleased: "2026-10-30T17:02:45.3665Z"
count: 1766
vulnerabilities: []
sources:
  - id: manifest.json
    resource: tests/data/kev-data/manifest.json
    title: the commit, the size and the hashes
  - id: test_kev_data.py
    resource: tests/test_kev_data.py
    title: the profile and the departures
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# The pinned KEV catalogue release

`tests/data/kev-data/manifest.json` pins this release by its address at commit `7ccba8e1223c`, its size of 1,826,755 bytes, its SHA-256 and its git object hash `db928594`.[^manifest.json]

`just test-kev-data` fetches the file into `tmp/kev-data/` and validates it unchanged through the LinkML validator, the committed JSON Schema and both generated models. `tests/test_kev_data.py` also checks the numbers the file shows:[^test_kev_data.py]

- the file has 1,766 entries, with a `count` equal to that length and no CVE listed twice;
- `knownRansomwareCampaignUse` is `Known` on 361 entries and `Unknown` on 1,405;
- `forensicTriage` is `Yes` on 96 entries and `No` on 1,670;
- `cwes` is empty on 175 entries;
- `requiredAction` names BOD 26-04 on 149 entries and BOD 22-01 on 340.

The one departure from CISA's JSON schema is the file's `title`, a key that schema does not list.

This concept is typed `KevCatalog`, so it must carry the `vulnerabilities` key. That key takes whole entries in the adapt copy, not references, so its list here is empty: the entries are in the file.[^manifest.json]

[^manifest.json]: tests/data/kev-data/manifest.json, the commit, the size and the hashes
[^test_kev_data.py]: tests/test_kev_data.py, the profile and the departures
