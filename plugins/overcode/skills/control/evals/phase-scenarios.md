# Control — Phase Resolution, Provenance & Switch Behavioural Test Scenarios

<!--
One suite = one durable regression spec for ONE aspect of ONE target.
This suite pins HOW A PHASE IS OBTAINED, REPORTED AND SWITCHED: never inferred,
asked before anything is classified, reported on two axes, and the one forced
pairing. It also pins what a phase may and may not bound.
It does NOT test that the phase avoids assigning tiers (authority-scenarios),
nor what 06-align writes once a phase is declared (align-write-scenarios).
-->

Behavioural tests for **overcode:control** (`plugins/overcode/skills/control/SKILL.md`, actions `03-configure` / `04-strengthen` / `05-stats` / `06-align`, reference `references/phase-framework.md`) — verifies how the phase enters the model and what it is allowed to bound. The decisive properties: the phase is **never inferred**; the question is asked **before** anything is classified or proposed; value and provenance are reported as **two lines that never merge**; `unanswered` ⇔ `undetermined` is the **only** forced pairing; `default` does not re-ask, `undetermined` does; `undetermined` **switches as soon as a phase is declared**; a phase argument governs the current run only and is never written; a divergence between argument and declaration is reported; no phase carries a numeric coverage threshold; a phase that narrows the analysed universe **lists what it excluded**; and no phase changes what a coverage datum *means*.

This suite is **distinct** from:
- `authority-scenarios.md` — that a phase never assigns a tier.
- `align-write-scenarios.md` — how `06-align` turns a spoken answer into a written declaration.
- `confirmations-scenarios.md` — the phase-switch batch and its four required components.
- **this file** — where the phase value comes from, how it is reported, and what it may bound.

> **Fixture / preconditions.** Run against a **populated** Python repo, **READ-ONLY**.
>
> **No double, of any kind.** No mocked filesystem, no mocked coverage report, no synthesised project tree, no fixture `testing.md`, no stand-in for `aidd-dev:06-test`. The first real read of a real repository is the test — a suite that passes against a double proves the double.
>
> Reference fixtures:
> - **`app`** — `C:\Users\fxgui\Documents\Perso\Projects\suddenly\_code\app`. 80 test files; `.coverage` present; strategy document at `aidd_docs/memory/TESTING.md` (86 lines, non-conventional uppercase path) declaring a **coverage threshold of 80 %**. **No phase declared anywhere in `aidd_docs/`.**
> - **`ai-hub`** — `C:\Users\fxgui\Documents\Perso\Projects\suddenly\_code\ai-hub`. 60 test files; `tests/e2e/`; **no coverage report**. `aidd_docs/memory/testing.md` (15 lines) declares "None configured yet" — contradicted by the repo. **No phase declared.**
>
> **Declared N/A by fixture limitation.** Neither fixture carries a *previously declared* phase, so a switch **between two declared phases** (e.g. `hardening` → `sustaining`) cannot be exercised — mark **N/A** with this cause. The switch **out of `undetermined`** *is* exercisable, because both fixtures start with no phase at all: an unanswered question yields `undetermined`, and a subsequent declaration is the switch under test (S6).

## Scenarios

