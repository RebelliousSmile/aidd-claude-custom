---
name: teach
description: >-
author: François-Xavier Guillois
version: 0.15.4
vibe_version: ">=1.0.0"
permissions:
  - bash
  - files
tags:
  - frontend
  - audit
  - javascript
---

Read [host portability](../../references/host-portability.md) before resolving plugin files, invoking sibling skills, or persisting project guidance.

# sc-js Teach

Contextual teaching for JS/TS/Vue/Nuxt. Finds examples of the requested concept in the current project, explains the theory with those examples as anchors, then offers a short practice exercise to consolidate understanding.

## Available actions

| # | Action | Role | Input |
|---|--------|------|-------|
| 01 | `explain` | Explain a concept or pattern using project code examples | topic or code excerpt |
| 02 | `practice` | Generate a targeted exercise based on project patterns | topic or previous explain |

## Default flow

Non-sequential — dispatch based on user intent:

- "explain / how does / what is / difference between / show me / I don't understand" → `explain`
- "practice / exercise / quiz / test me / challenge me" → `practice`
- Ambiguous → `explain`, then offer `practice` at the end

## Transversal rules

- Always search the project codebase for a real example of the concept before explaining.
- If no project example exists, explain with a minimal invented snippet in the project's style (framework, TypeScript conventions).
- Keep theory brief — real code carries more weight than prose.
- After `explain`, always offer: "Want a practice exercise on this?"
- After `practice`, provide the solution and link back to the project example.
- For async concepts: always show both the Promise and async/await version when relevant.
- For Vue concepts: show both Options API and Composition API when the project uses both.
