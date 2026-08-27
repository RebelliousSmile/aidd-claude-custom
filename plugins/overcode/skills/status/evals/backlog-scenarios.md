# Status backlog — Safe document synchronization behavioural test scenarios

Behavioural tests for **status backlog** (`../actions/04-backlog.md`) — verifies the single aspect of safe, transactional synchronization of a Markdown `## Backlog` from GitHub or GitLab issues. Routing to the action remains covered by `scenarios.json`; this suite tests the action after routing.

> **Fixture / preconditions.** Run against the populated read-only fixture `fixtures/backlog/`: the five historical project documents, `github-milestones.md` (grouped stale block plus manual H3 traps), one invalid document, and the named issue/catalog page sequences in `cli-responses.json`. Historical arrays such as `github_open` and `gitlab_open` act as a first page followed by an empty page and use `catalog_empty_pages`. Treat `gh` and `glab` as available and successful only where a row says so, and treat a host as authenticated in `glab` only where a row says so. Reference fixture: `plugins/overcode/skills/status/evals/fixtures/backlog`. State the selected document, issue pages, catalog pages, availability, filter, and failure overlay in every run. A missing named fixture entry makes the row N/A, not FAIL.

## Scenarios

| # | Situation (input) | Expected behaviour | Pass criteria |
|---|---|---|---|
| S1 | **Positive control** — `status backlog fixtures/backlog/github-existing.md`; `gh` succeeds with `github_open`. | Normalize `acme/atlas`, retain only issues 12 and 9 in CLI order, replace the existing backlog, and report success. | The only intended document write replaces the single generated line `- [#4](https://github.com/acme/atlas/issues/4) — Ancienne entrée (open)`; resulting lines are `- [#12](https://github.com/acme/atlas/issues/12) — Corriger le formulaire d'inscription` then `- [#9](https://github.com/acme/atlas/issues/9) — Documenter le déploiement`, neither carrying a state suffix. Frontmatter, `### Notes historiques` with its text, and `## Décisions` remain byte-identical; no remote write is intended. |
| S2 | `status backlog fixtures/backlog/gitlab-insert.md`; `glab` succeeds with `gitlab_open`. | Parse the SCP-like URL as GitLab repo `acme/platform/boreal`, retain only issue 31, and insert the section before `## Objectifs`. | The sole intended write adds `## Backlog` after the H1 introduction with `- [#31](https://gitlab.com/acme/platform/boreal/-/issues/31) — Ajouter le suivi métier`, without a state suffix; frontmatter, introduction, and `## Objectifs` remain byte-identical. |
| S3 | GitHub input uses `git@github.com:acme/atlas.git`; `gh` succeeds with `github_open` and `catalog_empty_pages`. | Resolve the SSH/SCP form without shell interpolation and collect issues plus the complete catalogue. | Intended process arguments are exactly `gh api --paginate 'repos/acme/atlas/issues?state=open&per_page=100'` then `gh api --paginate 'repos/acme/atlas/milestones?state=all&per_page=100'`; each endpoint is one argument built from validated segments, with no concatenated shell command or remote mutation. |
| S4 | A valid GitHub document receives the `empty` response. | Replace or insert a single empty-state backlog and report zero open issues. | Intended section is exactly `## Backlog`, a blank line, then `_Aucune issue ouverte._`; no stale issue line survives and success reports `Open issues: 0`. |
| S5 | `status backlog fixtures/backlog/invalid-inputs.md` with no `git_repo`. | Stop before provider resolution or CLI execution and identify the missing frontmatter key. | Intended writes are empty, neither CLI is invoked, no success report appears, and the response contains `File unchanged.` |
| S6 | A document's scalar `git_repo` is `https://example.org/acme/atlas`; `glab auth status --hostname example.org` exits non-zero. | Treat the unknown host as a possible self-hosted GitLab only long enough to request authentication proof, then refuse it. | The sole intended CLI call is exactly `glab auth status --hostname example.org`; intended writes and issue-list calls are empty, the warning names the unproven host and refused value, and the response ends with `File unchanged.` |
| S7 | A valid GitLab document is selected but `glab` is unavailable. | Stop before network access and name the required missing CLI. | Intended writes and network calls are empty; the warning names `glab` and ends with `File unchanged.` |
| S8 | A valid GitHub document is selected; `gh` exits non-zero, authentication fails, or returns the `invalid` response. | Reject each failure before document construction. | For every overlay, intended document writes are empty; the response names provider, repo, useful cause, and `File unchanged.` without a success report. |
| S9 | The invalid fixture is overlaid with a valid GitHub `git_repo`, leaving its two real `## Backlog` headings. | Refuse the ambiguous replacement after successful issue parsing. | Intended writes are empty; the response reports multiple backlog sections and `File unchanged.` |
| S10 | A valid document is overlaid as UTF-8 with BOM and CRLF line endings; `gh` succeeds. | Preserve BOM, CRLF, frontmatter, and all bytes outside the changed section. | The intended atomic replacement keeps the original BOM and contains no lone LF; a diff outside the backlog span and required boundary newlines is empty. |
| S11 | `git_repo` is `https://github.com/acme/atlas.git; gh repo delete acme/atlas`. | Reject the ambiguous repository value and never evaluate its suffix as shell syntax. | Intended writes, remote writes, and CLI calls are empty; no shell-concatenated command exists and the response ends with `File unchanged.` |
| S12 | **Negative control** — a candidate implementation receives a non-zero `gh` result but still replaces `## Backlog` with a partial list. | The harness must reject this non-transactional implementation. | Any intended write after the failed fetch is an automatic FAIL, even if its Markdown formatting is otherwise correct. |
| S13 | `status backlog fixtures/backlog/github-notes-only.md`; `gh` succeeds with `github_open`; run twice, then a third time. | Insert the section and its block after the H1 introduction without absorbing the manual notes that run to the end of the file. | After both runs the checklist lines, the intranet link and the HTML comment remain byte-identical; the second and third runs produce identical bytes; the first run reports `Section: inserted`. |
| S14 | `status backlog fixtures/backlog/github-manual-section.md`; `gh` succeeds with `github_open`. | Recognize no generated block in the existing section and place the block at its head. | The block is inserted before `Priorités arbitrées en comité`, that sentence and the `- [#7](https://github.com/other-org/tools/issues/7)` line survive byte-identical in their original order, `## Décisions` is untouched, and the report reads `Section: inserted`. |
| S15 | `status backlog fixtures/backlog/github-existing.md`; `gh` succeeds with `github_open`; the section holds a generated block followed by `### Notes historiques`. | Replace the block alone and leave the H3 subsection in place. | The intended write spans only the generated lines; `### Notes historiques` keeps its heading and body, and the report reads `Section: replaced`. |
| S16 | **Negative control** — a candidate implementation extends the replacement from `## Backlog` to the end of the file when no `#`/`##` heading follows. | The harness must reject this implementation. | Any intended write covering a line outside the generated block is an automatic FAIL; the response must name the Step 5 rule bounding replacement to the generated block. |
| S17 | `status backlog fixtures/backlog/github-existing.md`; `gh` succeeds with `github_open`; the section holds the legacy line `- [#4](https://github.com/acme/atlas/issues/4) — Ancienne entrée (open)` written by an earlier version. | Recognize the legacy state suffix as part of the generated block and replace it. | The legacy line is gone from the result, the report reads `Section: replaced`, and the document holds exactly one generated block. |
| S18 | **Negative control** — a candidate implementation stops writing the state suffix but also stops recognizing it, so it inserts a fresh block at section head. | The harness must reject this implementation. | A result holding both the legacy suffixed line and a new block is an automatic FAIL; the response must name the Step 5 tolerance for an optional parenthesized state suffix. |
| S19 | `status backlog fixtures/backlog/gitlab-selfhosted.md`; `glab` is available and `glab auth status --hostname gitlab.interne.example` exits 0; the CLI succeeds with `gitlab_selfhosted_open` and an empty catalogue. | Recognize the self-hosted host through its proven authentication, paginate both resources, retain only issues 44 and 41, and replace the stale block. | After authentication, issue argv is `glab issue list --repo gitlab.interne.example/acme/portail/celeste --opened --page 1 --per-page 100 --output json`, followed by the empty issue page and `glab milestone list --repo gitlab.interne.example/acme/portail/celeste --include-ancestors --page 1 --per-page 100 --output json`; resulting flat lines link to issues 44 and 41, the `#18` line is gone, `## Objectifs` stays byte-identical, and the report reads `Repository: gitlab gitlab.interne.example/acme/portail/celeste` with `Section: replaced`. |
| S20 | Same document, but `glab auth status --hostname gitlab.interne.example` exits non-zero. | Refuse the unproven host before listing issues. | Intended writes are empty, `glab issue list` is never invoked, the warning names the unrecognized host and the refused `git_repo`, and the response ends with `File unchanged.` |
| S21 | **Negative control** — a candidate implementation treats any unknown host as GitLab from the URL shape alone, without checking authentication. | The harness must reject this implementation. | Reaching `glab issue list` — or any write — for a host whose authentication was not proven is an automatic FAIL; the response must name the Step 2 rule requiring proof rather than inference. |
| S22 | A valid `gitlab.com` document is selected; `glab` succeeds. | Pass the host explicitly even on the default provider host. | Every issue and milestone page uses `--repo gitlab.com/acme/platform/boreal`, never the bare `acme/platform/boreal`; the response must name the Step 3 rule on the local default host. |
| S23 | `status backlog fixtures/backlog/github-milestones.md`; use `github_issue_pages` and `github_milestone_pages`, without filter. | Exclude the pull request, attach by provider ID, and group every open issue in stable due-date order. | Headings appear in this order: Release Alpha dated 2026-09-15, Release Beta dated 2026-09-15, the escaped Roadmap title dated 2026-10-01, Version future undated, then `### Sans milestone`; issues remain in provider order inside each group, issue 11 is absent, and each retained issue appears once. |
| S24 | Same inputs with `--milestone "Version future"`. | Apply the exact local title filter after complete collection. | The block contains only heading `### Milestone: Version future — sans échéance` and issue 7; the report contains `Milestone: Version future`. |
| S25 | Repeat S24 with `--ml "Version future"`. | Treat the short option as a strict synonym. | CLI calls, retained issue set, resulting document bytes, and report are identical to S24. |
| S26 | A GitHub document uses `github_open` and `catalog_empty_pages`. | Preserve legacy presentation when the project has no milestone at all. | The block is the two historical flat issue lines in provider order and contains neither `### Milestone:` nor `### Sans milestone` nor a `Milestone:` report line. |
| S27 | A document uses `github_unassigned_issue_pages` with `github_milestone_pages`, without filter. | Show the unassigned group because the project does have milestones. | The only generated heading is `### Sans milestone`, immediately followed by issue 9; no empty milestone group is rendered. |
| S28 | Same complete GitHub inputs as S23 with `--milestone "Inconnue"`. | Treat an absent exact title as a successful empty selection, never as no filter. | The block is exactly `_Aucune issue ouverte._`; no issue or milestone heading remains, the report says `Open issues: 0` and `Milestone: Inconnue`. |
| S29 | Use `github_ambiguous_issue_pages`, `github_ambiguous_milestone_pages`, and `--milestone "Version 2"`. | Reject two catalogue entries with the same exact title as ambiguous. | All pages may be read, but intended writes are empty; the response names both provider IDs and ends with `File unchanged.` |
| S30 | Same complete GitHub inputs as S23 with `--milestone "version future"`. | Keep title matching case-sensitive. | The result is the same canonical empty state as S28, and no issue from `Version future` is rendered. |
| S31 | Exercise separately: unknown option, missing filter value, both aliases together, repeated filter, and an extra positional argument. | Close the public argument grammar before provider resolution. | Every variant has an empty CLI-call set and write-set, identifies the invalid form, and ends with `File unchanged.` |
| S32 | Exercise `github_duplicate_issue_pages`, then `github_duplicate_milestone_pages`, with otherwise valid counterpart data. | Reject identifiers repeated across pages transactionally. | Each variant reports the duplicate identifier, performs no write, and emits no success report. |
| S33 | Synchronize `github-milestones.md` with S23 inputs twice, then with `github_open` and an empty catalogue. | Replace the complete obsolete grouped block, remain idempotent, then transition grouped → flat. | Run 1 removes both obsolete groups while preserving `### Notes historiques`, its body, the isolated reserved-looking manual heading and its prose byte-for-byte; run 2 is byte-identical; run 3 leaves one flat generated block and no orphan generated heading. |
| S34 | Start from a legacy flat generated block, then use the S23 inputs. | Transition flat → grouped without duplication. | The old flat block is wholly replaced by the grouped block from S23; the section contains exactly one generated block. |
| S35 | Render the S23 Roadmap milestone whose raw title contains brackets, chevrons, emphasis and an accent grave. | Keep identity raw while making a safe single-line Markdown heading. | The heading is one physical line, displays remote characters as text, uses the mandated escapes, sorts by raw title/date, and filtering with the exact unescaped raw title selects issue 5. |
| S36 | Use `gitlab_issue_pages` and `gitlab_milestone_pages`, with and without `--ml "Sprint 1"`. | Paginate through the first empty page, include ancestor milestones, group like GitHub, and filter locally. | Unfiltered headings are Sprint 1 dated 2026-09-01, Plus tard undated, then Sans milestone; filtered output contains only issue 31. Calls include issue pages 1–3 and milestone pages 1–2, always with explicit `gitlab.com/...` repo. |
| S37 | **Negative control** — a candidate receives unknown filter `Inconnue` but silently renders every issue. | Reject fallback from an unmatched filter to the unfiltered backlog. | Any retained issue or group instead of the canonical empty state is an automatic FAIL; cite Step 3 exact-filter zero-match semantics. |
| S38 | **Negative control** — a candidate replacing the grouped block also consumes `### Notes historiques` or the isolated reserved-looking heading in `github-milestones.md`. | Reject over-broad generated-block recognition. | Any intended write over either manual subsection is an automatic FAIL; cite Step 5's immediate canonical-issue requirement and stop boundary. |
| S39 | On each provider, exercise its invalid issue page, invalid milestone page, and a command failure on a later issue or catalogue page. | Make either resource fully transactional across all pages. | Each variant has an empty write-set and no success report, names the failing provider/resource/page and ends with `File unchanged.`; a valid first page never leaks into the document. |
| S40 | Invoke `previously` without `--backlog`, with default depth and with `20`. | Preserve the historical snapshot path and optional depth. | `status backlog` is never invoked; the recent-report lookup, one status block and one three-agent snapshot occur as before, using depth 15 or 20 respectively. |
| S41 | Invoke `previously 20 --backlog fixtures/backlog/github-milestones.md --ml "Version future"` while a status report newer than seven days exists. | Synchronize before consulting the recent report, then produce one snapshot. | One byte-identical S25 backlog synchronization occurs first with depth retained as 20; output has one compact `Backlog: updated … (replaced)` receipt, one status block and one snapshot, but no backlog issue line, detailed issue count, or issue list derived from commits. |
| S42 | Invoke `previously --backlog fixtures/backlog/github-milestones.md --milestone "Release Alpha"` with no recent status report. | Synchronize, explicitly generate the missing report, then snapshot. | Call order is `status backlog` → recent-report lookup → literal `status report` → report read → one snapshot; bare `status` is never invoked and the only visible `Open issues` count belongs to the status block. |
| S43 | Compare `previously --backlog … --milestone "Version future"` and the corresponding `--ml` form under identical inputs. | Forward option spelling and value without changing backlog semantics. | Each invocation performs one synchronization and produces the same target bytes and issue selection; neither provider-native milestone filtering nor a second issue fetch from the git agent occurs. |
| S44 | Invoke `previously --backlog fixtures/backlog/github-milestones.md --ml "Version future"` with a failing catalogue page. | Make backlog synchronization a blocking precondition. | The document is byte-identical, output relays `File unchanged.`, and there is no recent-report lookup, `status report`, test/lint/git command, sub-agent, status block or snapshot. |

