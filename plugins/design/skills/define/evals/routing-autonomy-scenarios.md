# Define — Routing autonomy Behavioural Test Scenarios

Behavioural tests for **design:define**. Authority: `SKILL.md` §Routing and §Transversal rules; `actions/01-intake.md` §Process; `actions/04-write-material.md` §Artefacts écrits; `actions/05-copycat-fanout.md` §Process.

> **Fixture / preconditions.** Use populated `plugins/design/fixtures/brief-only/brief.md`, CSS evidence `skills/enforce/fixtures/adapters/tokens.css`, and bulk state `skills/define/fixtures/copycat-two-pages.json`. Dry-run intended writes only.

## Scenarios

| # | Situation (input) | Expected behaviour | Pass criteria |
|---|---|---|---|
| S1 | Supply the fully populated clinic brief with no visual evidence. | Route `intake → construct → write-material`. | Per `actions/04-write-material.md` §Artefacts écrits, intended writes are exactly `design/tokens.json` and `design/design-system.md`; forbidden writes include `release.json`, `components.json`, `policies.json`, `oracle.json`, and adapters. |
| S2 | Ask only to extract tokens from `fixtures/adapters/tokens.css`. | Route `intake → extract → write-material` and stop. | Per `actions/04-write-material.md` §Artefacts écrits, intended writes are exactly `design/tokens.json` and `design/design-system.md`; no gate, freeze, component render or adapter generation is invoked. |
| S3 | Ask to freeze an already prepared draft. | Do not activate `define`. | Selected target is `adjust`; no `define` action and no draft rewrite is planned. |
| S4 | Mention a visual reference that is unavailable. | Ask for accessible evidence; do not invent its contents. | Output names the missing source; intended writes are `[]` until evidence or an explicit brief-only choice is supplied. |
| S5 | Apply `copycat-two-pages.json`, with one signed-off page, one pending page, and unresolved 8px/10px spacing. | Select `copycat-fanout` only for the pending leaf and stop at the conflict checkpoint. | Signed-off `home` is excluded; pending `booking` is selected; conflict is listed without arbitration; no contract/freeze write occurs and the P2 checkpoint is reported. |

## How to run

Agent-as-define, read-only dry-run. Record the action sequence, exact intended/forbidden paths and invoked capabilities.

**Decisive observables:** mutable-material boundary; unavailable evidence never invented; exact downstream non-activation; fan-out preserves human arbitration.

## Results log

### 2026-08-12 — run 1 (initial, dry-run, target=define, fixture=brief+CSS) — **4 PASS, 1 N/A**

Fixture state: populated brief and CSS; the first run lacked a populated two-page bulk state.

| # | Behaviour | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|---|
| S1 | brief to mutable material | PASS | — | `actions/01-intake.md §Process`; `04-write-material.md §Artefacts écrits` |
| S2 | CSS extraction stops | PASS | — | `actions/02-extract.md §Process` |
| S3 | freeze excluded | PASS | — | `SKILL.md §Transversal rules` |
| S4 | missing visual not invented | PASS | — | `actions/01-intake.md §Process 2` |
| S5 | bulk copycat boundary | N/A | — | populated bulk fixture absent |

**Frictions / gaps:** S5 required signed-off/pending page state and a concrete unresolved conflict.
**Tally:** 4/4 applicable PASS (1 N/A) — fixture gap reproduced.

### 2026-08-12 — run 2 (post-fix, dry-run, target=define, fixture=brief+CSS+copycat-two-pages) — **5/5 PASS**

Fixture state: `copycat-two-pages.json` adds signed-off `home`, pending `booking`, and unresolved 8px/10px conflict.

| # | Behaviour | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|---|
| S1–S4 | unchanged routes/boundaries | PASS | = | citations from run 1 remain applicable |
| S5 | pending leaf only, conflict stop | PASS | ▲ | `actions/05-copycat-fanout.md §Process A,C` |

**Frictions / gaps:** none.
**Tally:** 5/5 PASS (0 N/A) — fixture gap closed.
