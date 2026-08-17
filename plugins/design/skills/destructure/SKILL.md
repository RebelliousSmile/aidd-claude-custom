---
name: destructure
description: Critiques a draft, component, page, or existing design system through visual, accessibility, interaction, and hierarchy lenses. Use when the user wants actionable alternatives without changing the contract or source.
author: François-Xavier Guillois
version: 2.13.0
vibe_version: ">=1.0.0"
permissions:
  - files
tags:
  - design-system
  - ui
  - contract
  - challenge
  - critique
---

# Destructure

```mermaid
flowchart LR
  target([draft, component, page, or system]) --> challenge --> report([critique report])
```

Read the action when this capability is selected.

| Action | Does |
| --- | --- |
| challenge | challenge a visual direction and propose alternatives |

## Routing

- "critique or challenge this design target" → `challenge`

## Transversal rules

- Resolve the plugin root using [host-portability.md](../../references/host-portability.md) before loading bundled tools or references.
- Work standalone on the target supplied by the user; a draft from another capability is optional.
- Never change the frozen contract or source code.
- Persist only the critique report unless the user requests conversation-only output.
- Produce concrete alternatives across distinction, consistency, accessibility, interaction states, responsive behavior, and reading hierarchy.
