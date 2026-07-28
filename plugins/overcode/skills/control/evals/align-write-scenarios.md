# Control — Project Document Ownership, Gap Natures & Write Discipline Behavioural Test Scenarios

<!--
One suite = one durable regression spec for ONE aspect of ONE target.
This suite pins THE ONE ACTION THAT WRITES: who owns the project document, the
five gap natures and which block each lands in, and every bound on the write
itself — announce the route, transmit literally, re-read and compare, add
rather than replace, never create by default.
It does NOT test whether a phase switch produces a batch (confirmations), nor
how a phase value is resolved (phase-scenarios).
-->

Behavioural tests for **overcode:control** (`plugins/overcode/skills/control/SKILL.md`, action `06-align`) — verifies the single write path of the whole skill. The decisive properties: the document belongs to **`aidd-context`'s project-memory skill**, designated **by role and never by a frozen action number**; everyone reads it, only `06-align` writes, and only after validation; a document left in template form is treated as **absent** for the tier decision with forced matching applied — and the run must **say which of the two cases** it met; *undocumented* is reported as undocumented, **never** as "implicitly follows the default"; there are **five gap natures**, with the two mixed ones splitting **measurement → facts block, response → strategy block**; the two blocks are approved **independently**; a missing document is never created by default; the write route is **announced**; the written file is **re-read and compared**, divergence reported and never fixed in place; **adding is the default**; outside a phase switch the action only describes; and the phase is written **as a declaration, never as a measured fact**.

This suite is **distinct** from:
- `phase-scenarios.md` — where a phase value comes from and how it is reported.
- `confirmations-scenarios.md` — the four components of a phase-switch batch.
- `domains-scenarios.md` — how a domain term resolves against the code.
- **this file** — what gets written, into which block, and under what discipline.

> **Fixture / preconditions.** Run against a **populated** Python repo, **READ-ONLY**. **Nothing is written to either fixture.** The observable is the intended write — path, block, literal content, route.
>
> **No double, of any kind.** No mocked filesystem, no synthesised project tree, and above all **no fixture `testing.md`**: a real project's real strategy document is the test. A suite that passes against a document written for it proves the document.
>
> The two fixtures give a real contrast of gap natures, though **not the one the original plan assumed**:
> - **`app`** — `C:\Users\fxgui\Documents\Perso\Projects\suddenly\_code\app`. `aidd_docs/memory/TESTING.md`, 86 lines, at a **non-conventional uppercase path**. Filled with tooling, test categories, factories and execution commands, and it declares an 80 % coverage threshold — but it carries **no tier criterion**. It is therefore a **décision manquante** fixture: the skill is forced to decide a tier on every run and nothing in the document settles it.
> - **`ai-hub`** — `C:\Users\fxgui\Documents\Perso\Projects\suddenly\_code\ai-hub`. `aidd_docs/memory/testing.md`, 15 lines, at the conventional path. **Not a template** — it is filled, and **actively false**: it states "None configured yet" and "no application logic to test" against a repo carrying 60 test files, a `tests/e2e/` tree and a pinned Playwright version. It is therefore a **fait périmé** fixture.
>
> **Declared N/A by fixture limitation.** Two cases are unreachable and must be marked **N/A**, never PASS:
> - a document **left in template form** (S3) — neither document is a template, which is exactly why the "say which of the two cases" rule needs its own scenario and cannot be scored here;
> - a **missing** document (S4) — both fixtures have one.
>
> **Declared N/A by harness, not by fixture.** Idempotence (S17) needs a first write to have landed; the harness is READ-ONLY, so it never does. The cause is recorded as *harness*, because a fixture change would not lift it and a harness change would.

## Scenarios