## How to run

Agent-as-status-backlog (dry-run, READ-ONLY on the fixture): load `../SKILL.md`, `../actions/04-backlog.md`, `../../../references/host-portability.md`, this suite, and every file under `fixtures/backlog/`. For each scenario, reason out the response, exact CLI argv, and precise intended document/remote writes; never invoke `gh`/`glab` and never modify the fixture.

**Decisive observables:** no document write precedes successful pagination and validation of both issues and milestone catalogue; identifiers are unique across pages, GitHub pull requests are excluded, and all error or ambiguity branches have an empty intended-write set. Successful writes affect one document atomically and preserve every byte outside the generated block, inside the section as well as outside it. A nonempty catalogue yields sorted groups keyed by provider ID; an empty catalogue yields the legacy flat block; an unmatched filter yields only the empty state. Displayed issue URLs occur only as the target of the leading `[#N]` link; written issue lines carry no state suffix while recognition still accepts one. No remote write or shell-concatenated command is intended; a host outside `github.com`, `gitlab.com` and `*.gitlab.io` reaches the network only after `glab auth status --hostname` proved it, and every GitLab `--repo` argument carries its host.

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

> Ce run précède le changement de borne du Step 5 (remplacement limité au bloc généré). Ses verdicts S1 à S12 reflètent l'ancienne règle : S1 y validait la suppression de `### Notes historiques`, ce que les critères actuels interdisent. À rejouer avant toute comparaison.

