---
name: bruno
description: >-
  Run Bruno API tests in CLI mode and iterate until all targeted tests pass. Use to run or fix existing Bruno tests with the bru CLI. Do NOT use to write new Bruno files from scratch, run Playwright or unit tests, or handle non-Bruno testing.
---

Read [host portability](../../references/host-portability.md) before resolving plugin files, invoking sibling skills, or persisting project guidance.

# Bruno

Bruno runs the project's Bruno API test suite via the `bru` CLI, parses results, and iterates — investigating root causes and applying fixes — until all targeted tests pass.

## Available actions

| #  | Action | Role                                                          | Input                                                  |
|----|--------|---------------------------------------------------------------|--------------------------------------------------------|
| 01 | `test` | Run Bruno tests, parse results, fix failures, repeat until all pass | Folder or `.bru` file path (`$ARGUMENTS`, optional) |

## Default flow

Single action. Dispatch to `test` on any trigger.

## Transversal rules

- Always pass `--env local` to every `bru run` invocation.
- Always pass `--tests-only` to every `bru run` invocation.
- If `$ARGUMENTS` specifies a path, run only that path — never expand scope automatically.

## External data

- `${SC_PHP_PLUGIN_ROOT}/skills/sniff/references/capabilities/testing/bruno.md` — Bruno conventions (capability pivot, loaded at audit time by sc-php:audit)
