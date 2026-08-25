# Alias backlog — Safe document synchronization behavioural test scenarios

Behavioural tests for **alias backlog** (`../actions/11-backlog.md`) — verifies the single aspect of safe, transactional synchronization of a Markdown `## Backlog` from GitHub or GitLab issues. Routing to the action remains covered by `scenarios.json`; this suite tests the action after routing.

> **Fixture / preconditions.** Run against the populated read-only fixture `fixtures/backlog/`: two project documents, one invalid document, and recorded GitHub/GitLab CLI responses. Treat `gh` and `glab` as available and successful only where a row says so; their returned JSON is the named entry in `cli-responses.json`. Reference fixture: `plugins/overcode/skills/alias/evals/fixtures/backlog`. State the selected document, CLI response, availability, and failure overlay in every run. A missing named fixture entry makes the row N/A, not FAIL.

## Scenarios

| # | Situation (input) | Expected behaviour | Pass criteria |
|---|---|---|---|
| S1 | **Positive control** — `backlog fixtures/backlog/github-existing.md`; `gh` succeeds with `github_open`. | Normalize `acme/atlas`, retain only issues 12 and 9 in CLI order, replace the existing backlog, and report success. | The only intended document write replaces the bytes from `## Backlog` through `### Notes historiques`; resulting lines are `- [#12](https://github.com/acme/atlas/issues/12) — Corriger le formulaire d'inscription (open)` then `- [#9](https://github.com/acme/atlas/issues/9) — Documenter le déploiement (open)`. Frontmatter and `## Décisions` remain byte-identical; no remote write is intended. |
| S2 | `backlog fixtures/backlog/gitlab-insert.md`; `glab` succeeds with `gitlab_open`. | Parse the SCP-like URL as GitLab repo `acme/platform/boreal`, retain only issue 31, and insert the section before `## Objectifs`. | The sole intended write adds `## Backlog` after the H1 introduction with `- [#31](https://gitlab.com/acme/platform/boreal/-/issues/31) — Ajouter le suivi métier (open)`; frontmatter, introduction, and `## Objectifs` remain byte-identical. |
| S3 | GitHub input uses `git@github.com:acme/atlas.git`; `gh` succeeds with `github_open`. | Resolve the SSH/SCP form without shell interpolation and call the documented GitHub command. | Intended process arguments are exactly `gh`, `issue`, `list`, `--repo`, `acme/atlas`, `--state`, `open`, `--limit`, `1000`, `--json`, `number,title,state`; no concatenated shell command or remote mutation is intended. |
| S4 | A valid GitHub document receives the `empty` response. | Replace or insert a single empty-state backlog and report zero open issues. | Intended section is exactly `## Backlog`, a blank line, then `_Aucune issue ouverte._`; no stale issue line survives and success reports `Open issues: 0`. |
| S5 | `backlog fixtures/backlog/invalid-inputs.md` with no `git_repo`. | Stop before provider resolution or CLI execution and identify the missing frontmatter key. | Intended writes are empty, neither CLI is invoked, no success report appears, and the response contains `File unchanged.` |
| S6 | A document's scalar `git_repo` is `https://example.org/acme/atlas`. | Refuse the unsupported host before any CLI call. | Intended writes and CLI calls are empty; the warning names the refused value and ends with `File unchanged.` |
| S7 | A valid GitLab document is selected but `glab` is unavailable. | Stop before network access and name the required missing CLI. | Intended writes and network calls are empty; the warning names `glab` and ends with `File unchanged.` |
| S8 | A valid GitHub document is selected; `gh` exits non-zero, authentication fails, or returns the `invalid` response. | Reject each failure before document construction. | For every overlay, intended document writes are empty; the response names provider, repo, useful cause, and `File unchanged.` without a success report. |
| S9 | The invalid fixture is overlaid with a valid GitHub `git_repo`, leaving its two real `## Backlog` headings. | Refuse the ambiguous replacement after successful issue parsing. | Intended writes are empty; the response reports multiple backlog sections and `File unchanged.` |
| S10 | A valid document is overlaid as UTF-8 with BOM and CRLF line endings; `gh` succeeds. | Preserve BOM, CRLF, frontmatter, and all bytes outside the changed section. | The intended atomic replacement keeps the original BOM and contains no lone LF; a diff outside the backlog span and required boundary newlines is empty. |
| S11 | `git_repo` is `https://github.com/acme/atlas.git; gh repo delete acme/atlas`. | Reject the ambiguous repository value and never evaluate its suffix as shell syntax. | Intended writes, remote writes, and CLI calls are empty; no shell-concatenated command exists and the response ends with `File unchanged.` |
| S12 | **Negative control** — a candidate implementation receives a non-zero `gh` result but still replaces `## Backlog` with a partial list. | The harness must reject this non-transactional implementation. | Any intended write after the failed fetch is an automatic FAIL, even if its Markdown formatting is otherwise correct. |

