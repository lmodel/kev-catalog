---
type: Service
id: https://w3id.org/lmodel/kev-catalog/knowledge/workflows/knowledge-sync
title: Knowledge sync (knowledge-sync.yaml)
description: "The Knowledge sync workflow, `.github/workflows/knowledge-sync.yaml`: every Monday at 04:10 UTC it copies the sidecar files from KTL's newest release when the skills pin is behind, and opens one pull request."
genre: reference
resource: .github/workflows/knowledge-sync.yaml
references:
  - https://w3id.org/lmodel/kev-catalog/knowledge/workflows/knowledge-librarian
sources:
  - id: knowledge-sync.yaml
    resource: .github/workflows/knowledge-sync.yaml
    title: the header comment, the on key and the jobs
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# Knowledge sync (knowledge-sync.yaml)

`.github/workflows/knowledge-sync.yaml` runs every Monday at 04:10 UTC and by hand. It reads the skills pin and KTL's newest release, and when the pin is behind it copies the files `knowledge-sync.manifest` lists from that release. Its `publish` job opens or refreshes one pull request. A change to a workflow waits for the review Environment that `KNOWLEDGE_SYNC_REVIEW_ENVIRONMENT` names.[^knowledge-sync.yaml]

[^knowledge-sync.yaml]: .github/workflows/knowledge-sync.yaml, the header comment, the on key and the jobs
