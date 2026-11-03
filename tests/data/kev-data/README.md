# The pinned KEV catalogue

`manifest.json` pins one dated catalogue file from [cisagov/kev-data](https://github.com/cisagov/kev-data), the official mirror of CISA's data, by its address at a commit, its size, its SHA-256 and its git object hash. The catalogue changes most weekdays, so a dated pin is what keeps the test stable. The upstream watch is about the JSON schema, and it does not report new data.

`extract/known_exploited_vulnerabilities.json` holds twelve entries copied unchanged from that file, chosen because they vary: both values of each enum, no CWE and several, a four-digit CVE number and a long one, spaces at the edge of a value, and a `requiredAction` that names the older directive. The data is under CC0 1.0, on the terms [NOTICE](../../../NOTICE) gives.

`just test-kev-data` fetches the full file into `tmp/kev-data/`, refusing any host but `raw.githubusercontent.com`, and `tests/test_kev_data.py` validates it unchanged.

To move the pin, change the commit, size and hashes here together, then read what `tests/test_kev_data.py` reports: its `PROFILE` and `KNOWN_DATA_DEPARTURES` say what the file holds.
