# Control — Classification Authority & Modulator Boundaries Behavioural Test Scenarios

<!--
One suite = one durable regression spec for ONE aspect of ONE target.
This suite pins the SINGLE-CLASSIFYING-AUTHORITY invariant: the tier table alone
assigns a tier, and the four modulators (phase, domains, density, pivot Risk
signals) prioritise without ever classifying, refusing, or excluding.
It does NOT test phase resolution (phase-scenarios), domain declaration
(domains-scenarios), or how density is computed (measurement-scenarios).
-->

Behavioural tests for **overcode:control** (`plugins/overcode/skills/control/SKILL.md`, actions `01-write` / `02-audit` / `04-strengthen` / `05-stats`) — verifies the load-bearing invariant of the whole model: **one classifying authority, four modulators**. The decisive properties: a test is refused on a *tier criterion* and never "because we are in production"; a density outlier signals and never changes a tier; a domain reorders and never removes; the pivot's *Risk signals* prioritise and never classify; the pivot's *Tier thresholds* never reclassify a case that crosses a **real** external boundary; every tier emitted carries the **motive that decided it**, without which the invariant is unauditable; an **established** e2e runner is never proposed for replacement, a tool being a project decision and not a wiring defect; and `control` writes only what it measured, proposing strategy without applying it.

This suite is **distinct** from:
- `phase-scenarios.md` — how a phase is resolved, reported, and switched.
- `domains-scenarios.md` — who declares domains and how an unmatched term is reported.
- `measurement-scenarios.md` — how density, coverage and percentages are computed and read.
- **this file** — who is *allowed* to decide a tier, and what every other mechanism is forbidden to do.

> **Fixture / preconditions.** Run against a **populated** Python repo, **READ-ONLY**. The judge must not write, create, move or delete anything; the decisive observable is the set of writes the skill *would* perform plus the content of its report.
>
> **No double, of any kind.** No mocked filesystem, no mocked coverage report, no synthesised project tree, no fixture `testing.md`, no stand-in for `aidd-dev:06-test`. The first real read of a real repository is the test — a suite that passes against a double proves the double.
>
> Reference fixtures:
> - **`app`** — `C:\Users\fxgui\Documents\Perso\Projects\suddenly\_code\app`. 80 test files under `tests/`; `pytest` + `pytest-django` + `pytest-playwright`; `-m e2e` marker; `.coverage` present; gate `make check`. Strategy document at the **non-conventional** path `aidd_docs/memory/TESTING.md` (86 lines) — filled with tooling and categories but carrying **no tier criterion**. **No phase declared, no domain declared.** Contains `tests/test_federation.py` (mocks outbound `httpx`, never hits a real instance) and `tests/test_federation_e2e.py` — the pair that makes the external-boundary question concrete.
> - **`ai-hub`** — `C:\Users\fxgui\Documents\Perso\Projects\suddenly\_code\ai-hub`. 60 test files; `tests/e2e/`; `playwright==1.40.0`; **no coverage report**. `aidd_docs/memory/testing.md` (15 lines) declares "None configured yet" and "no application logic to test" — **actively contradicted by the repo**.
>
> State the fixture and its relevant state in every run. A precondition the fixture lacks → **N/A**, never FAIL.

## Scenarios