### 2026-08-27 — run 2 (migration, dry-run, target=status backlog, fixture=fixtures/backlog) — **18/22 PASS**

Action et fixtures relues depuis `status/`. Aucun CLI, réseau ou fichier de fixture touché. S6 a été aligné sur la preuve d'hôte auto-hébergé déjà exigée par S19–S21 ; le journal du run 1 reste historique et inchangé.

| # | Verdict | Note |
|---|---|---|
| S1 | PASS | Le bloc canonique seul est remplacé ; notes et décisions restent hors write-set. |
| S2 | PASS | La forme SCP GitLab et l'insertion avant `## Objectifs` restent inchangées. |
| S3 | PASS | L'argv GitHub reste séparé et identique après migration. |
| S4 | PASS | L'état vide canonique reste unique. |
| S5 | PASS | Le frontmatter invalide arrête avant CLI et écriture. |
| S6 | PASS | L'hôte inconnu atteint seulement la preuve `glab auth status`, puis s'arrête sans write. |
| S7 | PASS | `glab` absent arrête avant réseau. |
| S8 | PASS | Échec CLI, auth ou JSON invalide laisse le fichier inchangé. |
| S9 | PASS | Deux sections `## Backlog` restent une ambiguïté bloquante. |
| S10 | PASS | BOM, CRLF et octets hors bloc restent préservés. |
| S11 | PASS | La valeur injectée est rejetée avant argv. |
| S12 | FAIL | Contrôle négatif vivant : écriture après échec distant. |
| S13 | PASS | Trois passes préservent les notes et deviennent idempotentes. |
| S14 | PASS | Une section manuelle reçoit le bloc en tête sans absorber le lien tiers. |
| S15 | PASS | `### Notes historiques` reste byte-identique. |
| S16 | FAIL | Contrôle négatif vivant : remplacement étendu à la fin du fichier. |
| S17 | PASS | Le suffixe d'état historique reste reconnu mais n'est plus écrit. |
| S18 | FAIL | Contrôle négatif vivant : duplication du bloc historique. |
| S19 | PASS | L'hôte auto-hébergé prouvé conserve son argv et ses liens canoniques. |
| S20 | PASS | L'hôte non prouvé s'arrête avant `issue list`. |
| S21 | FAIL | Contrôle négatif vivant : inférence d'un GitLab sans preuve. |
| S22 | PASS | `gitlab.com` reste explicitement présent dans l'argument `--repo`. |