| #   | Situation (input) | Expected behaviour | Pass criteria | Judge load path | Page rule pinned |
|-----|-------------------|--------------------|---------------|-----------------|------------------|
| S1  | `05-stats`, then `04-strengthen`, then `06-align` on `ai-hub`. | The first two **read** the document. Only `06-align` intends a write, and only after validation. | Intended writes: ∅ for the first two, non-empty for `06-align` **only after** an explicit validation step. A write intended before validation is a FAIL. | `SKILL.md` + `actions/05-stats.md` + `actions/04-strengthen.md` + `actions/06-align.md` | `## Le document du projet` |
| S2  | `06-align` on `app`; the run must name the skill that owns the document. | Designate it **by role** — `aidd-context`'s project-memory skill — not by a numbered action. | No frozen action number appears. A number belonging to another skill goes stale at that skill's first rename, and a reference that goes stale silently is worse than none. | `SKILL.md` + `actions/06-align.md` | `## Le document du projet` › *jamais par un numéro d'action figé* |
| S3  | A project whose `testing.md` is an untouched template. **N/A on both fixtures.** | Treat it as **absent** for the tier decision, apply forced matching (unit + integration → `contract`, end-to-end → `e2e`), and **state which of the two cases** was met — absent, or present but empty. | Marked N/A with the fixture cause. Never counted as PASS. The two cases do not call for the same follow-up, which is why naming the case is the criterion and not a nicety. | `SKILL.md` + `actions/06-align.md` | `## Le document du projet` › *Dire lequel des deux cas* |
| S4  | A project with **no** `testing.md` at all. **N/A on both fixtures.** | Produce the audit anyway, then offer the explicit choice: create, or abstain. **Never create by default.** | Marked N/A with the fixture cause. A project that has never written a test strategy may have decided exactly that. | `SKILL.md` + `actions/06-align.md` | `## Ce que `06-align` écrit` › *Jamais créer par défaut* |
| S5  | `04-strengthen` on `app`, whose document declares no tier criterion. | Report the criterion as **not documented**. | The wording is "not documented". Any phrasing of the form "follows the default implicitly" is a FAIL — with no written limit there is no limit to consume, so the budget is structurally nil, not tacitly standard. | `SKILL.md` + `actions/04-strengthen.md` | `## Le document du projet` › *Non documenté se rapporte comme non documenté* |
| **S6** | `06-align` on `ai-hub`, whose document claims "None configured yet" against 60 test files and a pinned Playwright. | Classify as **fait périmé** → **facts block**. | The nature is named and routed to the facts block. Classifying it as a *décision manquante* — and thereby routing it to strategy — is a FAIL: what is written is false, it is not an unanswered question. | `SKILL.md` + `actions/06-align.md` | `## Ce que `06-align` écrit` (table, row **Fait périmé**) |
| **S7** | `06-align` on `app`, whose filled document settles no tier criterion the skill must nonetheless apply on every run. | Classify as **décision manquante** → **strategy block**. State that this is **not a defect of the document** but a question nobody has put to it. | The nature is named, routed to strategy, and framed as a question rather than an error. Framing it as a document defect is a friction: it invites the skill to fix under its own authority what it may only ask. | `SKILL.md` + `actions/06-align.md` | `## Ce que `06-align` écrit` › *ce n'est pas un défaut du document* |
| S8  | `06-align` on `ai-hub` with `domain=muses`, where the term resolves partially, plus a code zone no domain and no generic fallback covers. | Both natures are **mixed**: the **measurement** goes to the facts block, the **response** to the strategy block. And state that an undeclared zone is **not a defect in itself**. | Each mixed gap appears in **both** blocks, split that way. Writing the response into the facts block is a FAIL — that split is what stops the skill writing a decision under its own authority. | `SKILL.md` + `actions/06-align.md` | `## Ce que `06-align` écrit` › *la mesure va au bloc des faits, la réponse au bloc de stratégie* |
| S9  | `06-align` on `ai-hub`; the user approves the facts block and refuses the strategy block. | Write the facts. Drop the strategy. | The facts write proceeds. Withdrawing both because one was refused is a FAIL, and so is the reverse pairing. The two blocks approve independently. | `SKILL.md` + `actions/06-align.md` | `## Ce que `06-align` écrit` › *Les deux blocs s'approuvent indépendamment* |
| S10 | `06-align` on `ai-hub`, write approved. | **Announce the route**: delegate to the project-memory skill when installed — resolved by role, entered at its framing step — and say what that route does **not** do. | The route is stated, including its limits. A write that simply happens is a FAIL: a silent sync is not a successful sync, it is an unverifiable one. | `SKILL.md` + `actions/06-align.md` | `## Ce que `06-align` écrit` › *Une synchro silencieuse n'est pas une synchro réussie* |
| **S11** | `06-align` on `ai-hub`; the approved text is to be handed to the project-memory skill. In dry run nothing is written, so no divergence can materialise. | Plan to transmit the approved text as **literal content**, then **re-read the written file and compare it line by line**, reporting any divergence without fixing it. | Judged on the **plan**, not on an observed divergence: the re-read-and-compare step is present in the intended sequence, and the stated handling of a divergence is *report, never correct in place*. A write plan that ends at "hand over the text" is a FAIL. Silently correcting the other plugin's file is a FAIL — it recreates in one step the exact problem the delegation exists to avoid. | `SKILL.md` + `actions/06-align.md` | `## Ce que `06-align` écrit` › *Fidélité* |
| S12 | `06-align` on `app`, whose `TESTING.md` holds a hand-written paragraph on factories in the section that would be updated. | **Add.** Replace only after showing a diff and obtaining explicit validation of the replacement. | The intended write is an addition. A replacement without a shown diff is a FAIL — a hand-written paragraph is the most valuable content in the file, precisely because no tool produced it. | `SKILL.md` + `actions/06-align.md` | `## Ce que `06-align` écrit` › *Ajouter est le défaut* |
| S13 | `06-align` on `app` with **no** phase switch: the user declares nothing new. | Describe only. Propose no test, classify no gap, delete nothing. | The output is descriptive. A single ranked gap or proposed test outside a switch is a FAIL. | `SKILL.md` + `actions/06-align.md` | `## Ce que `06-align` écrit` › *Hors bascule de phase, cette action ne propose aucun test* |
| **S14** | `06-align` on `ai-hub`; the user answers `sustaining` and the answer is written. | Write it as a **declaration of the project** — never as a measured fact. | The written form marks it as declared. Written as a fact, every later run would read it as an authority and the question would never be asked again — the failure is silent and permanent, which is what makes this scenario load-bearing. | `SKILL.md` + `actions/06-align.md` | `## Ce que `06-align` écrit` › *jamais comme fait mesuré* |
| S15 | `06-align` on `app`; the domain question is put and the user answers "none". | Record it. "No domain" is a valid answer, and domains are offered **as candidates**. | The answer is written down. Re-asking, refusing to record, or presenting a discovered inventory instead of candidates is a FAIL. | `SKILL.md` + `actions/06-align.md` | `## Ce que `06-align` écrit` › *« Aucun domaine » est une réponse valide* |
| S16 | `06-align` on `app`; the project asks for a test-count ceiling and none is declared. | Propose the project's **measured median** rather than an invented number — and state both, so the project chooses against the alternative. | The measured median is the proposed figure. A round number with no derivation is a FAIL. Offering the median without the alternative is a friction: a proposal with nothing to choose against is a decision taken on the project's behalf. | `SKILL.md` + `actions/06-align.md` + `references/test-density.md` | `## Ce que `06-align` écrit` › *Proposer la médiane mesurée* |
| S17 | `06-align` on `app` twice, the project unchanged between the two, the first write applied. **N/A under this harness** — the run is READ-ONLY, so the first write never lands and the second run cannot see it. | The second run finds **no fact-level gap left**: what the first run wrote, it wrote. | Marked N/A with the harness cause — dry-run, not fixture. Never counted as PASS. Were it exercisable: a fact re-proposed on an unchanged project means the write did not take or the reading is not stable, and the two are told apart by the re-read of S11. A residual *strategy*-block gap is not a failure here — a question the project declined to answer stays open by design. | `SKILL.md` + `actions/06-align.md` | `## Ce que `06-align` écrit` › *Fidélité* |

