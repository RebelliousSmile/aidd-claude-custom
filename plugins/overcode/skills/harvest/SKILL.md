---
name: harvest
description: Global maintenance skill — reconciles tracker items with implemented AIDD plan directories and legacy processed plans, harvests durable decisions, purges eligible task artifacts, and reviews what remains
author: François-Xavier Guillois
version: 4.7.0
vibe_version: ">=1.0.0"
permissions:
  - files
  - bash
tags:
  - collection
  - workflow
  - automation
  - productivity
  - data-mining
---

Read [host portability](../../references/host-portability.md) before resolving plugin files, invoking sibling skills, or persisting project guidance.

# Harvest — global plan and tracker maintenance

## Purpose

Clean up the growing `aidd_docs/tasks/` tree, close orphan tracker items, reconcile memory and rules accumulated by `/learn`, then methodically review every remaining task artifact. Modern AIDD work is owned by a feature directory containing `plan.md` and `phase-<n>.md`; plan lifecycle is read from `plan.md` frontmatter, never from a filename suffix.

## Processing order

1. Completed plans and ephemeral files first (phases 2–5)
2. Remaining files next, by type (phase 6)

## Rules

- Never close a tracker item without showing the closing comment to the user
- Never delete files without explicit confirmation
- Use only the CLI detected in Phase 1 for tracker operations (never MCP)
- Shell commands adapted to the OS detected in Phase 1

## Configuration (defaults, overridable via argument)

| Parameter | Default | Description |
|---|---|---|
| `plan_warn_days` | 14 | Age above which an active plan is flagged |
| `plan_stale_days` | 60 | Age above which an active plan is proposed for deletion |
| `audit_stale_days` | 90 | Age above which an audit is flagged |
| `rule_elevation_threshold` | 3 | Minimum number of decisions on the same topic to propose rule elevation |

If the user passes an argument (e.g. `/harvest plan_stale_days=30`), use the provided value.

---

## Phase 1 — Full inventory

Detect the OS from the session context **once** and remember it for all subsequent phases.

Detect the tracker type **once** and remember it:

| Priority | Tracker | Detection |
|---|---|---|
| 1 | **GitHub** | `gh repo view` returns without error |
| 2 | **GitLab** | `glab repo view` returns without error |
| 3 | **Local** | User stories present in `aidd_docs/tasks/` (type 5 below) |
| 4 | **None** | None of the above |

List every `.md` file in `aidd_docs/tasks/`:

```bash
# macOS / Linux
find aidd_docs/tasks -type f -name "*.md" | sort

# Windows (PowerShell)
Get-ChildItem -Recurse -Filter "*.md" aidd_docs/tasks | Sort-Object Name | Select-Object -ExpandProperty FullName
```

Build **feature-directory records first** for every `aidd_docs/tasks/<yyyy_mm>/<feature>/plan.md`: read its frontmatter `status`, enumerate its sibling `phase-<n>.md` and optional `review.md`, and treat those files as one plan unit. Do not count files owned by a feature directory again as loose plans, checklists or reviews.

Then classify feature directories and remaining loose legacy files in this order:

| Priority | Type | Detection | Action |
|---|---|---|---|
| 1 | **Completed feature directory** | direct `plan.md` has `status: implemented` or `status: reviewed` | Harvest the directory → purge its enumerated files if eligible |
| 2 | **Active feature directory** | direct `plan.md` has `status: pending`, `in-progress`, or `blocked` | Review as active or abandoned; never infer completion from phase contents |
| 3 | **Legacy completed plan** | loose `*.processed.md` | Harvest → purge if eligible |
| 4 | **Loose review** | `*.review*.md` outside a feature directory | Purge if eligible |
| 5 | **Journey** | `*.journey.md` outside a feature directory | Purge if eligible |
| 6 | **Audit** | `aidd_docs/tasks/audits/**` (directory) | Review by age |
| 7 | **User story** | frontmatter `type: user-story`, or `# User Story` / `## Acceptance Criteria` in content, or `story-` prefix | Purge if tracker item closed or `status: done` |
| 8 | **Legacy checklist / phase** | loose `*checklist*` or `*phase-[0-9]*`; sibling phases inside a feature directory stay owned by it | Purge if tracker item closed |
| 9 | **Legacy sub-plan** | `-part-[0-9]` or `-master` in name **AND** a sibling `-master.md` or `-master.processed.md` exists | Apply legacy master rules |
| 10 | **Legacy active plan** | remaining loose `.md` file | Review as active or abandoned |

