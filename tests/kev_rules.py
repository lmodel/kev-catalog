"""The rules of KEV's format that no generated validator states.

CISA's JSON schema describes `count` as the catalog's total, which JSON Schema
cannot compare with the length of a list, and the catalog keys its entries by
CVE identifier, which LinkML says through `identifier: true` and no generated
JSON Schema checks. tests/test_data.py holds the examples to these rules, and
tests/test_kev_data.py the pinned catalogue.
"""

from collections import Counter


def catalogue_faults(record):
    """What breaks the rules of a whole catalogue: the count is the length of
    its list, and no two entries name one CVE."""
    faults = []
    entries = record.get("vulnerabilities") or []
    if record.get("count") != len(entries):
        faults.append(
            f"count says {record.get('count')}, the list holds {len(entries)}"
        )
    repeated = sorted(
        cve for cve, n in Counter(e.get("cveID") for e in entries).items() if n > 1
    )
    if repeated:
        faults.append(f"repeats {', '.join(repeated)}")
    return faults
