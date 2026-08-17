---
name: teach
description: >-
author: François-Xavier Guillois
version: 0.5.2
vibe_version: ">=1.0.0"
permissions:
  - bash
  - files
tags:
  - backend
  - audit
  - rust
---

Read [host portability](../../references/host-portability.md) before resolving plugin files, invoking sibling skills, or persisting project guidance.

# sc-rust Teach

Contextual teaching for Rust. Finds examples of the requested concept in the current project, explains the theory with those examples as anchors, then offers a short practice exercise to consolidate understanding.

## Available actions

| # | Action | Role | Input |
|---|--------|------|-------|
| 01 | `explain` | Explain a concept or pattern using project code examples | topic or code excerpt |
| 02 | `practice` | Generate a targeted exercise based on project patterns | topic or previous explain |

## Default flow

Non-sequential — dispatch based on user intent:

- "explain / how does / what is / difference between / show me / why does the compiler" → `explain`
- "practice / exercise / quiz / test me / challenge me" → `practice`
- Ambiguous → `explain`, then offer `practice` at the end

## Transversal rules

- Always search the project codebase for a real example of the concept before explaining.
- If no project example exists, explain with a minimal invented snippet in the project's style (crate versions, error handling style).
- Keep theory brief — real code carries more weight than prose.
- For ownership/borrow checker explanations: always show the rejected code + compiler error, then the corrected version.
- After `explain`, always offer: "Want a practice exercise on this?"
- After `practice`, provide the solution and link back to the project example.
- For async concepts: always clarify which executor (Tokio vs async-std) is relevant to the project.
