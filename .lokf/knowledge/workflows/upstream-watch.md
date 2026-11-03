---
type: Service
id: https://w3id.org/lmodel/kev-catalog/knowledge/workflows/upstream-watch
title: Upstream watch (upstream-watch.yaml)
description: "The Upstream watch workflow, `.github/workflows/upstream-watch.yaml`: every Monday at 07:00 UTC and by hand, its `kev-sources` job runs `scripts/check_upstream_release.py` against the GitHub API and CISA's copy, and on a finding opens or updates the issue titled Upstream watch: the KEV JSON schema or licence has changed."
genre: reference
resource: .github/workflows/upstream-watch.yaml
about:
  - https://w3id.org/lmodel/kev-catalog/knowledge/references/cisa-kev-json-schema
sources:
  - id: upstream-watch.yaml
    resource: .github/workflows/upstream-watch.yaml
    title: the header comment, the on key and the jobs
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# Upstream watch (upstream-watch.yaml)

`.github/workflows/upstream-watch.yaml` runs every Monday at 07:00 UTC and by hand. Its one job, `kev-sources`, reads the checkout and holds `issues: write`. It runs `scripts/check_upstream_release.py` on the runner's Python, with the workflow's token, which the script sends to `api.github.com` alone. On a finding, `.github/scripts/report-issue.sh` opens the issue titled "Upstream watch: the KEV JSON schema or licence has changed", or comments on the one already open. The catalogue's daily data is no finding.[^upstream-watch.yaml]

[^upstream-watch.yaml]: .github/workflows/upstream-watch.yaml, the header comment, the on key and the jobs
