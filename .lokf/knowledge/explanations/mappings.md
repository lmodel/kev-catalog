---
type: Explanation
id: https://w3id.org/lmodel/kev-catalog/knowledge/explanations/mappings
title: Mappings and how each kind was chosen
description: "What the schema maps to and why each mapping has its kind: DCAT, schema.org, Dublin Core, SKOS, Wikidata, SPDX 3.0.1, SEPSES, lmodel/stix and lmodel/cve, with the sample of 120 entries that decided the kinds toward CVE. The schema's mappings are the one home for mappings, and `tests/test_mappings.py` holds each."
genre: explanation
about:
  - https://w3id.org/lmodel/kev-catalog/knowledge/datasets/kev-catalog-linkml-schema
references:
  - https://w3id.org/lmodel/kev-catalog/knowledge/datasets/neighbour-copies
sources:
  - id: test_mappings.py
    resource: tests/test_mappings.py
    title: the table and the checks
  - id: kev_catalog.yaml
    resource: src/kev_catalog/schema/kev_catalog.yaml
    title: the mappings and their notes
  - resource: https://www.w3.org/TR/vocab-dcat-3/
    title: DCAT 3, the definitions of the classes and properties
  - resource: https://spdx.github.io/spdx-spec/v3.0.1/model/Security/Classes/ExploitCatalogVulnAssessmentRelationship/
    title: SPDX 3.0.1's class
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# Mappings and how each kind was chosen

The schema's mappings are the one home for mappings. The earlier hand-kept SSSOM file is gone, since its rows named removed elements and no source confirmed them. `tests/test_mappings.py` checks each mapping's kind and bound prefix, and that a target in a neighbour's namespace is in that neighbour's copy.[^test_mappings.py]

**The catalogue.** DCAT 3 defines a catalog as a curated collection of metadata about resources, and an entry here describes a vulnerability, so `dcat:Catalog` is only related. A KEV release is a kind of dataset, so `dcat:Dataset` and `schema:Dataset` are broad.[^kev_catalog.yaml]

**The entry.** An entry is a statement in a catalog about a vulnerability, not the vulnerability. So Wikidata's `Q631425`, `stix:StixVulnerability`, SPDX 3.0.1's `Security/Vulnerability` and SEPSES's `CVE` are only related. SPDX 3.0.1's `Security/ExploitCatalogVulnAssessmentRelationship` says a vulnerability is listed in an exploit catalog, and names KEV as one, so it is close.[^kev_catalog.yaml]

**Down to CVE.** A seeded sample of 120 entries, compared with their CVE records on 2026-11-03, decided these kinds:[^kev_catalog.yaml]

- `cveID` matched `cveMetadata.cveId` on all 120, so `cve:cveId` is exact.
- `vendorProject` matched the affected vendor that a CVE Numbering Authority (CNA) wrote on 54, and `product` matched an affected product on 14, so `cve:vendor` and `cve:product` are close.
- `cwes` equalled the codes of the CNA and ADP containers together on 94, so `cve:cweId` is close.
- `vulnerabilityName` equalled a CNA title on 2 of the 39 records that had one, and `shortDescription` equalled no CNA description, so `cve:title` and `cve:descriptions` are related.
- `dateAdded` equalled the date in CISA's ADP container on all 120, but that metric's content is free-form, so no slot mapping reaches it.

Mappings across the lmodel family point from this schema to `cve`, and this schema imports neither.

[^test_mappings.py]: tests/test_mappings.py, the table and the checks
[^kev_catalog.yaml]: src/kev_catalog/schema/kev_catalog.yaml, the mappings and their notes
