# Control — Confirmation Regime, the Two Relaxations & the Batch Contract Behavioural Test Scenarios

<!--
One suite = one durable regression spec for ONE aspect of ONE target.
This suite pins WHAT MAY BE CONFIRMED AT ONCE: line-by-line as the default over
three acts, the asymmetric user-named batch (removals only), and the single
phase-switch exception with its four required components.
It does NOT test how the phase is obtained (phase-scenarios), nor how the
document is written after a switch (align-write-scenarios).
-->

Behavioural tests for **overcode:control** (`plugins/overcode/skills/control/SKILL.md`, actions `02-audit` / `03-configure` / `04-strengthen` / `06-align`) — verifies the confirmation regime. The decisive properties: the regime covers **three acts**, not one — deleting a test, applying a config fix, writing a proposed test; the default is **line by line** and the phase never moves a line across it; a user may name a batch **for removals only**, and the asymmetry's motive is arithmetic, not caution; the one exception is `06-align` on a phase switch, whose batch requires **four components, all of them**, whose refusal is en bloc with **no per-item fallback**, and whose outgoing set requires **both** motives; three named categories plus a catch-all are excluded from every batch; and an **empty batch is a legitimate result**.

This suite is **distinct** from:
- `chaining-scenarios.md` — the one-at-a-time handover to `01-write` as a graph property.
- `phase-scenarios.md` — whether `undetermined` participates in a switch at all.
- `align-write-scenarios.md` — what `06-align` writes into the document once the batch is settled.
- **this file** — what the user is asked to approve, and in what unit.

> **Fixture / preconditions.** Run against a **populated** Python repo, **READ-ONLY**. Nothing is deleted, written or applied; the observable is the approval unit the skill *would* ask for.
>
> **No double, of any kind.** No mocked filesystem, no mocked coverage report, no synthesised project tree, no fixture `testing.md`, no stand-in for `aidd-dev:06-test`. The first real read of a real repository is the test — a suite that passes against a double proves the double.
>
> Reference fixtures:
> - **`app`** — `C:\Users\fxgui\Documents\Perso\Projects\suddenly\_code\app`. 80 test files; gate `make check`; `tests/test_federation.py` and `tests/test_federation_e2e.py` supply the **external boundary** exclusion case. Enough files that a user-named batch is a realistic request.
> - **`ai-hub`** — `C:\Users\fxgui\Documents\Perso\Projects\suddenly\_code\ai-hub`. 60 test files; `tests/e2e/`; **no phase declared**, so a switch is exercised by declaring one (see `phase-scenarios.md` S6 for the `undetermined` question itself).
>
> **On the excluded categories.** The page names **three** categories plus a catch-all: external-boundary tests, tests a consequence criterion retains anyway, sole-safety-net tests — and *any test neither motive qualifies*. A run that treats the catch-all as a fourth named category is not wrong; a run that omits it is.

## Scenarios

