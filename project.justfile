## Add your own just recipes here. This is imported by the main justfile.

# Overriding recipes from the root justfile by adding a recipe with the same
# name in this file is not possible until a known issue in just is fixed,
# https://github.com/casey/just/issues/2540

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
