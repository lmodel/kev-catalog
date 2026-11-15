---
type: Service
id: https://w3id.org/lmodel/kev-catalog/knowledge/services/documentation-site
title: Documentation site
description: "The knowledge website in `website/`, a Hugo site that the Knowledge website workflow publishes to GitHub Pages at `https://lmodel.github.io/kev-catalog/`: the README as its home page, `docs/`, the schema's pages, a page per concept and the four `lokf export` files, with redirects from the retired mkdocs site's addresses."
genre: reference
resource: website
dependsOn:
  - https://w3id.org/lmodel/kev-catalog/knowledge/workflows/knowledge-website
derivedFrom:
  - https://w3id.org/lmodel/kev-catalog/knowledge/datasets/kev-catalog-linkml-schema
sources:
  - id: website-readme.md
    resource: website/README.md
    title: the whole file
  - id: site.toml
    resource: website/site.toml
    title: the site's address, title and redirects
  - resource: website
generated:
  by: process:ktl-librarian
  at: "2026-11-15T03:05:15Z"
status: draft
---

# Documentation site

`website/` builds the site that the Knowledge website workflow publishes to GitHub Pages at `https://lmodel.github.io/kev-catalog/`. The site shows:[^website-readme.md]

- the README as its home page;
- each page under `docs/` as a page under `docs/`;
- each schema page that `gen-doc` writes as a page under `schema/`;
- each concept as a page under `knowledge/`, beside the four files `lokf export` writes.

`website/site.toml` redirects the retired mkdocs site's addresses: `/about`, and each old element page under `/elements/` to its successor or to the schema's index.[^site.toml]

`scripts/build.sh`, run from `website/`, writes the site to `dist/` with its search index, then checks every link between its pages. It needs bash, git and uv, and takes Hugo and Pagefind from PyPI.[^website-readme.md]

[^website-readme.md]: website/README.md, the whole file
[^site.toml]: website/site.toml, the site's address, title and redirects