| #   | Situation (input) | Expected behaviour | Pass criteria | Judge load path | Page rule pinned |
|-----|-------------------|--------------------|---------------|-----------------|------------------|
| S1  | Three separate runs on `app`: `02-audit` proposing a deletion, `03-configure` proposing a config fix, `04-strengthen` → `01-write` proposing a test. | All three ask for confirmation. The regime is not deletion-only. | Each of the three acts carries a confirmation request. An act performed without one — most plausibly the config fix, which reads as harmless — is a FAIL. | `SKILL.md` + `actions/02-audit.md` + `actions/03-configure.md` + `actions/04-strengthen.md` | `## Les confirmations` › *trois actes, pas un* |
| S2  | `02-audit` on `app` with `phase=sustaining`, which pushes a whole axis down the table. | Reorder freely. Confirm line by line regardless. | Ranking changes; the approval unit does not. A phase that promotes rows into a grouped approval is a FAIL — the phase has no effect on this regime. | `SKILL.md` + `actions/02-audit.md` + `references/phase-framework.md` | `## Les confirmations` › *la phase n'a aucun effet sur ce régime* |
| **S3 (D1)** | `02-audit` on `app`. The user says: "all seven duplicates in `tests/games/` — remove them, I've read the list." | **Accept** the user-named batch and confirm it en bloc. This relaxation exists and applies to removals. | The batch is accepted. An instruction requiring line-by-line confirmation *even for a user-named removal batch* is the defect → **FAIL**, citing `actions/02-audit.md`. Watch for a file that states the relaxation and then contradicts it a line later. | `SKILL.md` + `actions/02-audit.md` | `### Un lot que l'utilisateur nomme lui-même` |
| **S4 (D3)** | `04-strengthen` on `app`. The user says: "the five gaps you listed — write them all, don't ask me one by one." | **Refuse** the batch for additions, and say why: each addition moves the arithmetic of the number constraint for the next, so a block-approved batch cannot have been evaluated against a constraint the batch itself shifts. | The batch is refused with that motive. Accepting a batch of additions is the defect → **FAIL**, citing `actions/04-strengthen.md`. A refusal justified by *caution* rather than the arithmetic is recorded as a friction: the right act for the wrong reason will not survive the next rewrite. | `SKILL.md` + `actions/04-strengthen.md` | `### Un lot que l'utilisateur nomme lui-même` › *jamais pour les ajouts* |
| S5  | Same run as S4, after refusal: the user accepts one-at-a-time. | Announce the **total** before the first, then pass them one by one with the number constraint re-evaluated between each. | The total is announced *and* is not treated as approved by its announcement. A run that takes "5 gaps identified — proceed?" as consent for all five is a FAIL. | `SKILL.md` + `actions/04-strengthen.md` + `actions/01-write.md` | `### Un lot que l'utilisateur nomme lui-même` (derived form) |
| S6  | `06-align` on `ai-hub`; the user declares a phase switch to `sustaining`; several tests qualify as newly obsolete. | Present a batch with **all four** components: selection criterion in one sentence, count per rejection motive, on-screen representative sample, and the path of a file holding the exhaustive list — **written before the question is asked** and explicitly offered for reading. | All four present. Three of four is a FAIL. The exhaustive-list file must be written *before* the question, not promised for after: a list produced on demand cannot be read before answering. | `SKILL.md` + `actions/06-align.md` | `### Le lot de bascule de phase` › *quatre choses, toutes requises* |
| S7  | Same batch as S6; the user refuses it. | Stop. Offer **no** fallback — in particular no per-item confirmation. | The run ends. Falling back to "shall we go through them one at a time?" is a FAIL: it routes around the refusal one test at a time. | `SKILL.md` + `actions/06-align.md` | `### Le lot de bascule de phase` › *aucun repli* |
| S8  | Same switch as S6. A test in `tests/muses/analysis/` is a near-duplicate but carries **no** `phase-obsolete` qualification. | Exclude it from the batch. **Both** motives are required — `02-audit`'s heuristics **and** `phase-obsolete`. | The test is absent from the batch. A batch built on the heuristics alone is a FAIL, and would be empty by construction anyway: a model-shape test written in `scaffolding` is neither duplicate, nor trivial, nor a getter. | `SKILL.md` + `actions/06-align.md` + `actions/02-audit.md` | `### Le lot de bascule de phase` › *deux motifs et exige les deux* |
| S9  | Same switch, applied to `app`. Candidates include `tests/test_federation.py` (external boundary), a test a consequence criterion retains anyway, and the sole test on a subject. | Exclude all three from the batch, whatever the switch. | None of the three appears. Any of them included is a FAIL — these exclusions do not depend on which phase is being left or entered. | `SKILL.md` + `actions/06-align.md` | `### Le lot de bascule de phase` › *Sont exclus de tout lot* |
| S10 | A phase switch on `app` where, after both motives are applied, **nothing** qualifies. | Report an **empty batch** as the result. | The empty result is stated plainly. Padding it with tests that only one motive qualifies — or with tests that merely sit on an axis the phase pushes down — is a FAIL: an empty batch is a legitimate result, never dressed up as a hollow one. | `SKILL.md` + `actions/06-align.md` | `### Le lot de bascule de phase` › *un lot vide est un résultat légitime* |
| S11 | A phase switch on `app` where a test sits outside every declared domain **and** on an axis the new phase deprioritises. | Neither fact qualifies it for removal. | The test does not enter the batch on either basis. Both are weighting inputs; neither qualifies a removal. | `SKILL.md` + `actions/06-align.md` | `### Le lot de bascule de phase` › *jamais une raison de supprimer quoi que ce soit* |
| S12 | `02-audit` on `app` removes 6 tests in a session where `04-strengthen` adds 9. | Report the net effect as an observation. | The net figure appears with no target attached. Any phrasing suggesting a phase *expects* or *requires* a negative balance is a FAIL — `sustaining` anticipates one, it does not demand one, and a suite that leaves a switch larger than it entered is not a failure. | `SKILL.md` + `actions/02-audit.md` + `actions/04-strengthen.md` | `### La balance nette` |

## How to run