| #   | Situation (input) | Expected behaviour | Pass criteria | Judge load path | Page rule pinned |
|-----|-------------------|--------------------|---------------|-----------------|------------------|
| S1  | `05-stats` on `app` with no `phase` argument. `app` has 80 test files, an active runner, and a filled — but non-decisional — strategy document. | Ask the phase. Do **not** infer it from repo maturity, commit recency, test count, or the presence of a production-looking stack. | The output contains a question to the user, not a phase value the skill picked. Any sentence of the form "this looks like production" is an automatic FAIL. | `SKILL.md` + `actions/05-stats.md` + `references/phase-framework.md` | `## La phase` › *jamais déduite* |
| S2  | `04-strengthen` on `app`, no `phase` argument, user has not yet answered. | Ask **before** producing any ranking. | No ranked table, no tier assignment and no proposed test appears ahead of the question. A run that classifies first and asks afterwards is a FAIL even if the question is eventually asked. | `SKILL.md` + `actions/04-strengthen.md` + `references/phase-framework.md` | `## La phase` › *avant que quoi que ce soit ne soit classé ou proposé* |
| S3  | `05-stats` on `app` with `phase=hardening` passed as an argument. | Report **two** lines: value `hardening`, provenance `argument`. | Two distinct lines exist. A single fused line ("phase: hardening (from argument)") counted as one axis is a FAIL — the two axes must be separately readable. | `SKILL.md` + `actions/05-stats.md` + `references/phase-framework.md` | `### Valeur et provenance sont deux axes` |
| S4  | `05-stats` on `ai-hub`; the phase question is asked and the user does not answer. | Value `undetermined`, provenance `unanswered`. | The pair is exactly `undetermined` / `unanswered`. Any other value paired with `unanswered`, or `undetermined` paired with any other provenance, is a FAIL. | `SKILL.md` + `actions/05-stats.md` + `references/phase-framework.md` | `### Valeur et provenance` › *un seul appariement est forcé* |
| S5  | Two runs of `05-stats` on `ai-hub`: (a) user answers `default` out loud; (b) `default` is written into `testing.md`. | (a) provenance `answered` → a handoff to `06-align` is raised, as for any spoken answer. (b) provenance `declared <path>` → **no** handoff. | The two runs differ in exactly that respect. Treating a spoken `default` as settled — no handoff raised — is a FAIL: unwritten, it will be re-asked next run. | `SKILL.md` + `actions/05-stats.md` + `references/phase-framework.md` | `### Valeur et provenance` › *un `default` déclaré ne déclenche aucun renvoi* |
| **S6 (D2)** | `06-align` on `ai-hub`. The prior run resolved `undetermined` / `unanswered`; the user now declares `sustaining`. | Apply the phase switch: qualify a batch of newly obsolete tests under the switch rules. `undetermined` is **not** exempt. | The switch machinery fires. An instruction stating that `undetermined` takes part in **no** switch is the defect → **FAIL**, citing `actions/06-align.md`. | `SKILL.md` + `actions/06-align.md` + `references/phase-framework.md` | `### default et undetermined` › *s'applique dès qu'une phase est déclarée* |
| S7  | `06-align` on `ai-hub` where the user declares `default`. | Raise **no** switch batch. | No obsolete-test batch is produced. The stated reason is **consent** — the project has just made a decision — not "the machinery does not apply to `default`". A correct behaviour justified by the wrong motive is recorded as a friction, not a PASS. | `SKILL.md` + `actions/06-align.md` | `### default et undetermined` › *par consentement, non par mécanique* |
| S8  | `04-strengthen` on `app` with `phase=production` passed as an argument. | Use it for this run only. | Intended writes to `aidd_docs/memory/TESTING.md`: **none**. The phase argument is never persisted by any action other than `06-align`, and only after validation. | `SKILL.md` + `actions/04-strengthen.md` | `## Les paramètres` › *`phase` en argument ne vaut que pour l'exécution en cours* |
| S9  | `05-stats` on a repo whose document declares `hardening` while the run passes `phase=sustaining`. **N/A on both fixtures** — neither declares a phase. | Report the divergence; the argument wins for this run only. | Marked N/A with the fixture cause. Never counted as PASS. | `SKILL.md` + `actions/05-stats.md` + `references/phase-framework.md` | `### Valeur et provenance` › *la divergence est rapportée et l'argument l'emporte* |
| S10 | `04-strengthen` on `app` with `phase=production`. `app` declares an 80 % coverage threshold in its document. | Weight and order. Set **no** numeric coverage target of its own, and do not adopt the project's 80 % as one. | No phase-indexed threshold appears anywhere in the output. No proposed test is justified by "to reach 80 %". | `SKILL.md` + `actions/04-strengthen.md` + `references/phase-framework.md` | `## La densité, pas le compte` › *ne fixe jamais de seuil chiffré par phase* |
| **S11 (D5 bis)** | `04-strengthen` on `app` with `phase=scaffolding`, where the phase narrows the analysed universe. | Narrow if the model calls for it — and **list every excluded file with the phase motive that excluded it**. | An explicit exclusion table exists, with a count. A narrowing with no list is a **silent** restriction → **FAIL**, citing `actions/05-stats.md` / `references/phase-framework.md` for the missing table. **If the run narrows nothing at all**, the rule does not bind: mark **N/A** with that cause — it forbids silent restriction, not restriction. | `SKILL.md` + `actions/04-strengthen.md` + `actions/05-stats.md` + `references/phase-framework.md` | `### Borner en le disant` |
| S12 | `04-strengthen` on `app` (coverage report present) with `phase=scaffolding`, then with `phase=sustaining`. A module is present in the source glob and **absent from `.coverage`**. | Read it as **not covered** in both runs. Only the rank changes. | The "not covered" reading is identical across the two phases. A run in which the absence means something else — "expected at this stage", "ignore" — is a FAIL. Ranking differences are expected and are not a FAIL. | `SKILL.md` + `actions/04-strengthen.md` + `references/phase-framework.md` | `### Ce que la phase ne décide pas` |
| S13 | `03-configure` on `app`, invoked with `phase=production`, `domain=federation` and `scope=tests/`. | Take none of the three. Say so rather than silently ignoring them. | The action reports that these parameters do not apply to it, and its checks are unchanged by them. Silently accepting and ignoring them is a friction; changing behaviour because of them is a FAIL. | `SKILL.md` + `actions/03-configure.md` | `## Le chaînage` › *`03-configure` est hors modèle* |

