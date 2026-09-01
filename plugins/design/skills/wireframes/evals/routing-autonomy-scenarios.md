# Wireframes — Routing autonomy Behavioural Test Scenarios

Authority: `SKILL.md` §Routing and §Transversal rules, its four actions §Process, and the shared wireframe contract, normalization and handoff references.

> **Fixture / preconditions.** Bundled fixtures under `adapters/wireframes/fixtures/`; static selftest uses Python and Bash, while rendered cases use Playwright 1.60.0 plus explicit Chromium. Never mutate a fixture during a dry-run.

## Scenarios

| # | Situation (input) | Expected behaviour | Pass criteria |
|---|---|---|---|
| S1 | Generate a responsive component board from the bundled valid fixture. | Select `scaffold`; generate, apply and statically lint. | Distinct output; desktop/mobile and both states exist; static exit 0; rendered/review remain unclaimed. |
| S2 | Lint a board with three annotations. | Select `lint` and fail the candidate. | Exit 1 and `annotation-count`; no rewrite. |
| S3 | Ask for safe repair of a unique element id missing its data attribute. | Select `lint --fix` with a distinct output. | Only the derived attribute changes and full re-lint runs. |
| S4 | Normalize an author HTML document or fragment. | Select `normalize`; analyze first, rebuild in a fresh shell. | Source digest stays unchanged; reviewed inventory is complete; new board passes both lints. |
| S5 | Normalize a source with two defensible journeys. | Select `normalize` and stop after analysis. | Inventory names the semantic decision; no board, manifest or payload is written. |
| S6 | Promote a reviewed page with current green evidence and `desktop-derived`. | Select `promote`; sign then hand off. | Receipt and three linked bundle files exist; initial state alone becomes the page body; `invokeHarness` is true. |
| S7 | Promote with stale or revoked review evidence. | Select `promote` and refuse before output. | Exit 2; no handoff directory. |
| S8 | Promote with `defer`. | Select `promote`; emit bundle only. | `invokeHarness` is false and no harness is created. |
| S9 | Ask for a free component prototype without a board/manifest/pillars. | Do not activate `wireframes`; bypass it for `diffuse/prototype`. | No wireframes action or artifact is selected. |

## How to run

Agent-as-wireframes, dry-run plus deterministic bundled selftest. Record action, intended paths, exit, active pillars and claimed proof layers.

**Decisive observables:** one action; distinct writes; immutable source; no silent external dependency; static/rendered/review conclusions stay separate; promotion is receipt-bound and tablet-explicit.

## Results log

### 2026-09-01 — run 1 (generality, dry-run, target=wireframes, fixture=bundled) — **9/9 PASS**

| # | Behaviour | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|---|
| S1 | canonical scaffold | PASS | — | `actions/01-scaffold.md §Process`; deterministic selftest |
| S2 | annotation failure | PASS | — | `actions/03-lint.md §Process`; static selftest |
| S3 | safe mechanical repair | PASS | — | `actions/03-lint.md §Process`; static selftest |
| S4 | immutable normalization | PASS | — | `actions/02-normalize.md §Process`; static + Chromium normalized-page proof |
| S5 | ambiguous stop | PASS | — | `actions/02-normalize.md §Process 2`; analyzer exit 1 |
| S6 | accepted page promotion | PASS | — | `actions/04-promote.md §Process`; official harness interfaces consume bundle |
| S7 | stale/revoked refusal | PASS | — | `actions/04-promote.md §Process 3`; exit 2 counter-cases |
| S8 | deferred handoff | PASS | — | `actions/04-promote.md §Process 5`; `invokeHarness=false` |
| S9 | diffuse boundary | PASS | — | `SKILL.md §Routing`; no wireframe or contract write |

**Tally:** 9/9 PASS (0 N/A). **Instruction citations:** `actions/01-scaffold.md`, `02-normalize.md`, `03-lint.md`, `04-promote.md`; shared wireframe contract and handoff references. **Gap:** Chromium remains a targeted prerequisite and is not claimed by the dependency-free global runner.