## How to run

Agent-as-alias-backlog (dry-run, READ-ONLY on the fixture): load `../SKILL.md`, `../actions/11-backlog.md`, `../../../references/host-portability.md`, this suite, and every file under `fixtures/backlog/`. For each scenario, reason out the response, exact CLI argv, and precise intended document/remote writes; never invoke `gh`/`glab` and never modify the fixture.

**Decisive observables:** no document write precedes successful CLI execution and JSON validation; all error and ambiguity branches have an empty intended-write set; successful writes affect one document atomically and preserve bytes outside the backlog span; displayed issue URLs occur only as the target of the leading `[#N]` link; no remote write or shell-concatenated command is intended.

## Results log

<!-- Append dry-run results here. -->

### 2026-08-25 — run 1 (initial, dry-run, target=alias backlog, fixture=fixtures/backlog) — **11/12 PASS**

Fixture complète et lisible : documents GitHub, GitLab et invalide, plus réponses JSON `github_open`, `gitlab_open`, `empty` et `invalid`. Aucun CLI, réseau ou fichier de fixture touché. Pre-flight checker: n/a.

| # | Behaviour | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|---|
| S1 | Remplacement GitHub filtré et ordonné | PASS | — | `11-backlog.md` Steps 3–5 ; `github-existing.md` et `github_open`. |
| S2 | Insertion GitLab depuis URL SCP | PASS | — | Steps 2–5 ; `gitlab-insert.md` et `gitlab_open`. |
| S3 | Arguments GitHub séparés, sans shell concaténé | PASS | — | Steps 2–3 acceptent SCP et imposent des arguments séparés. |
| S4 | État vide canonique | PASS | — | Steps 4 et 6 ; réponse `empty`. |
| S5 | Frontmatter sans `git_repo` | PASS | — | `Context required` et Step 1 arrêtent avant CLI et écriture. |
| S6 | Hébergeur non supporté | PASS | — | Step 2 refuse la valeur avant tout CLI. |
| S7 | `glab` indisponible | PASS | — | Step 2 vérifie l'outil avant le réseau. |
| S8 | CLI, authentification ou JSON en échec | PASS | — | Step 3 impose fichier inchangé et avertissement utile. |
| S9 | Plusieurs sections backlog | PASS | — | Step 5 refuse l'ambiguïté après parsing, sans écrire. |
| S10 | Préservation BOM et CRLF | PASS | — | Steps 1 et 5 imposent conservation et écriture atomique. |
| S11 | Valeur `git_repo` ambiguë/injectée | PASS | — | Steps 2–3 refusent l'identifiant et interdisent la commande concaténée. |
| S12 | Écriture candidate après échec de `gh` | FAIL | — | Contrôle négatif : viole Step 1 (« aucune écriture avant réussite ») et Step 3 (« fichier strictement inchangé »). |

**Frictions / gaps:** S9 et S10 utilisent implicitement `github_open`, seule réponse GitHub valide cohérente avec leurs préconditions ; S10 décrit son BOM/CRLF par overlay plutôt que par un fichier physique distinct. S12 est l'échec intentionnel vivant de la famille transactionnelle, pas un défaut du target.

**Tally:** 11/12 PASS (0 N/A) — aucun défaut réel de l'action détecté ; S12 reste rouge comme contrôle négatif discriminant.
