---
name: legacy
description: >-
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

# sc-php Legacy

Detects version-specific and deprecated patterns in the PHP codebase, then produces a migration plan and applies changes file by file — either upgrading to modern PHP or downgrading to a target version for compatibility.

## Available actions

| # | Action | Role | Input |
|---|--------|------|-------|
| 01 | `scan` | Detect legacy patterns and version gaps | path, target PHP version |
| 02 | `migrate` | Apply upgrade or downgrade transformations | scan manifest, direction |

## Default flow

Always sequential: `scan` → `migrate`.

1. `scan` reads `composer.json`, detects current and target PHP versions, finds deprecated/missing patterns, emits a structured manifest
2. `migrate` reads the manifest and applies transformations file by file

## Transversal rules

- Always detect the current PHP version from `composer.json` or Dockerfile before scanning.
- Never remove a working pattern without providing its replacement inline.
- For breaking changes: show a diff of what will change and ask for confirmation before writing.
- Downgrade migrations: never remove a feature without confirming the target version actually lacks it.
- Framework-specific patterns (Laravel, Symfony): check composer.json for framework version before applying framework-level migrations.
- Never touch files under `vendor/`.
