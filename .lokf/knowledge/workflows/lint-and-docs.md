---
type: Service
id: https://w3id.org/lmodel/kev-catalog/knowledge/workflows/lint-and-docs
title: Lint and docs (lint-and-docs.yaml)
description: "The Lint and docs workflow, `.github/workflows/lint-and-docs.yaml`: ShellCheck, actionlint, the word budgets of CONTRIBUTING.md and SECURITY.md, markdownlint, lychee and codespell, on a push to `main`, every pull request and Mondays at 06:00 UTC."
genre: reference
resource: .github/workflows/lint-and-docs.yaml
sources:
  - id: lint-and-docs.yaml
    resource: .github/workflows/lint-and-docs.yaml
    title: the header comment, the on key and the jobs
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# Lint and docs (lint-and-docs.yaml)

`.github/workflows/lint-and-docs.yaml` runs on a push to `main`, on every pull request, on Mondays at 06:00 UTC and by hand. It runs ShellCheck and actionlint, holds `CONTRIBUTING.md` to 1000 words and `SECURITY.md` to 900, and runs markdownlint, lychee and codespell.[^lint-and-docs.yaml]

[^lint-and-docs.yaml]: .github/workflows/lint-and-docs.yaml, the header comment, the on key and the jobs
