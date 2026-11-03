---
type: Policy
id: https://w3id.org/lmodel/kev-catalog/knowledge/policies/security-policy
title: Security policy
description: How to report a vulnerability (GitHub's private vulnerability reporting), which release receives fixes (the latest), what executes in the repository and what holds each surface, what the upstream watch and the fetcher may reach, and the two repository settings not yet in force.
genre: reference
resource: SECURITY.md
about:
  - https://w3id.org/lmodel/kev-catalog/knowledge/workflows/main
  - https://w3id.org/lmodel/kev-catalog/knowledge/workflows/lint-and-docs
  - https://w3id.org/lmodel/kev-catalog/knowledge/workflows/upstream-watch
  - https://w3id.org/lmodel/kev-catalog/knowledge/workflows/semantic-release
  - https://w3id.org/lmodel/kev-catalog/knowledge/workflows/knowledge-website
  - https://w3id.org/lmodel/kev-catalog/knowledge/workflows/knowledge-librarian
  - https://w3id.org/lmodel/kev-catalog/knowledge/workflows/knowledge-registrar
  - https://w3id.org/lmodel/kev-catalog/knowledge/workflows/knowledge-release
  - https://w3id.org/lmodel/kev-catalog/knowledge/workflows/knowledge-sync
sources:
  - id: security.md
    resource: SECURITY.md
    title: every section
  - id: dependabot.yml
    resource: .github/dependabot.yml
    title: the five update entries
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# Security policy

`SECURITY.md` asks for a vulnerability to be reported through GitHub's private vulnerability reporting, not in a public issue. One person maintains the repository, so a first reply takes days, and there is no bounty. Only the latest release receives fixes. A vulnerability in a product goes to its vendor, and a report of exploitation goes to CISA.[^security.md]

A release carries the schema and the Python models generated from it. Nothing goes to PyPI. When the bundle or the schema changed, the knowledge release attaches three assets, each with its `.sha256` and a build-provenance attestation: the schema's adapt copy, the bundle as a zip and a Microsoft 365 Copilot skill zip.[^security.md]

`scripts/check_upstream_release.py` runs only in the upstream watch. It sends the workflow's token, which can write issues, to `api.github.com` alone. It reads at most 5 MB of an answer, and follows a redirect only over https to `www.cisa.gov` or `api.github.com`. `scripts/fetch_kev_data.py` takes the catalogue only from `raw.githubusercontent.com`, and refuses a file whose size or hashes are not the pinned ones.[^security.md]

Every workflow declares `permissions: {}` at the top, pins its actions to commit hashes that Dependabot keeps current, and runs harden-runner in audit mode. Two settings are not yet in force: required reviewers on the `release` Environment, and secret scanning with push protection.[^security.md] `.github/dependabot.yml` watches the actions, both uv locks and both npm locks.[^dependabot.yml]

[^security.md]: SECURITY.md, every section
[^dependabot.yml]: .github/dependabot.yml, the five update entries
