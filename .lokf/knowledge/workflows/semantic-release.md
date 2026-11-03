---
type: Service
id: https://w3id.org/lmodel/kev-catalog/knowledge/workflows/semantic-release
title: Semantic release (semantic-release.yml)
description: "The Semantic release workflow, `.github/workflows/semantic-release.yml`: `plan` previews a pull request's release, and `release`, on a push to `main` in the `release` Environment, promotes the changelog, tags, publishes and dispatches the knowledge release."
genre: reference
resource: .github/workflows/semantic-release.yml
references:
  - https://w3id.org/lmodel/kev-catalog/knowledge/workflows/knowledge-release
sources:
  - id: semantic-release.yml
    resource: .github/workflows/semantic-release.yml
    title: the header comment, the on key and the jobs
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# Semantic release (semantic-release.yml)

`.github/workflows/semantic-release.yml` has two jobs. On a pull request to `main`, `plan` reads the checkout and says what the merge would release. On a push to `main`, `release` runs in the `release` Environment. It installs its tools from `.github/release/package-lock.json` with `npm ci --ignore-scripts`. It then promotes the changelog, tags the release, publishes it, and dispatches the knowledge release once `KNOWLEDGE_RELEASE_ENABLED` is `true`.[^semantic-release.yml]

[^semantic-release.yml]: .github/workflows/semantic-release.yml, the header comment, the on key and the jobs