Any other `status` value or malformed/missing frontmatter on a feature `plan.md` is **invalid**, not active: report it and exclude the directory from closure and purge until corrected.

Print the per-type summary: N completed feature directories, N active feature directories, N legacy processed plans, N loose reviews, N journeys, N audits, N user stories, N legacy checklists, N legacy sub-plans and N legacy active plans.

---

## Phase 2 — Tracker reconciliation

This phase's behavior depends on the tracker detected in Phase 1.

### Tracker: GitHub

Check the total item count:

```bash
# macOS / Linux
gh issue list --state all --json number | jq 'length'

# Windows (PowerShell)
gh issue list --state all --json number | ConvertFrom-Json | Measure-Object | Select-Object -ExpandProperty Count
```

If total ≤ 200: single query:

```bash
gh issue list --state all --limit 200 --json number,state,title,url
```

If total > 200: two separate queries, concatenate results:

```bash
gh issue list --state open   --limit 500 --json number,state,title,url
gh issue list --state closed --limit 500 --json number,state,title,url
```

### Tracker: GitLab

```bash
glab issue list --all --output json
```

If pagination is needed, use `--page` and `--per-page 100`.

### Tracker: Local (user stories only)

Read each user story. An item is considered **closed** if its frontmatter contains `status: done` or `status: closed`. No network calls.

### Tracker: None

All completed feature directories and legacy `.processed.md` files are treated as group C — Phase 3 is skipped.

---

### Extracting the associated tracker item

For each completed plan root — modern `<feature-directory>/plan.md` first, legacy `.processed.md` second — extract the tracker identifier in this order:
1. Frontmatter `issue_number:` or `tracker_id:`
2. Filename: `issue-42` prefix, `#42-` segment, or `story-slug`
3. Content: `Fixes #42`, `Closes #42`, `**Issue:** #42`, `**Story:**`
4. Fully-numeric isolated segment (`-42-` only if not preceded by a `YYYY_MM_DD` date)

Build the association table. Files inside a modern feature directory inherit that directory's group directly. For every loose review variant, `.journey.md`, user story, checklist and legacy sub-plan, find a modern feature directory or legacy processed/active plan with the same slug and inherit its group.

**Base matching for loose legacy artifacts** — use the modern feature-directory name or the legacy filename, then strip the leading date prefix and lifecycle suffix before comparing. Reviews and plans may have different `YYYY_MM_DD`:

- `2026_05_07-#83-firebase-bundle-split.review_code.md` → slug `#83-firebase-bundle-split`
- `2026_05/2026_05_06_#83-firebase-bundle-split/plan.md` → directory slug `#83-firebase-bundle-split`
- `2026_05_06-#83-firebase-bundle-split.processed.md` → slug `#83-firebase-bundle-split`
- → either plan form matches the loose review, which inherits its group

Only fall back to "orphan" if no modern feature directory or legacy active/processed plan shares the slug.

### Groups

- **A — Tracker item open with completed plan** → close in Phase 3, then purge the completed feature directory or legacy processed plan in Phase 5
- **B — Tracker item closed** → purge directly in Phase 5
- **C — No tracker item detected** → purge directly in Phase 5 (Phase 3 skipped — internal or direct task)

---

## Phase 3 — Tracker item closure (group A)

**If group A is empty → skip directly to Phase 4.**

For each item in group A, read the template:

```
aidd_docs/templates/custom/close-issue.md
```

Fill the variables in this order:
- `{Branch}`: from the plan (`**Branch name**`)
- `{PR}` / `{MR}`: search for a PR/MR associated with the branch — if none, set to `none`
- `{Done}`: summary line from `## Summary` or `## Objectif` in the plan
- `{Changelog}`: scope and type inferred from the plan
- `{Plan}`: relative path of the modern feature directory's `plan.md`, or of the legacy `.processed.md`
- `{Notes}`: summary of the associated `.review.md` if present, otherwise omit the section

Write the comment to a temporary file:

```bash
# macOS / Linux: /tmp/harvest-close-<n>.md
# Windows     : $env:TEMP\harvest-close-<n>.md
```

Show it to the user and **wait for confirmation** before posting.

**GitHub:**
```bash
# macOS / Linux
gh issue comment <n> --body-file /tmp/harvest-close-<n>.md && gh issue close <n>

# Windows
gh issue comment <n> --body-file "$env:TEMP\harvest-close-<n>.md" && gh issue close <n>
```

