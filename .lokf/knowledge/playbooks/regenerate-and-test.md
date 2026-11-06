---
type: Playbook
id: https://w3id.org/lmodel/kev-catalog/knowledge/playbooks/regenerate-and-test
title: Regenerate and test after a schema change
description: "How to change the schema: edit `src/kev_catalog/schema/kev_catalog.yaml`, then run `just lint`, `just gen-project`, `just gen-doc`, `just lokf-adapt` and `just test`, and commit what they write."
genre: how-to
dependsOn:
  - https://w3id.org/lmodel/kev-catalog/knowledge/datasets/kev-catalog-linkml-schema
sources:
  - id: contributing.md
    resource: CONTRIBUTING.md
    title: Before opening a pull request
  - id: justfile
    resource: justfile
    title: the lint, gen-project and test recipes
  - id: project.justfile
    resource: project.justfile
    title: the lokf-adapt recipes and their roots
generated:
  by: process:ktl-librarian
  at: "2026-11-06T21:21:49Z"
status: draft
---

# Regenerate and test after a schema change

1. Edit `src/kev_catalog/schema/kev_catalog.yaml`. Never edit `project/`, `src/kev_catalog/datamodel/`, `docs/schema/` or `.lokf/schema/kev-catalog.yaml`, which are generated.[^contributing.md]
2. Run `just lint`. A warning fails it as an error does.[^justfile]
3. Run `just gen-project` and `just gen-doc`.
4. Run `just lokf-adapt`, or `just lokf-adapt-check` to see whether the copy is stale.[^project.justfile]
5. Run `just test`: schema generation, `pytest` and the examples.[^justfile]
6. Add an example for a new class and a counter-example for a new constraint.[^contributing.md]

[^contributing.md]: CONTRIBUTING.md, Before opening a pull request
[^justfile]: justfile, the lint, gen-project and test recipes
[^project.justfile]: project.justfile, the lokf-adapt recipes and their roots
