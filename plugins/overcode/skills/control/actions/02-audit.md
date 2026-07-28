# Audit

Find low-value tests in an existing suite and propose their removal - never delete without explicit per-item confirmation.

## Inputs

- `project_path` (required) - absolute path to the target project root
- `scope` (optional, default: whole project) - a subdirectory or glob to limit the audit. **`scope` designates one universe, here as everywhere in this skill: the source code and the tests that match it.** The resolution is **symmetric** - a path landing in the test tree resolves up to the corresponding source, a path landing in the source resolves down to its tests, and the universe is the pair either way. `scope=tests/legacy/` therefore stays expressible, and no action has a universe of its own. What this action *reads* is the test side of that pair; what bounds it is the pair.
- `domain` (optional) - a functional domain declared by the project (`auth`, `payment`), resolved to code by the terms the project supplies and by the pivot's *Domain resolution* field. It **prioritises the audit; it never restricts it**: a test matching no domain is still audited, ranks lower, and is reported with the term that failed to match it. Mutually exclusive with `scope` - given both, stop and ask which was meant (`SKILL.md`, *Parameters*).
- `phase` (optional) - overrides the resolved project phase for this run only

## Outputs

```
| file | test | reason | proposed_action |
|------|------|--------|------------------|
| tests/x.spec.js | "returns default" | duplicate of tests/y.spec.js:12 | propose-delete |
```

No file is deleted as part of producing this table.

When a `domain` was given, the table is followed by the **resolution report**: which terms matched what, and which terms matched nothing. A term that resolved to no file is stated as such - it usually means the domain is named differently in this codebase than in the document that declared it, and an unreported miss reads as a domain that is genuinely clean.

## Process

1. Resolve `project_path` and `scope`. Enumerate test files using the active language plugin's `testing` pivot glob if loaded (`@../references/pivot-contract.md`), else a generic `**/*.{test,spec}.*` glob.
2. For each test, apply three low-value heuristics:
   - **Duplicate** - asserts the same behavior as another test already in the suite.
   - **Trivial** - test body under 5 lines AND asserting only a framework/library guarantee or an unbranched assignment, excluding imports and setup/teardown. A short test that asserts a real input -> output transformation (the ideal shape of a `contract` test per `decision-framework.md`) is not trivial merely for being short - line count alone is never sufficient to flag it.
   - **Getter/setter-only** - asserts only that a property was set or read, with no branching or business logic involved.
3. Build the candidates table with a one-line reason per row, referencing the duplicate's location when applicable.
3-bis. Resolve the project **phase** per `@../references/phase-framework.md` - **never by deduction**: argument, declaration in the project's own documentation, or a question asked before the table is built. State it with its provenance, and use it to **order** the table along the two reading axes - `foundations` and the project's declared domains (or the generic `critical journeys` fallback): a candidate the current phase deprioritises rises in the list, one it raises falls. Under `default` and `undetermined` the weighting is neutral and the table comes out in heuristic order alone - say so rather than presenting an unweighted order as if it were a phase's. The phase **qualifies nothing**: a row is in this table because one of the three heuristics flagged it, never because of the phase. A test the phase deprioritises but no heuristic flags does not appear here at all - it stays - the phase prioritises, it never qualifies, and a row is proposed for removal on a heuristic criterion, never "because we are in production".
3-ter. **Density outliers point this action at a file; they never fill a row of its table.** When `05-stats` or `01-write` reported a file past 3× the project's median density under the *low-value* reading (`@../references/test-density.md`), audit that file first - the ratio says many cases sit on little logic, which is where duplicates and trivia concentrate. But a row still needs one of the three heuristics to hold. A high density is a reason to **look**, and on its own it is not a reason found: the calibration turned up a file whose cases each exercised a distinct regex alternative the denominator could not see, and every one of them was worth keeping. Report a file examined on that signal and cleared as examined and cleared - a silently dropped outlier reads as an outlier nobody looked at.
4. Present the table to the user. Delete only the rows the user explicitly confirms (individually, or via an explicit batch selection they name) - anything not explicitly confirmed stays untouched.
5. Never invoke a delete on a row the user's confirmation does not cover, mirroring `overcode:harvest`'s per-item confirmation gate. **The confirmation regime of this action is unchanged by the phase**: whatever the phase, however it re-orders the table, no row is removed unless a confirmation covers it - its own, or the batch the user named themselves. That relaxation is a removal-side one and does not exist on the addition side (`SKILL.md`, *Confirmations*).

## Test

Covered by `../evals/authority-scenarios.md` (S1, S9), `../evals/confirmations-scenarios.md` (S1, S3) and `../evals/chaining-scenarios.md` (S6).
Run: `overcode:behave 02-run <suite> <fixture>`.
