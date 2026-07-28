# Control — Density, Coverage Reading & Measurement Bounds Behavioural Test Scenarios

<!--
One suite = one durable regression spec for ONE aspect of ONE target.
This suite pins WHAT IS MEASURED AND HOW IT IS READ: density against the
project's own median, orders never shares, covered/total never a bare
percentage, the three measurement bounds, the degenerate cases and their order,
and the external-boundary ceiling.
It does NOT test who may act on a measurement (authority-scenarios), nor how a
measured fact reaches the project document (align-write-scenarios).
-->

Behavioural tests for **overcode:control** (`plugins/overcode/skills/control/SKILL.md`, actions `04-strengthen` / `05-stats`, references `references/test-density.md` / `references/pivot-contract.md`) — verifies the measurement layer. The decisive properties: density is read **against the project's own median**, alerting past 3×, never against an imported absolute; an outlier **points and never qualifies**, and admits two readings to be discriminated before either is emitted; density is **not a target**; a declared count ceiling **wins as a ceiling** with density reported beside it, never in its place; `limit` comes only from an explicit test-count limit; a coverage percentage is never a budget; **no percentage is produced at all** — orders, never shares; the reading is `covered`/`total`, an absence at the glob means **not covered**; the source glob drives the universe; the degenerate cases are reported in order, outermost fact first; a declared gate is reported as **invoked or inert**, never merely "configured"; and an external boundary is worth **one** test by default.

This suite is **distinct** from:
- `authority-scenarios.md` — that density never changes a tier.
- `phase-scenarios.md` — that no phase sets a numeric threshold, and that an absence means the same thing in every phase.
- `domains-scenarios.md` — that a domain does not shrink the universe.
- **this file** — the arithmetic itself, and how its results are stated.

> **Fixture / preconditions.** Run against a **populated** Python repo, **READ-ONLY**. The contrast between the two fixtures **is** the observable for the degenerate cases.
>
> **No double, of any kind.** No mocked filesystem, no mocked coverage report, no synthesised project tree, no fixture `testing.md`, no stand-in for `aidd-dev:06-test`. The first real coverage run — or the real static fallback on a real repository — is the test; a suite that passes against a double proves the double.
>
> Reference fixtures:
> - **`app`** — `C:\Users\fxgui\Documents\Perso\Projects\suddenly\_code\app`. 80 test files; **`.coverage` present** — the only fixture on which a real denominator, a real median and a real outlier can be computed. `aidd_docs/memory/TESTING.md` declares an **80 % coverage threshold**: a genuine attempt to turn a percentage into a target, sitting in the project's own document.
> - **`ai-hub`** — `C:\Users\fxgui\Documents\Perso\Projects\suddenly\_code\ai-hub`. 60 test files; **no coverage report** → degenerate case 2. `tests/e2e/` supplies the *path already walked in e2e* case.
>
> **Declared N/A by fixture limitation.** Two cases are unreachable and must be marked **N/A**, never PASS:
> - degenerate case 1, **no test at all** (S13) — 80 and 60 test files respectively; case 3, *insufficient population*, **is** reachable under a narrow `scope` and is scored at S12;
> - an explicit **test-count ceiling** (S4) — `app` declares a coverage percentage, which is precisely not a ceiling, and `ai-hub` declares nothing.

## Scenarios

