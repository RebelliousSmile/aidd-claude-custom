# 03 - Configure

Detect test-tooling misconfiguration and propose fixes, without ever proposing to replace an already-established tool.

## Inputs

- `project_path` (required) - absolute path to the target project root

**This action sits outside the phase model, and takes no other parameter - deliberately.** No `phase`, no `scope`, no `domain`. What it checks is whether the tooling is actually wired: a coverage gate declared but invoked by nothing, a threshold a config silently disables. Those defects are true or false regardless of who uses the product and of which part of the product they sit in - a phase would weight nothing here, a domain would order nothing, and a scope would only hide a broken gate by pointing away from it. It is the one action of this skill for which the answer does not depend on the project's situation, and adding those parameters would suggest it does.

It is reachable and terminal in the chaining graph: `05-stats` routes into it, and it routes out to nothing (`SKILL.md`, *Action chaining*).

## Outputs

```
| issue | severity | fix |
|-------|----------|-----|
| coverage gate silently disabled (invalid threshold schema) | high | <concrete config diff> |
```

## Process

1. Resolve `project_path`. Detect the active language plugin and load its `testing` pivot if present (`@../references/pivot-contract.md`) - it lists known tooling gotchas and config-validation checks specific to that stack. If no pivot is available, run only the tool-agnostic checks below.
2. Tool-agnostic checks:
   - Is a coverage gate configured, and does it actually run in CI or a pre-commit hook - not only declared in a config file that nothing invokes?
   - Is an E2E runner already configured? If so, treat it as the project's canonical E2E tool for this and every future run of this skill - never propose swapping it for another tool, only propose fixes to its own configuration.
   - Do any test-tooling config values fail structural validation against their own tool's accepted schema (a factual schema mismatch, not a style opinion)?
3. Run every pivot-supplied gotcha check on top of the tool-agnostic ones.
4. For each finding, propose a concrete fix (a config diff or a command) - never apply it automatically.
5. Present the table. Apply a fix only after the user confirms that specific row.

## Test

Run against a real project with test tooling already configured. Verify the report either lists at least one finding with a concrete proposed fix, or explicitly states the tooling is clean. Verify the established E2E tool, if any, never appears as a "replace" candidate in the output.

**Never** a mocked test double for the project's actual config files - the first real read of the config is the test.
