# Diffuse — Routing autonomy Behavioural Test Scenarios

Behavioural tests for **design:diffuse**. Authority: `SKILL.md` §Routing and §Transversal rules; `actions/00-prototype.md` §Process; `actions/02-render.md` §Étape 0–5; `actions/03-pivot.md` §Étape 2a–2b.

> **Fixture / preconditions.** Prototype input is `plugins/design/fixtures/brief-only/brief.md`. Governed input uses declared `card` in `skills/enforce/fixtures/retrofit/components.json`; candidate baseline outputs are `retrofit-clean.html` and `retrofit-dirty.html`.

## Scenarios

| # | Situation (input) | Expected behaviour | Pass criteria |
|---|---|---|---|
| S1 | Produce one card from the named brief with no contract. | Select `prototype` alone. | Output states `governance: none` and `conformity: not assessed`; no contract path is an intended write and no lifecycle skill is invoked. |
| S2 | Render declared `card` as baseline HTML/CSS candidate `retrofit-clean.html`. | Select `define-element → render`, check freshness and gates, then deliver only the baseline preview. | Per `actions/02-render.md` §Étape 0–5, contract is read-only; gate exit is 0; output is labeled non-integrated and names the later native-promotion path. |
| S3 | Render declared `card` as candidate `retrofit-dirty.html`. | Select `define-element → render`, stop on the blocking gate, and do not hand off or deliver. | Per `actions/02-render.md` §Étape 3, gate exit is 1; delivery and pivot hand-off are absent; response requires correction then re-lint. |
| S4 | Render a component name absent from `retrofit/components.json`. | Refuse invention. | No component, variant, token or preview write is intended; output names the undeclared component. |
| S5 | Ask to audit an existing page without producing a component. | Do not activate `diffuse`. | No diffuse action, component write or preview write is planned. |
| S6 | Render declared `card` natively for installed provider `sc-css`. | Select `pivot`, hand off the render spec, then gate the returned native output before delivery. | Per `actions/03-pivot.md` §Étape 2a–3, hand-off names `sc-css`, component `card` and native target; provider return precedes gate 0 and only then final native delivery; no baseline is called integrated. |
| S7 | Render declared `card` for a WordPress FSE target with sc-php and sc-css installed. | Emit two ordinary render specs, collect non-overlapping platform and stylesheet outputs, then gate them together. | sc-php alone owns the pattern and `fse-bindings.css`; sc-css owns tokens/components/index and later lints the binding; delivery waits for both returns and gate 0. |

## How to run

Agent-as-diffuse, dry-run. Record selected sequence, fixture, gate exit, delivery decision, governance label and intended paths.

**Decisive observables:** autonomous prototype; governed delivery is gate-dependent; baseline is never called integrated; unknown declarations are not invented; audit entry excluded; a compound native target repeats the simple spec and has one producer per output path.

## Results log

### 2026-08-12 — run 1 (initial, dry-run, target=diffuse, fixture=brief+retrofit) — **5/6 PASS**

Fixture state: card declared; clean candidate gates 0; dirty candidate gates 1; sc-css provider installed.

| # | Behaviour | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|---|
| S1 | autonomous prototype | PASS | — | `actions/00-prototype.md §Process` |
| S2 | clean baseline delivery | PASS | — | `actions/02-render.md §Étape 0–5` |
| S3 | dirty candidate not delivered | PASS | — | `actions/02-render.md §Étape 3` |
| S4 | unknown component refused | PASS | — | `SKILL.md §Transversal rules` |
| S5 | audit excluded | PASS | — | `SKILL.md §Routing` |
| S6 | native pivot sequence | FAIL | — | criterion placed provider hand-off after the gate, contrary to `actions/03-pivot.md §Étape 2a–3` |

**Frictions / gaps:** S6 reversed hand-off and final-gate ordering.
**Tally:** 5/6 PASS (0 N/A) — sequencing defect reproduced in the scenario contract.

### 2026-08-12 — run 2 (post-fix, dry-run, target=diffuse, fixture=brief+retrofit) — **6/6 PASS**

Fixture state: unchanged; installed sc-css receives the render spec, returns output, then exit 0 permits native delivery.

| # | Behaviour | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|---|
| S1–S5 | unchanged routes/boundaries | PASS | = | citations from run 1 remain applicable |
| S6 | pivot → provider → gate → delivery | PASS | ▲ | `actions/03-pivot.md §Étape 1–3`; `actions/02-render.md §Étape 3,5` |

**Frictions / gaps:** none.
**Tally:** 6/6 PASS (0 N/A) — ordering corrected and confirmed.

### 2026-08-12 — run 3 (regression, dry-run, target=diffuse, fixture=brief+retrofit) — **6/6 PASS**

Fixture state: card declared; clean gate=0, dirty gate=1, and sc-css provider remains installed.

| # | Behaviour | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|---|
| S1 | autonomous prototype | PASS | = | `actions/00-prototype.md §Output,Process` |
| S2 | clean baseline delivery | PASS | = | `actions/02-render.md §Étape 0–3,5` |
| S3 | dirty candidate not delivered | PASS | = | `actions/02-render.md §Étape 3` |
| S4 | unknown component refused | PASS | = | `actions/01-define-element.md §Entrée` |
| S5 | audit excluded | PASS | = | `SKILL.md §Routing` |
| S6 | pivot → provider → gate → delivery | PASS | = | `actions/03-pivot.md §Étape 1–3`; `02-render.md §Étape 3,5` |

**Frictions / gaps:** no concrete target-app promotion path or returned provider artifact in the dry-run fixture; routing logic remains fully applicable.
**Tally:** 6/6 PASS (0 N/A) — no PASS→FAIL regression.

### 2026-08-14 — run 4 (generality, dry-run, target=diffuse, fixture=brief+retrofit+fse) — **7/7 PASS**

Fixture state: prior fixtures unchanged; FSE target has sc-php and sc-css installed with disjoint output paths.

| # | Behaviour | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|---|
| S1 | autonomous prototype | PASS | = | `actions/00-prototype.md §Output,Process` |
| S2 | clean baseline delivery | PASS | = | `actions/02-render.md §Étape 0–3,5` |
| S3 | dirty candidate not delivered | PASS | = | `actions/02-render.md §Étape 3` |
| S4 | unknown component refused | PASS | = | `actions/01-define-element.md §Entrée` |
| S5 | audit excluded | PASS | = | `SKILL.md §Routing` |
| S6 | single-provider pivot sequence | PASS | = | `actions/03-pivot.md §Étape 1–3` |
| S7 | two simple specs → disjoint returns → one final gate | PASS | ▲ | `actions/03-pivot.md §Étape 1–3`; `references/sc-pivot-contract.md § Cardinalité du spec de rendu` |

**Frictions / gaps:** none.
**Tally:** 7/7 PASS (0 N/A) — mixed FSE routing is explicit without a second composite schema.
