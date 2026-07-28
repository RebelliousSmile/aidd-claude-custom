# Write

Decide whether a requested test should exist, at which tier, and within budget - before any test code is written.

## Inputs

- `behavior` (required) - one-line description of the behavior or code path that needs coverage
- `project_path` (required) - absolute path to the target project root
- `phase` (optional) - overrides the resolved project phase for this run only

This action takes **neither `scope` nor `domain`**, and the reason is the same for both: it judges one behaviour. There is no universe of files to bound structurally, and none to weight semantically. A domain would change nothing about a single classification - it orders a table, and this action produces no table.

## Outputs

```
tier: contract | e2e | skip
phase: <resolved phase, one of scaffolding | hardening | production | sustaining | default | undetermined>
       (provenance: argument | declared <path> | answered | unanswered)
rationale: <one paragraph, citing the phase as context - never as the tier's cause>
budget_check: { current_count: <n>, limit: <n or null>, status: ok | warn | blocked }
density: { target_file: <path>, value: <ratio>, median: <ratio>, status: ok | outlier (<n>x median) | insufficient population | not applicable }
delegated_to: aidd-dev:06-test#01-test | aidd-dev:06-test#02-test-journey | none
```

## Process

1. Resolve `project_path`. Look for a documented test strategy at `<project_path>/aidd_docs/memory/testing.md` (the AIDD memory convention). If present, use its tier table. Otherwise load `@../references/decision-framework.md` as the default.
1-bis. Resolve the project **phase** per `@../references/phase-framework.md`, at the same rank as the documented strategy and the pivot: it is loaded context, not a decision input. It is **never deduced** - it comes from the `phase` argument, from the project's own documentation, or from asking the user before the classification is stated. It never changes the tier - see step 3 - and never populates `limit`. Under `default` and `undetermined` there is nothing to cite as context; say so in `rationale` rather than citing a neutral weighting as if it were a reading of the project - and distinguish the two, since one is a decision the project took and the other a question it has not answered.
2. Detect the active language plugin for `project_path` and check whether it ships a `testing` capability pivot per `@../references/pivot-contract.md`. If present, load it for tooling-specific mechanics (test runner, test-count command, tier thresholds). If absent, proceed without it and note the gap in the output.
3. Classify `behavior` against the loaded tier table (project doc, else default) into `contract`, `e2e`, or `skip`, following the decision order in the loaded source. **The tier comes from the tier table alone.** The phase is cited in `rationale` - it says whether this behavior is what the project should be securing right now - but it never moves a `contract` to an `e2e`, and never turns a classifiable behavior into a `skip`. A behavior the phase deprioritises is still classified: what the phase informs is the user's decision to write it now, not the tier it would get.
3-bis. **What no test can prove, and the ceiling that follows.** Before any delegation, separate the part of `behavior` the suite can settle from the part it cannot. A behavior whose truth depends on a **third party still honouring its contract** - that the remote inbox accepts the payload, that the vendor's schema has not moved, that the provider is up - is **out of reach of testing**, whatever tier the table assigns it. Say so, name **monitoring** as what covers it, and never delegate a test for it: a test written against a live external boundary passes for reasons the project does not control and fails for reasons it cannot fix, so it reports the vendor's weather, not the code's health. The same rule and the same words are in `04-strengthen.md` (*Process*, **External contract dependency**); it belongs here too, because `SKILL.md` › *Action chaining* makes this action the sink every new test enters through - a ceiling that exists only in the ranking action is a ceiling with a door next to it.

   What remains testable is the code's **own side** of the boundary: that the request is built as specified, and that the **degraded path** - refusal, timeout, malformed answer - is handled. **One boundary is worth one test by default, and that is a ceiling, not a quota** - the degraded path, once. The built payload earns a **second** test only when it carries data with a verifiable in-process consequence: an amount, an order identifier, an authorisation status, a consent. A measurement pixel carries none. When `behavior` asks for more than that on a single boundary, say what the extra cases would and would not prove, and let the user decide before step 6 or 7 runs. Reclassify nothing on this basis: the tier stays what step 3 decided, and what changes is whether the delegation happens at all.

4. Number constraint: get the current test count via the pivot's test-count command if available, else count matching test files manually. `limit` is populated exclusively from the project's own documented test strategy - never from an internal default invented by this skill. If the project's strategy doc states a budget, compare against it and set `limit` accordingly; otherwise `limit` stays `null` and the only check is a subjective warn once the count is unusually large for the project's size, asking the user to confirm before proceeding. Record `budget_check`, and state the phase alongside it: the phase does not set `limit` - nothing but the project's own document does - but it is what makes a `warn` readable, since the same count means something different in `scaffolding` and in `sustaining`.
4-bis. **Density** per `@../references/test-density.md` - the constraint that applies when no cap is declared, and the one that says something even when a cap is. Compute the project's distribution from its coverage report, take its median, and place the file this test would land on. Report `density` in the output block, and when the file already sits past 3× the median, **say it before delegating** - a new case on a file already saturated is the moment where saying so is still cheap. Then delegate anyway if the tier says so: **density never refuses, and it never changes the tier.** It is the same boundary the phase has, and it is why `tier` is decided at step 3, before this step runs at all. When the project has too few tested files for a median, report `insufficient population` and move on without an outlier - that is the normal state of a `scaffolding` project, not a finding.
5. If `tier = skip`: report the rationale and stop. Set `delegated_to: none`.
6. If `tier = contract`: delegate to `aidd-dev:06-test` action `01-test`, passing `behavior` and the tier's quality constraints as explicit input.
7. If `tier = e2e`: delegate to `aidd-dev:06-test` action `02-test-journey`, passing `behavior`.
8. Report the full outcome block to the user before the delegated action starts executing - the user can override the tier or cancel before delegation happens.

## Test

Covered by `../evals/authority-scenarios.md` (S6, S8, S10, S11), `../evals/chaining-scenarios.md` (S13) and `../evals/measurement-scenarios.md` (S14, external boundary).
Run: `overcode:behave 02-run <suite> <fixture>`.
