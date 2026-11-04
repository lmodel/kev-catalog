---
type: Service
id: https://w3id.org/lmodel/kev-catalog/knowledge/workflows/knowledge-registrar
title: Knowledge Registrar (knowledge-registrar.yaml)
description: "The Knowledge Registrar workflow, `.github/workflows/knowledge-registrar.yaml`: the gate of the sidecar. It validates the bundle and its conventions, and checks that each new `human:` confirmation is backed by an approval or a signed commit."
genre: reference
resource: .github/workflows/knowledge-registrar.yaml
about:
  - https://w3id.org/lmodel/kev-catalog/knowledge/playbooks/knowledge-sources
sources:
  - id: knowledge-registrar.yaml
    resource: .github/workflows/knowledge-registrar.yaml
    title: the header comment, the on key and the jobs
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# Knowledge Registrar (knowledge-registrar.yaml)

`.github/workflows/knowledge-registrar.yaml` is the gate of the Knowledge Trust Ladder (KTL) sidecar. It runs on a pull request that touches `.lokf/` or `knowledge_bundle`, on Mondays at 06:00 UTC and by hand. Its `validate` job runs `lokf validate --check-refs` and the conventions script. Its `provenance` job checks that each new `human:` confirmation is backed by the pull request's approval or a signed commit.[^knowledge-registrar.yaml]

[^knowledge-registrar.yaml]: .github/workflows/knowledge-registrar.yaml, the header comment, the on key and the jobs
