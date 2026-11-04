---
type: Playbook
id: https://w3id.org/lmodel/kev-catalog/knowledge/playbooks/release
title: Release a version
description: "How a version is released: changelog entries under `## [Unreleased]`, a releasing commit type, the `v0.0.0` baseline tag before the first release, and `semantic-release.yml`, which tags and publishes on the merge and dispatches the knowledge release."
genre: how-to
dependsOn:
  - https://w3id.org/lmodel/kev-catalog/knowledge/workflows/semantic-release
references:
  - https://w3id.org/lmodel/kev-catalog/knowledge/workflows/knowledge-release
sources:
  - id: contributing.md
    resource: CONTRIBUTING.md
    title: the Releasing (maintainers) section
  - id: releaserc
    resource: .releaserc.json
    title: the release rules
  - id: changelog
    resource: CHANGELOG.md
    title: the baseline paragraph
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# Release a version

1. Write each change under `## [Unreleased]` in `CHANGELOG.md`. The release job refuses an empty section.[^contributing.md]
2. Give the commit the type that says what it is. Only `feat:`, `fix:`, `security:` and a breaking change start a release, and below 1.0.0 a breaking change bumps the minor version.[^releaserc]
3. Before the first releasing merge, push the `v0.0.0` baseline tag on `main`, so the first release is 0.1.0.[^changelog]
4. On the merge, `semantic-release.yml` retitles the section, commits `CHANGELOG.md`, tags `vX.Y.Z` and publishes the GitHub release. Once `KNOWLEDGE_RELEASE_ENABLED` is `true`, it dispatches the knowledge release, which attaches `schema-<tag>-kev-catalog.yaml`, the bundle zip and the Copilot skill zip, each with its `.sha256` and attestation.[^contributing.md]

[^contributing.md]: CONTRIBUTING.md, the Releasing (maintainers) section
[^releaserc]: .releaserc.json, the release rules
[^changelog]: CHANGELOG.md, the baseline paragraph