**GitLab:**
```bash
# macOS / Linux
glab issue note <n> --message "$(cat /tmp/harvest-close-<n>.md)" && glab issue close <n>

# Windows
glab issue note <n> --message (Get-Content "$env:TEMP\harvest-close-<n>.md" -Raw) && glab issue close <n>
```

**Local (user story):**
Update the user story's frontmatter: `status: done`.

The `&&` ensures the item is only closed if the comment was posted successfully.

---

## Phase 4 — Memory & normative-load reconciliation (sub-skill)

This phase is delegated to the `reconcile-normative` skill:

```markdown
@../reconcile-normative/SKILL.md
```

Invoke the skill, wait for its user confirmations, collect the returned metrics (entries migrated, rules enriched, duplicates merged, contradictions resolved, patterns elevated, obsolete decisions, rules flagged in the freshness pass) and merge them into the Phase 7 final report.

`reconcile-normative` can also be invoked standalone outside harvest when the user wants a normative audit without tracker/file lifecycle work.

---

## Phase 5 — Purge of ephemeral files

**Order constraint**: Phase 4 must complete before Phase 5. A completed feature directory or legacy `.processed.md` may contain a normative slice that Phase 4 needs to elevate — purging first destroys the source. Never reorder.

Since `aidd-context:10-learn` already ran during `endtask`, a completed feature directory can be purged as soon as its tracker item is confirmed closed. `status: implemented|reviewed` in `plan.md` is the completion marker; no rename or extra suffix is expected. Legacy `.processed.md` remains eligible under the same rule.

Eligibility criteria:

| Type | Purge condition |
|---|---|
| Completed feature directory group A | Tracker item closed in Phase 3; enumerate `plan.md`, declared phases, `review.md` and other files in the directory for the confirmation |
| Completed feature directory group B | Tracker item already closed; enumerate the directory's files for the confirmation |
| Completed feature directory group C | No tracker item — enumerate the directory's files for the confirmation |
| Legacy `.processed.md` group A/B/C | Same group rules as before |
| Loose `.review*.md` | completed plan root of the same slug (any group) — or orphan with no completed **nor active** plan root of the same slug |
| `.journey.md` | completed plan root of the same slug (any group) — or orphan with no completed **nor active** plan root of the same slug |
| Audits | **Never purged here** — handled in Phase 6 |
| Other types | **Never purged here** — handled in Phase 6 |

Build the eligible-files list. For a feature directory, list every file explicitly; never delete the directory recursively or include an unenumerated file. Display each relative path with its modification date. Ask for a single confirmation:

> "Delete these N files? (irreversible)"

```bash
# macOS / Linux
rm <file1> <file2> ...

# Windows (PowerShell)
Remove-Item -Path "<file1>", "<file2>", ...
```

---

## Phase 5b — Code and documentation freshness audit (taste)

This phase is delegated to the `taste` skill:

```markdown
@../taste/SKILL.md
```

Run both modes in sequence:

1. **assess-doc scan mode** — scan all `.md` files remaining after Phase 5 (oldest-first). Skip files already purged in Phase 5.
2. **assess-code** — scan the project source directories detected in Phase 1 (e.g., `src/`, `app/`, `components/`). Skip `node_modules/`, `.git/`, `vendor/`, `dist/`.

Collect the returned metrics and merge them into the Phase 7 final report:
- N docs Obsolète, N docs Partiel, N docs Current
- N code findings (by type: missing import, missing function, rule violation, stale comment)

`taste` can also be invoked standalone outside harvest when the user wants an obsolescence check without tracker/file lifecycle work.

---

## Phase 6 — Methodical review of remaining files

Analyze each type below and **collect** all proposed actions without acting. Present the consolidated table at the end of the phase, then wait for a single confirmation before acting.

### 6a — User stories

For each user story, check the associated tracker item (same extraction as Phase 2):
- Tracker item **closed** or frontmatter `status: done` → collect: **delete**
- Tracker item **open** → collect: **keep**, flag
- **No tracker item** → collect: **needs clarification** (ask the user)

### 6b — Checklists and intermediate phases

For a `phase-<n>.md` inside a modern feature directory, inherit the directory decision; never classify or delete the phase independently. For each loose legacy checklist/phase file:

- Its modern plan root is completed, or its legacy master is `.processed.md` → collect: **delete**
- Its modern or legacy master plan is still active → collect: **keep**
- **No master found** → collect: **orphan — needs clarification**

### 6c — Sub-plans (`-part-N`, `-master`)

These are legacy-only rules; modern phased work uses a feature directory and is handled as one unit. For each loose master (`-master.md`):
- A `-master.processed.md` file **exists** → collect: **delete** all associated `-part-N`
- No `.processed.md` yet but **associated tracker item closed** (same extraction as Phase 2) → collect: **delete** the master AND all its `-part-N` (legacy work done, completion marker absent)
- No `.processed.md` yet and tracker item **open or absent** → collect: **keep**

For each `-part-N` with no detectable master → fall back to Active plan (Phase 6d).

### 6d — Active plans potentially abandoned

For each active modern feature directory (`plan.md` status `pending`, `in-progress`, or `blocked`), compute age from the directory's leading `YYYY_MM_DD` or its `plan.md` modification date. Apply the same age table below to the directory as a unit. Never treat `phase-<n>.md` as separate active plans.

Apply the same logic to each remaining loose legacy `.md` plan (not processed, user story, checklist, or sub-plan):

Compute age from the date in the filename (`YYYY_MM_DD`) or from the modification date.

| Age | Collected action |
|---|---|
| < 14 days | **keep** — probably in progress |
| 14–60 days | **needs clarification** — still active, abandoned, or waiting for implementation? |
| > 60 days | **delete** — abandoned plan |

For plans whose associated tracker item is **closed** (regardless of age) → collect: **delete**. Apply the same extraction rules as Phase 2 (frontmatter, filename, content) to find the tracker identifier.

For a modern feature directory with `review.md` but a plan still `pending`, `in-progress`, or `blocked` → collect: **needs clarification** (ask whether implementation must resume or the plan status/report is inconsistent). Never infer `implemented` from the review file.

For loose legacy plans with a `.review*.md` of the same slug and created the same day → collect: **needs clarification**. A review file alone does not prove completion and never justifies an automatic delete or a `.processed.md` rename.

### 6e — Active plans without tracker item nor sufficient age

Completed feature directories and legacy `.processed.md` group C plans are purged in Phase 5 — this section no longer covers them.

For active modern feature directories or loose legacy plans with no detected tracker item and within the 14–60 day band (Phase 6d "needs clarification"): ask whether the plan is still active, abandoned, or whether a tracker item should be created to track it.

### 6e-bis — Group C cluster signal

If Phase 5 purged ≥ 5 completed feature directories and/or legacy `.processed.md` group C plans sharing a thematic prefix (same feature area, same `perf-*`, `psi-*`, etc. slug fragment), surface to the user:

> "N plans groupe C purgés sur le thème `<slug>`. Workflow drift possible : `endtask` exécuté sans tracker associé. Créer une issue de tracking rétroactif ?"

Never silent — recurring group C is a signal, not a normal mode.

### 6f — Audits

For each file in `audits/`:

| Age | Collected action |
|---|---|
| < 90 days | **keep** — recent snapshot |
| > 90 days | **needs clarification** — still relevant or to delete? |

### Consolidated confirmation

Present the table of all collected actions:

| File | Type | Proposed action | Reason |
|---|---|---|---|
| `{path}` | feature directory / legacy plan / user story / checklist / sub-plan / group C / audit | delete / keep / needs clarification | {short reason} |

Resolve **needs clarification** rows first by asking grouped questions. Once all decisions are made, ask for a single confirmation:

> "Apply these N deletions? (irreversible)"

---

## Phase 7 — Final report

Fill the report template:

```
aidd_docs/templates/harvest.md
```

Write the report to:

```
aidd_docs/harvests/YYYY_MM_DD-harvest.md
```

`aidd_docs/harvests/` is a reports directory — it is never scanned by Phase 1 and its files are never purged.

The report must include the metrics returned by Phase 4 (`reconcile-normative`) and Phase 5b (`taste`):

| Section | Metrics to include |
|---|---|
| Tracker | Items closed, files purged (by group) |
| Normative | Entries migrated, rules enriched, duplicates merged, patterns elevated, obsolete decisions, rules refreshed |
| Freshness | Docs Obsolète / Partiel / Current; code findings by type (missing import, missing function, rule violation, stale comment) |
| Files reviewed | Actions taken per type (Phase 6) |

Display the full report. If 0 actions taken → "Nothing to do — directory clean."
