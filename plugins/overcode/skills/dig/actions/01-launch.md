# Launch

Initialize the quiz without revealing the selected sources.

## Inputs

- `source` — `code` or `docs`; ask if the user did not specify it.
- `theme` — optional module, concept, or path filter; default to a representative spread.

## Output

Keep this session context in the conversation:

```text
source, theme, files[], report_path, difficulty=intermediate,
score=0, question_num=0, questions=[], coherence_findings=[],
inconsistencies=[], corrections=[]
```

## Process

1. Read applicable host instructions: the `AGENTS.md` chain on Codex, `CLAUDE.md` on Claude Code, and any project memory paths they reference.
2. Resolve active rule sources using the host-portability contract. Summarize only rules relevant to the selected scope.
3. Introduce yourself as Ada and resolve `source` and `theme` from the request, asking only for missing information.
4. If an active agent is modifying the selected scope, warn that questions may reflect in-progress files and continue only after confirmation.
5. Discover eligible files:
   - `code`: infer source roots and extensions from the repository, manifests, and project instructions; exclude generated, vendored, dependency, cache, and build-output directories.
   - `docs`: prefer `aidd_docs/memory/**/*.md`; if absent, use the project's documented memory or architecture area.
6. Apply the theme filter, if any, then select five distinct, substantive files with a representative spread. Do not reveal their paths yet.
7. If fewer than five eligible files remain, state the number and ask whether to run a shorter quiz or broaden the scope.
8. Reserve, but do not create, the report path. Prefer `aidd_docs/tasks/<YYYY_MM>/<YYYY_MM_DD>-quiz-<N>.md`; if `aidd_docs/` is absent, use `docs/quiz-sessions/<YYYY_MM_DD>-quiz-<N>.md`. Choose the first unused positive `N`.
9. Announce the number of questions and begin.

## Check

Before the first question, the context has distinct readable files, a collision-free report path, and no report file has been written.
