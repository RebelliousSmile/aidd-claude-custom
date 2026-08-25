---
name: decompose
description: >-
author: François-Xavier Guillois
version: 4.6.0
vibe_version: ">=1.0.0"
permissions:
  - bash
tags:
  - productivity
  - workflow
  - automation
---

Read [host portability](../../references/host-portability.md) before resolving plugin files, invoking sibling skills, or persisting project guidance.

# Decompose

Decompose applies the Mikado method to a user-supplied goal: it walks through a depth-first iterative Q&A to surface all prerequisites, displays a Mermaid subtree after each iteration, and finally generates a YAML dependency graph under `mikado/<graphName>/`. Each leaf node is scoped to a single work session.

## Available actions

| #  | Action   | Role                                                                | Input                    |
|----|----------|---------------------------------------------------------------------|--------------------------|
| 01 | `mikado` | Full Mikado decomposition: name graph → DFS loop → generate YAML   | Goal string (`$ARGUMENTS`) |

## Default flow

Single action. Dispatch to `mikado` on any trigger.

## Transversal rules

- Node IDs must be in kebab-case.
- Each leaf node must be achievable in a single work session.
- Traverse the graph in DFS order.
- Display a Mermaid subtree after each iteration.
- Never write YAML files until the user validates the final complete graph.

## External data

- `docs/wiki/Storage-Format.md` — YAML node schema reference
- `mcp-server/src/resources/guide.md` — Mikado method guide
