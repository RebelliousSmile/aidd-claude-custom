# Run quiz

Drive the interactive question loop. Ask exactly one question per turn and wait for the user's answer before scoring it.

## Input

The session context produced by `01-launch`.

## Output

An updated in-conversation context containing the scored questions and any coherence findings. Do not write the report during this action.

## Per-question loop

For every selected file:

1. Read the file fully enough to establish the question, expected answer, and source evidence. If the file is too large, inspect all relevant sections and record the bounded range used.
2. Compare it with the applicable project rules and already-read quiz sources. Record only evidenced violations, suspicious patterns, or direct contradictions; do not force a finding.
3. For a direct contradiction between two sources, read `03-flag-inconsistency.md` and follow it.
4. Alternate formats:
   - odd questions: multiple choice with four plausible options and one correct answer;
   - even questions: open question with an expected answer of one to three sentences.
5. Use the current difficulty:
   - easy: definitions and broad roles;
   - intermediate: relationships, flows, and conventions;
   - hard: edge cases, trade-offs, and architectural consequences.
6. Reveal only the current source and ask the question as `Question i/n · <path> · [Difficulty]`.
7. Wait for the answer, then score it:
   - multiple choice: 4 points on the first correct attempt; after a wrong answer, give one source-grounded hint and allow one retry worth 2 points; otherwise award 0 and explain the answer;
   - open: 4 complete and precise, 3 correct but incomplete, 2 right direction with important omissions, 1 one relevant element, 0 off-topic.
8. Give concise feedback grounded in the source and show the cumulative score.
9. Append `{ file, topic, points, justification, difficulty, evidence }` to `questions[]`; append real findings to the appropriate context arrays.
10. Raise difficulty after two consecutive 4/4 answers. Lower it after two consecutive scores of 2/4 or less. Keep it within easy–hard.

Do not apply any correction during the quiz.

## Check

At completion, every selected file produced exactly one answered question, the maximum score is four times the question count, and each expected answer is traceable to source evidence.
