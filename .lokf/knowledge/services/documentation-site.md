---
type: Service
id: https://w3id.org/lmodel/kev-catalog/knowledge/services/documentation-site
title: Documentation site
description: "The knowledge website in `website/`, an Astro Starlight site that the Knowledge website workflow publishes to GitHub Pages at `https://lmodel.github.io/kev-catalog/`: the README as its home page, `docs/`, the schema's pages, a page per concept and the four `lokf export` files, with redirects from the retired mkdocs site's addresses."
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
  - id: site.config.mjs
    resource: website/site.config.mjs
    title: REPO, SITE, BASE, DOCS and REDIRECTS
  - resource: website
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# Documentation site

`website/` builds the site that the Knowledge website workflow publishes to GitHub Pages at `https://lmodel.github.io/kev-catalog/`. The site shows:[^website-readme.md]

- the README as its home page;
- each page under `docs/` as a page under `docs/`;
- each schema page that `gen-doc` writes as a page under `schema/`;
- each concept as a page under `knowledge/`, beside the four files `lokf export` writes.

`website/site.config.mjs` redirects the retired mkdocs site's addresses: `/about`, `/elements`, and each old element page to its successor or to the schema's index.[^site.config.mjs]

`cd website && npm ci --ignore-scripts && npm run build` builds it and checks every link.[^website-readme.md]

[^website-readme.md]: website/README.md, the whole file
[^site.config.mjs]: website/site.config.mjs, REPO, SITE, BASE, DOCS and REDIRECTS