| #   | Situation (input) | Expected behaviour | Pass criteria | Judge load path | Page rule pinned |
|-----|-------------------|--------------------|---------------|-----------------|------------------|
| S1  | `05-stats` on `app`, coverage report present. | Compute density as test cases per branch point, read **against the median of `app`'s own distribution**. Alert past 3× that median. | The comparison baseline is the project's own median. Any absolute threshold imported from outside — "under 2 cases per branch is thin" — is a FAIL, whatever its source. | `SKILL.md` + `actions/05-stats.md` + `references/test-density.md` | `## La densité, pas le compte` |
| **S2 (B5)** | `05-stats` on `app`. The report is produced. | Compare **orders**, not shares. Produce **no percentage anywhere in the output**. | Zero percentage figures **computed by `control`**. A density percentage, a coverage share the run derived itself, or a "73 % of files are below median" is an automatic **FAIL** — that rule is absolute, not a preference. A figure the *project* declared, quoted verbatim on the `declared` line and used as a target by nothing, is **not** a produced percentage: the page forbids producing one, not repeating one, and S3 of this suite requires the threshold to be reportable. Cite the action file that produces the figure. | `SKILL.md` + `actions/05-stats.md` | `## Les axes de lecture` › *compare des **ordres**, jamais des parts. Aucun pourcentage n'est produit* |
| S3  | `04-strengthen` on `app`, whose document declares an **80 % coverage threshold**. | Report the declared threshold as the project's own statement. Propose **no** work whose only justification is raising it. | No proposed gap cites "to reach 80 %". The threshold may be reported; it may not become the reason for a single line of work. This is the mother rule, and the fixture exercises it for real. | `SKILL.md` + `actions/04-strengthen.md` | `## La densité, pas le compte` › *un symptôme, jamais une cible* |
| S4  | A project declaring an explicit ceiling of **N tests** for a module. **N/A on both fixtures** — `app` declares a coverage percentage, not a test-count ceiling, and `ai-hub` declares nothing. | The ceiling **wins as a ceiling**. Density is reported **beside** it, never in its place. | Marked N/A with the fixture cause; never counted as PASS. Were it exercisable: both figures appear distinctly, and substituting one for the other is a FAIL — a ceiling says *how many*, a density says *whether it is in the right place*, and neither contains the other. | `SKILL.md` + `actions/04-strengthen.md` + `references/test-density.md` | `### Densité et plafond ne se remplacent pas` |
| S5  | `04-strengthen` on `app`. The only numeric statement available is the 80 % coverage threshold; no test-count limit is declared. | Derive **no** `limit`. | `limit` is unset or defaults. Deriving a `limit` from the percentage is a FAIL — a coverage percentage is not a budget and never becomes one. | `SKILL.md` + `actions/04-strengthen.md` | `### Densité et plafond ne se remplacent pas` › *`limit` ne vient que d'une limite de nombre* |
| S6  | `05-stats` on `app`; a file exceeds 3× the median **and** sits in the top decile of branch points. | Read it as a **refactoring signal** — and propose no refactoring, which is out of this skill's scope. | The reading is discriminated *before* any recommendation is emitted. Routing it to `02-audit` without discriminating is a FAIL; proposing a refactor is also a FAIL. | `SKILL.md` + `actions/05-stats.md` + `references/test-density.md` | `### Ce qu'un outlier dit` |
| S7  | `05-stats` on `app`; a file exceeds 3× the median and is **not** in the top decile of branch points. | Read it as many cases over little logic → a subject for `02-audit`. Report the known blind spot: data-driven discrimination does not enter the denominator. | The second reading is emitted and the blind spot is declared. A verdict rendered on the file is a FAIL — an outlier is a file to look at. A parametrised test file flagged with no caveat is the blind spot firing unacknowledged. | `SKILL.md` + `actions/05-stats.md` + `references/test-density.md` | `### Ce qu'un outlier dit` › *jamais un verdict rendu sur lui* |
| S8  | `04-strengthen` on `app`. A module appears in the pivot's **source glob** and is **absent from `.coverage`**. | Read it as **not covered**, and keep it in the classifiable universe. | The module is present and read as uncovered. Treating the absence as "no such file" or as covered is a FAIL — reports routinely omit files no test imports, which is exactly the most exposed population. | `SKILL.md` + `actions/04-strengthen.md` + `references/pivot-contract.md` | `## Les bornes de mesure` › *non couvert, pas inexistant* |
| S9  | `05-stats` on `app`. A file has **no branches** and no test. | Report `covered`/`total`, not a bare percentage. | The pair is reported. A file with no branch reports 100 % branch coverage while being entirely untested — a run that presents it as covered is a FAIL, and this is precisely why the rule exists. | `SKILL.md` + `actions/05-stats.md` | `## Les bornes de mesure` › *Raisonner sur `covered`/`total`* |
| S10 | `05-stats` on `app` with `scope=suddenly/games/` and `domain=federation` **not** set; then the same run with the domain set. | The universe comes from the **pivot's source glob**, reduced by `scope`. The coverage report enriches branch detail; it never defines the universe. `domain` does not reduce it. | The file set is identical with and without the domain, and is never derived from `.coverage`'s file list. Deriving the universe from the report is a FAIL — it would silently exclude everything the report omits. | `SKILL.md` + `actions/05-stats.md` + `references/pivot-contract.md` | `## Les bornes de mesure` › *L'univers classifiable vient du glob source du pivot* |
| S11 | `05-stats` on `ai-hub` — 60 test files, **no coverage report**. | Report **case 2**: no denominator, density **not computed** — neither approximated nor replaced by a line count — and name `03-configure` as what changes it. | No density figure, no substitute metric. An invented ratio on a missing denominator is worse than the absent measurement it replaces, and is an automatic FAIL. `03-configure` must be named. | `SKILL.md` + `actions/05-stats.md` + `references/test-density.md` | `### Les cas dégénérés, et leur ordre` |
| S12 | `05-stats` on `ai-hub` with `scope=pipelines/anonymization/` — a population too small for a median. | Report **case 3**: no median, no outlier. And in every case, declare the matching rule used and **how many files it failed to pair**. | The unmatched count is stated even here. Its absence is a FAIL in every run of this suite, not only this one. | `SKILL.md` + `actions/05-stats.md` + `references/test-density.md` | `### Les cas dégénérés, et leur ordre` › *déclarer la règle de correspondance […] et le nombre de fichiers qu'elle n'a pas appariés* |
| S13 | A repo with **no test at all** and no coverage report. **N/A on both fixtures.** | Report case 1 only — the outermost fact, reported once, rendering the others moot. Leading with the coverage report would suggest that wiring it is what separates the project from a density. It is not. | Marked N/A with the fixture cause. Never counted as PASS. | `SKILL.md` + `actions/05-stats.md` | `### Les cas dégénérés, et leur ordre` › *le fait le plus extérieur se rapporte une fois* |
| S14 | `01-write` / `04-strengthen` on `app` for the outbound ActivityPub integration. | **One** test by default — the degraded path. A second only if the payload carries a consequence verifiable in-process. Declare "the provider still accepts this payload" **out of test scope**, referred to monitoring, never converted into a proposed test. | The ceiling holds and the out-of-scope statement is present. Proposing a live call is a FAIL. Note that this is a **ceiling per boundary, not a quota** — an integration may legitimately receive nothing. | `SKILL.md` + `actions/04-strengthen.md` + `actions/01-write.md` | `## Les frontières externes` |
| S15 | `04-strengthen` on `ai-hub`, where `tests/e2e/` already walks a path that a candidate gap would cover. | Exclude the path as *already walked in e2e* — one of the three legitimate exclusion sources — and say so. | The exclusion is stated with that reason. A silent drop is a FAIL; so is proposing the gap as though nothing covered it. | `SKILL.md` + `actions/04-strengthen.md` | `## Les bornes de mesure` + `### Le garde-fou` |
| S16 | `05-stats` on `app`: a wired runner (`make check`), a real `.coverage`, and a strategy document at a non-conventional path. | Name the authority in force **by path** — or say *generic default* outright; derive the volume from a **real count**, declaring whether cases or files were counted; and say whether the coverage gate is **configured and invoked** or **configured but never invoked**. | The three lines are present and each is decidable on its own. An authority line naming neither a path nor an explicit generic default is a FAIL. An estimated volume, or one whose counting mode is unstated, is a FAIL. A coverage line reading "configured" without saying whether anything invokes it is a FAIL: in a report, a gate nothing runs is indistinguishable from a gate that runs — which is the defect `03-configure` exists to catch, and it cannot be routed to what nobody reported. | `SKILL.md` + `actions/05-stats.md` | `## La configuration` › *le gate déclaré est-il réellement invoqué* |

