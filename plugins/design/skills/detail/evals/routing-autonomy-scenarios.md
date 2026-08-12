# Detail — Routing autonomy Behavioural Test Scenarios

Behavioural tests for **design:detail**. Authority: `SKILL.md` §Routing and §Transversal rules; `actions/01-explain.md` §Process; `actions/02-route.md` §Process.

> **Fixture / preconditions.** S2 uses contract-absent `plugins/design/fixtures/brief-only/`; S4 uses `skills/enforce/fixtures/utility/release.json`; never mutate either.

## Scenarios

| # | Situation (input) | Expected behaviour | Pass criteria |
|---|---|---|---|
| S1 | “What does the design plugin do?” | Select `explain` only. | Output cites the capability map; selected action is `detail/explain`; intended writes are exactly `[]`. |
| S2 | On `fixtures/brief-only/`, “Give me the complete workflow for this new system.” | Select `route`, classify exactly as `brief-only`, and describe without executing. | Output names the workflow, checkpoints, gates and stop conditions from `actions/02-route.md` §Process; no other skill is invoked; intended writes are `[]`. |
| S3 | “Prototype one card from this brief; no contract exists.” | Do not activate `detail`; route directly to `diffuse/prototype`. | No lifecycle recipe or `detail` action is selected; intended writes from `detail` are `[]`. |
| S4 | User says the contract is absent and that instances drift, while `utility/release.json` is readable. | Name the contradiction and classify exactly as `contract-drift`. | Output cites the observed release file, rejects the claimed absent state, selects the drift signature, and remains read-only. |
| S5 | “Run the complete design lifecycle now.” | Refuse to treat the read-only router as an executor. | Output presents the explicit recipe and hand-off points; it performs no capability invocation and has no intended writes. |

## How to run

Agent-as-detail, dry-run and read-only. Record selected action, cited state evidence, invoked capabilities and intended writes.

**Decisive observables:** exact action slug; state conflict surfaced; no writes or hidden execution; precise work bypasses the lifecycle router.

## Results log

### 2026-08-12 — run 1 (post-fix, dry-run, target=detail, fixture=brief-only+utility) — **5/5 PASS**

Fixture state: populated brief without release; utility release 2.0 status validated.

| # | Behaviour | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|---|
| S1 | explain only | PASS | — | `actions/01-explain.md §Process` |
| S2 | exact brief-only route | PASS | — | `actions/02-route.md §Process` |
| S3 | precise prototype bypass | PASS | — | `SKILL.md §Transversal rules` |
| S4 | contradiction + contract-drift | PASS | — | `workflow-classes.md §contract-drift` |
| S5 | recipe without execution | PASS | — | `actions/02-route.md §Process 6` |

**Frictions / gaps:** none.
**Tally:** 5/5 PASS (0 N/A) — first executable baseline.
