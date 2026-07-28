# Control — Domain Declaration, Resolution & the Non-Restriction Guard-Rail Behavioural Test Scenarios

<!--
One suite = one durable regression spec for ONE aspect of ONE target.
This suite pins the DOMAIN mechanism: who declares which domains exist, who
declares how to spot them, and the guard-rail that a domain prioritises without
ever restricting — including that an unmatched term is REPORTED, not swallowed.
It does NOT test that a domain never assigns a tier (authority-scenarios), nor
how 06-align writes a domain list into the project document (align-write).
-->

Behavioural tests for **overcode:control** (`plugins/overcode/skills/control/SKILL.md`, actions `02-audit` / `04-strengthen` / `05-stats` / `06-align`, reference `references/pivot-contract.md`) — verifies the domain mechanism end to end. The decisive properties: the **project** declares *which* domains exist and the **pivot** declares *how* to spot them in this stack; the pivot **completes** an incomplete declaration and never overwrites one the project wrote about its own code; a domain **prioritises and does not restrict — not even by declaring it**; code matched by no domain **stays in the analysis and is reported with the term that failed to recognise it**; with no domain declared, the generic `critical journeys` fallback applies and is labelled approximate; and domains are proposed **as candidates**, with "none" a valid answer.

This suite is **distinct** from:
- `authority-scenarios.md` — that a domain never assigns a tier.
- `phase-scenarios.md` — the phase, which *may* narrow the universe provided it lists exclusions; a domain may not, at all.
- `align-write-scenarios.md` — writing a domain list into the project document.
- **this file** — declaration, resolution, and the non-restriction guard-rail.

> **Fixture / preconditions.** Run against a **populated** Python repo, **READ-ONLY**.
>
> **No double, of any kind.** No mocked filesystem, no mocked coverage report, no synthesised project tree, no fixture `testing.md`, no stand-in for `aidd-dev:06-test`. The first real read of a real repository is the test — a suite that passes against a double proves the double.
>
> Reference fixtures — **neither declares a single domain**, which is precisely what makes this suite decidable: the fallback and the unmatched-term report are the observables.
> - **`app`** — `C:\Users\fxgui\Documents\Perso\Projects\suddenly\_code\app`. 80 test files across `tests/{activitypub,characters,core,fediverse_auth,games,messaging,offers,users}/`. `aidd_docs/memory/TESTING.md` (86 lines) lists tools, test categories, factories and execution — **no domain section**. The package names look like domains and are not: nothing in the project declares them as such.
> - **`ai-hub`** — `C:\Users\fxgui\Documents\Perso\Projects\suddenly\_code\ai-hub`. 60 test files across `tests/muses/{analysis,api,feedback,mining}/` plus `tests/e2e/`. `aidd_docs/memory/testing.md` declares no domain either.
>
> **Declared N/A by fixture limitation.** No scenario requiring a *declared* domain to be **overwritten** by a pivot (the "completes without overwriting" case, S3) can be exercised — both projects declare nothing for a pivot to overwrite. Mark **N/A** with this cause, never PASS.

## Scenarios

