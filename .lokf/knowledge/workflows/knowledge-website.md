---
type: Service
id: https://w3id.org/lmodel/kev-catalog/knowledge/workflows/knowledge-website
title: Knowledge website (knowledge-website.yaml)
description: "The Knowledge website workflow, `.github/workflows/knowledge-website.yaml`: it builds the site on a change to its inputs and on Mondays at 05:23 UTC, and its `deploy` job publishes to GitHub Pages from `main` once `KNOWLEDGE_WEBSITE_ENABLED` is `true`."
genre: reference
resource: .github/workflows/knowledge-website.yaml
sources:
  - id: knowledge-website.yaml
    resource: .github/workflows/knowledge-website.yaml
    title: the header comment, the on key and the jobs
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# Knowledge website (knowledge-website.yaml)

`.github/workflows/knowledge-website.yaml` builds the site in `website/` on a pull request or push that touches its inputs, on Mondays at 05:23 UTC and by hand. Its `build` job reads the checkout only. Its `deploy` job alone holds `pages: write` and `id-token: write`, and deploys from `main` once `KNOWLEDGE_WEBSITE_ENABLED` is `true`.[^knowledge-website.yaml]

[^knowledge-website.yaml]: .github/workflows/knowledge-website.yaml, the header comment, the on key and the jobs
