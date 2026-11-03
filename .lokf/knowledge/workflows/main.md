---
type: Service
id: https://w3id.org/lmodel/kev-catalog/knowledge/workflows/main
title: Build and test (main.yaml)
description: "The Build and test workflow, `.github/workflows/main.yaml`: on a push to `main` and every pull request, its `test` job lints, tests and checks the adapt copy across Python 3.10 to 3.14, and its `kev-data` job validates the pinned catalogue in full."
genre: reference
resource: .github/workflows/main.yaml
dependsOn:
  - https://w3id.org/lmodel/kev-catalog/knowledge/datasets/example-data
  - https://w3id.org/lmodel/kev-catalog/knowledge/datasets/pinned-kev-catalogue-release
sources:
  - id: main.yaml
    resource: .github/workflows/main.yaml
    title: the header comment, the on key and the jobs
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# Build and test (main.yaml)

`.github/workflows/main.yaml` runs on a push to `main` and on every pull request. Its `test` job runs `just test` on Python 3.10 to 3.14. On 3.13 alone it also runs `just lint` and `just lokf-adapt-check`. Its `kev-data` job restores the catalogue from a cache keyed on the manifest, then runs `just test-kev-data`. Both jobs read the checkout only, and install with `uv sync --locked`.[^main.yaml]

[^main.yaml]: .github/workflows/main.yaml, the header comment, the on key and the jobs