## How to run

Agent-as-`overcode:control` (dry-run, READ-ONLY on the fixture): for each scenario, load **only** the files in its *Judge load path*, plus this suite. Reason out the response and the exact figures the run would emit, then judge against the pass criteria.

**S2 is checked mechanically, not by reading.** Scan the produced report for the `%` character and for the words "percent"/"pourcentage", **excluding the `declared` line of the STRATEGY block** — that line exists to quote the project's own figure verbatim and is the single sanctioned exception. Any other hit is a FAIL. Keeping the check mechanical matters: it is the criterion most likely to be waved through by a judge reading for intent. Narrowing it to computed figures is a deliberate arbitration of 2026-07-28, recorded in the log below — the earlier absolute form contradicted both the authority page (which forbids *producing* a percentage, not repeating one) and S3 of this same suite.

**The degenerate cases are judged on order, not only on content.** S11 and S13 both admit outputs containing the right facts in the wrong sequence. Record which fact the run leads with.

**Decisive observables** (write-scoped):

- **Zero percentages in the output.** Mechanical check, automatic FAIL.
- **The universe is glob-derived.** Never the coverage report's file list.
- **No density where there is no denominator.** No approximation, no line-count substitute.
- **The unmatched-file count is present in every run**, degenerate or not.
- **No work justified by a number going up.** Neither coverage nor density.

