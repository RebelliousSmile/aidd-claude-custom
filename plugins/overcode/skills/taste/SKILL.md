---
name: taste
description: >-
author: François-Xavier Guillois
version: 4.5.1
vibe_version: ">=1.0.0"
permissions:
  - bash
tags:
  - productivity
  - workflow
  - automation
---

Read [host portability](../../references/host-portability.md) before resolving plugin files, invoking sibling skills, or persisting project guidance.

# Taste

Keeps repository-backed document freshness native. Code targets delegate to the current AIDD audit or assertion authority.

## Available actions

| #  | Action        | Role                                                               | Input                              |
|----|---------------|--------------------------------------------------------------------|------------------------------------|
| 01 | `assess-doc`  | Weight and verify Markdown claims against repository evidence; delegate external facts separately | File path, or bounded scan if omitted |
| 02 | `assess-code` | Route code freshness, dependency, or runnable-resolution concerns to AIDD | File or directory path (required) |

## Default flow

Dispatch on file extension (or absence of argument):
- No argument OR `.md` / `.markdown` path → `assess-doc`
- Any code file extension (`.ts`, `.js`, `.vue`, `.php`, `.py`, etc.) → `assess-code`

## Harvest integration

`harvest` invokes taste as a dedicated phase via `@../taste/SKILL.md`. Taste returns aggregated document-verdict metrics; an explicitly requested code branch returns the delegated AIDD report and receipt instead of legacy detector counts.

## Delegation

Read [the AIDD delegation contract](../../references/aidd-delegation.md) before `assess-code` or external fact verification. Delegated reports remain authoritative; taste returns a receipt and never restores a local code detector when AIDD is unavailable.

## Transversal rules

- Extract only claims that are explicitly stated — never infer.
- Skip issue-status checks when no tracker CLI is detectable.
- Never modify the assessed document or project source during assessment.
- Resolve the active rule sources from host portability: `AGENTS.md` plus `.agents/rules/` on Codex, `.claude/rules/` on Claude Code, or their union in a dual-host project. Skip the rule-violation check silently only when none exists.
- Verdicts use weighted local evidence: **Current** (≥80%), **Partial** (20–79%), **Obsolete** (<20%), **Superseded** (subject-matched replacement after ≥80%), or **N/A** (no eligible local claim). A critical obsolete claim vetoes Current and Superseded.
- Scan at most 25 documents by default and report unscanned coverage. Git history prioritizes work but never proves obsolescence.