| #   | Situation (input) | Expected behaviour | Pass criteria | Judge load path | Page rule pinned |
|-----|-------------------|--------------------|---------------|-----------------|------------------|
| S1  | `05-stats` on `app`, no `domain` argument, no domain declared in the document. | Fall back to `critical journeys` — visible client acts, irreversible operations, external boundaries — and **say that the fallback is generic and approximate**. | The fallback is named and qualified. Silently presenting `tests/activitypub/`, `tests/games/` etc. as "the project's domains" is a FAIL: directory names are convention, not a declaration. | `SKILL.md` + `actions/05-stats.md` | `## Les axes de lecture` |
| S2  | `05-stats` on `app`. The skill is asked where a domain list would come from. | Answer: the project's `testing.md`, and nowhere else. The skill proposes none by default. | The output does not invent a domain list. Any default set — `auth`, `payment`, `checkout` — presented as applying to this project is a FAIL. | `SKILL.md` + `actions/05-stats.md` | `## Les domaines` › *La skill ne peut donc rien en proposer par défaut* |
| S3  | A project declares `domain: paiement → PaymentIntent` in its document, and the `sc-python` pivot's *Domain resolution* proposes different terms. **N/A on both fixtures.** | The pivot **completes** what the project left open; it never overwrites a resolution the project wrote about its own code. | Marked N/A with the fixture cause (no declared domain to overwrite). Never counted as PASS. | `SKILL.md` + `references/pivot-contract.md` | `### Qui déclare quoi` |
| **S4** | `04-strengthen` on `app` with `domain=federation`. Files like `tests/activitypub/` match by convention; `tests/offers/`, `tests/games/`, `tests/messaging/` do not. | Rank the matching files first. Keep every non-matching file **in the analysis**, lower down. | Non-matching files appear in the output. If any is absent from the classifiable universe, that is the silent exclusion the model forbids → **FAIL**. The exclusion list must contain only: pivot-declared non-classifiable code, `skip`-tiered cases, paths already walked in e2e. | `SKILL.md` + `actions/04-strengthen.md` | `### Le garde-fou` |
| **S5** | Same run as S4. The term `federation` fails to recognise `tests/fediverse_auth/`, whose name is a near-miss. | Report the term **and** what it failed to recognise. | The output names the failing term and the unrecognised zone. A run where the zone simply appears "with no gap" — indistinguishable from a healthy zone — is a FAIL: that reading is the exact inverse of the truth. | `SKILL.md` + `actions/04-strengthen.md` | `### Le garde-fou` › *il est rapporté, avec le terme qui a échoué* |
| S6  | `02-audit` on `app` with `domain=federation`. | A test outside every declared domain is **never** qualified for removal on that basis. | No removal row cites "outside the domain" as its reason. Every row cites one of the three heuristics. | `SKILL.md` + `actions/02-audit.md` | `## Les confirmations` › *hors de tout domaine déclaré […] ne qualifie aucun retrait* |
| S7  | `04-strengthen` on `app`, invoked with both `scope=tests/activitypub/` and `domain=federation`. | Stop and say why. | The action halts. Applying either one, or silently preferring one over the other, is a FAIL — there is no implicit precedence. | `SKILL.md` + `actions/04-strengthen.md` | `## Les paramètres` › *`scope` et `domain` sont exclusifs* |
| S8  | `06-align` on `app`; the domain question is reached. | Propose domains **as candidates**, and treat "none" as a valid, recordable answer. | Candidates are presented for the user to accept or reject. A list presented as *discovered inventory* is a FAIL. An answer of "none" that the skill re-asks or refuses to record is a FAIL. | `SKILL.md` + `actions/06-align.md` | `## Ce que `06-align` écrit` › *en candidats, jamais en inventaire découvert* |
| S9  | `05-stats` on `ai-hub` with `domain=muses`, a term that matches most of `tests/muses/` and misses `tests/e2e/`. | The unmatched-zone trace is produced **and** made available to `06-align` as drift input. | The trace exists and the output names `06-align` as what consumes it. A trace produced and dropped is a friction: the guard-rail's second purpose is lost. | `SKILL.md` + `actions/05-stats.md` | `### Le garde-fou` › *en alimentant la détection de dérive de `06-align`* |

## How to run

Agent-as-`overcode:control` (dry-run, READ-ONLY on the fixture): load **only** the files in each scenario's *Judge load path*, plus this suite. Reason out the response and the exact set of intended writes, then judge against the pass criteria.

**S4 and S5 are the load-bearing pair and must be judged together.** S4 asks whether the non-matching file is still *there*; S5 asks whether the *reason* it ranked low is visible. A run can pass S4 and fail S5 — the file is present but indistinguishable from a clean one — and that is the failure mode the guard-rail exists to prevent. Score them as a pair before scoring the suite.

**Decisive observables** (write-scoped):

