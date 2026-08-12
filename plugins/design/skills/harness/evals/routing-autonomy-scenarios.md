# Harness — Routing autonomy Behavioural Test Scenarios

Behavioural tests for **design:harness**. Authority: `SKILL.md` §Routing and §Transversal rules; `actions/01-scaffold.md` §Process; `actions/02-contract-inline.md` §Process; `references/harness-contract.md`.

> **Fixture / preconditions.** Use generator `adapters/harness/harness.py` and fixtures `adapters/harness/fixtures/{1x,2x,2x-style-breakout,2x-no-stylesheet}/`. Output is a unique temporary HTML path.

## Scenarios

| # | Situation (input) | Expected behaviour | Pass criteria |
|---|---|---|---|
| S1 | Supply `/tmp/design-behave-scaffold.html` and pages `home,contact`, without a contract. | Select `scaffold`. | Intended writes contain exactly that HTML; contract reads/writes are `[]`; public exit is 0. |
| S2 | Supply the same valid pages and fixture `2x`. | Select `contract-inline`. | `adapters/tokens.css` is read and inlined; only output HTML is written; contract artifacts stay unchanged; exit is 0. |
| S3 | Supply page key `/contact/`. | Refuse the invalid slug. | Exit is 2 and the output HTML does not exist. |
| S4 | Supply fixture `1x`. | Refuse the unsupported contract. | Exit is 3 and no output is written. |
| S5 | Supply fixture `2x-style-breakout`. | Reject unsafe `</style>` content. | Exit is 2 and no output is written. |
| S6 | Supply fixture `2x-no-stylesheet`. | Generate with an explicit warning. | Exit is 0; one output HTML is written; warning names the absent stylesheet. |
| S7 | Ask to create the complete design system. | Do not activate `harness`. | No harness action or output path is planned. |

## How to run

Agent-as-harness plus the real generator in a temporary directory. Record selected action, stdout/stderr, exit code, output existence and contract checksums.

**Decisive observables:** one output only; contract immutable; public exits 0/2/3; unsafe or legacy inputs write nothing; unrelated lifecycle request excluded.

## Results log

### 2026-08-12 — run 1 (post-fix, dry-run, target=harness, fixture=harness-fixtures) — **7/7 PASS**

Fixture state: real `harness.py` run in isolated temp output; exits S1–S6 = 0/0/2/3/2/0; only successful cases produced one HTML.

| # | Behaviour | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|---|
| S1 | standalone scaffold | PASS | — | `actions/01-scaffold.md §Process` |
| S2 | contract stylesheet inline | PASS | — | `actions/02-contract-inline.md §Process` |
| S3 | invalid slug exit 2 | PASS | — | `references/harness-contract.md` |
| S4 | legacy exit 3 | PASS | — | `SKILL.md §Transversal rules` |
| S5 | style breakout exit 2 | PASS | — | `references/harness-contract.md` |
| S6 | absent stylesheet warning | PASS | — | `actions/02-contract-inline.md §Process` |
| S7 | lifecycle request excluded | PASS | — | `SKILL.md §Routing` |

**Frictions / gaps:** none; runtime selfchecks also pass for generated outputs.
**Tally:** 7/7 PASS (0 N/A) — first executable baseline.
