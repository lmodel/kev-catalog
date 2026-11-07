---
lokf_version: "0.2"
okf_version: "0.2"
base_iri: https://w3id.org/lmodel/kev-catalog/knowledge/
context: https://w3id.org/lokf/context.jsonld
title: kev-catalog Knowledge Bundle
description: CISA Known Exploited Vulnerabilities (KEV) Catalog (LinkML)
license: https://creativecommons.org/licenses/by/4.0/
publisher:
  type: Person
  id: https://w3id.org/lmodel/kev-catalog/knowledge/person/noel-mcloughlin
  name: Noel McLoughlin
---

# kev-catalog Knowledge Bundle

A [LOKF](https://lokf.nolan-nichols.com) knowledge base for kev-catalog. Every Markdown file under `knowledge/` is one concept; together they form a queryable knowledge graph, derived from this repository's code and docs.

# Services

* [Documentation site](services/documentation-site.md) - The knowledge website in `website/`, an Astro Starlight site that the Knowledge website workflow publishes to GitHub Pages at `https://lmodel.github.io/kev-catalog/`: the README as its home page, `docs/`, the schema's pages, a page per concept and the four `lokf export` files, with redirects from the retired mkdocs site's addresses.

# Datasets

* [kev-catalog LinkML schema](datasets/kev-catalog-linkml-schema.md) - The LinkML schema of the JSON format of the Known Exploited Vulnerabilities (KEV) catalog, `src/kev_catalog/schema/kev_catalog.yaml` (schema id `https://w3id.org/lmodel/kev-catalog`, version 2026-09-17): the classes `KevCatalog` and `KevVulnerability`, CISA's keys as its slots, and two enums. Its `lokf adapt` copy `.lokf/schema/kev-catalog.yaml` is the bundle's domain schema.
* [The pinned KEV catalogue release](datasets/pinned-kev-catalogue-release.md) - The release of the KEV catalog that the tests pin: `catalogVersion` 2026.10.30, released 2026-10-30, with a count of 1,766 entries, fetched from `cisagov/kev-data` at commit `7ccba8e1223c` and validated in full by `just test-kev-data`. This concept lists no entries inline.
* [The entry for CVE-2021-44228](datasets/worked-entry-cve-2021-44228.md) - The KEV catalog's entry for CVE-2021-44228, Apache Log4j2, as a worked example of an entry with every key. It is copied from the pinned catalogue into `tests/data/valid/KevVulnerability-every-key.yaml` and the extract.
* [Generated artefacts](datasets/generated-artefacts.md) - What the LinkML generators write from the schema: `project/` (JSON Schema, OWL, SHACL, ShEx, JSON-LD and others), the Python models in `src/kev_catalog/datamodel/`, and the merged schema in `docs/schema/`. They are never edited by hand.
* [Example data](datasets/example-data.md) - The examples the tests hold the schema to, under `tests/data/`: valid examples, counter-examples that each name the JSON pointer they fail at, a folder for valid data the generated dataclasses refuse, and the pinned catalogue's manifest and twelve-entry extract.
* [Upstream copies](datasets/upstream-copies.md) - The exact copies of CISA's files under `tests/upstream/`: the JSON schema and the licence of the mirror, each held to its pin by `tests/test_upstream.py`. The test walks the JSON schema, and fails on any part with no element in the LinkML schema.
* [Neighbours' adapt copies](datasets/neighbour-copies.md) - The adapt copies of other lmodel repositories under `tests/neighbours/`, each pinned by its SHA-256 in `tests/test_schema_rules.py`. The test holds this repository's copy apart from them and from LOKF, so that a new shared name fails.

# References

* [CISA's KEV JSON schema](references/cisa-kev-json-schema.md) - CISA's JSON schema for the KEV catalog, draft-07, the file this project renders, at the edition of 2026-09-17. It states no version of its own. CISA serves it from `www.cisa.gov`, and `cisagov/kev-data` holds the same bytes.
* [cisagov/kev-data](references/cisagov-kev-data.md) - The official GitHub mirror of CISA's KEV data files, at `https://github.com/cisagov/kev-data`, default branch `develop`: the JSON and CSV catalogue, the JSON schema, and a CC0 licence. This project pins the schema and one dated catalogue from it.
* [Binding Operational Directive 26-04](references/bod-26-04.md) - Binding Operational Directive (BOD) 26-04, *Prioritizing Security Updates Based on Risk*, which kev-data's README and CISA's JSON schema now cite for the catalog. CISA's page answered a plain client with 403 on 2026-11-03, so this project cites it by address and restates none of its terms.

# Glossary

* [Known Exploited Vulnerabilities (KEV)](glossary/kev.md) - The Known Exploited Vulnerabilities (KEV) catalog: the list of CVEs that the Cybersecurity and Infrastructure Security Agency (CISA) publishes as a JSON and a CSV file, each entry naming the action it asks for and a due date.
* [Adapt copy](glossary/adapt-copy.md) - An adapt copy: the copy of a published LinkML schema that `lokf adapt` writes so that it can sit beside LOKF's `lokf.yaml` in a domain schema, with its classes re-rooted on `Concept` and every name LOKF also defines renamed with its IRI kept. Here it is `.lokf/schema/kev-catalog.yaml`.
* [Forensic triage (forensicTriage)](glossary/forensic-triage.md) - The KEV key `forensicTriage`: `Yes` when BOD 26-04 calls for forensic triage of a vulnerability and `No` when it does not. CISA types it as a string and names the two values in its description, and the schema makes them an enum.

# Explanations

* [Keys, edition and departures](explanations/keys-edition-and-departures.md) - Why the schema keeps CISA's keys and values, why its version is a date, and where it departs from CISA's JSON schema: the `title` key, two enums, closed classes and null on an optional key. It also says why nothing imports `lmodel/vulnerability-core`.
* [Mappings and how each kind was chosen](explanations/mappings.md) - What the schema maps to and why each mapping has its kind: DCAT, schema.org, Dublin Core, SKOS, Wikidata, SPDX 3.0.1, SEPSES, lmodel/stix and lmodel/cve, with the sample of 120 entries that decided the kinds toward CVE. The schema's mappings are the one home for mappings, and `tests/test_mappings.py` holds each.

# Playbooks

* [Regenerate and test after a schema change](playbooks/regenerate-and-test.md) - How to change the schema: edit `src/kev_catalog/schema/kev_catalog.yaml`, then run `just lint`, `just gen-project`, `just gen-doc`, `just lokf-adapt` and `just test`, and commit what they write.
* [Validate a KEV file](playbooks/validate-a-kev-file.md) - How to validate a real KEV file with `linkml-validate` against `KevCatalog`, what the validator checks, and the two rules only `tests/kev_rules.py` checks: the count and a repeated CVE.
* [Move the upstream pins](playbooks/move-the-upstream-pins.md) - What to do when the upstream watch reports a change: the pins for the JSON schema and the licence in `scripts/check_upstream_release.py`, the copies in `tests/upstream/`, the schema header, and separately the catalogue's pin in `tests/data/kev-data/manifest.json`.
* [Release a version](playbooks/release.md) - How a version is released: changelog entries under `## [Unreleased]`, a releasing commit type, the `v0.0.0` baseline tag before the first release, and `semantic-release.yml`, which tags and publishes on the merge and dispatches the knowledge release.
* [Knowledge sources map](playbooks/knowledge-sources.md) - The librarian's scrape map: every repository location and external source this bundle derives concepts from, the concepts each yields, how to re-check each on a refresh run, and the paths left out on purpose.

# Policies

* [Security policy](policies/security-policy.md) - How to report a vulnerability (GitHub's private vulnerability reporting), which release receives fixes (the latest), what executes in the repository and what holds each surface, what the upstream watch and the fetcher may reach, and the two repository settings not yet in force.
* [AI covenant](policies/ai-covenant.md) - The rules for AI-assisted work here: a person owns every contribution, an element says what the upstream says, no rule of a model's own goes in the schema, no dated fact sits in an element, and the scheduled librarian's changes need a person's review.
* [Licence and attribution](policies/license-and-attribution.md) - The terms here: Apache-2.0 for the schema and code, CC BY 4.0 for the bundle, and CC0 1.0 for CISA's copied files, with CISA's statement that use gives no right to the CISA Logo or the DHS Seal and is no endorsement. NOTICE holds the whole position.

# Workflows

* [Build and test (main.yaml)](workflows/main.md) - The Build and test workflow, `.github/workflows/main.yaml`: on a push to `main` and every pull request, its `test` job lints, tests and checks the adapt copy across Python 3.10 to 3.14, and its `kev-data` job validates the pinned catalogue in full.
* [Lint and docs (lint-and-docs.yaml)](workflows/lint-and-docs.md) - The Lint and docs workflow, `.github/workflows/lint-and-docs.yaml`: ShellCheck, actionlint, the word budgets of CONTRIBUTING.md and SECURITY.md, markdownlint, lychee and codespell, on a push to `main`, every pull request and Mondays at 06:00 UTC.
* [Upstream watch (upstream-watch.yaml)](workflows/upstream-watch.md) - The Upstream watch workflow, `.github/workflows/upstream-watch.yaml`: every Monday at 07:00 UTC and by hand, its `kev-sources` job runs `scripts/check_upstream_release.py` against the GitHub API and CISA's copy, and on a finding opens or updates the issue titled Upstream watch: the KEV JSON schema or licence has changed.
* [Semantic release (semantic-release.yml)](workflows/semantic-release.md) - The Semantic release workflow, `.github/workflows/semantic-release.yml`: `plan` previews a pull request's release, and `release`, on a push to `main` in the `release` Environment, promotes the changelog, tags, publishes and dispatches the knowledge release.
* [Knowledge website (knowledge-website.yaml)](workflows/knowledge-website.md) - The Knowledge website workflow, `.github/workflows/knowledge-website.yaml`: it builds the site on a change to its inputs and on Mondays at 05:23 UTC, and its `deploy` job publishes to GitHub Pages from `main` once `KNOWLEDGE_WEBSITE_ENABLED` is `true`.
* [Knowledge Librarian (knowledge-librarian.yaml)](workflows/knowledge-librarian.md) - The Knowledge Librarian workflow, `.github/workflows/knowledge-librarian.yaml`: every Monday at 05:00 UTC, once `KNOWLEDGE_LIBRARIAN_ENABLED` is `true`, it runs the ktl-librarian skill with no write token and opens a pull request a person reviews.
* [Knowledge Registrar (knowledge-registrar.yaml)](workflows/knowledge-registrar.md) - The Knowledge Registrar workflow, `.github/workflows/knowledge-registrar.yaml`: the gate of the sidecar. It validates the bundle and its conventions, and checks that each new `human:` confirmation is backed by an approval or a signed commit.
* [Knowledge Release (knowledge-release.yaml)](workflows/knowledge-release.md) - The Knowledge Release workflow, `.github/workflows/knowledge-release.yaml`: on a published release once `KNOWLEDGE_RELEASE_ENABLED` is `true`, or when dispatched, it attaches the schema copy, the bundle zip and the Copilot skill zip, each with its `.sha256` and an attestation.
* [Knowledge sync (knowledge-sync.yaml)](workflows/knowledge-sync.md) - The Knowledge sync workflow, `.github/workflows/knowledge-sync.yaml`: every Monday at 04:10 UTC it copies the sidecar files from KTL's newest release when the skills pin is behind, and opens one pull request.