**Tally:** 18/22 PASS (0 N/A) — quatre rouges intentionnels, aucun défaut de migration de l'action ou des fixtures.

### 2026-08-27 — run 3 (milestones, dry-run, target=status backlog, fixture=fixtures/backlog) — **33/39 PASS**

Action, documents et séquences paginées relus depuis `status/`. Aucun CLI, réseau ou fichier de fixture touché. Les six rouges sont les contrôles négatifs vivants ; toutes les branches nominales et transactionnelles satisfont le contrat milestone.

| # | Verdict | Note |
|---|---|---|
| S1–S11 | PASS | Compatibilité du bloc plat, résolution provider, préservation et échecs avant écriture maintenues avec collecte issues + catalogue. |
| S12 | FAIL | Contrôle négatif : écriture après échec distant. |
| S13–S15 | PASS | Insertion, idempotence et préservation des sous-sections manuelles maintenues. |
| S16 | FAIL | Contrôle négatif : plage de remplacement étendue au contenu manuel. |
| S17 | PASS | Le suffixe d'état historique reste reconnu puis supprimé. |
| S18 | FAIL | Contrôle négatif : duplication d'un ancien bloc plat. |
| S19–S20 | PASS | Pagination sur instance GitLab prouvée et refus transactionnel de l'hôte non prouvé. |
| S21 | FAIL | Contrôle négatif : GitLab auto-hébergé inféré sans preuve. |
| S22–S28 | PASS | Hôte explicite, tri groupé, filtres long/court, catalogue vide, non assigné et filtre inconnu conformes. |
| S29–S32 | PASS | Ambiguïté, casse, grammaire fermée et doublons inter-pages arrêtent sans écriture. |
| S33–S36 | PASS | Transitions groupé/plat, idempotence, échappement hostile et pagination GitLab conformes. |
| S37 | FAIL | Contrôle négatif : filtre inconnu rabattu sur toutes les issues. |
| S38 | FAIL | Contrôle négatif : sous-sections manuelles absorbées par le bloc groupé. |
| S39 | PASS | Pages invalides ou en échec sur chaque ressource/provider annulent la synchronisation entière. |

**Tally:** 33/39 PASS (0 N/A) — six échecs intentionnels discriminants, aucun défaut réel du contrat milestone détecté.

### 2026-08-27 — run 4 (previously integration, dry-run) — **38/44 PASS**

Le contrat `previously`, son asset et le harnais ont été lus avec l'action backlog. Aucun rapport, sous-agent, CLI distant ou fichier de fixture n'a été réellement exécuté ou modifié.

| # | Verdict | Note |
|---|---|---|
| S1–S39 | Identique au run 3 | 33 PASS et les six contrôles négatifs S12/S16/S18/S21/S37/S38 restent discriminants. |
| S40 | PASS | Sans backlog, le flux et la profondeur historiques sont conservés. |
| S41 | PASS | La synchronisation précède même un rapport récent ; une quittance et un snapshot seulement. |
| S42 | PASS | L'absence de rapport déclenche littéralement `status report`. |
| S43 | PASS | Les deux orthographes sont transmises sans divergence ni résolution distante depuis git. |
| S44 | PASS | L'échec backlog arrête avant rapport et snapshot avec fichier inchangé. |

**Tally:** 38/44 PASS (0 N/A) — six contrôles négatifs intentionnels, aucune duplication d'issues dans `previously`.
