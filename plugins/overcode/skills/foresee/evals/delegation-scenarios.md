# Foresee delegation scenarios

Each scenario is scored as Situation → Expected behavior → Pass criteria. These fixtures do not mutate a real project.

| ID | Situation | Expected behavior | Pass criteria |
|---|---|---|---|
| F1 | Codex receives an unfinished plan path. | Resolve `aidd-refine:04-shadow-areas` and use Codex-native skill invocation. | Receipt names shadow-areas; no local scoring rubric or foresee history is used. |
| F2 | Claude Code receives completed work plus its agreed plan. | Resolve `aidd-refine:02-challenge` and use Claude-native invocation. | Both artifacts reach challenge; receipt is otherwise host-equivalent to F1. |
| F3 | A general code directory is supplied. | Delegate audit pillar `architecture`. | Exactly one audit route; no per-file local agents or improvement catalogue. |
| F4 | `aidd-dev` is absent. | Apply the common package-absent failure. | Package and minimum version are named; no local audit runs. |
| F5 | `aidd-dev` is below `2.4.1`. | Stop the affected branch as incompatible. | Installed and required versions are reported. |
| F6 | A manifest contains 80 dependencies. | Run AIDD audit, then horizon-analyze its top five only. | Scope is `5 of 80`; no sixth horizon profile exists. |
| F7 | The user supplies the same manifest with `--all`. | Announce count/cost and analyze the audit result set using native bounded execution. | Explicit flag is honored without model-specific instructions. |
| F8 | Maintainer metadata cannot be sourced. | Record continuity as `unknown` and reduce coverage. | Unknown is absent from the mean denominator and cannot improve horizon. |
| F9 | A prior local horizon report exists. | Compare only horizon signals. | AIDD CVE/version findings are linked, never copied into persistence. |
| F10 | A legacy detector/checklist is reintroduced into doc or code routes. | Reject the fixture. | Any local generic scoring/checklist makes the scenario fail. |
