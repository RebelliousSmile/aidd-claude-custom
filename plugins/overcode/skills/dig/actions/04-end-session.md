# End session

Close the quiz, explain the result, and persist one complete report.

## Input

The completed session context from `02-run-quiz`.

## Process

1. Sum the question scores and normalize the displayed score to `/20` if the user accepted a shorter quiz.
2. Assign the grade:
   - 18–20: Excellente maîtrise 🏆
   - 14–17: Bonne compréhension ✅
   - 10–13: Base correcte, points à approfondir 📖
   - 0–9: Besoin de révision 🔄
3. Display the final score, each question's points and justification, and the concepts to revisit. Distinguish knowledge gaps from project coherence findings.
4. Fill `assets/quiz_report.md` from session context. Include evidence for every coherence finding and contradiction; write `none` when a section has no entries.
5. Create the report directory if needed, then write the report once to the reserved path. Never overwrite an existing file.
6. Return the report path.
7. If verified corrections exist, offer a separate follow-up. With explicit agreement, route planning to `aidd-dev:01-plan` when available; otherwise describe the unavailable capability and leave the report unchanged. Implementation and commits require their own explicit user request.
8. Offer another quiz with the same theme, a new theme, or the other source.

## Check

The report contains the final score, one row per question, source evidence, coherence findings or `none`, inconsistencies or `none`, and non-empty takeaways.
