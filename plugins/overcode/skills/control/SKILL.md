---
name: control
description: Governs test creation, existing-test value, coverage gaps, suite-wide reporting, test-tooling configuration, and the alignment of a project's own test strategy document with what it actually does, so tests stay bounded in number and correctly tiered in kind. Use when asked to "add a test", "write a test for X", "should I write a test for X", "audit the test suite", "find low-value tests", "clean up tests", "what should I test next", "which coverage gaps matter most", "check the test config", "why isn't coverage failing the build", "how many tests do we have", "what test strategy is in place", "align the test documentation", "is the test strategy still up to date", "declare the project's phase", "the test document no longer matches the project", or "govern the test strategy". Do NOT use for behavioural/prompt-driven testing of skills or agents - use `behave` instead. Do NOT use to write the test code itself once a tier is decided - this skill delegates that to `aidd-dev:06-test`.
disable-model-invocation: true
---

# Control

Sits in front of `aidd-dev:06-test` as a gate: before a new test is written, decides whether it should exist at all and at which tier; separately, audits a project's existing tests for low-value candidates, ranks its uncovered code by risk to say what is worth testing next, checks its test tooling for silent misconfiguration, reports at a glance where the suite stands and which strategy governs it, and closes the loop by proposing that the project's own strategy document be brought back in line with what the project actually does. Every action is generic - a project's own documented test strategy, or a language plugin's `testing` pivot, refines the decision; neither is required for this skill to run.

## Available actions

| #  | Action      | Role                                                                                   | Input                                    |
|----|-------------|-----------------------------------------------------------------------------------------|-------------------------------------------|
| 01 | `write`     | Decide tier (contract / e2e / skip) and budget for a new test request, then delegate    | Behavior description, target project path |
| 02 | `audit`     | Find low-value existing tests (duplicates, trivial, getter/setter-only), propose removal | Target project path                       |
| 03 | `configure` | Detect test-tooling misconfiguration and propose fixes, without swapping tools           | Target project path                       |
| 04 | `strengthen`| Rank missing tests / uncovered code by risk, propose the few that matter, via `01-write` | Target project path                       |
| 05 | `stats`     | Read-only snapshot: test volume by tier, and which test strategy is actually in force    | Target project path                       |
| 06 | `align`     | Audit the gap between the project's test document and its reality, propose the update    | Target project path                       |

## Default flow

Non-sequential - the router dispatches on user intent. Trigger-to-action mapping:

- "add/write a test for X", "should I test X", "is this worth testing" → `01-write`
- "audit the tests", "find low-value tests", "clean up the test suite", "which tests can I delete" → `02-audit`
- "check the test config", "why isn't coverage failing", "fix the test tooling" → `03-configure`
- "what should I test next", "which tests are missing", "where is my coverage weakest", "what's the riskiest untested code" → `04-strengthen`
- "how many tests do we have", "what's our test strategy", "which strategy is in force", "test suite overview", "where do we stand on tests" → `05-stats`
- "align the test documentation", "is the test strategy still up to date", "declare the project's phase", "the test document no longer matches the project", "update our testing.md" → `06-align`

If the target project path is not given, ask for it before running any action - not one of them can produce a meaningful result without it.

## Action chaining

The routes between actions are a **contract, not a suggestion**: an action that names another must hand the case over rather than do that action's job itself, and an action that is handed a case must not recompute what it was handed.

```
                        05-stats            entry hub
                     /    |    |    \
                    v     v    v     v
         03-configure  02-audit |  06-align
          (terminal)      ^     |    /  |
                          |     v   v   |
                          +-- 04-strengthen
                                  |      |
                                  v      v
                                  01-write        sink
                                     |
                                     v
                            aidd-dev:06-test      leaves this skill
```

Edge by edge, and nothing else is an edge: `05-stats` routes to the four actions that act; `04-strengthen` refers a saturated file back to `02-audit`; `06-align` mobilises `02-audit`'s motives and re-runs `04-strengthen`'s ranking on a phase switch; `04-strengthen` hands every confirmed gap to `01-write`, which delegates to `aidd-dev:06-test`.

- **`05-stats` is the entry point.** It reads the situation and routes; it proposes no removal, ranks no gap, writes nothing. When the starting point is unknown, it is the action to run.
- **`01-write` is the sink** - every new test enters through it (the transversal rule below states why), and it is where control leaves this skill for `aidd-dev:06-test`. **`02-audit` has no edge to it**, and that is not an omission: an audit removes, it never originates a test.
- **`02-audit` ↔ `04-strengthen` are the two directions of one judgement**, and `06-align` is the only action that mobilises both at once, on a phase switch, and even then it originates neither: the outgoing motives come from `02-audit`, the incoming ranking from `04-strengthen`.
- **`03-configure` is reachable and terminal.** It answers a question the others do not ask, and its answer feeds none of them.

