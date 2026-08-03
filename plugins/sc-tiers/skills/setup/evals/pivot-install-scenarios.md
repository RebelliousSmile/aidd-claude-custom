# Pivot installers — Written-vs-Announced Behavioural Test Scenarios

<!--
One suite = one durable regression spec for ONE aspect of ONE target.
This suite pins THE GAP BETWEEN WHAT AN INSTALLER ANNOUNCES AND WHAT IT WROTE,
across every plugin that lays pivot files under .claude/rules/07-quality/.
It does NOT test detection quality, pivot content, or the consumer side —
only the honesty of the installer's own output.
-->

Behavioural tests for the **pivot installers** — `sc-tiers:setup 01-install`, and `sniff 02-install-pivots` in `sc-js`, `sc-php`, `sc-python`, `sc-rust` — verifies that an installer's output reports **what it actually wrote**, never a pre-decided list.

**This is the counterpart spec to issue #11.** A consumer can only report an honest provenance if the installer reported an honest installation. Three defects are pinned, and they are not the same: **a source declared by the installer that does not exist on disk**, **a fixed output block printed regardless of what happened**, and **an illustrated body that reads as the list to copy** — the third being what survives once the second is fixed at header level only.

This suite is **distinct** from:
- `pivot-provenance-scenarios.md` (`plugins/overcode/skills/web-optimize/evals/`) — what the **consumers** say about what they loaded.
- **this file** — what the **installers** claim to have written.

> **No verdict is announced in a scenario row.** A row states a situation, an expected behaviour and a falsifiable criterion — nothing else. Measurements taken at a given run live in *Appendix — instruction measurements by run*, dated, and a judge reads that appendix **after** grading, never before. This is not cosmetic: at run 2 the previous form would have returned six false FAILs to any judge that read it off the page.

