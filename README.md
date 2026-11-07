<a href="https://github.com/linkml/linkml-project-copier"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-teal.json" alt="Copier Badge" style="max-width:100%;"/></a>

# kev-catalog

CISA Known Exploited Vulnerabilities (KEV) Catalog (LinkML)

> **Only want to ask?** Install `ktl-docent` into any agent you use, by a route from [the install page](https://w3id.org/ktl/docs/install/), and ask it about this project. It answers from the bundle and says how far each answer has been checked.
>
> **Agents:** if `.lokf/knowledge/index.md` exists, read it first. `llms.txt` says how to weigh it.

## Documentation Website

[https://lmodel.github.io/kev-catalog](https://lmodel.github.io/kev-catalog)

## What it models

The schema renders the JSON format of the [Known Exploited Vulnerabilities (KEV) catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) that the Cybersecurity and Infrastructure Security Agency (CISA) publishes: one release of the catalog and its entries.

It follows [CISA's JSON schema](https://github.com/cisagov/kev-data/blob/d98075f22b11ca60ede428f4397966d3523dc692/known_exploited_vulnerabilities_schema.json). That file states no version, so the edition is the date of the commit that last changed it in the official mirror, `2026-09-17`.

CISA's keys and values are the schema's, such as `cveID` and `Known`, so a real KEV file validates unchanged. `just test-kev-data` and a CI job validate the catalogue of 2026-10-30 in full, pinned by its git object hash. `tests/upstream/` copies the JSON schema, and `tests/test_upstream.py` fails on any part of it with no element here. A weekly workflow opens an issue when the JSON schema or its licence changes.

## Mappings

The schema's mappings are the one home for what it crosses to, and `tests/test_mappings.py` checks each: its kind, its bound prefix, and that a target in lmodel/cve, lmodel/stix or lmodel/spdx is in that neighbour's copy under `tests/neighbours/`. The earlier hand-kept SSSOM file is gone, since its rows named removed elements and no source confirmed them. The kinds rest on [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/), on schema.org and on a sample of 120 entries compared with their CVE records on 2026-11-03.

* `KevCatalog`: `dcat:Dataset` and `schema:Dataset` in `broad_mappings`, and `dcat:Catalog`, Wikidata `wd:Q125498394` (the KEV catalog itself) and SPDX 3.0.1's `spdx3:Security/ExploitCatalogType/kev` in `related_mappings`, since a class here is one release of that catalog.
* `KevVulnerability`: `spdx3:Security/ExploitCatalogVulnAssessmentRelationship` in `close_mappings`; Wikidata `wd:Q631425`, `stix:StixVulnerability`, `spdx3:Security/Vulnerability`, `sepses_cve:CVE`, `dcat:CatalogRecord` and `cve:CveRecord` in `related_mappings`, since an entry is a statement about a vulnerability.
* `cveID`: `cve:cveId` and Wikidata's `wdt:P3587` in `exact_mappings`.
* `vendorProject`, `product` and `cwes`: `cve:vendor`, `cve:product` and `cve:cweId` in `close_mappings`.
* `vulnerabilityName`, `shortDescription` and `requiredAction`: `cve:title`, `cve:descriptions` and `cve:solutions` in `related_mappings`.
* `cwes` also: Wikidata's `wdt:P3624` in `close_mappings`, since it holds the number without the `CWE-` prefix, and `sepses_cve:hasCWE` in `related_mappings`.
* `title` and `catalogVersion`: `dcterms:title` and `dcat:version` in `exact_mappings`, and `schema:version` in `close_mappings` for the second.
* `dateReleased` and `dateAdded`: `dcterms:issued` in `close_mappings`, and `schema:datePublished` too for the first.
* `count`: `schema:numberOfItems` in `related_mappings`.
* `vulnerabilities`: `dcterms:hasPart` in `broad_mappings`.
* `notes`: `skos:note` in `close_mappings`.

## Not modelled here

* Any rule CISA does not state, such as a `dueDate` not before its `dateAdded`.
* The contents of `notes`, which stays one string, since CISA states no form for it.
* The terms of the directives behind the catalog, and any contact address, milestone date or count from them.

## Repository Structure

* [docs/](docs/): the website's own pages
* [project/](project/): generated project files (do not edit them)
* [scripts/](scripts/): the upstream watch and the catalogue's fetcher
* [src/kev_catalog/schema/](src/kev_catalog/schema): the LinkML schema, `kev_catalog.yaml` (edit this)
* [src/kev_catalog/datamodel/](src/kev_catalog/datamodel): the generated Python datamodel
* [tests/](tests/): Python tests, with example data in [data/](tests/data), CISA's files in [upstream/](tests/upstream) and the neighbours' adapt copies in [neighbours/](tests/neighbours)
* [website/](website/): the Astro Starlight site built from the README, `docs/`, the schema's pages and the knowledge bundle

## Developer Tools

Run `just` to list the project's [just](https://github.com/casey/just/) recipes.

## Knowledge Trust Ladder (KTL)

`.lokf/` holds this project's [KTL](https://w3id.org/ktl/) knowledge bundle. Its domain schema, `.lokf/schema/kev-catalog.yaml`, is the copy `just lokf-adapt` writes from `src/kev_catalog/schema/kev_catalog.yaml`, and `just lokf-adapt-check` says when it is stale. Edit the source, never the copy. A release carries the copy as `schema-<tag>-kev-catalog.yaml`, on the terms [CONTRIBUTING.md](CONTRIBUTING.md#releasing-maintainers) gives.

The copy roots both classes on `Concept`, so a concept may name either as its `type`. In Obsidian, add them to the *Known LOKF types* setting of the KTL Registrar and KTL Curator plugins:

```text
KevCatalog, KevVulnerability
```

In the copy, LOKF's `id` replaces `cveID`, and `title` becomes `kev_title` with its IRI kept. The keys `count` and `product` are lmodel/stix's too, and `product` is lmodel/cve's, each under another IRI there. `tests/test_schema_rules.py` lists every shared name and fails on a new one.

## License

The schema and the code are under the Apache License 2.0 ([LICENSE](LICENSE)), and the knowledge bundle in [.lokf/knowledge/](.lokf/knowledge) is under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

CISA states the KEV data's terms as CC0 1.0, and `tests/upstream/` and the examples copy it on those terms: see [NOTICE](NOTICE). This is not a CISA or Department of Homeland Security project, and its use implies no endorsement by either.

## Contributing and security

[CONTRIBUTING.md](CONTRIBUTING.md) is the checklist for pull requests and
releases, [AI_COVENANT.md](AI_COVENANT.md) sets the rules for AI-assisted work,
[SECURITY.md](SECURITY.md) says how to report a vulnerability, and
[CHANGELOG.md](CHANGELOG.md) records the changes.

## Credits

Built from the [linkml-project-copier](https://github.com/linkml/linkml-project-copier) template ([doi:10.5281/zenodo.15163584](https://doi.org/10.5281/zenodo.15163584)).