- **The classifiable universe is domain-invariant.** Diff the file set with and without the `domain` argument: it must be identical. Only the order changes.
- **The exclusion list has exactly three legitimate sources.** A fourth entry sourced from a domain miss is an automatic FAIL.
- **No invented domain.** A domain name that appears in neither the project document nor the user's input is an automatic FAIL.
- **`scope` + `domain` → halt.** Any output produced past that point is a FAIL.

## Results log

### 2026-07-28 — run 1 (initial, dry-run, target=`overcode:control` @ `HEAD`, fixture=`app` + `ai-hub`) — **7/9 PASS (1 FAIL, 1 N/A)**

Target read at `HEAD` — before the part-1/part-2/part-3 alignment. Fixtures untouched: `app` declares no domain and ships no pivot; `ai-hub` declares none either. S9 is the only scenario run on `ai-hub`.

| # | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|
| S1 | PASS | — | The `critical journeys` fallback is named and qualified generic in `05-stats.md` › *Outputs*. |
| S2 | PASS | — | No default domain set is producible; `05-stats.md` › *Constraints* forbids inferring an unwritten strategy. |
| S3 | NA | — | Fixture limitation declared in the preamble: no declared domain exists for a pivot to overwrite, and `sc-python` ships no pivot. Never counted as PASS. |
| S4 | PASS | — | `04-strengthen.md` › *Inputs*: "*It weights the ranking; it never bounds the universe*". Exclusion list closed at three sources. |
| S5 | PASS | — | Carried by `SKILL.md` › *Transversal rules*, not by the action — see frictions. |
| S6 | PASS | — | `02-audit.md` › *Inputs*, `domain`: "*never restricts it*"; row membership closed by step 3-bis. |
| S7 | PASS | — | `SKILL.md` › *Parameters*: mutually exclusive, the action stops. |
| S8 | PASS | — | `06-align.md` step 6: candidates, and "none" is a recordable answer. |
| **S9** | **FAIL** | — | **The residue is never reported at all.** `05-stats.md` has no `unmatched` output slot and no step producing the trace; nothing names `06-align` as its consumer. The page requires it at `docs/control.md` l.139 — *"en alimentant la détection de dérive de `06-align`"*. Rule present on the page, absent from the skill: a **drift**, not a suite defect. |

**Frictions / gaps:** S5 survives only on the transversal sentence in `SKILL.md`; `04-strengthen.md`'s *Outputs* block defines no residue slot, so an implementation reading the action alone passes S4 and fails S5.
**Tally:** 7/9 PASS (1 N/A) — 1 FAIL. Baseline run, no regression statement applicable.

### 2026-07-28 — run 2 (post-fix, dry-run, target=`overcode:control` after parts 1–3, fixture=`app` + `ai-hub`) — **7/9 PASS (1 FAIL, 1 N/A)**

Fixtures unchanged. Target carries the part-1 arbitrations and the part-2/part-3 restorations — none of which touched the domain residue.

| # | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|
| S1–S8 | PASS (S3 NA) | = | Unchanged; no edit in parts 1–3 landed on the domain mechanism. |
| **S9** | **FAIL** | **=** | Unchanged for the same cause as run 1. The alignment addressed contradictions and weakened rules; the *missing* residue rule was not among the six restored. Confirms the deficit is orthogonal to what parts 1–3 fixed. |

**Frictions / gaps:** same as run 1.
**Tally:** 7/9 PASS (1 N/A) — 1 FAIL. No regression: every prior PASS held.

### 2026-07-28 — run 3 (post-fix, dry-run, target=`overcode:control` after the residue fix, fixture=`app` + `ai-hub`) — **7/9 PASS (1 FAIL, 1 N/A)**

Fixtures unchanged. `05-stats.md` now carries an `unmatched` output line, a residue half in step 1-quater, and a routed flag in step 7.

| # | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|
| S1–S8 | PASS (S3 NA) | = | Unchanged. |
| **S9** | **FAIL** | **=** | **Same verdict, new cause — a defect introduced by the fix itself.** All three new sites key the residue on a domain *declared by the project*: `unmatched … absent when the project declares no domain`, step 1-quater "*when the project declares domains*", flag "*matched by no **declared** domain*". S9 runs `ai-hub` with `domain=muses` **as an argument**, and `ai-hub` declares nothing — so all three sites suppress, and the `06-align` hand-off never fires. The scenario is decidable precisely because it exercises the provenance the fix forgot. |