## Results log

### 2026-07-28 — run 1 (initial, dry-run, target=`overcode:control` @ `HEAD`, fixture=`app` + `ai-hub`) — **11/16 PASS (3 FAIL, 2 N/A)**

Target read at `HEAD`, before the alignment. Fixtures untouched and READ-ONLY. N/A per the preamble: S4 (no declared cap on either fixture) and S13 (both fixtures well past a handful of test files).

| # | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|
| S1, S3, S5–S8, S11–S12, S15–S16 | PASS | — | Eleven scenarios held at `HEAD`; the measurement layer's prohibitions (no percentage as a target, no coverage figure as a budget, absent-from-report ≠ nonexistent) were already stated. |
| S4, S13 | NA | — | Suite-declared fixture limitations. |
| **S2** | **FAIL** | — | The mechanical scan hits percentages the skill sanctions in two distinct classes while the criterion sanctioned one location. Root cause is a criterion/skill mismatch, not a produced percentage — see the 2026-07-28 arbitration below. |
| **S9** | **FAIL** | — | The `covered`/`total` bound exists in `SKILL.md` and `04-strengthen.md`, and **nowhere in `05-stats.md`** — the action that produces the figures. Page l.210 requires it. Rule on the page, absent from the producing action: a drift. |
| **S14** | **FAIL** | — | The external-boundary ceiling ("*out of reach of testing*", referred to monitoring, one test per boundary) lives in `04-strengthen.md` only, while `SKILL.md` › *Action chaining* makes `01-write` the sink every new test enters through. The ceiling does not exist at the gate. |

**Frictions / gaps:** the suite preamble asserts `app` is "the only fixture on which a real denominator, a real median and a real outlier can be computed" — see run 3, where that premise is disproved.
**Tally:** 11/16 PASS (2 N/A) — 3 FAIL. Baseline run.

### 2026-07-28 — run 2 (post-fix, dry-run, target=`overcode:control` after parts 1–3, fixture=`app` + `ai-hub`) — **11/16 PASS (2 FAIL, 3 N/A)**

Fixtures unchanged. The part-1/2/3 arbitrations and restorations landed; none targeted the measurement layer directly.

| # | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|
| S1 | NA | ▼ | **Re-score, not a regression.** `app/.coverage` carries `meta.has_arcs = 0`, and neither `[tool.coverage.run]` nor `addopts` enables branch tracking. Under *judge faithfully*, the scenario's precondition simply does not hold on the fixture; the earlier PASS credited a run that could not be produced. |
| S9 | PASS | ▲ | Fixed: `05-stats.md` step 3-quater now carries the bound unconditionally — "*Whenever a figure comes out of the coverage report — to feed the density denominator, or to be reported at all — carry both terms*", with the `0/0`-reads-as-100 % trap named. |
| **S2** | **FAIL** | **=** | Unchanged cause. |
| **S14** | **FAIL** | **=** | Unchanged cause: no edit in parts 1–3 touched `01-write.md`. |
| others | PASS / NA | = | S4, S13 remain N/A by fixture. |

**Tally:** 11/16 PASS (3 N/A) — 2 FAIL. No regression: S1's move is a re-score under a stricter and correct reading, recorded ▼ per the harness convention.

### 2026-07-28 — run 3 (post-fix, dry-run, target=`overcode:control` after the universe and branch-data fixes, fixture=`app` + `ai-hub`) — **8/16 PASS (2 FAIL, 6 N/A)**