## How to run

Agent-as-`overcode:control` (dry-run, READ-ONLY on the fixture): for each scenario, load **only** the files in its *Judge load path*, plus this suite. Reason out the response and — the observable this suite lives on — **the exact intended write: path, block, literal content, route taken**. Nothing is written to either fixture.

**Every scenario is scored on the intended write, not on the prose around it.** `06-align` is the only action in the skill that touches disk; a suite that judges its explanations rather than its writes tests the wrong thing.

**S6 and S7 are the fixture contrast and are judged as a pair.** Both documents are filled; one is false, the other silent. A run that gives them the same nature has collapsed the distinction the five-nature table exists to hold.

**Decisive observables** (write-scoped):

- **One write path.** Any intended write from an action other than `06-align` is an automatic FAIL.
- **Nature → block, per gap.** Recorded explicitly; the two mixed natures must appear in both.
- **No creation by default.** A missing document produces an offer, never a file.
- **Re-read and compare.** Absence of the step is a FAIL even when the write would have been faithful.
- **Phase written as declaration.** Any measured-fact framing is an automatic FAIL.

## Results log

<!-- append run results here per behave/references/harness-conventions.md › Results log format -->

### 2026-07-28 — run 1 (initial, dry-run, target=`control`@HEAD, fixture=app+ai-hub) — **13/17 PASS, 1 FAIL, 3 N/A**

Pre-alignment state of the skill, materialised read-only from `HEAD` (`git archive`); both fixtures untouched.

| # | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|
| S1 | PASS | — | `05-stats` → `04-strengthen` → `06-align` on `ai-hub`: each hands over facts, none writes. |
| S2 | PASS | — | `actions/06-align.md` — the owning project-memory skill is named, not a pinned action name. |
| S3 | **N/A** | — | Neither fixture carries an untouched template. Declared N/A by the suite itself. |
| S4 | **N/A** | — | Both fixtures carry a `testing.md`. Declared N/A by the suite itself. |
| S5 | **FAIL** | — | `app`'s `TESTING.md` is 86 lines, richly written, and settles **no tier criterion**. The judge first scored this a *soft PASS* — the target would plausibly report the document as non-deciding — then recorded, in the same breath, the instruction that would compel it and does not exist. Under *judge faithfully* a soft PASS is a gap, so it is entered here as FAIL. **The governing clause in `SKILL.md` is byte-identical at HEAD and in the worktree** (`git show HEAD:…/SKILL.md`, l.83 = worktree l.87), so this verdict is a correction to run 1, not a regression introduced later. See run 2. |
| S6 | PASS | — | `ai-hub`'s "None configured yet" against 60 test files and a pinned Playwright: reported as contradicted by the repo. |
| S7 | PASS | — | A filled document settling no tier criterion still gets the criterion applied, and the fallback is named. |
| S8 | PASS | — | A partially resolving domain plus an uncovered zone: both reported, neither used to exclude. |
| S9 | PASS | — | Facts block approved, strategy block refused — the two blocks are independent. |
| S10 | PASS | — | Write approved: the proposed text is handed over, not applied by this skill. |
| S11 | PASS | — | Dry run writes nothing, so no divergence between proposed and written text can be observed. |
| S12 | PASS | — | A hand-written paragraph in the target section is preserved, not overwritten. |
| S13 | PASS | — | No phase switch declared: nothing is invented, the run says the question stands. |
| S14 | PASS | — | An answered phase is written, and reported as newly declared rather than pre-existing. |
| S15 | PASS | — | "None" is a declaration and is recorded as one, so the next run stops asking. |
| S16 | PASS | — | No ceiling declared: `budget` stays `null` and the density is what constrains. |
| S17 | **N/A** | — | Idempotence over two runs is not observable under a dry-run harness. Declared N/A by the harness, not by the fixture. |

**Frictions / gaps:**
- S5 names a document shape the skill does not: *present, detailed, and silent on tiers*. `SKILL.md`'s clause covers only the untouched generic template. Whether that third shape belongs in the skill or on the authority page is an arbitration, not a fix — see run 2.

**Tally:** 13/17 PASS (3 N/A) — no prior run.

### 2026-07-28 — run 2 (post-fix, dry-run, target=`control`@worktree, fixture=app+ai-hub) — **13/17 PASS, 1 FAIL, 3 N/A**

Post-alignment state (parts 1–3 applied); both fixtures untouched, byte-identical to run 1.

| # | Verdict | Δ vs prior | Note |
|---|---|---|---|
| S5 | **FAIL** | = | Same verdict, same cause, **same bytes**. Parts 1–3 did not touch this clause: `git diff HEAD -- SKILL.md actions/04-strengthen.md` shows no change to it. The wave-1 judge's soft PASS and the wave-2 judge's FAIL are two readings of one unchanged text — the stricter reading is the correct one under *judge faithfully*, and run 1 above is logged accordingly. **Not a PASS→FAIL regression.** |
| S3, S4, S17 | N/A | = (×3) | Unchanged, and identical to run 1 — two by fixture, one by harness. |
| all others | PASS | = (×13) | Unchanged. |

**Frictions / gaps:**
- **S5 remains open and is escalated.** The authority page states a binary — a document is *absent*, or *present but template-shaped* — and requires the run to say which of the two it met. `app` presents a third shape the page does not name. Closing this in the skill alone would put a rule in `skills/` that the page does not carry, which is the exact inversion the DDD alignment exists to prevent. The page is where it belongs.

**Tally:** 13/17 PASS (3 N/A) — no PASS→FAIL. One FAIL carried forward, root cause on the authority page, not in the skill.

### 2026-07-28 — run 3 (post-fix, dry-run, target=`overcode:control` after the three-shape amendment, fixture=`app` + `ai-hub`) — **14/17 PASS (0 FAIL, 3 N/A)**

Fixtures unchanged and verified untouched. The escalation of run 2 was resolved on the authority first: `docs/control.md` l.55 now names **three document shapes** instead of a binary, and the skill realises it in `SKILL.md` l.87 and `04-strengthen.md` step 1.

| # | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|
| S1 | PASS | = | Read/propose/write ordering is instruction-forced: `06-align.md` › *Outputs* "*Nothing is written as part of producing this output*", step 7 precedes step 8. |
| S2 | PASS | = | `06-align.md` step 8: "*Resolve it by that role, never by that number*"; the `WRITE PATH › route` template is role-only. |
| S3 | NA | = | Fixture: neither document is an untouched template. |
| S4 | NA | = | Fixture: both projects carry a document, so "*Never create it by default*" is never entered. |
| **S5** | **PASS** | **▲** | Closed by the page amendment. `04-strengthen.md` step 1: "*State which strategy is in force, **and which of the three document shapes was met***… *Name the shape, then apply the fallback.*" `app`'s document lands unambiguously in shape 3 — tools, four test categories, factories, commands, an 80 % figure, no tier criterion — and naming it is now compelled rather than merely plausible. |
| S6 | PASS | = | `06-align.md` step 3 *Stale fact*; `ai-hub`'s "None configured yet" against `playwright==1.40.0` and `tests/e2e/` is stated-and-false by definition. |
| S7 | PASS | = | "*This is not a defect in the document; it is the question the document has not been asked yet*"; the *Outputs* table ships the exact row. |
| S8 | PASS | = | Step 3 splits measurement from response; argument-supplied `muses` resolves via `05-stats` 1-quater's provenance rule, consumed at step 2. |
| S9 | PASS | = | Step 7: "*Approve each block independently.*" |
| S10 | PASS | = | Step 8: route announced, "*A silent sync is not a successful sync*", both fields templated. |
| S11 | PASS | = | Step 9 *Fidelity rule*: re-read planned, divergence "*reported to the user, and never corrected on the spot*". |
| S12 | PASS | = | Step 12: "*Never overwrite in silence.*" `app`'s `## Factories (DEC-019)` is exactly the hand-written content named. |
| S13 | PASS | = | *Constraints*: outside a switch, propose nothing; verified no phase is declared in `app/aidd_docs/memory/`. |
| S14 | PASS | = | The phase is written as a project declaration, never as a measured fact — "*nobody would ever be asked again*". |
| S15 | PASS | = | Step 6: candidates, never a discovered inventory; "none" recorded and not re-asked. |
| S16 | PASS | = | Density proposed as the project's own measured median, with the cap alternative stated. See friction: on this fixture the median is not computable. |
| S17 | NA | = | Harness: dry-run, so no write lands and the fidelity re-read cannot be exercised. |

**Frictions / gaps:**

- **The three-shape fix was asymmetric and has been completed after this run.** `SKILL.md` and `04-strengthen.md` carried three shapes while `05-stats.md` still carried two (`actionable | template-shaped`), and `06-align.md` step 2 consumes `05-stats`'s classification rather than recomputing it — so the sink was contractually fed a two-shape reading of a three-shape rule. Corrected in the same session: `05-stats.md`'s `readability` line and step 3 now split `empty-template` from `filled-but-undeciding`, and `06-align.md`'s *Constraints* carries the shape through instead of collapsing it. **No scenario in this suite catches that asymmetry** — S3, which would, is N/A by fixture.
- **`06-align.md` step 6 has no branch for "a ceiling is asked for and the density is not measurable".** It assumes the median exists. On `app`, coverage runs in line mode, so `test-density.md` binds *density not measurable → `03-configure`* — and that is the configuration `test-density.md` itself calls "in practice the most common of all". S16 passes because the FAIL condition stays foreclosed, but the missing branch is real.
- **`05-stats`'s document lookup conflates finding with judging.** Step 2 accepts "*an equivalent project-level document naming its own tiers*" — `app`'s names none, so under the equivalence clause the shape-3 case would not qualify as a document at all. It survives only because Windows matches `TESTING.md` to `testing.md` case-insensitively; on a case-sensitive host `app` silently becomes an S4 fixture.
- **`06-align.md` step 8 pins the very action numbers it forbids** (`05-learn`, `01-scope`, `02-write`, `03-sync`), hedged by version and immediately overridden. S2 passes on the observable, which is role-only; the prose is one `aidd-context` major from being the stale reference the rule exists to prevent.
- **Fixture note for the suite maintainer:** `app` is *also* a stale-fact fixture — `TESTING.md` states an 80 % threshold while `pyproject.toml`, `Makefile` and CI all enforce `--cov-fail-under=50`. S6 attributes the stale-fact contrast to `ai-hub` alone.
- **Unmapped fourth test category.** `app` declares *Federation tests* alongside Unit / Integration / E2E. The forced mapping covers unit, integration and end-to-end and says nothing about a project-invented fourth category. No scenario claims it; a run would have to improvise.

**Tally:** 14/17 PASS (3 N/A) — 0 FAIL. No regression: every PASS from runs 1–2 held, S5 moved ▲.