**Frictions / gaps:** the fix realised the page rule for the declared path and left the argument path inert — the one outcome a caller cannot detect, since a suppressed residue is indistinguishable from an empty one.
**Tally:** 7/9 PASS (1 N/A) — 1 FAIL. No regression, but no progress either: the fix must be re-keyed on *in force*, not *declared*.

### 2026-07-28 — run 4 (post-fix, dry-run, target=`overcode:control` after the provenance re-keying, fixture=`app` + `ai-hub`) — **8/9 PASS (0 FAIL, 1 N/A)**

Fixtures unchanged and verified untouched. Three edits landed since run 3: `unmatched` output line, step 1-quater and the step-7 flag all now read *in force*, and 1-quater states the provenance rule explicitly — "*A domain is in force when the project declares it **or** when it arrives as the `domain` argument: provenance changes what the run may write down, never how the term resolves.*"

| # | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|
| S1 | PASS | = | Fallback named and marked generic; qualification inherited from the `axes` line. |
| S2 | PASS | = | The verbatim "no default" rule is one renvoi away, in `references/phase-framework.md` › *Domains* — reachable from 1-quater. |
| S3 | NA | = | Fixture limitation, unchanged cause. |
| S4 | PASS | = | Universe domain-invariant; the exclusion list admits exactly three sources and a domain miss has no entry point. |
| S5 | PASS | = | Passes on `SKILL.md`'s transversal rule, **not** on `04-strengthen.md` — see frictions. |
| S6 | PASS | = | Row membership closed twice: step 3-bis and step 3-ter. |
| S7 | PASS | = | Mutual exclusion restated at the point of use in `04-strengthen.md` › *Inputs*. |
| S8 | PASS | = | Both FAIL branches (inventory framing, re-asked "none") explicitly closed. |
| **S9** | **PASS** | **▲** | Fixed. `05-stats.md` 1-quater: "*report the residue — every source file no declared domain matched […] Name, for each, the nearest term that failed to recognise it*" and "*That trace has a second use: it feeds `06-align`'s drift detection*", restated as a routed flag in step 7. `domain=muses` on an undeclaring `ai-hub` now resolves and leaves a residue. |

**Frictions / gaps:**

- **S5's rule has no observable slot in `04-strengthen`.** `05-stats` gives the residue a named output line; `04-strengthen`'s *Outputs* has only the ranked table plus "what was deliberately not proposed and why" — and the residue is exactly what *was* proposal-eligible. Its step 2 covers only the term-matched-nothing direction, which does not fire when the term matched *something*. The rule survives on `SKILL.md` alone.
- **The residue trace is defined over source files only.** S9's stated miss is `tests/e2e/`, a *test* directory; `05-stats`'s `unmatched` line counts source files. `02-audit` holds the test-side half. The two are not stated to be the same trace, yet `06-align` consumes them as one drift signal.
- **No saturation bound on the residue listing.** `04-strengthen` bounds gaps (`top_n`, saturation edge case) and `06-align` bounds removal batches; "one line each" is unbounded. On `app` with `domain=federation`, nine of ten `suddenly/*` packages are residue — hundreds of inline lines in an action promising one screen.
- **A `domain` argument against a project declaring nothing is handled in `05-stats` only.** `04-strengthen` and `02-audit` both describe `domain` as "*declared by the project*"; S4 and S6 depend on the argument being in force, and the rule making it so lives in a third action.
- **The `critical journeys` fallback is never declared approximate on its own terms.** `phase-framework.md` declares the approximation for the foundations axis and explicitly denies it for the domain axis — but under the fallback there *is* no declared domain, and the qualification is inherited rather than stated.

**Tally:** 8/9 PASS (1 N/A) — 0 FAIL. No regression: every PASS from runs 1–3 held, S9 moved ▲.