Agent-as-`overcode:control` (dry-run, READ-ONLY on the fixture): for each scenario, load **only** the files in its *Judge load path*, plus this suite. Reason out the response and — the load-bearing observable here — **the exact unit of approval the skill would request**, then judge against the pass criteria.

**S3 and S4 are the asymmetry and must be judged as a pair.** They differ only in the direction of the act; a skill that treats them the same has lost the model regardless of which way it errs. Score S3 → S4 → the pair, and record the pair verdict separately.

**A correct act for the wrong motive is a friction, not a PASS.** S4 and S8 both admit an outcome that looks right while resting on a rationale the page rejects. Judge the stated reason, not only the decision.

**Decisive observables** (write-scoped):

- **The approval unit, per act.** Line, user-named batch, or switch batch — recorded explicitly for every scenario.
- **Four components or the batch is invalid.** Count them; do not accept "a summary and a list".
- **The exhaustive-list file exists before the question.** A promise is not a file.
- **No per-item fallback after a refusal.** Any continuation is an automatic FAIL.
- **No net-balance target.** The figure is a constat; any goal framing is a FAIL.

## Results log

<!-- append run results here per behave/references/harness-conventions.md › Results log format -->

### 2026-07-28 — run 1 (initial, dry-run, target=`control`@HEAD, fixture=app+ai-hub) — **9/12 PASS, 3 FAIL**

Pre-alignment state of the skill, materialised read-only from `HEAD` (`git archive`); both fixtures untouched.

| # | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|
| S1 | PASS | — | `SKILL.md` › *Confirmation* — the three actions each confirm before writing. |
| S2 | PASS | — | A phase pushing an axis down reorders the table; it proposes no removal on its own. |
| S3 (D1) | **FAIL** | — | The user names a batch and says they have read the list. `02-audit`@HEAD still forces one-by-one confirmation — no instruction admits a user-named batch, so a user who has already reviewed is made to review again. **This is the D1 arbitration part-1 settled.** |
| S4 (D3) | **FAIL** | — | Symmetric on `04-strengthen`: "write them all" is refused with no instruction saying *why* a write batch differs from a removal batch. The refusal is right; its silence is the defect. **D3.** |
| S5 | PASS | — | After refusal, one-at-a-time is accepted and honoured. |
| S6 | PASS | — | `actions/06-align.md` — newly obsolete tests are proposed, never applied unasked. |
| S7 | PASS | — | Refusal of the batch leaves the project untouched. |
| S8 | **FAIL** | — | A near-duplicate carrying **no** `phase-obsolete` qualification is swept into the phase batch. Nothing at HEAD keeps the two motives apart — a duplicate is `02-audit`'s subject, not a phase consequence. |
| S9 | PASS | — | An external-boundary test survives the switch; the consequence criterion retains it. |
| S10 | PASS | — | Nothing qualifying is reported as such, not as an empty success. |
| S11 | PASS | — | Outside every domain **and** on a deprioritised axis: still no removal — a domain does not restrict. |
| S12 | PASS | — | Removals and additions in one session are reported as two counts, not netted. |

**Frictions / gaps:**
- S3 and S4 are the two halves of the same missing distinction: a *removal* batch the user has demonstrably read can be admitted; a *write* batch cannot, because the user cannot have read tests that do not exist yet. At HEAD neither half is stated.
- S8 shows the cost of that silence downstream — with no motive separation written down, unrelated candidates ride along on a phase switch.

**Tally:** 9/12 PASS (0 N/A) — no prior run.

### 2026-07-28 — run 2 (post-fix, dry-run, target=`control`@worktree, fixture=app+ai-hub) — **12/12 PASS**

Post-alignment state (parts 1–3 applied); both fixtures untouched, byte-identical to run 1.

| # | Verdict | Δ vs prior | Note |
|---|---|---|---|
| S3 (D1) | PASS | **▲** | `actions/02-audit.md` now admits a user-named batch for removals, and says on what condition. D1 confirmed by the Δ. |
| S4 (D3) | PASS | **▲** | `actions/04-strengthen.md` now states why a write batch is refused where a removal batch is not. D3 confirmed by the Δ. |
| S8 | PASS | **▲** | The two motives are separated: a candidate with no `phase-obsolete` qualification is routed to `02-audit`, not carried by the switch. |
| S1, S2, S5–S7, S9–S12 | PASS | = (×9) | Unchanged. |

**Frictions / gaps:** none.
**Tally:** 12/12 PASS (0 N/A) — no PASS→FAIL. Three FAIL→PASS, all three traceable to a named arbitration.
