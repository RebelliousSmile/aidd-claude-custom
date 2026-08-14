# Taste freshness and delegation scenarios

Each scenario is scored as Situation → Expected behavior → Pass criteria. Fixtures are read-only and do not target a real project.

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
