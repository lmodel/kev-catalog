---
type: Service
id: https://w3id.org/lmodel/kev-catalog/knowledge/workflows/knowledge-release
title: Knowledge Release (knowledge-release.yaml)
description: "The Knowledge Release workflow, `.github/workflows/knowledge-release.yaml`: on a published release once `KNOWLEDGE_RELEASE_ENABLED` is `true`, or when dispatched, it attaches the schema copy, the bundle zip and the Copilot skill zip, each with its `.sha256` and an attestation."
genre: reference
resource: .github/workflows/knowledge-release.yaml
references:
  - https://w3id.org/lmodel/kev-catalog/knowledge/datasets/kev-catalog-linkml-schema
sources:
  - id: knowledge-release.yaml
    resource: .github/workflows/knowledge-release.yaml
    title: the header comment, the on key and the jobs
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# Knowledge Release (knowledge-release.yaml)

`.github/workflows/knowledge-release.yaml` runs on a published release once `KNOWLEDGE_RELEASE_ENABLED` is `true`, and when dispatched. Its `pack` job reads the checkout, validates the bundle and packs it, and says whether the bundle or the schema changed since the last release. Its `attach` job then attaches the assets, each with its `.sha256` and a build-provenance attestation.[^knowledge-release.yaml]

[^knowledge-release.yaml]: .github/workflows/knowledge-release.yaml, the header comment, the on key and the jobs