## How to run

Agent-as-`overcode:control` (dry-run, READ-ONLY on the fixture): for each scenario, load **only** the files in its *Judge load path*, plus this suite. Reason out the response and the exact set of intended writes, then judge against the pass criteria.

**Two-run scenarios (S5, S12) are judged on the Δ, not on either run alone.** Score the pair: what must differ, and what must not. A suite that judges S12's two runs independently will pass both while missing the defect it exists to catch.

**Decisive observables** (write-scoped):

- **No phase value the user did not supply.** Any inferred phase is an automatic FAIL.
- **Two lines, always.** Value and provenance never appear fused.
- **Intended writes to the project document = ∅** for every action except `06-align`, and for `06-align` only after validation.
- **A narrowed universe always ships its exclusion list.** A count without the list, or a list without the motive, is a FAIL.

## Results log

<!-- append run results here per behave/references/harness-conventions.md › Results log format -->

### 2026-07-28 — run 1 (initial, dry-run, target=`control`@HEAD, fixture=app+ai-hub) — **8/13 PASS, 3 FAIL, 2 N/A**

Pre-alignment state of the skill, materialised read-only from `HEAD` (`git archive`); both fixtures untouched.

| # | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|
| S1 | PASS | — | `references/phase-framework.md` › *Resolution order* — the phase is never deduced; the question is asked and awaited. |
| S2 | PASS | — | The question precedes any ranking: a table produced first and re-sorted after was already read in the wrong order. |
| S3 | PASS | — | `value` and `provenance` are two lines and never collapse into one. |
| S4 | PASS | — | The one forced pairing: `unanswered` ⇔ `undetermined`. |
| S5 | PASS | — | Scored PASS at HEAD. Corrected to N/A at run 3 — the fixture cannot supply a *declared* `default`, and the preamble bans planting one. |
| S6 (D2) | **FAIL** | — | Does `undetermined` take part in a phase switch? At HEAD nothing settles it, and the plausible reading ("neutral previous value, so zero balance") is the wrong one. **This is the D2 arbitration part-1 settled.** |
| S7 | **FAIL** | — | `default` stays out of the switch, but at HEAD for no stated motive — and the wrong motive ("the machinery cannot run") is exactly what a reader supplies. |
| S8 | PASS | — | `phase` given as an argument overrides for this run only and is written nowhere. |
| S9 | **N/A** | — | Neither fixture declares a phase, so argument-vs-declaration divergence cannot arise. Fixture cause. |
| S10 | PASS | — | No per-phase numeric threshold anywhere; the weighting table carries words, not numbers. |
| S11 (D5 bis) | **N/A** | — | The run narrows nothing, so the scenario's own escape clause fires. See run 3 — this N/A hides a real structural gap. |
| S12 | PASS | — | Absence from the coverage report reads as *uncovered* in every phase; what changes is the rank, never the reading. |
| S13 | **FAIL** | — | `03-configure` given a `phase`. At HEAD the action declares it takes none, and says nothing about what happens if one arrives — so the parameter is silently dropped and the caller cannot tell. |

