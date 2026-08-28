---
name: audit
description: >-
  Audit a detected PHP stack by delegating review with the applicable framework and capability pivots.
author: François-Xavier Guillois
version: 0.12.0
vibe_version: ">=1.0.0"
permissions:
  - bash
  - files
tags:
  - backend
  - php
  - audit
---

Read [host portability](../../references/host-portability.md) before resolving plugin files, invoking sibling skills, or persisting project guidance.

# sc-php Audit

PHP code quality audit — detects applicable pivots via sniff and delegates to `aidd-dev:reviewer`.

## Available actions

| # | Action | Role | Input |
|---|--------|------|-------|
| 01 | `audit` | Detect stack → load pivots → spawn aidd-dev:reviewer | project path |

## Default flow

Single action: `audit`.

## Conceptual model

- audit is a read-only orchestrator: it detects, loads, and delegates — it never writes to `.claude/rules/`
- The PHP knowledge lives in the plugin (`skills/sniff/references/capabilities/`) — loaded at runtime, not pre-installed
- `aidd-dev:reviewer` is the analysis engine — audit provides the acceptance criteria (pivots), reviewer provides the findings

## Transversal rules

- Never invoke `02-install-pivots` — audit is read-only.
- Never install any file to `.claude/rules/` or any project directory.
- Always invoke `01-scan` first to get the pivot manifeste before loading references.

## Actions

```markdown
@actions/01-audit.md
```
