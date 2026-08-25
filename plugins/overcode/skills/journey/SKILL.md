---
name: journey
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

# Journey

Journey drives end-to-end validation of a GitHub or GitLab issue: it finds the matching plan in `aidd_docs/tasks/`, generates a Playwright test file from the issue steps, runs it, logs every result into a structured report, and posts the Summary and Conclusion back to the issue.

## Available actions

| #  | Action | Role                                                                 | Input                                   |
|----|--------|----------------------------------------------------------------------|-----------------------------------------|
| 01 | `run`  | Parse issue → find plan → generate Playwright test → run → report → post comment | GitHub/GitLab issue URL or `#N` (`$ARGUMENTS`) |

## Default flow

Single action. Dispatch to `run` on any trigger.

## Transversal rules

- Issue reference is mandatory: abort with a clear message if `$ARGUMENTS` is empty or does not resolve to a valid issue.
- If no linked plan is found in `aidd_docs/tasks/`, propose `/plan` to the user and stop.
- Delete `tests/e2e/_journey_temp.spec.ts` after the test run completes, whether it passed or failed.
- Log results step by step into the report — never batch-write at the end.
- Post only the Summary and Conclusion sections to the issue comment, not the full report.

## Assets

- `assets/journey.md` — journey report template (copy to `<plan_stem>.journey.md` at step 3)

## External data

- `${PROJECT_RULES_ROOT}/custom/05-playwright-patterns.md`, when present — Playwright conventions for this project; on Codex also inspect the applicable `AGENTS.md`
