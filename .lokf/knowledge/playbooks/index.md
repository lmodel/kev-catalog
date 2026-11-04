# Playbooks

* [Regenerate and test after a schema change](regenerate-and-test.md) - How to change the schema: edit `src/kev_catalog/schema/kev_catalog.yaml`, then run `just lint`, `just gen-project`, `just gen-doc`, `just lokf-adapt` and `just test`, and commit what they write.
* [Validate a KEV file](validate-a-kev-file.md) - How to validate a real KEV file with `linkml-validate` against `KevCatalog`, what the validator checks, and the two rules only `tests/kev_rules.py` checks: the count and a repeated CVE.
* [Move the upstream pins](move-the-upstream-pins.md) - What to do when the upstream watch reports a change: the pins for the JSON schema and the licence in `scripts/check_upstream_release.py`, the copies in `tests/upstream/`, the schema header, and separately the catalogue's pin in `tests/data/kev-data/manifest.json`.
* [Release a version](release.md) - How a version is released: changelog entries under `## [Unreleased]`, a releasing commit type, the `v0.0.0` baseline tag before the first release, and `semantic-release.yml`, which tags and publishes on the merge and dispatches the knowledge release.
* [Knowledge sources map](knowledge-sources.md) - The librarian's scrape map: every repository location and external source this bundle derives concepts from, the concepts each yields, how to re-check each on a refresh run, and the paths left out on purpose.
