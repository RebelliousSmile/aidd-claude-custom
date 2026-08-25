---
name: foresee
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

# Foresee

Keeps the stable `foresee` entry point. Documents and code delegate to the current AIDD authority; dependency analysis adds only prospective maintenance and migration-horizon signals after the AIDD dependency audit.

## Available actions

| #  | Action          | Role                                                           | Input                                        |
|----|-----------------|----------------------------------------------------------------|----------------------------------------------|
| 01 | `analyze-doc`   | Route prospective or completed documents to the matching AIDD refine skill | Path to document, or issue number |
| 02 | `analyze-code`  | Route a code target to one explicit AIDD audit pillar | File path or directory path |
| 03 | `analyze-dep`   | Audit dependencies with AIDD, then add abandonment and lock-in horizon signals | Package name or dependency manifest |

## Default flow

Dispatch on target type:
- `.md` / `.markdown` path, issue number (`#N`), or document-related trigger → `analyze-doc`
- Code file extension (`.ts`, `.js`, `.vue`, `.php`, `.rs`, `.py`, etc.) or directory path → `analyze-code`
- Package name or dependency manifest trigger → `analyze-dep`

## Delegation and flags

Read [the AIDD delegation contract](../../references/aidd-delegation.md). `--discuss`, `--plan`, default output, dependency failures, host invocation, and delegation receipts follow that shared contract.

## Transversal rules

- Delegated reports remain authoritative and are not rescored locally.
- Never fall back to the removed local document/code analysis when AIDD is absent or incompatible.
- Only `analyze-dep` may add a local horizon report, under its bounded contract.
