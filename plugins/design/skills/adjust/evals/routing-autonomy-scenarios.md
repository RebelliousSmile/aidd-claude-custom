# Adjust — Routing autonomy Behavioural Test Scenarios

Behavioural tests for **design:adjust**. Authority: `SKILL.md` §Routing and §Transversal rules; `actions/01-arbitrate.md` §Processus; `actions/02-freeze.md` §Test de validité; `actions/03-migrate.md` §Étape 1–5.

> **Fixture / preconditions.** Use `skills/enforce/fixtures/utility/` for 2.x refreeze, `skills/enforce/fixtures/migration/{nominal-1x,mode-undeclared}/` for migration, and `skills/adjust/fixtures/conflict-sources.json` for arbitration. Dry-run before any write.

## Scenarios

| # | Situation (input) | Expected behaviour | Pass criteria |
|---|---|---|---|
| S1 | Apply bounded delta `color.brand.primary: #2563eb → #0044cc` to the utility contract. | Select `arbitrate → freeze` directly; preserve everything outside the declared dependency closure. | Per `actions/02-freeze.md` §En mode re-figeage, output lists the exact changed key and derived artifacts; unrelated token/component entries compare unchanged; no upstream skill is invoked. |
| S2 | Migrate `migration/nominal-1x` after exit 3, with `pre-migration-verdict.json` captured. | Select `migrate`, load the baseline, dry-run, then pause for approval. | Per `actions/03-migrate.md` §Étape 1–3, intended writes remain `[]` before explicit approval; output names baseline exit 0 and the migration report; mode is explicit. |
| S3 | Migrate `migration/mode-undeclared`. | Ask for the mode; never guess. | Intended writes are `[]`; response names the missing mode and does not proceed to migration write. |
| S4 | Freeze with neither mutable draft nor contract-plus-delta. | Stop for missing input. | No contract path is an intended write and no upstream capability is auto-invoked. |
| S5 | Supply `conflict-sources.json`, whose two populated values disagree with no 2-of-3 majority. | Keep arbitration open and block freeze. | Per `actions/01-arbitrate.md` §Étape 4, conversation names `color.brand.primary` and the human checkpoint; `freeze` is not selected and intended writes are `[]`. |
| S6 | Ask to install gates on the frozen fixture. | Do not activate `adjust`. | Selected target is `enforce/wire-gates`; no adjust action or contract mutation is planned. |

## How to run

Agent-as-adjust, dry-run. Record exact fixture, action sequence, approval checkpoint, intended paths and non-selected capabilities.

**Decisive observables:** bounded delta accepted independently; migration never guesses or writes before approval; unresolved arbitration blocks; adjacent enforcement excluded.

## Results log

### 2026-08-12 — run 1 (initial, dry-run, target=adjust, fixture=utility+migration+conflict) — **5 PASS, 1 N/A**

Fixture state: 2.x delta, undeclared-mode and conflict cases populated; nominal 1.x initially lacked an archived baseline.

| # | Behaviour | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|---|
| S1 | bounded delta | PASS | — | `actions/02-freeze.md §En mode re-figeage` |
| S2 | safe migration | N/A | — | pre-migration verdict absent |
| S3 | mode never guessed | PASS | — | `actions/03-migrate.md §Étape 2` |
| S4 | missing input stops | PASS | — | `actions/01-arbitrate.md §Entrées acceptées` |
| S5 | unresolved conflict blocks | PASS | — | `actions/01-arbitrate.md §Étape 4` |
| S6 | enforcement request excluded | PASS | — | `SKILL.md §Transversal rules` |

**Frictions / gaps:** S2 needed an archived pre-2.x verdict.
**Tally:** 5/5 applicable PASS (1 N/A) — fixture gap reproduced.

### 2026-08-12 — run 2 (post-fix, dry-run, target=adjust, fixture=utility+migration+conflict) — **6/6 PASS**

Fixture state: `pre-migration-verdict.json` records exit 0 before migration; real dry-run reports declared BEM and writes nothing.

| # | Behaviour | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|---|
| S1,S3–S6 | unchanged routes/boundaries | PASS | = | citations from run 1 remain applicable |
| S2 | baseline, dry-run, approval stop | PASS | ▲ | `actions/03-migrate.md §Étape 1–3` |

**Frictions / gaps:** none.
**Tally:** 6/6 PASS (0 N/A) — fixture gap closed.

### 2026-08-12 — run 3 (regression, dry-run, target=adjust, fixture=utility+migration+conflict) — **6/6 PASS**

Fixture state: bounded delta, archived baseline, explicit/absent migration modes, and unresolved conflict remain populated.

| # | Behaviour | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|---|
| S1 | bounded delta | PASS | = | `actions/02-freeze.md §En mode re-figeage` |
| S2 | baseline, dry-run, approval stop | PASS | = | `actions/03-migrate.md §Étape 1–3` |
| S3 | mode never guessed | PASS | = | `actions/03-migrate.md §Étape 2` |
| S4 | missing input stops | PASS | = | `actions/01-arbitrate.md §Entrées acceptées` |
| S5 | unresolved conflict blocks | PASS | = | `actions/01-arbitrate.md §Étape 4` |
| S6 | enforcement request excluded | PASS | = | `SKILL.md §Transversal rules` |

**Frictions / gaps:** archived baseline does not enumerate the eventual Step 5 reference-file set; outside this pre-approval scenario.
**Tally:** 6/6 PASS (0 N/A) — no PASS→FAIL regression.