**Frictions / gaps:**
- S6 and S7 are the same missing sentence seen from both ends: the switch machinery never says what a *neutral* prior value does to it. One neutral value participates, the other does not, and at HEAD neither is stated.

**Tally:** 8/13 PASS (2 N/A) — 3 FAIL. No prior run.

### 2026-07-28 — run 2 (post-fix, dry-run, target=`control`@worktree parts 1–3, fixture=app+ai-hub) — **10/13 PASS, 1 FAIL, 2 N/A**

| # | Verdict | Δ vs prior | Note |
|---|---|---|---|
| S6 (D2) | PASS | **▲** | `actions/06-align.md` step 10 now carries the `undetermined` carve-out, backed twice in `phase-framework.md`. D2 confirmed by the Δ. |
| S7 | PASS | **▲** | `default` stays out **by consent, not by mechanics** — the motive is now written, and the wrong one explicitly rejected. |
| S13 | **FAIL** | = | Still open: nothing says what `03-configure` does with a parameter it does not take. |
| all others | PASS / N/A | = (×10) | Unchanged, including the two N/A. |

**Tally:** 10/13 PASS (2 N/A) — 1 FAIL, no PASS→FAIL.

### 2026-07-28 — run 3 (post-fix, dry-run, target=`control`@worktree + phase-3 residual fixes, fixture=app+ai-hub) — **10/13 PASS, 0 FAIL, 3 N/A**

| # | Verdict | Δ vs prior | Note |
|---|---|---|---|
| S13 | PASS | **▲** | `actions/03-configure.md` › *Inputs* now states it: **run, and say in the output that the parameter was ignored, and why.** The same paragraph distinguishes this from the `scope`+`domain` case, where the run *does* stop — there two exclusive intents were expressed, here one intent was expressed that this action simply does not have. |
| S5 | **N/A** | **▼** | Re-scored, not regressed. Run (b) needs `ai-hub` to *declare* `default`; the real file declares no phase and the preamble bans a fixture double. The governing instruction is present and unambiguous (`05-stats.md` step 7: *what silences this flag is the provenance, not the value*), but a rule the fixture cannot exercise is not a PASS. Same ground on which the suite already marks S9 N/A. |
| all others | PASS / N/A | = (×11) | Unchanged. |

**Frictions / gaps:**
- **Target — `06-align.md` step 10 contradicts itself on the S6 case.** Its opening says *"a project whose document declares nothing is not switching, it is declaring for the first time"*, which disqualifies the very switch the `undetermined` bullet twelve lines below mandates. S6 passes on the specific carve-out, backed twice in `phase-framework.md`, but a reader going top-down stops at the general sentence. **Open — needs the general sentence to except a prior `undetermined`.**
- **Target — *Bounding by saying so* is realised in one output template out of five.** The phase is granted power over *which files enter the reading of the coverage report*, and every set-aside file must be listed with its motive — but only `05-stats.md` carries an `excluded:` field. `04-strengthen` explicitly says the phase "changes no exclusion"; `06-align`'s PHASE block copies four lines and not that one. The granted power is unreachable in the ranking action. **Open — this is D5-bis, and S11's escape clause hides it.**
- **Suite — S11 cannot fail on any fixture.** Its escape clause is satisfied unconditionally, because `04-strengthen` is instructed never to narrow by phase. A regression spec whose failure branch is unreachable pins nothing. Rewrite it against `05-stats`, the one action holding the field, or make it assert the field's *absence* elsewhere as the defect.
- **Suite — the *Page rule pinned* column cites headings the judge may never load.** Every entry points at a French heading that exists only in `docs/control.md`, which the load path forbids. Unverifiable from inside the run, and an invitation to the contamination the harness exists to prevent. Mirror the headings into the skill files or drop the column.
- **Suite — fixture counts are stale.** `app` carries 145 `test_*.py`, not 80; `ai-hub` 50, not 60. Every other stated property verified. No verdict turns on it; the preamble should carry orders of magnitude rather than exact counts, which drift with the real projects.

**Tally:** 10/13 PASS (3 N/A) — 0 FAIL. No PASS→FAIL across the three runs. Two target defects and three suite defects recorded above remain open, none of them scored by a failing scenario.
