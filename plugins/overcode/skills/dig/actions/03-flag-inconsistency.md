# Flag inconsistency

Handle a direct contradiction discovered between two quiz sources without interrupting the quiz.

## Inputs

- `file_1` and `file_2` — the conflicting paths.
- `description` — one sentence describing the contradiction.
- `evidence_1` and `evidence_2` — line references or short paraphrases proving both sides.

## Process

1. Verify both sources directly. A missing detail, ambiguity, or stylistic difference is not a contradiction.
2. Tell the user briefly that Ada found an inconsistency and name both paths.
3. Append `{ file_1, file_2, description, evidence_1, evidence_2 }` to `inconsistencies[]` in session context.
4. Continue the quiz. Do not create a task, plan, issue, or code change automatically.

At `end-session`, include the contradiction in the report. After presenting the final result, offer to turn verified findings into a separate task or plan; do so only if the user requests it.