Fixtures unchanged. Landed since run 2: `05-stats.md` step 3-bis (the universe comes from the source glob, never from the coverage report), the `density` output line's two non-measurable variants, and the *report present, no branch data* degenerate case in `docs/control.md` and `references/test-density.md`.

| # | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|
| S10 | PASS | ▲ | Fixed. Step 3-bis: "*The universe comes from the source glob, never from the coverage report … it adds detail to that universe; it never defines it … Report the two counts side by side whenever they differ.*" The fixture makes them differ — 131 source files against 125 in `.coverage`. |
| S6, S7 | NA | ▼ | **Consequence of run 2's S1 finding, not a regression.** Both preconditions require a median and a decile of branch points; with `has_arcs = 0` there is no denominator, so no outlier can be produced and neither the two-readings rule nor the blind-spot rule is reachable. |
| S11 | PASS | = | `ai-hub` has no coverage artefact at all ⇒ degenerate case *no coverage report*, and the `density` output line now hardcodes the routing to `03-configure`. |
| **S2**, **S14** | **FAIL** | **=** | Unchanged causes. |
| others | PASS / NA | = | — |

**Frictions / gaps:** three of the five density scenarios (S1, S6, S7) are now N/A on a premise the preamble asserts is satisfied. The suite cannot exercise the outlier half of the measurement layer on either fixture.
**Tally:** 8/16 PASS (6 N/A) — 2 FAIL. No regression: the two ▼ moves are re-scores propagating run 2's fixture finding.

### 2026-07-28 — run 4 (post-fix, dry-run, target=`overcode:control` after the S2 criterion arbitration, fixture=`app` + `ai-hub`) — **9/16 PASS (2 FAIL, 5 N/A)**

Fixtures unchanged and verified untouched. S2's pass criterion was narrowed this day (see *How to run*): a percentage the **project** declared and the run quotes verbatim is no longer a produced percentage. The arbitration is recorded here.

| # | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|
| S1 | NA | = | `has_arcs = 0`; `test-density.md` binds *report in line mode, density not measurable*. No median is produced, so the discriminating criterion is never exercised. |
| **S2** | **FAIL** | **=** | **Open, and escalated — do not re-score without a decision.** The narrowed criterion sanctions **one location** (the `declared` line). `SKILL.md` › *Transversal rules* sanctions **two classes**: a figure the project declared, quoted verbatim and *outside the `budget` line*, **and** a figure quoted from a tool's own report as that tool's output. Only the first is bounded by location. The second is a standing licence to print pytest-cov's own `TOTAL … %` on the TOOLING line, which the mechanical scan hits. Second path: step 7's flag text itself contains "100 %" — instruction prose, not a produced figure, and the scan cannot tell them apart. Page l.143 forbids *producing* a percentage, not quoting one, so the skill is faithful to the page and the **criterion** is what is too narrow. Fixing it means a second rewrite of the same criterion, which is exactly what the alignment plan forbids without validation. |
| S3 | PASS | = | Triple-sourced: "*Coverage percentage is a symptom, never a target*"; "*never a bulk 'raise coverage to N%' campaign*"; "*Rank each candidate gap by risk, not by missing percentage.*" Exercised for real against `app`'s declared 80 % threshold. |
| S4 | NA | = | No test-count ceiling on either fixture. |
| S5 | PASS | = | Quadruple-sourced, sink included: `01-write.md` step 4 — "*`limit` is populated exclusively from the project's own documented test strategy*". |
| S6, S7 | NA | = | No denominator ⇒ no outlier. |
| S8 | PASS | = | Exercised for real: six source files sit in `[tool.coverage.run] omit` and are absent from the report. `04-strengthen.md` step 2 — "*A file matching the source glob but absent from the coverage report is uncovered, not nonexistent.*" |
| S9 | PASS | = | Step 3-quater holds on line data; the fixture supplies nine files in the report with zero covered lines. The branch-specific `0/0`→100 % flavour is not reproducible in line mode. |
| S10 | PASS | = | Step 3-bis plus the domain-invariance clauses in `SKILL.md` › *Parameters* and `05-stats.md` › *Inputs*. |
| S11 | PASS | = | Outermost applicable fact led with; `03-configure` named. |
| S12 | PASS | = | Scored on its unmatched-count half only: the `matching : … - <n> unmatched` output line carries **no** absence clause, unlike the conditional PHASE-block lines. The *case 3* half is unreachable — see frictions. |
| S13 | NA | = | 145 test files in `app`, 50 in `ai-hub`. |
| **S14** | **FAIL** | **=** | Confirmed and **fixed after this run**, unverified by any run yet. Via `04-strengthen` the rule holds; via `01-write` it does not — steps 1–8 carried no external-boundary handling, so "prove our AP delivery reaches the remote inbox" reached step 3, was routed to `e2e` by `decision-framework.md` and delegated. `app` supplies the real boundary at `suddenly/activitypub/tasks.py:72`. Fix landed as `01-write.md` step 3-bis (out of reach of testing → monitoring; one boundary, one degraded-path test, a ceiling not a quota). **Requires a run 5 to confirm.** |
| S15 | PASS | = | Exactly three exclusion sources; `ai-hub/tests/e2e/test_ml_quality.py` exercises the third for real. |
| S16 | PASS | = | Authority, volume and gate each independently forced. Gate decidable as *configured and invoked* (`--cov-fail-under=50` in `addopts`, `Makefile:30`, `.github/workflows/ci.yml:69`). |

