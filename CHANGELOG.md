# Changelog

All notable changes to this project are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The `v0.0.0` tag is a baseline, not a release: it marks where versioning starts so the first real release is `0.1.0` rather than `1.0.0`. The schema stays below 1.0.0 until its shape settles, so a breaking change bumps the minor version. See [CONTRIBUTING.md](CONTRIBUTING.md#releasing-maintainers).

## [Unreleased]

### Added

- **A LinkML model of the JSON format of the Known Exploited Vulnerabilities (KEV) catalog, at the edition of CISA's JSON schema of 2026-09-17.** Its classes are `KevCatalog` and `KevVulnerability`, and CISA's keys and values are the schema's, so a real KEV file validates unchanged.
- **Tests that walk an exact copy of CISA's JSON schema**: each definition, property, required key, cardinality, type, format and pattern must have its element, each departure is listed with its reason, and a keyword the walk does not read fails.
- **The full catalogue of 2026-10-30, all 1,766 entries, validated unchanged** by `just test-kev-data` and a CI job that fetches it from `raw.githubusercontent.com`, pinned by its git object hash, and twelve real entries in a committed extract.
- **Mappings to DCAT, schema.org, Dublin Core, SKOS, Wikidata, SPDX 3.0.1, SEPSES, lmodel/stix and lmodel/cve**, each read at its source and held by a test.
- **A weekly upstream watch** that reports a changed JSON schema, a changed licence, a different copy at CISA, or a check that could not finish.
- **`.lokf/kev_catalog.yaml`, the schema's `lokf adapt` copy, rooted on `KevCatalog` and `KevVulnerability`.** The knowledge release attaches it as `schema-<tag>-kev_catalog.yaml`, and tests hold its names apart from those of the Linked Open Knowledge Format (LOKF) and of the released lmodel copies.
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
