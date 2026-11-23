# Changelog

All notable changes to this project are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The `v0.0.0` tag is a baseline, not a release: it marks where versioning starts so the first real release is `0.1.0` rather than `1.0.0`. The schema stays below 1.0.0 until its shape settles, so a breaking change bumps the minor version. See [CONTRIBUTING.md](CONTRIBUTING.md#releasing-maintainers).

## [Unreleased]

### Security

- **The sidecar copies and the skills pin are at Knowledge Trust Ladder [v0.70.4](https://github.com/noelmcloughlin/knowledge-trust-ladder/compare/v0.66.0...v0.70.4).** The release changed `.github/workflows/knowledge-registrar.yaml`, `.github/workflows/knowledge-librarian.yaml`, `.github/workflows/knowledge-release.yaml`, `.github/workflows/knowledge-sync.yaml`, `.github/PULL_REQUEST_TEMPLATE/knowledge-sync.md`, `.lokf/scripts/knowledge-conventions.sh`, `.lokf/scripts/knowledge-conventions.py`, `.lokf/scripts/knowledge-preflight.sh`, `.lokf/scripts/knowledge-provenance.sh`, `.lokf/scripts/knowledge-feedback.sh`, `.lokf/scripts/knowledge-apply.py`, `.lokf/scripts/knowledge-report.sh`, `.lokf/scripts/knowledge-sync.sh`, `.lokf/m365/ktl-docent-m365.md`, `.lokf/justfile`, `website/assets/css/site.css`, `website/assets/js/graph.js`, `website/assets/js/site.js`, `website/content/_content.gotmpl`, `website/content/knowledge/_content.gotmpl`, `website/.gitignore`, `website/hugo.toml`, `website/layouts/_markup/render-blockquote.html`, `website/layouts/_markup/render-codeblock-mermaid.html`, `website/layouts/_markup/render-heading.html`, `website/layouts/_markup/render-link.html`, `website/layouts/_partials/gendoc.html`, `website/layouts/_partials/heroes.html`, `website/layouts/_partials/icon.html`, `website/layouts/_partials/markdown-file.html`, `website/layouts/_partials/nav-key.html`, `website/layouts/_partials/route.html`, `website/layouts/_partials/schema-file.html`, `website/layouts/_partials/sidebar.html`, `website/layouts/_partials/tools.html`, `website/layouts/_partials/vendor.html`, `website/layouts/baseof.html`, `website/layouts/health.html`, `website/layouts/home.badge.json`, `website/layouts/home.llms.txt`, `website/layouts/page.atom.xml`, `website/layouts/page.html`, `website/layouts/schema/section.html`, `website/pyproject.toml`, `website/scripts/build.sh`, `website/scripts/clean-html.py`, `website/scripts/prepare.sh`, `website/uv.lock`, `.github/workflows/knowledge-website.yaml`, `website/layouts/_partials/own.html`, `website/layouts/_partials/spec.html`, `website/scripts/check-svg.py`, `website/scripts/lokf-export.py`, `website/scripts/site-values.py`, `website/scripts/uv-env.sh` and `website/scripts/vendor.sh` here.

## [0.2.3] - 2026-11-16

### Fixed

- **Each GitHub release carries its changelog section as its body**: semantic-release asks for the notes again after the changelog commit, and `changelog-release.mjs notes` now answers with the promoted section instead of the empty Unreleased one.

## [0.2.2] - 2026-11-15

### Changed

- **The release tools are in `.release/`**, outside `.github/`, where Dependabot's pull requests for them were refused.

## [0.2.1] - 2026-11-15

### Added

- **`scorecard.yml` publishes this repository's OpenSSF Scorecard.**
- **The README shows the CI, licence, OpenSSF Scorecard and KTL scorecard badges.**
- **`codeql.yml` scans the Python, the JavaScript and the workflows with CodeQL.**

### Changed

- **The knowledge website is built with Hugo from the ktl-website templates**, set by `website/site.toml`, in place of the Astro site.
- **The project requires Python 3.11 or later**, since Python 3.10's support ended in October 2026.

### Security

- **The sidecar copies are at Knowledge Trust Ladder [v0.66.0](https://github.com/noelmcloughlin/knowledge-trust-ladder/blob/v0.66.0/CHANGELOG.md), and `.lokf/pyproject.toml` pins `ktl==0.66.0`**, which the librarian installs its skill from.

## [0.2.0] - 2026-11-07

### Added

- **The schema as RDF Turtle and the merged schema**, in `project/rdf/` and `project/linkml/`, from `just gen-rdf` and `just gen-merged-schema`.

## [0.1.1] - 2026-11-07

### Changed

- **The bundle's schema files sit in `.lokf/schema/`**: `lokf.yaml` and the `lokf adapt` copy `kev-catalog.yaml`, as KTL v0.62.0 lays them out.

### Fixed

- **The knowledge librarian workflow can install its skill.** The root `.gitignore` now ignores `.agents/`, `.claude/` and `skills-lock.json`, where the workflow installs the ktl-librarian skill. While git did not ignore them, the workflow stopped before the agent ran.

## [0.1.0] - 2026-11-04

### Added

- **A LinkML model of the JSON format of the Known Exploited Vulnerabilities (KEV) catalog, at the edition of CISA's JSON schema of 2026-09-17.** Its classes are `KevCatalog` and `KevVulnerability`, and CISA's keys and values are the schema's, so a real KEV file validates unchanged.
- **Tests that walk an exact copy of CISA's JSON schema**: each definition, property, required key, cardinality, type, format and pattern must have its element, each departure is listed with its reason, and a keyword the walk does not read fails.
- **The full catalogue of 2026-10-30, all 1,766 entries, validated unchanged** by `just test-kev-data` and a CI job that fetches it from `raw.githubusercontent.com`, pinned by its git object hash, and twelve real entries in a committed extract.
- **Mappings to DCAT, schema.org, Dublin Core, SKOS, Wikidata, SPDX 3.0.1, SEPSES, lmodel/stix and lmodel/cve**, each read at its source and held by a test.
- **A weekly upstream watch** that reports a changed JSON schema, a changed licence, a different copy at CISA, or a check that could not finish.
- **`.lokf/kev-catalog.yaml`, the schema's `lokf adapt` copy, rooted on `KevCatalog` and `KevVulnerability`.** The knowledge release attaches it as `schema-<tag>-kev-catalog.yaml`, and tests hold its names apart from those of the Linked Open Knowledge Format (LOKF) and of the released lmodel copies.
- **An example of each class and a counter-example for each constraint**, each counter-example held to the one place it fails.
- **The repository's Knowledge Trust Ladder (KTL) knowledge bundle and its sidecar automation**, from the KTL v0.61.0 templates with the lokf floor at 0.9.0, and a knowledge website that replaces the mkdocs site.
- **The governance files**: SECURITY.md, AI_COVENANT.md, NOTICE, a CONTRIBUTING checklist, and semantic-release from a v0.0.0 baseline.

### Changed

- **The keys and values are CISA's.** `cve_id`, `vendor_project`, `date_added` and the rest become `cveID`, `vendorProject`, `dateAdded` and so on, and `known` and `unknown` become `Known` and `Unknown`. `KevEntry` becomes `KevVulnerability`.
- **`forensicTriage` and `cwes` are added**, as CISA's format has them, and `knownRansomwareCampaignUse`, `forensicTriage`, `notes` and `cwes` stay optional, as CISA's JSON schema says.
- **`version` is the edition's date, `2026-09-17`.** CISA's JSON schema states no version, and the old `1.0` was never CISA's.
- **The project moves to linkml-project-copier v0.5.0**, with linkml and linkml-runtime locked at 1.12.1, and its Python project is named `kev-catalog-linkml`. PyPI publishing is off.

### Removed

- **The import of `lmodel/vulnerability-core`**, with the ten inherited fields KEV's format does not have, so that a real file validates. The schema now imports only `linkml:types`.
- **The notes on Binding Operational Directive 22-01 and 19-02**, the counts from 2022, the milestone dates and the contact addresses. Directive terms belong at their source, and CISA's data now cites Binding Operational Directive 26-04.
- **`src/kev_catalog/mappings/cve_to_kev_catalog.sssom.tsv`**, whose rows named elements that are gone and were never checked. The schema's mappings are the one home for mappings, each held by a test.
- **`BUG.txt`, the patched generator scripts, the PyPI publishing workflow and the mkdocs site.** The knowledge website replaces the site.
