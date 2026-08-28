---
name: decompose
description: >-
  Apply the Mikado method to decompose a goal into a dependency graph through iterative questions, then generate YAML nodes under mikado/GRAPH_NAME/. Use to decompose a complex goal into safe incremental steps or create a Mikado graph. Do NOT use to implement code, write tests, or manage aidd_docs tasks.
author: François-Xavier Guillois
version: 4.7.0
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