## Parameters

| Parameter | Actions | What it means there |
|---|---|---|
| `phase` | 01, 02, 04, 05, 06 | The project's phase (`references/phase-framework.md`). Never deduced; resolved and reported with its provenance. |
| `scope` | 02 · 04, 05, 06 | **The name is one, the target is not.** On `02-audit` it bounds a set of *test files* - the suite is what is being judged. On `04-strengthen`, `05-stats` and `06-align` it bounds a set of *source files* - the production code is what is being read. Each action states its own target where it declares the parameter; none of them leaves it implicit. |
| `domain` | 02, 04, 05, 06 | A declared functional domain (`auth`, `payment`). It prioritises within the analysed universe; it never removes anything from it. |
| `top_n` | 04 | How many ranked gaps to report. Bounds the output, never the analysis. |

`03-configure` takes `project_path` and nothing else - see the rule below. `01-write` takes neither `scope` nor `domain`: it judges one behaviour, so there is no universe to bound and none to weight.

`scope` and `domain` are **mutually exclusive**. Given both, the action **stops and says so** rather than applying a precedence: one bounds a file set structurally, the other weights a universe semantically, and a silent winner between the two would produce a result whose universe nobody can name. Ask which one was meant.

## Transversal rules

- Tier and configuration decisions are sourced in this order of precedence: (1) the target project's own documented test strategy (conventionally `aidd_docs/memory/testing.md`, per the AIDD memory layout) if present, (2) `references/decision-framework.md` (this skill's generic default) otherwise. A language plugin's `testing` pivot (`references/pivot-contract.md`) layers stack-specific mechanics on top of whichever source applies, and MAY refine a tier classification through its own "Tier thresholds" section - but only when the refinement is justified by a boundary that stays local/emulated and crosses no UI, no browser, and no external network/DB. A pivot must never reclassify a case that crosses a real external boundary. **That bound covers tiers and nothing else.** Every other thing a pivot supplies carries its own bound, stated where that thing is defined: *Risk signals* prioritise without classifying, *Domain resolution* completes without overriding. A pivot's authority is never granted in general - it is granted field by field, and a field with no stated bound has no authority to extend.
- **Every action but `03-configure`** resolves the target project's **phase** (`scaffolding` / `hardening` / `production` / `sustaining` / `default` / `undetermined`) per `references/phase-framework.md`, and reports it with its provenance (`argument` / `declared <path>` / `answered` / `unanswered`) - **two distinct lines, never merged**: the value says which phase, the provenance says where it came from, and only one pairing is forced (`unanswered` ⇔ `undetermined`). **The phase is never deduced from the repository**: it comes from an explicit `phase` argument, from a declaration in the project's own documentation, or from a question put to the user *before* anything is ranked or proposed. A repository shows what was built; it does not show whether anyone is using it, which is the one thing the phase turns on. `undetermined` means the question went unanswered, never that a guess fell short; `default` means neutrality was chosen and written down, so the question stops being asked. The phase governs the **analysis strategy** - which criteria weigh, how the coverage report is read, in which order the result comes out - and it **prioritises; it never classifies a tier** - same boundary as a pivot's *Risk signals*. It may move a gap to the top of a table or a low-value test to the top of a removal list, never change the tier proposed for either: tier authority stays with the loaded tier table. A test is refused on a tier criterion, never "because we are in production". And it weights without ever setting a numeric threshold: a per-phase coverage floor would turn the percentage into a target, which the rule below forbids.
- **`03-configure` sits outside the phase model, deliberately.** It checks whether the tooling is wired - a coverage gate declared but invoked by nothing, a threshold its own config silently disables. Those defects are true or false regardless of who uses the product, so the phase would weight nothing and the domains would scope nothing. It therefore takes neither `phase`, nor `domain`, nor `scope`; `05-stats` routes *into* it, and it routes out to nothing.
- The target project may declare **domains** - functional parts of the product (`auth`, `payment`, `checkout`) resolved in code by terms. The project declares *which* domains exist, the pivot's **Domain resolution** field declares *how* to spot them in this stack, and the two cannot contradict each other because they answer different questions; a pivot completes a domain named without a resolution, and never overrides one the project wrote about its own code. **A domain prioritises; it never restricts.** What no domain matches stays in the analysis, ranks lower, and **is reported together with the term that failed to match it** - a silent false negative would declare a central part of the code out of scope with nobody able to see it, which is the exact failure this skill exists to prevent. When a project declares no domain, the generic `critical journeys` fallback applies and nothing is lost.
- Never delete a test file, apply a config fix, or write a proposed missing test, without a separate, explicit per-item confirmation from the user. **One exception, and it is bounded twice over: `06-align` only, and only on a phase switch.** There, a removal may be consented to as a **characterised batch** - one consent covering a set defined by its *selection criterion*, not by its enumeration. The reason is worth keeping with the rule: a generated test is rewritten at low cost, so deletion is no longer the irreversible act that per-item confirmation was protecting; what still has to be protected is **knowing what is being deleted**, and at the scale where a batch becomes useful that is what the criterion says and what a several-hundred-line list does not. Past the volume at which the analysis stops being meaningful, demand a narrower `scope` rather than unrolling the list - the same saturation bound `04-strengthen` already applies. Every other removal in this skill, `02-audit` included, keeps per-item confirmation unchanged.
- Every new test enters through `01-write`, whichever action surfaced the need - `04-strengthen` proposes and ranks, but hands each confirmed gap back to `01-write` so the tier decision and the number constraint are applied in exactly one place.
- This skill **never decides** the strategic content of the target project's test strategy document on its own. `aidd_docs/memory/testing.md` is owned by `aidd-context`'s project-memory skill, which generates and syncs it (the skill and action names have changed across `aidd-context` majors - refer to the document, never to a pinned action number). Every action but one only reads it. The exception is `06-align`, and only under its own terms: it writes what it has **measured** under its own authority, and it *proposes* a strategy in full prose that the user validates line by line before a word of it reaches the file. What a project decides to test stays the project's decision; what the skill observed is the skill's to state. When that document is still the untouched generic template - test *types* or empty placeholders rather than decision criteria - treat it as absent for tier decisions, map unit and integration to `contract` and end-to-end to `e2e`, and say so in the output rather than pretending the project has a strategy.
- **The number constraint of this skill is a density, not a count** - `references/test-density.md`. Test cases exercising a file over its branch points, read against the **median of the project's own distribution**, with an outlier reported past 3× that median. It replaces the absolute cap as the default constraint, for the reason a cap could never handle: it distinguishes a suite that is too large from a codebase that is large. An explicit test-count cap declared by the project still wins, as a cap - the project's declared strategy is not overridden by a measurement - and the density is reported alongside it, because a cap says how many and a density says whether they are in the right place. A coverage percentage is neither, and is never read as either: `limit` comes only from an explicit test-count limit.
- Density **prioritises and reports; it never refuses.** A refusal is a tier decision and comes from the tier table in force - same boundary as the phase. And it is never a target: no action proposes work whose only justification is moving a density toward the median.
- Coverage percentage is a symptom, never a target. No action of this skill proposes work whose only justification is moving a coverage number.
- `02-audit` and `04-strengthen` are two directions of one judgement, and they answer to a **net balance**: the suite's worth is what it proves per unit of maintenance, not its size in either direction. Neither action is a quota - an audit that finds nothing to remove and a strengthen that finds nothing worth adding are both valid outcomes. `04-strengthen` never proposes a test on a path the user has just had `02-audit` remove, unless the risk picture has demonstrably changed since; when both run in one session, report the net effect on the test count rather than each side in isolation.
- Never propose replacing a project's already-established E2E tool. Only propose fixes to its configuration.
- This skill orchestrates and decides; it never writes test code itself. Once a tier is decided in `write`, the actual test is written by delegating to `aidd-dev:06-test`.

## References

- `references/decision-framework.md` - generic contract / e2e / skip tier criteria, used when the target project has no documented test strategy
- `references/phase-framework.md` - the six project phases (four on the product-maturity axis, plus `default` and `undetermined` off it), how each is resolved, which risk criteria each raises or lowers, the two reading axes and the expected ordering they produce per phase, and how a domain is resolved and bounded; carries the **external contract dependency** criterion and its cost cap
- `references/test-density.md` - the number constraint: the density formula, its calibration on the project's own median, the 3× alert factor, the two readings of an outlier and the blind spot that bounds them
- `references/pivot-contract.md` - expected shape of a language plugin's `testing` capability pivot (`sc-js` ships one today; other language plugins could add one following the same shape), and what happens when none is available
