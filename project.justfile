## Add your own just recipes here. This is imported by the main justfile.

# Overriding recipes from the root justfile by adding a recipe with the same
# name in this file is not possible until a known issue in just is fixed,
# https://github.com/casey/just/issues/2540

# ============ Knowledge bundle: the adapted domain schema ============

# `.lokf/kev-catalog.yaml` is the copy `lokf adapt` writes from the schema so that
# it can sit beside `.lokf/lokf.yaml` (`lokf adapt --help` lists the moves). The
# roots are the schema's two classes, so a concept may name either as its `type`:
# a release of the catalog, or one entry. adapt replaces the identifier `cveID`
# with LOKF's own `id`, and refuses a class that lists an identifier without
# descending from a root, so KevVulnerability must be one. KevCatalog has no
# identifier, and it is a root so that a concept can stand for a release. The
# prefix names what the copy renames to keep apart from LOKF, which today is
# `title`, as kev_title with its IRI kept. The recipes run the `lokf` the
# sidecar's floor pins (0.9.0 or later); LOKF_CMD runs another, such as a checkout:
# LOKF_CMD="uv run --project ../lokf lokf" just lokf-adapt
lokf_cmd := env_var_or_default("LOKF_CMD", "uv run --project .lokf lokf")
lokf_adapt_roots := "--root KevCatalog --root KevVulnerability --prefix kev"

# Rewrite .lokf/kev-catalog.yaml from the schema (run after every schema change)
[group('knowledge bundle')]
lokf-adapt:
  {{lokf_cmd}} adapt {{source_schema_path}} {{lokf_adapt_roots}} --lokf .lokf/lokf.yaml -o .lokf/kev-catalog.yaml

# Fail when .lokf/kev-catalog.yaml is stale against the schema or .lokf/lokf.yaml
[group('knowledge bundle')]
lokf-adapt-check:
  {{lokf_cmd}} adapt {{source_schema_path}} {{lokf_adapt_roots}} --lokf .lokf/lokf.yaml -o .lokf/kev-catalog.yaml --check

# ============ The pinned KEV catalogue ============

# Download the pinned catalogue into tmp/kev-data/, checking it against the size
# and hashes in tests/data/kev-data/manifest.json
[group('model development')]
fetch-kev-data:
  uv run scripts/fetch_kev_data.py

# Validate the pinned catalogue in full, unchanged, after fetching it if
# tmp/kev-data/ lacks it
[group('model development')]
test-kev-data: fetch-kev-data
  KEV_DATA=1 uv run python -m pytest tests/test_kev_data.py
