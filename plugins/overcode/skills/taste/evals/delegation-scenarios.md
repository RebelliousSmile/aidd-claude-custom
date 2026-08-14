# Taste freshness and delegation scenarios

Each scenario is scored as Situation → Expected behavior → Pass criteria. Fixtures are read-only and do not target a real project.

## Target and fixture

- Target: `../SKILL.md`, both files under `../actions/`, both files under `../assets/`, and `../../../references/aidd-delegation.md`.
- Populated fixture: this repository after the weighted-freshness refactor, plus the exact weighted claim set, decision evidence, catalogue state, and file count stated in each row. Numeric boundary cases are complete inline data fixtures; no project file is mutated.
- How to run: use `overcode:behave run`, read the target and repository read-only, and judge verdict math, qualification, intended delegation, and forbidden local code analysis. T2 is the positive threshold control; T12 is the negative removed-engine control.

| ID | Situation | Expected behavior | Pass criteria |
|---|---|---|---|
| T1 | Weighted fixture produces 19% local evidence. | Verdict Obsolete. | Exact point totals shown. |
| T2 | Boundary fixtures produce 20%, 79%, and 80%. | Verdicts Partial, Partial, Current. | Same result in single-file worker and aggregation. |
| T3 | Overall local score is 85%, but one critical claim is obsolete. | Veto Current and Superseded. | Verdict Partial; critical evidence named. |
| T4 | Document has no eligible local claim. | Return N/A with no percentage. | No division by zero or invented evidence. |
| T5 | Decision is 90% current and its subject-matched replacement is implemented. | Superseded precedes Current. | Replacement location and relationship are cited. |
| T6 | Decision references one unrelated closed issue. | Do not apply Superseded. | Signal appears under unmatched evidence. |
| T7 | Document mixes local paths and an external market-share claim. | Score local paths; delegate extracted external text to fact-check. | Source file unchanged; fact-check artifact separate. |
| T8 | Fact-check is absent. | Mark external-unverified and qualify the local verdict. | No local fallback and no unqualified global Current. |
| T9 | Scan finds 60 Markdown files. | Prioritize and assess 25 by default. | All 35 unscanned paths and `25/60` coverage are reported. |
| T10 | Codex and Claude Code receive the same dependency-deprecation code request. | Delegate audit pillar `dependencies` through native syntax. | Same canonical receipt and no language detector. |
| T11 | Broken import or compilation concern is explicit. | Delegate `aidd-dev:03-assert`. | No regex import resolver executes. |
| T12 | A removed language reference or detector is restored. | Reject the fixture. | Any active reference to the removed engine fails. |

## Results log

### 2026-08-14 — run 1 (initial, dry-run, target=taste freshness, fixture=my-marketplace + inline claim sets) — **12/12 PASS**

Repository populated after the weighted-freshness refactor; threshold, decision, external-claim, catalogue and 60-file states supplied inline. Pre-flight checker: n/a.

| # | Behavior | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|---|
| T1 | 19% boundary | PASS | — | `01-assess-doc.md` › Single-file process/output. |
| T2 | 20/79/80 boundaries | PASS | — | `01-assess-doc.md` › Single-file/Scan process. |
| T3 | Critical veto | PASS | — | `01-assess-doc.md` › Single-file process step 6. |
| T4 | Zero eligible claims | PASS | — | `01-assess-doc.md` › Single-file process steps 3/5. |
| T5 | Subject-matched supersession | PASS | — | `decision-doc.md` › Subject-matched evidence. |
| T6 | Unrelated closed issue | PASS | — | `decision-doc.md` › Subject-matched evidence/Output. |
| T7 | Mixed local/external claims | PASS | — | `01-assess-doc.md` › Ground rules/steps 8–9. |
| T8 | Missing fact-check | PASS | — | `01-assess-doc.md` › steps 8–9. |
| T9 | Bounded scan | PASS | — | `01-assess-doc.md` › Scan process; `SKILL.md` › Transversal rules. |
| T10 | Cross-host dependency route | PASS | — | `02-assess-code.md` › Process; contract › Resolution. |
| T11 | Runnable import route | PASS | — | `02-assess-code.md` › Process/Boundaries. |
| T12 | Removed-engine control | PASS | — | `02-assess-code.md` › Boundaries; contract › Failure contract. |

**Frictions / gaps:** T12's automatic enforcement belongs to the repository structural guard; T9 determines `25/60` through selected/eligible fields rather than a mandated literal rendering.
**Tally:** 12/12 PASS (0 N/A) — initial green run, no fixture writes.
