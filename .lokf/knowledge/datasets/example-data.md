---
type: Dataset
id: https://w3id.org/lmodel/kev-catalog/knowledge/datasets/example-data
title: Example data
description: "The examples the tests hold the schema to, under `tests/data/`: valid examples, counter-examples that each name the JSON pointer they fail at, a folder for valid data the generated dataclasses refuse, and the pinned catalogue's manifest and twelve-entry extract."
genre: reference
resource: tests/data
references:
  - https://w3id.org/lmodel/kev-catalog/knowledge/datasets/kev-catalog-linkml-schema
hasPart:
  - https://w3id.org/lmodel/kev-catalog/knowledge/datasets/worked-entry-cve-2021-44228
derivedFrom:
  - https://w3id.org/lmodel/kev-catalog/knowledge/datasets/pinned-kev-catalogue-release
sources:
  - id: tests-data-readme.md
    resource: tests/data/README.md
    title: the whole file
  - id: test_data.py
    resource: tests/test_data.py
    title: the valid examples
  - id: kev_rules.py
    resource: tests/kev_rules.py
    title: the catalogue rules
  - resource: tests/data
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# Example data

`tests/data/` holds the examples, and `tests/data/README.md` says what each folder is for:[^tests-data-readme.md]

- `valid/` holds data that conforms, named `ClassName-anything.yaml`. Each entry is a real one, or a real one cut down to the required keys.
- `invalid/` holds counter-examples. The first line of each, `# Fails at: <pointer>`, names where the validator must report it, and `tests/test_data.py` fails one that fails anywhere else.[^test_data.py]
- `problem/valid/` holds a catalogue with an empty list, which CISA's JSON schema accepts and the generated dataclasses refuse under LinkML 1.12.1.
- `kev-data/` holds the manifest of the pinned catalogue and an extract of twelve real entries, copied unchanged.

`tests/kev_rules.py` holds two rules that no generated validator states: `count` is the length of the list, and no two entries name one CVE.[^kev_rules.py]

[^tests-data-readme.md]: tests/data/README.md, the whole file
[^test_data.py]: tests/test_data.py, the valid examples
[^kev_rules.py]: tests/kev_rules.py, the catalogue rules
