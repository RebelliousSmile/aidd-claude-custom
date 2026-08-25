---
name: status
description: >-
author: François-Xavier Guillois
version: 4.6.1
vibe_version: ">=1.0.0"
permissions:
  - bash
tags:
  - productivity
  - workflow
  - automation
---

Read [host portability](../../references/host-portability.md) before resolving plugin files, invoking sibling skills, or persisting project guidance.

# Status

Three independent actions covering project memory synthesis, full status reporting, and memory quality auditing. Actions are non-sequential and dispatched by intent.

## Available actions

| #  | Action   | Role                                              | Input                        |
|----|----------|---------------------------------------------------|------------------------------|
| 01 | `memory` | Synthesize project memory and export decisions    | None required (optional scope) |
| 02 | `report` | Full project status with audit, security, 7-day plan | None required             |
| 03 | `audit`  | Audit memory files for quality, freshness, contradictions | Optional scope path   |

## Default flow

Dispatch based on user intent:

- "project memory / memory export / synthesize memory" → `memory`
- "project status / status report / project health" → `report`
- "audit memory / memory quality / check memory files" → `audit`

## Transversal rules

- Every finding must come from actual file or command output — never assume.
- Never modify files during `report` or `audit` P2/P3 — only `memory` writes its export and `audit` applies P1 auto-fixes.
- Cite `file:line` for every finding in `audit`.
- Quick wins in `report` are strictly tasks under 15 minutes.

## Assets

- `assets/project_memory.md` — Output template for the memory action
- `assets/project_status.md` — Output template for the report action
- `assets/audit_memory.md` — Output template for the audit action
