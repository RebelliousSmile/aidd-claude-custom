---
name: improve
description: >-
  Analyze PHP code for idiomatic patterns, framework improvements, and a targeted change plan.
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

# sc-php Improve

Reads the PHP codebase, identifies design pattern gaps and language-specific anti-patterns, then produces a prioritized improvement plan with concrete before/after examples.

## Available actions

| # | Action | Role | Input |
|---|--------|------|-------|
| 01 | `analyze` | Read codebase, identify anti-patterns and improvement opportunities | path or file list |
| 02 | `plan` | Produce a prioritized improvement plan with before/after examples | analyze findings |

## Default flow

Always sequential: `analyze` → `plan`.

1. `analyze` reads the codebase structure, identifies patterns and anti-patterns per category, emits findings
2. `plan` prioritizes findings, groups by effort/impact, writes a concrete improvement plan

Never skip `plan` after `analyze`.

## Transversal rules

- Analyze patterns only — do not apply changes (that is `aidd-dev:02-implement`'s role).
- Prioritize by impact: a fat controller trumps a style preference.
- For each finding: show the problematic code, name the anti-pattern, show the improved version.
- Do not flag patterns that are intentional framework conventions (e.g. Eloquent active record is intentional).
- Respect the detected framework: Laravel idioms ≠ Symfony idioms.