| #   | Situation (input) | Expected behaviour | Pass criteria | Judge load path | Page rule pinned |
|-----|-------------------|--------------------|---------------|-----------------|------------------|
| S1  | `02-audit` on `app`, user says: "we're in production now, drop the shallow tests." | Treat `production` as a **weighting** input only. Any removal proposed must be qualified by one of the three removal heuristics (duplicate / trivial / lone getter-setter). | No row in the removal table is justified by the phase. Every row cites a heuristic. A test that no heuristic qualifies does **not** appear — even if the phase makes it rank low. | `SKILL.md` + `actions/02-audit.md` + `references/phase-framework.md` | `## Les quatre autorités` › *La phase priorise ; elle ne classe jamais un tier* |
| S2  | **Two runs** of `04-strengthen` on `app`: `phase=production`, then `phase=scaffolding`. | Reweight the six risk criteria and the output ordering. Assign no tier. | Judged on the **Δ**: row order changes between the two runs, **tier values do not**. Every tier traces to the tier table (project doc → `decision-framework.md` → pivot refinement); no tier text cites the phase as its reason. A single run cannot decide this axis. | `SKILL.md` + `actions/04-strengthen.md` + `references/phase-framework.md` + `references/decision-framework.md` | `## Les quatre autorités` (row **Phase**) |
| S3  | `05-stats` on `app`; a test module sits above 3× the project median density. | Flag it as an outlier. Discriminate the two readings first (see `measurement-scenarios.md` S6/S7); if the second reading holds, route it to `02-audit`. | The outlier is reported as **a file to look at**, not a verdict. No tier anywhere is altered by the density value. No test is refused on density alone. Routing to `02-audit` **without** discriminating is scored in `measurement-scenarios.md`, not here — this scenario judges only that no tier and no refusal follow from the density. | `SKILL.md` + `actions/05-stats.md` + `references/test-density.md` | `## La densité, pas le compte` › *elle ne refuse jamais, et ne change aucun tier* |
| S4  | `04-strengthen` on `app` with `domain=federation`. `app` declares **no** domain, so the term resolves by convention only and will miss files. | Rank federation-matching files first; keep everything else **in** the analysis, lower down; report the term and what it failed to recognise. | No file is dropped from the classifiable universe by the domain. The output names the unmatched term. The exclusion list (if any) contains only pivot-declared non-classifiable code, `skip`-tiered cases, and paths already walked in e2e — **never** "did not match the domain". | `SKILL.md` + `actions/04-strengthen.md` | `## Les domaines` › `### Le garde-fou` |
| S5  | `04-strengthen` on `app`; the `sc-python` `testing` pivot supplies *Risk signals*. | Fold the signals into the weighting of the six criteria. | No gap is assigned or refused a tier by a *Risk signal*. The pivot's contribution appears in ordering, never in the tier column. | `SKILL.md` + `references/pivot-contract.md` | `## Les quatre autorités` › *Quatre modulateurs, une seule autorité de classement* |
| **S6 (B3)** | `01-write` on `app` for a behaviour that calls a **real** external instance (ActivityPub delivery to a remote server, as in `tests/test_federation.py`'s subject matter). The pivot's *Tier thresholds* would pull it down to `contract`. | Refuse the pivot's refinement: a pivot may refine a tier **only** when the boundary stays local or emulated. A real external boundary is out of its reach. | The judge reaches this conclusion from the **bounded load path alone**. If `pivot-contract.md` defines *Tier thresholds* without stating the boundary at the point where the field is defined, the judge cannot know it → **FAIL**, and the FAIL cites `references/pivot-contract.md`. | `SKILL.md` + `actions/01-write.md` + `references/pivot-contract.md` — **and nothing else**. Do not load `docs/control.md`, do not load sibling references. | `### Qui remplit la table des tiers` › *Un pivot ne reclasse jamais un cas qui traverse une vraie frontière externe* |
| S7  | `05-stats` on `ai-hub`, whose `testing.md` claims "no application logic to test" while 60 test files exist. | Report the divergence as a measured fact. Propose that `06-align` handle it. Write nothing. | Intended writes: **none**. The strategy correction is *proposed*, never applied. `05-stats` does not edit `testing.md`, and does not invoke `06-align` — it names it. | `SKILL.md` + `actions/05-stats.md` | `## Les quatre autorités` (row **`control`**) + `### Le contrat de chaînage` |
| S8  | `01-write` on `app` for a behaviour nothing settles: `TESTING.md` carries no tier criterion, and the case is not clearly local nor clearly cross-boundary. | Start at **`contract`**, with the ambiguity flagged. | The tier is `contract` and the ambiguity is stated in the output. A silent `e2e` is an automatic FAIL — the most expensive tier is never the default. | `SKILL.md` + `actions/01-write.md` + `references/decision-framework.md` | `### Qui remplit la table des tiers` › *jamais sur `e2e` en silence* |
| S9  | `02-audit` on `app`; a file is a density outlier **and** none of the three heuristics holds after inspection. | Report it as **examined and cleared**. | The file appears in the output with an "examined, cleared" status. Silently dropping it is a FAIL — an abandoned outlier reads as an outlier nobody opened. | `SKILL.md` + `actions/02-audit.md` + `references/test-density.md` | `## Ce qui qualifie un retrait` |
| S10 | `01-write` on `app` for a behaviour nothing settles, then `04-strengthen` on `app`. | Every tier emitted carries the motive that decided it: `01-write`'s outcome block reports `tier`, a **non-empty** `rationale` and `budget_check`; each `04-strengthen` row carries its tier and a one-line justification. | No tier appears anywhere without its motive beside it. An empty or generic rationale — "standard case" — is a FAIL: the single-authority invariant is auditable only through the motive, and a tier with no stated reason cannot be shown to come from the tier table rather than from a modulator. | `SKILL.md` + `actions/01-write.md` + `actions/04-strengthen.md` | `## Les quatre autorités` › *Quatre modulateurs, une seule autorité de classement* |
| S11 | **Two runs** of `01-write` on `app` with the **same** behaviour: one targeting a file below the project median density, one targeting a declared outlier. | Assign the same tier both times. | Judged on the **Δ**: the tier value is identical. A tier that moves with the density is the authority bound broken, and this is the check that catches it. A single run cannot decide this axis. | `SKILL.md` + `actions/01-write.md` + `references/test-density.md` | `## La densité, pas le compte` › *elle ne refuse jamais, et ne change aucun tier* |
| S12 | `03-configure` on `app`, where `pytest-playwright` and the `-m e2e` marker make Playwright the **established** E2E runner. | Report findings, each with a concrete fix, or state plainly that the tooling is clean. Propose fixes to the runner's own configuration and **never a swap**. | Every row carries a concrete config diff or command, or the output says "clean" in so many words. A row proposing to replace the established runner is an automatic FAIL — the choice of a tool is a project decision, not a wiring defect. A finding carrying a severity but no fix is a friction: it reports a problem the user cannot act on. | `SKILL.md` + `actions/03-configure.md` | `## La configuration` › *Ne jamais proposer de remplacer l'outil e2e établi* |

## How to run

Agent-as-`overcode:control` (dry-run, READ-ONLY on the fixture): for each scenario, load **only** the files listed in its *Judge load path* column, plus this suite. Reason out what the skill **would** do — its response AND the precise set of files it would write or modify (paths + scope) — and judge against the pass criteria. Nothing is written to the fixture.

**The bounded load path is the test, not a convenience.** S6 exists to detect a boundary that is stated in the right *model* but the wrong *place*. A judge that reads `docs/control.md` will "know" the boundary and score PASS while the skill, as an agent would actually load it, does not. Loading beyond the declared path invalidates the scenario.

**S2 and S11 are Δ-scored and cannot be decided by a single run.** Record both runs, then score what changed against what must not have: in S2 the order moves and the tier does not; in S11 neither moves. A judge scoring either run alone will pass it while the defect sits in the pair.

**Decisive observables** (write-scoped):

- **No tier value traceable to a modulator.** Every tier cites the tier table, the project document, or a pivot refinement that stays within its boundary.
- **No tier without its motive.** An emitted tier with an empty rationale is unauditable and is scored a FAIL, not a friction.
- **No file leaves the classifiable universe because of a domain.** The exclusion list has exactly three legitimate sources.
- **`05-stats` intended writes = ∅.** Any intended write from `05-stats` is an automatic FAIL.
- **No silent `e2e`.** An unresolved case that lands on `e2e` without the ambiguity being stated is an automatic FAIL.

## Results log

<!-- append run results here per behave/references/harness-conventions.md › Results log format -->

### 2026-07-28 — run 1 (initial, dry-run, target=`control`@HEAD, fixture=app+ai-hub) — **12/12 PASS**

Pre-alignment state of the skill, materialised read-only from `HEAD` (`git archive`); both fixtures untouched.

| # | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|
| S1 | PASS | — | `SKILL.md` › *Authority bounds* — a phase reprioritises, it never authorises a removal. |
| S2 | PASS | — | Same bound, held across both runs: the tier of a behaviour did not move with the phase. |
| S3 | PASS | — | `references/test-density.md` › *Authority bound* — density reports, it does not classify. |
| S4 | PASS | — | `references/phase-framework.md` — an unresolved domain reorders nothing and excludes nothing. |
| S5 | PASS | — | `references/pivot-contract.md` — the pivot supplies signals, never a tier. |
| S6 (B3) | PASS | — | `actions/01-write.md` — a real external boundary lands `e2e`, not `contract`. |
| S7 | PASS | — | `actions/05-stats.md` › *Strategy provenance* — the document is contradicted by the repo and reported as stale, not believed. |
| S8 | PASS | — | `references/decision-framework.md` — the generic default carries the undecided case. |
| S9 | PASS | — | `actions/02-audit.md` — no heuristic holding means no removal proposed. |
| S10 | PASS | — | `actions/01-write.md` — tier, non-empty rationale and budget check all reported. |
| S11 | PASS | — | Two runs, same behaviour, below then above the median: tier identical. Density does not classify. |
| S12 | PASS | — | `actions/03-configure.md` › *Process* step 2 — an established E2E runner is never a replacement candidate. |

**Frictions / gaps:** none — this suite was already green before part-1. It measures the bounds part-1 did not touch, and its value here is the negative control: it shows the alignment did not loosen an authority bound while fixing others.
**Tally:** 12/12 PASS (0 N/A) — no prior run.

### 2026-07-28 — run 2 (post-fix, dry-run, target=`control`@worktree, fixture=app+ai-hub) — **12/12 PASS**

Post-alignment state (parts 1–3 applied); both fixtures untouched, byte-identical to run 1.

| # | Verdict | Δ vs prior | Note |
|---|---|---|---|
| S1 – S12 | PASS | = (×12) | Every bound held. No verdict moved in either direction. |

**Frictions / gaps:** none.
**Tally:** 12/12 PASS (0 N/A) — no PASS→FAIL. The alignment cost this suite nothing.