**Frictions / gaps:**

- **The fixture preamble is factually wrong about `app`, and it costs three scenarios.** `has_arcs = 0` makes it degenerate case *report present, line mode*, not the branch-data fixture the preamble claims. S1, S6 and S7 are unexercisable, so the entire outlier / decile / blind-spot half of the measurement layer is untested by this suite. Closing this needs either a branch-enabled fixture or an explicit N/A declaration for S1/S6/S7 alongside S4 and S13. **Not repaired here: both options touch a fixture or the suite, and neither is a target fix.**
- **`test-density.md` contradicted itself on the ordering of degenerate cases** — the prose said check "no tests at all" first, the first bullet said "no coverage report … the first to check". Corrected after this run: the bullets are now listed in check order, and the prose says so explicitly. Order is load-bearing for S11 and S13.
- **Case 3 is unreachable on `ai-hub`, contrary to the preamble.** With no coverage report at all, `05-stats` reports case 2 and stops; *insufficient population* is a statement about a distribution and cannot be reached without a denominator.
- **No rule reconciles a project's coverage `omit` list with the source glob.** S8's rule reads `settings.py`, `wsgi.py` and `celery.py` as uncovered production code, when the project deliberately excluded them. With no `sc-python` testing pivot, the fallback exclusion list is "build output, vendored and generated code", which does not cover them. Correct by the letter, noisy in practice.
- **A declared-vs-enforced threshold divergence has no flag.** `app` declares 80 % while everything wired enforces 50 %. Step 7 flags a *stale document* only for a tool named-but-not-installed; a threshold diverging from the one actually enforced is the same species of drift and goes unreported.
- **S16's "non-conventional path" barely bites.** `app`'s document is `TESTING.md`, the skill pins `testing.md`; it resolves only because Windows is case-insensitive.

**Tally:** 9/16 PASS (5 N/A) — 2 FAIL. No regression: every PASS from runs 1–3 held. **This suite does not close.** S14's fix is written but unverified; S2 is an open arbitration on the criterion, not on the target.

### 2026-07-28 — run 5 (post-fix, dry-run, target=`overcode:control` after the `01-write` boundary fix, fixture=`app` + `ai-hub`) — **10/16 PASS (1 FAIL, 5 N/A)**

Fixtures unchanged and verified untouched. Run launched to verify the `01-write` step 3-bis fix written after run 4, and nothing else: no criterion was touched between run 4 and run 5.

| # | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|
| S1 | NA | = | `has_arcs = 0`, line mode, no median produced. |
| **S2** | **FAIL** | **=** | **Still open — and now grounded in emitted text rather than a standing licence.** The mechanical scan finds two hits outside the sanctioned `declared` line. (1) Concrete on the fixture: three 0-byte `__init__.py` (`suddenly/core/management/`, `…/commands/`, `suddenly/games/management/`) score 100 in coverage.py; `05-stats.md` step 7 fires "*a per-file coverage figure of `0/0` reported as 100 % → …*" and step 3-quater demands "*flag any `0/0` explicitly*" — so emitting the required flag prints `100 %` in FLAGS. (2) `SKILL.md` l.91 still licenses "*a figure quoted from a tool's own report as that tool's output*", unbounded by location. The skill is faithful to its authority page; the **criterion** is what fails to model instruction prose reproduced in output. No third form proposed — that decision is not a judge's to take. |
| S3 | PASS | = | Unchanged, exercised against `app`'s declared 80 % threshold. |
| S4 | NA | = | No test-count ceiling on either fixture. |
| S5 | PASS | = | Unchanged, sink included. |
| S6, S7 | NA | = | No denominator ⇒ no outlier. |
| S8 | PASS | = | 131 source files against 125 in `.coverage`; `[tool.coverage.run] omit` at `pyproject.toml:113` removes the six. |
| S9 | PASS | = | **Stronger than run 4**: the `0/0`→100 % case is reproducible in *line* mode, via the three empty `__init__.py`. Run 4's note that this flavour needed branch data was too pessimistic. |
| S10 | PASS | = | 131 vs 125 makes the two counts differ for real, so the invariance is exercised rather than asserted. |
| S11 | PASS | = | Outermost applicable fact led with; `03-configure` named. |
| S12 | PASS | = | Unmatched-count half only; *case 3* still unreachable. |
| S13 | NA | = | 145 test files in `app`, 50 in `ai-hub`. |
| **S14** | **PASS** | **FAIL→PASS** | **The fix holds, through both entry paths.** Scored against the real boundary `app/suddenly/activitypub/tasks.py` › `deliver_activity` (outbound `httpx` POST to `inbox_url`). Via `04-strengthen` step 3, and via the new `01-write` step 3-bis which now intercepts **before** the delegation run 4 observed. Tier untouched — "*Reclassify nothing on this basis*" — so the run reports the step-3 tier with `delegated_to: none`. No live call proposed at either site. |
| S15 | PASS | = | Exactly three exclusion sources. |
| S16 | PASS | = | Authority, volume and gate each independently forced. |

**Frictions / gaps:**

- **`01-write` step 3-bis drops `04-strengthen`'s outbound-only carve-out.** `04-strengthen.md` l.60 conditions the one test on "*only when a vendor failure can interrupt the journey … An outbound-only integration whose failure is invisible client-side gets no test*"; `01-write.md` l.33 states the ceiling unconditionally. `deliver_activity` is a Celery task — outbound-only, invisible to any client journey — so `04-strengthen` would propose **nothing** while `01-write` proposes **one**. Step 3-bis's own claim that "*the same rule and the same words are in `04-strengthen.md`*" is therefore inaccurate as written. **Deficit of the target; no scenario can see it**, because S14 scores the ceiling, not the condition that lifts it to zero.
- **`01-write.md`'s Outputs block has no slot for the out-of-scope statement**, where `04-strengthen`'s does. `delegated_to: none` is documented at step 5 as the `skip` case only, so the out-of-reach outcome borrows a field whose documented meaning is different. Minor deficit of the target.
- **`01-write.md` › *Test* names only `authority-scenarios.md` and `chaining-scenarios.md`.** Step 3-bis was added after the renvoi pass, so the S14 back-reference is missing.
- **The `phase-framework.md` attribution edit moves no verdict.** That file is in no scenario's Judge load path; it closes a contradiction step 3-bis would otherwise create, invisibly to the suite. **Deficit of the suite** — it scores the two actions and never the reference that arbitrates between them.
- **Carried forward, unrepaired:** fixture preamble factually wrong about `app` (`has_arcs = 0`), costing S1/S6/S7; case 3 unreachable on `ai-hub`; no rule reconciles a project's coverage `omit` list with the source glob; declared-80 vs enforced-50 divergence raises no flag; S16's non-conventional path resolves only because Windows is case-insensitive.

**Tally:** 10/16 PASS (5 N/A) — 1 FAIL. No regression: every PASS from runs 1–4 held. **This suite still does not close.** What remains: (1) a decision on S2 — either a third form of the criterion that models instruction prose reproduced in output, or an explicit N/A declaration for it, neither of which a judge may take; (2) a branch-enabled fixture, or explicit N/A declarations for S1, S6 and S7 alongside S4 and S13.