> **Fixture / preconditions.** Judgement is a **dry-run**: the observable is the *intent to write* plus the output text the action prescribes. **No mutation is needed to conclude**, and none is permitted. Reference repositories, READ-ONLY, under `C:\Users\fxgui\Documents\Perso\Projects\`.
>
> Sources are read **in `plugins/`, never in the installed cache** — a cache copy proves nothing about the source of truth.
>
> **Fixture paths carry a `_code\` segment** — omitting it names a directory that does not exist (friction raised at run 1). Reference fixtures:
> - **`lyremember\_code\app`** — `rust-backend/Cargo.toml:10` declares **`rusqlite`**; the one fixture in the park that carries a stack `sc-rust` genuinely covers in family `data`. Fixture for S4.
> - **`email-to-markdown\_code\app`** — Rust, **no web framework and no ORM**; declares neither `axum`, nor `sqlx`, nor `diesel`, nor `rusqlite`. ⚠ Git refuses to operate here (*dubious ownership*): verify non-mutation by listing, never by `git status`, and **do not alter the global git config** to work around it.
> - **`winfxstart\_code`** — pure Win32 Rust (`tao`, `windows`, `serde`, JSON storage), no `.claude/` at all.
> - **`scriptami\_code\wp-2026`** — WordPress FSE, **no `composer.json`**. The only PHP fixture in the park, and the detection state is part of the observable. Fixture for S3.
> - **`suddenly\_code\app`** — Django (`manage.py`, `pyproject.toml`). Fixture for S5.
> - **`choix-narratifs\_code`** or **`lyremember\_code\site`** for `sc-js`.
>
> **No Symfony fixture and no Laravel fixture exist in the park.** S3 is therefore anchored on WordPress, where a frozen block misfires in the most legible way.
>
> **S8 needs no repository fixture**: its observable is the text of five action files, judged against each other.

## Scenarios

| #   | Situation (input) | Expected behaviour | Pass criteria | Judge load path |
|-----|-------------------|--------------------|---------------|-----------------|
| S1  | `sc-tiers:setup 01-install` on any target. The action declares a set of targets and draws each from a source file under `skills/setup/references/`. | The output counts and names **only what was written**, and a source that cannot be found is reported rather than silently counted. | Two independent binaries, both required: **(a)** every source the table declares resolves on disk; **(b)** the file count in the header is **derived**, not written into the file as a literal, and a not-found branch exists. A run that prints a fixed `✅ … N files written` with targets listed by name announces the outcome before the work. ⚠ **This row exhibits both defect families at once**, which is why it is the one to read when telling them apart: publishing missing sources would leave a frozen count intact, and deriving the count would leave unwritable targets declared. Both remedies are required here. | `sc-tiers/skills/setup/actions/01-install.md` + listing of `skills/setup/references/` |
| S2  | `sc-css:sniff 02-install-pivots`. | *(archived)* | **Row closed — the target no longer exists.** Arbitration A1 of the fix removed the action; a vanished target is unjudgeable, never red. The row is kept because it **attests to the removal**: it contributes nothing to coverage and must not be replayed. Its `FAIL → N/A` at run 2 is the nominal outcome it was written to record, and was written into the row *before* being observed. | — |
| S3  | `sc-php:sniff 02-install-pivots` on **`scriptami\_code\wp-2026`** — WordPress FSE, **no `composer.json`**. (Re-anchored at run 1: the park holds no Symfony and no Laravel fixture.) | The header reflects the outcome; a Laravel pivot is not reported installed on a WordPress project. | The output branches on what happened — a case structure exists, and a derivation clause orders the header to follow it. A single unconditional block FAILs, and on this fixture it fails legibly: it would announce Laravel and Eloquent installed on a project that is neither, and report WordPress skipped. Sources are 6 of 6 present, so the output alone is under test here. | `sc-php/skills/sniff/actions/02-install-pivots.md` |
| S4  | `sc-rust:sniff 02-install-pivots` on **`lyremember\_code\app`**, `rust-backend/` side — `Cargo.toml:10` declares **`rusqlite`** and no other covered stack. (Re-anchored at run 1: neither `winfxstart` nor `email-to-markdown/app` carries `rusqlite`.) | A stack the plugin genuinely covers is reachable in the outcome. | **Criterion narrowed after run 2, which found the old wording licensed two opposite readings.** The single binary is now: the output **branches**, and a derivation clause orders the header to follow what was written — so that `rusqlite`, declared among the targets, *can* appear when installed. Whether the illustrated body names it is **no longer judged here**: that question moved to S8, where it applies to all four `sniff` installers at once instead of to this one. | `sc-rust/skills/sniff/actions/02-install-pivots.md` |
| S5  | `sc-python:sniff 02-install-pivots` on **`suddenly/app`**. | Same requirement as S3. | Same binary: a case structure plus a derivation clause. Sources are 9 of 9 present; only the output is under test. | `sc-python/skills/sniff/actions/02-install-pivots.md` |
| S6  | `sc-js:sniff 02-install-pivots` on **`choix-narratifs`** or **`lyremember/site`**. **Positive control of the *frozen output* family.** | The output is derived, not pre-decided. | Same binary as S3 and S5, plus: every declared target resolves on disk. This row exists to witness that the suite is not written to make everything red — it was free to fall and must be graded with no allowance. ⚠ **The PASS it earns is narrower than it looks** (measured at run 1, still true): the derivation clause governs the **header**; the case *bodies* are fixed text. That residual is S8's subject, and S8 grades `sc-js` on it like the others. | `sc-js/skills/sniff/actions/02-install-pivots.md` |
| S7  | `sc-js:sniff 03-clean` on any target. | Every path the action names resolves on disk. | Each path listed by the action is found on disk, and the guard carries a branch for a candidate whose plugin reference is missing — skipped and reported, never deleted. ⚠ This is the **second** `sc-js` row and its subject is the *declared source missing* family, not the *frozen output* one: do not read S6's positive control as covering the whole plugin. | `sc-js/skills/sniff/actions/03-clean.md` |
| S8  | The Case A output block of the four `sniff` installers — `sc-js`, `sc-php`, `sc-python`, `sc-rust` — read side by side with `sc-tiers:setup 01-install`. **Negative control, added 2026-08-03, not yet judged.** | An illustrated output body reads as an **example**, not as the list to reproduce. | The Case A block carries an example marker — the shape `01-install.md:42` uses, `… one line per target actually processed` — **or** a clause ordering the body, not only the header, to follow what was written. Measured 2026-08-03: **0 of the 4 `sniff` installers** carry either; `01-install.md` carries the marker. ⚠ Why this is not S3/S5's criterion restated: those rows are satisfied by a branching header, and all four installers now satisfy them. This one is red on the same four files, so the *frozen output* family keeps a live red after the header fix — without it the family has a positive control and nothing else. **Coverage of the illustrated body, measured 2026-08-03**: `sc-php` 6/6 targets named, `sc-rust` 3/4, `sc-python` 4/9, `sc-js` 3/13. A body at 75 % reads as exhaustive where one at 23 % reads as an extract; `sc-rust` is the most exposed to literal copying. | the four `<plugin>/skills/sniff/actions/02-install-pivots.md` + `sc-tiers/skills/setup/actions/01-install.md` |

**Coverage.** Six installers at run 1; **five** after the fix, S2 being the row that attests to the removal. Seven rows judged, one archived.

**The three defects are not one.** *Declared source missing* (S1, S7) calls for publishing the source or withdrawing the declaration. *Frozen output over existing sources* (S3, S4, S5, S6) calls for deriving the header from the outcome. *Illustrated body read as a list* (S8) calls for an example marker — and it only becomes visible once the second is fixed, which is why it was added after run 2 rather than before run 1. A run that merges any two into "the installer lies" has not judged.

## How to run

Agent-as-installer (**dry-run, READ-ONLY**): load the target action file from `plugins/`, list the `references/` directory it draws from, and reason out — without writing — which files the action *would* lay down and which output text it *prescribes*. Judge the second against the first.

**Decisive observables:**
- **Sources are read in `plugins/`**, never in `~/.claude/plugins/cache/`.
- For each declared target, its source is either found or not found on disk — that binary is the whole of S1 and S7.
- For each output line, either it is derived from the outcome or it is fixed in the file — that binary is the whole of S3, S4, S5, S6.
- For each illustrated block, either it is marked as an example or it is not — that binary is the whole of S8.
- No fixture is mutated, and no file is written to any plugin. A dry-run that installs to check has invalidated itself.
- **Do not read the appendix before grading.** It records what was measured at a past run against a text that has since changed.

## Appendix — instruction measurements by run

> Archived measurements, kept for provenance. **Each entry is anchored to the file text as it stood at that run** and is not rebased: several verbatim quotes below no longer exist at any line. They are evidence of what was true then, never an expectation for now.

**Run 1 (2026-07-31), against the pre-fix text.** S1 — nothing ordered the header to be derived; `:7` ordered "write its content verbatim" with no not-found branch while `:36` announced `12 files written` hard-coded. S2 — the `❌ non disponible` branch existed (`:12`, `:29`), so the failure was honest but total, and the action declared no source path at all. S3 — `:39-56` was a single unconditional block, no case structure anywhere in the file, sources 6 of 6 present: a pure *frozen output*. S4 — same kind, opposite symptom, an omission rather than a false positive; sources 4 of 4 present. S5 — the named block `:49-64` was fixed and carried none of `sc-js`'s derivation clause. S6 — `:46` stated *"Pick the header by what actually happened — never claim 'installed' when nothing was written"*, honoured by real three-case branching (`:48`, `:68-70`, `:88-90`), 13 of 13 targets resolving; and already then, its bodies (`:53-59`) named three pivots with no example marker — *lift `:46` and `:70`, never the blocks*. S7 — `03-clean.md:26` listed `capabilities/styling/design-system.md`, absent from disk, 12 of 13 resolving.

**Run 2 (2026-08-03), against the corrected text.** The five surviving installers all carry a derivation clause and a three-case structure; `01-install.md:42` is the only one whose illustrated body carries an example marker. That asymmetry is what S8 was written from.

## Results log

### 2026-07-31 — run 1 (initial), before any target is edited

**1 PASS · 6 FAIL · 0 N/A** on 7. Judge: one subagent, fresh context, dry-run READ-ONLY, sources read in `plugins/`.

| # | Verdict | Anchor |
|---|---------|--------|
| S1 | **FAIL** | `sc-tiers/…/01-install.md:26-29` declares 4 data pivots; `references/` holds **9 of 12** sources — `08-data-pivots-firebase.md` present, `supabase` / `dynamodb` / `hasura` absent. `:7` orders "write its content verbatim" with **no not-found branch**; `:36` announces `12 files written` hard-coded. |
| S2 | **FAIL** | `sc-css/…/02-install-pivots.md:17-23` declares 6 pivots; `skills/sniff/references/` **does not exist** — **0 of 6**. The honest branch is real (`:12`, `:29`). |
| S3 | **FAIL** | `sc-php/…/02-install-pivots.md:39-56` is a **single unconditional block**, no case structure anywhere in the file. Sources **6 of 6 present** → pure *frozen output*. |
| S4 | **FAIL** | `sc-rust/…/02-install-pivots.md:19-21` declares `rusqlite`; sources **4 of 4 present**; the frozen block `:37-51` never names it, and `:41` announces `axum` installed unconditionally. |
| S5 | **FAIL** | `sc-python/…/02-install-pivots.md` declares **9** targets (`:13-17`, `:23-25`, `:33`), sources **9 of 9 present**; block `:49-64` names 4 and is unconditional. No clause equivalent to `sc-js:46`. |
| S6 | **PASS** | `sc-js/…/02-install-pivots.md:46` carries the derivation clause verbatim; output **branches in three cases** (`:48`, `:68-70`, `:88-90`), `:70` reinforcing it. Targets **13 of 13** resolve on disk. |
| S7 | **FAIL** | `sc-js/…/03-clean.md:26` names `capabilities/styling/design-system.md`; `capabilities/styling/` holds only `css-transitions.md` → **12 of 13**. The guard `:38-45` has **no branch** for a missing reference. |

**The suite discriminates.** The positive control was free to fall and did not: `sc-js` genuinely derives its header, which is the model the four others must reach. *Reproduce-then-confirm* is satisfied — every pinned defect is red on current behaviour.

**Disclosed harness defects.**
- **Judge = suite author.** The suite was written in the same session that ran this judgement. Mitigation applied: the judge was ordered to measure first and deduce the verdict second, and to flag any disagreement with the suite's own "Expected FAIL" annotations. **Zero disagreement on 7 rows** — a clean result that is also, honestly, the weakest possible evidence against write-to-the-answer. S6 is the only real guard: it could have fallen.
- **The suite announces its expected verdicts** in the *Instruction pinned* column. Inherent to the 6-column form; open defect, not corrected here.
- The judge read no Results log — it was empty.

**Frictions raised, and what was done.** Fixture paths in the preconditions block omitted the `_code\` segment; S2 stated a fact rather than a falsifiable criterion; S3 and S4 named fixtures that do not carry the declared stack; S1 was filed under one defect family while exhibiting both. **All corrected below, after this run.** One judge conclusion was *not* adopted: it reported that no `rusqlite` fixture exists — `lyremember\_code\app\rust-backend\Cargo.toml:10` declares it, and S4 was re-anchored there rather than moved to `email-to-markdown`.

⚠ **The rows were amended after this run.** The verdicts above stand for the text as judged; the corrections are editorial (anchors, paths, criterion wording) and change no pinned behaviour, but a run 2 is what would re-validate them.

### 2026-08-03 — run 2 (post-fix), on the corrected installers

**6 PASS · 0 FAIL · 1 N/A** on 7. Judge: one subagent, **fresh context, author of neither the suite nor the fixes**, dry-run READ-ONLY, sources read in `plugins/`. Target: the working tree of parts 1–4 (six installer actions edited, one deleted).

| # | Before | After | Verdict of the delta |
|---|--------|-------|----------------------|
| S1 | FAIL | **PASS** | Both required remedies applied. The three orphan declarations are **removed** (`references/` holds 9 files, the table declares 9) — the alternative the row itself allowed, publish-or-withdraw, resolved by withdrawal. The frozen `12 files written` is gone: `:38` derives `<n>`, `:42` carries an example marker, `:50-52` adds the not-found branch, `:54` the total-failure header. |
| S2 | FAIL | **N/A** | **The intended outcome, written into the row at run 1 — not a suite debt.** `sc-css/skills/sniff/actions/02-install-pivots.md` no longer exists (arbitration A1 of part 4); no residual reference anywhere in the plugin. A vanished target is unjudgeable, never red. The row is now an **archive**: it attests to the removal and contributes nothing to coverage. It should be marked closed rather than replayed. |
| S3 | FAIL | **PASS** | The single unconditional block is gone. Three cases (`:41` A, `:62` B, `:83` C), derivation clause at `:39`, reinforced at `:64-66`. Sources 6/6. On the WordPress fixture the header is now derivable instead of announcing Laravel and Eloquent installed. |
| S4 | FAIL | **PASS**, with a residue named below | The pinned *mechanism* — the frozen block — is gone (`:37` clause, three cases at `:39`/`:57`/`:78`). The pinned *symptom* persists: the Case A illustration `:44-49` still names `axum`, `sqlx`, `diesel` and **not `rusqlite`**. Judged PASS for consistency with the standard the suite applies to its own positive control, which passes while naming 3 of its 13 targets. |
| S5 | FAIL | **PASS** | The clause whose absence the row pinned is present at `:49`, word for word identical to `sc-js:46`. Three cases at `:51`/`:70`/`:91`. Declaration tables unchanged, sources 9/9. |
| S6 | PASS | **PASS** | Positive control holds, **and for the measured reason**, not by carry-over: `:46` verbatim, real three-case branching, 13/13 targets resolve. It was free to fall — the same wave of edits deleted a source in `sc-python` (`capabilities/ap/django-activitypub.md`). |
| S7 | FAIL | **PASS** | `:18` announces **12** paths, `capabilities/styling/design-system.md` is out, 12/12 resolve. The missing guard branch exists at `:20`: a candidate with no plugin reference is skipped and reported, never deleted. Example arithmetic recalculated (`:67-69`, 5 + 1 + 6 = 12). |

**No `PASS → N/A` in this run** — no suite debt was created. The single `FAIL → N/A` is S2, the one the suite declared in advance as its nominal outcome.

**Five nominal disagreements with the run-1 annotations**, all in the same direction (annotated *Expected FAIL*, measured PASS): S1, S3, S4 (partial, see below), S5, S7. The judge was told the *Instruction pinned* column predates the fix and that *Expected FAIL* is no longer a valid expectation; it re-localised every anchor by meaning, the line numbers having moved on five files.

**Residues left open, none of them a regression.**
- **S4 is now ambiguous and should be rewritten.** Its criterion asserts that `rusqlite` "must appear in the outcome" and evidences this by "the frozen block never names it". The two propositions have come apart: the block is no longer frozen, the illustration still does not name it. Measured coverage of the Case A illustration: `sc-php` 6/6, `sc-rust` 3/4, `sc-python` 4/9, `sc-js` 3/13. A body at 75 % **reads as exhaustive** where one at 23 % reads as an extract — `sc-rust` is the most exposed to literal copying. Either the row demands an example marker (as `01-install.md:42` now carries), or it drops the naming requirement and keeps only the branching. As written it licenses two opposite readings.
- **The four `sniff` installers derive the header and nothing else.** The Case A bodies remain fixed text without an example marker — exactly what S6 warned about at run 1 (*lift `:46` and `:70`, not the blocks*). No scenario pins this as a pass criterion, so no row can fail on it. The only installer that shows the remedy is `01-install.md:42` — the one nobody took as a model.
- **S1's precondition is dead.** The row states "four data pivots are declared; three do not exist" — the table declares one. The row survives only because its *criterion* (the count is not frozen) outlives its *situation*.

**What the suite discriminates now, and what it no longer does.** It has changed function: at run 1 it separated honest installers from lying ones; all seven rows now fall on the same side. It still measures **degrees of derivation** — S1 overtakes the positive control (the only one with both an example marker and a dedicated missing-source branch), and the correction wave demonstrably followed S6's instruction, lifting the clause and the branching rather than the bodies. But **the negative control is gone**: with no red left in the *frozen output* family, the positive control alone no longer establishes that a faulty case would be caught. This is a non-regression suite now, not a reproduction one — structural, and not fixable by editing a row.

**Harness defects: one closed, one worsened.**
- **Closed — judge = suite author.** Fresh context, no part in writing the suite or the fixes, and 5 disagreements on 7 with the displayed expectations — the inverse of run 1's zero-disagreement, which was its own admission of weakness.
- **Worsened — the *Instruction pinned* column announces verdicts that are now false on 5 rows of 7.** At run 1 it was biasing; it is now actively misleading. A judge that copies it returns six wrong FAILs. The column needs rewriting before a run 3, or the annotations need moving out of the scenario rows.

**Non-mutation guard.** No write-class command of any kind; no `git` command in `email-to-markdown\_code\app` (*dubious ownership*), no `git config`. `find -newermt` over the fixtures returned zero results; all fixture mtimes predate the session. Declared for honesty: `lyremember\_code\app\.git` carries a directory mtime inside the session window with no file changed under it — attributed to an external process, reported rather than omitted.

### 2026-08-03 — suite revision, after run 2 and judged by no run

**Three of run 2's own findings applied to the suite, none to a target.** No skill, action or reference file was edited by this revision; the verdicts above stand unchanged.

- **The *Instruction pinned* column is removed.** Its content moved to *Appendix — instruction measurements by run*, dated and marked non-rebasable, and the rows lost their `Expected FAIL` / `PASS is the expected result` annotations. This closes the harness defect disclosed at both runs and worsened at run 2.
- **S8 added — the negative control the *frozen output* family lost.** Its subject is the residue run 2 named and no row could fail on: the illustrated body. Measured 0 of 4 on the `sniff` installers against `01-install.md:42`. **Not yet judged** — it enters the tally at run 3, and until then the family's red is documented but not adjudicated.
- **S4 narrowed and S2 archived.** S4 drops the naming requirement its run-2 verdict found ambiguous, keeping only the branching; the naming question is S8's, where it applies to four installers instead of one. S2 is marked closed rather than replayable. **S1's dead precondition is also repaired** — the row now states its criterion without asserting a count that the fix has changed.

**What a run 3 owes this suite.** Grade S8 for the first time, and re-grade S1, S3–S7 against criteria that no longer carry an announced verdict — the first run whose judge cannot read the answer off the page even by accident.
