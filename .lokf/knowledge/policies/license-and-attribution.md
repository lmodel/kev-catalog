---
type: Policy
id: https://w3id.org/lmodel/kev-catalog/knowledge/policies/license-and-attribution
title: Licence and attribution
description: "The terms here: Apache-2.0 for the schema and code, CC BY 4.0 for the bundle, and CC0 1.0 for CISA's copied files, with CISA's statement that use gives no right to the CISA Logo or the DHS Seal and is no endorsement. NOTICE holds the whole position."
genre: reference
resource: NOTICE
about:
  - https://w3id.org/lmodel/kev-catalog/knowledge/datasets/upstream-copies
sources:
  - id: readme.md
    resource: README.md
    title: the License section
  - id: license
    resource: tests/upstream/LICENSE
    title: the first paragraph
  - id: notice
    resource: NOTICE
    title: every section
  - resource: LICENSE
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# Licence and attribution

The schema and the code are under the Apache License 2.0, and the bundle is under CC BY 4.0.[^readme.md]

CISA distributes the KEV data under CC0 1.0. The mirror's LICENSE file opens with CISA's statement. Third-party links in the data keep their own terms. Use of the information does not authorize use of the CISA Logo or the DHS Seal, and it is no endorsement by CISA or DHS.[^license] NOTICE states this position, names the copies this repository holds, and says this project is not CISA's or DHS's.[^notice]

NOTICE also carries the MIT notice of linkml-project-copier, and says the sidecar's scripts and workflows and the website derive from Knowledge Trust Ladder templates under Apache-2.0.[^notice]

[^readme.md]: README.md, the License section
[^license]: tests/upstream/LICENSE, the first paragraph
[^notice]: NOTICE, every section
