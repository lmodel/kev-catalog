---
type: Playbook
id: https://w3id.org/lmodel/kev-catalog/knowledge/playbooks/knowledge-sources
title: Knowledge sources map
description: "The librarian's scrape map: every repository location and external source this bundle derives concepts from, the concepts each yields, how to re-check each on a refresh run, and the paths left out on purpose."
genre: reference
resource: .
about:
  - https://w3id.org/lmodel/kev-catalog/knowledge/datasets/kev-catalog-linkml-schema
exclusions:
  - resource: .github/ISSUE_TEMPLATE
    reason: Issue forms, which are governance text and state nothing about the schema.
  - resource: .github/pull_request_template.md
    reason: The pull request checklist, which repeats CONTRIBUTING.md.
  - resource: .github/PULL_REQUEST_TEMPLATE
    reason: The knowledge sync's pull request form, a copy from the sidecar.
  - resource: CODE_OF_CONDUCT.md
    reason: The Contributor Covenant, governance text with nothing about the schema.
  - resource: uv.lock
    reason: The package's lock file, tooling that pins versions.
  - resource: pyproject.toml
    reason: Package metadata and spell checkers' settings; the changelog states the Python project's name.
  - resource: .gitignore
    reason: "Tooling: the files git ignores."
  - resource: .editorconfig
    reason: "Tooling: editor settings."
  - resource: .yamllint.yaml
    reason: "Tooling: the YAML linter's settings."
  - resource: .pre-commit-config.yaml
    reason: "Tooling: the hooks and the files they leave alone."
  - resource: .markdownlint-cli2.jsonc
    reason: "Tooling: the Markdown linter's settings."
  - resource: lychee.toml
    reason: "Tooling: the link checker's settings."
  - resource: .copier-answers.yml
    reason: The copier template's answers, which `just update` reads.
  - resource: src/README.md
    reason: Text from the project template.
  - resource: docs/templates-linkml
    reason: The template's placeholders for gen-doc, not pages.
  - resource: docs/elements
    reason: "A placeholder: gen-doc writes the pages and git ignores them."
  - resource: examples/README.md
    reason: Text from the project template about generated example output.
  - resource: src/kev_catalog/__init__.py
    reason: Package plumbing.
  - resource: src/kev_catalog/_version.py
    reason: Package plumbing.
  - resource: llms.txt
    reason: The pointer that sends agents to this bundle.
  - resource: knowledge_bundle
    reason: The sidecar's link to the bundle.
  - resource: .lokf/README.md
    reason: The sidecar's own guide, a copy from its template.
  - resource: .lokf/.gitattributes
    reason: The sidecar's line-ending settings.
  - resource: .lokf/.gitignore
    reason: The sidecar's ignore list.
  - resource: .lokf/ingest.yaml.sample
    reason: The ingest's example manifest, unused here.
  - resource: .lokf/schema/lokf.yaml
    reason: LOKF's own schema, pinned from the installed package.
  - resource: .lokf/queries.http
    reason: The sidecar's sample queries.
  - resource: .lokf/uv.lock
    reason: The sidecar's lock file.
  - resource: .lokf/scripts
    reason: The sidecar's scripts, copies from its templates.
  - resource: .lokf/m365
    reason: The sidecar's Copilot skill builder, a copy from its template.
sources:
  - resource: README.md
  - resource: docs/about.md
  - resource: docs/index.md
  - resource: src/kev_catalog/schema
  - resource: src/kev_catalog/datamodel
  - resource: project.justfile
  - resource: .lokf/schema/kev-catalog.yaml
  - resource: .lokf/justfile
  - resource: .lokf/pyproject.toml
  - resource: NOTICE
  - resource: LICENSE
  - resource: scripts
  - resource: .github/scripts
  - resource: .github/workflows
  - resource: .github/dependabot.yml
  - resource: .github/release
  - resource: justfile
  - resource: .linkml/generators.yaml
  - resource: .linkmllint.yaml
  - resource: project
  - resource: docs/schema
  - resource: tests
  - resource: CONTRIBUTING.md
  - resource: .releaserc.json
  - resource: CHANGELOG.md
  - resource: website
  - resource: SECURITY.md
  - resource: AI_COVENANT.md
  - resource: config.public.mk
generated:
  by: process:ktl-librarian
  at: "2026-11-06T21:21:49Z"
status: draft
---

# Knowledge sources map

| Source | Yields | Re-check |
| --- | --- | --- |
| `src/kev_catalog/schema`, `project.justfile`, `.lokf/schema/kev-catalog.yaml`, `.lokf/justfile`, `.lokf/pyproject.toml` | `datasets/kev-catalog-linkml-schema.md`, `glossary/adapt-copy.md` | the schema's header and classes, and the adapt recipes |
| `tests/upstream`, `scripts` | `references/cisa-kev-json-schema.md`, `references/cisagov-kev-data.md`, `datasets/upstream-copies.md`, `playbooks/move-the-upstream-pins.md` | the pins, and what the upstream watch reports |
| `tests/data`, `tests` | `datasets/example-data.md`, `datasets/pinned-kev-catalogue-release.md`, `datasets/worked-entry-cve-2021-44228.md`, `datasets/neighbour-copies.md` | the manifest, the profile in `tests/test_kev_data.py`, and the neighbours' pins |
| `README.md`, `docs/about.md`, `docs/index.md`, `CHANGELOG.md` | `glossary/kev.md`, `glossary/forensic-triage.md`, `explanations/keys-edition-and-departures.md`, `explanations/mappings.md`, `playbooks/validate-a-kev-file.md` | the headings each concept cites |
| `justfile`, `CONTRIBUTING.md`, `.releaserc.json` | `playbooks/regenerate-and-test.md`, `playbooks/release.md` | the recipes and the release rules |
| `project`, `docs/schema`, `src/kev_catalog/datamodel`, `.linkml/generators.yaml`, `config.public.mk` | `datasets/generated-artefacts.md` | the generators' settings |
| `.linkmllint.yaml` | `explanations/keys-edition-and-departures.md` | the naming rule's comment |
| `SECURITY.md`, `AI_COVENANT.md`, `NOTICE`, `LICENSE`, `.github/dependabot.yml`, `.github/release` | `policies/security-policy.md`, `policies/ai-covenant.md`, `policies/license-and-attribution.md` | each file's sections |
| `.github/workflows`, `.github/scripts` | one concept under `workflows/` per workflow | the on key and the jobs |
| `website` | `services/documentation-site.md` | `website/README.md` and `site.config.mjs` |
| The pages of BOD 26-04 | `references/bod-26-04.md` | whether CISA's page answers a plain client, never by getting round a refusal |

The catalogue changes most weekdays, and the pin in `tests/data/kev-data/manifest.json` moves only by hand, so the bundle's numbers follow the pin and not CISA's latest file.
