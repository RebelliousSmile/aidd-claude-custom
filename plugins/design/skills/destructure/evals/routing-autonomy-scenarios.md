# Destructure — Routing autonomy Behavioural Test Scenarios

Behavioural tests for **design:destructure**. Authority: `SKILL.md` §Routing and §Transversal rules; `actions/01-challenge.md` §Process and §Outputs.

> **Fixture / preconditions.** S1–S4 use frozen contract `skills/enforce/fixtures/utility/`; S5 uses `skills/destructure/fixtures/zero-pair/`; report date is fixed to `2026-08-12`; source and contracts stay read-only.

## Scenarios

| # | Situation (input) | Expected behaviour | Pass criteria |
|---|---|---|---|
| S1 | Critique the fixture’s visual direction as a standalone target. | Select `challenge` without requiring an upstream draft. | Only intended write is `design/critique/2026-08-12-utility.md`; contract and source writes are `[]`. |
| S2 | Request alternatives emphasizing hierarchy and interaction states. | Emphasize those lenses while retaining every mandatory declared dimension and contract cost. | Per `actions/01-challenge.md` §Process, report contains the complete lens set plus 2–4 alternatives for each requested axis with effect and refreeze/re-entry cost. |
| S3 | Ask to challenge an implementation plan. | Do not activate this design critique. | Selected target is `aidd-refine:02-challenge`; no `destructure` action or design report is planned. |
| S4 | Request conversation-only critique. | Suppress persistence. | Intended writes are exactly `[]`, including no `design/critique/` path. |
| S5 | Critique `zero-pair/`, whose colour tokens have no measurable foreground/background pairing. | Treat zero pairs as the strongest finding and never infer contrast. | Per `actions/01-challenge.md` §Process, output emits the foreground/background pairing table to declare, explicitly refuses a future freeze until measurable, and makes no subjective pass claim or contract write. |

## How to run

Agent-as-destructure, dry-run. Record selected target, measurements, exact report path and contract/source intended writes.

**Decisive observables:** standalone activation; exact persistence boundary; neighboring plan challenge excluded; missing measurements never become a pass.

## Results log

### 2026-08-12 — run 1 (initial, dry-run, target=destructure, fixture=utility) — **4 PASS, 1 N/A**

Fixture state: utility is frozen/validated but its adapter finds two measurable pairs, so it cannot exercise zero-pair behavior.

| # | Behaviour | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|---|
| S1 | standalone critique write scope | PASS | — | `actions/01-challenge.md §Outputs` |
| S2 | mandatory lenses + costs | PASS | — | `actions/01-challenge.md §Process` |
| S3 | plan challenge excluded | PASS | — | `SKILL.md §Routing` |
| S4 | conversation-only opt-out | PASS | — | `actions/01-challenge.md §Outputs` |
| S5 | zero-pair refusal | N/A | — | utility adapter returned two pairs |

**Frictions / gaps:** a real zero-pair contract was required.
**Tally:** 4/4 applicable PASS (1 N/A) — fixture gap reproduced.

### 2026-08-12 — run 2 (post-fix, dry-run, target=destructure, fixture=utility+zero-pair) — **5/5 PASS**

Fixture state: zero-pair adapter returns exit 3, paired=0/declared=2, and names two unpaired brand tokens.

| # | Behaviour | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|---|
| S1–S4 | unchanged critique boundaries | PASS | = | citations from run 1 remain applicable |
| S5 | zero-pair table + freeze refusal | PASS | ▲ | `actions/01-challenge.md §Process 2-bis` |

**Frictions / gaps:** none.
**Tally:** 5/5 PASS (0 N/A) — fixture gap closed.
