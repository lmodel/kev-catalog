---
type: Dataset
id: https://w3id.org/lmodel/kev-catalog/knowledge/datasets/generated-artefacts
title: Generated artefacts
description: "What the LinkML generators write from the schema: `project/` (JSON Schema, OWL, SHACL, ShEx, JSON-LD and others), the Python models in `src/kev_catalog/datamodel/`, and the merged schema in `docs/schema/`. They are never edited by hand."
genre: reference
resource: project
derivedFrom:
  - https://w3id.org/lmodel/kev-catalog/knowledge/datasets/kev-catalog-linkml-schema
sources:
  - id: justfile
    resource: justfile
    title: the gen-project and gen-doc recipes
  - id: test_data.py
    resource: tests/test_data.py
    title: the valid examples
  - id: generators.yaml
    resource: .linkml/generators.yaml
    title: the generators' settings
  - resource: project
  - resource: docs/schema
  - resource: src/kev_catalog/datamodel
  - resource: config.public.mk
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# Generated artefacts

`just gen-project` writes `project/` and the Python models in `src/kev_catalog/datamodel/`. `just gen-doc` writes the merged schema in `docs/schema/` and the element pages in `docs/elements/`, which git ignores. `.linkml/generators.yaml` holds the generators' settings, and `config.public.mk` names that file.[^justfile]

`tests/test_data.py` checks the examples against the committed `project/jsonschema/kev_catalog.schema.json`, under the draft that file declares.[^test_data.py]

`just gen-project` also rewrites parts that carry no change, such as the date in the Excel file.[^generators.yaml]

[^justfile]: justfile, the gen-project and gen-doc recipes
[^test_data.py]: tests/test_data.py, the valid examples
[^generators.yaml]: .linkml/generators.yaml, the generators' settings
