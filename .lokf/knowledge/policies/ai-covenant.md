---
type: Policy
id: https://w3id.org/lmodel/kev-catalog/knowledge/policies/ai-covenant
title: AI covenant
description: "The rules for AI-assisted work here: a person owns every contribution, an element says what the upstream says, no rule of a model's own goes in the schema, no dated fact sits in an element, and the scheduled librarian's changes need a person's review."
genre: reference
resource: AI_COVENANT.md
about:
  - https://w3id.org/lmodel/kev-catalog/knowledge/workflows/knowledge-librarian
sources:
  - id: ai_covenant.md
    resource: AI_COVENANT.md
    title: the note specific to this project and Repository-Owned Agent Automation
generated:
  by: process:ktl-librarian
  at: "2026-11-03T22:15:22Z"
status: draft
---

# AI covenant

`AI_COVENANT.md` says that whoever submits a contribution owns it, whatever tools helped. For this repository, it adds four rules:[^ai_covenant.md]

- An element says what the upstream says, and `tests/test_upstream.py` walks the copy of CISA's JSON schema.
- A bound or a requirement CISA does not state does not go in the schema.
- A contact address, a milestone date, a count or a directive's terms belongs at its source, cited by address and date.
- Descriptions are written here, though CISA's files are under CC0, and nothing may suggest an endorsement or use the CISA Logo or the DHS Seal.

The scheduled librarian commits under a labelled bot identity, opens a pull request, and needs a person's approval. No model's text is a person's verdict. AI co-authorship in commit messages is discouraged.[^ai_covenant.md]

[^ai_covenant.md]: AI_COVENANT.md, the note specific to this project and Repository-Owned Agent Automation
