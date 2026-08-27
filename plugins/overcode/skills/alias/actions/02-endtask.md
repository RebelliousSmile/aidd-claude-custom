# Endtask

Fires the pre-crafted prompt for the full **commit → resolve implemented plan directory → learn → merge/push → changelog → push tags → close issue** workflow.

## Context required

- All changes must be implemented; any review required by the caller or project must have passed.
- The work may be on a dedicated plan branch or directly on the target branch (e.g. `develop`).
- AIDD plans use a feature directory `aidd_docs/tasks/<yyyy_mm>/<yyyy_mm_dd>_<feature>/` containing `plan.md` and its `phase-<n>.md` files. Completion is the `status: implemented` frontmatter value in `plan.md`; the filename carries no lifecycle suffix.
- Issue number: resolved automatically after the plan directory is found. No match means no issue; do not ask.

## Prompt

Execute the following workflow verbatim:

### Step 1 — Commit

Commit all staged and unstaged changes with a conventional commit message that summarises the work done. Do not push yet.

### Step 2 — Detect branch mode

Run `git branch --show-current`. Record as `current_branch`.

- If `current_branch` is `main`, `master`, `develop`, or `staging`: set `has_plan_branch = false` and `target_branch = current_branch`.
- Otherwise: set `has_plan_branch = true` and determine `target_branch`:
  - If a branch name was passed as argument, use it.
  - Otherwise, inspect `git log --oneline --decorate HEAD` to detect the parent branch.
  - If still ambiguous, ask: *"Which branch should I merge `<current_branch>` into?"*

### Step 2b — Resolve the completed plan directory

Search `aidd_docs/tasks/**/plan.md` for the feature directory matching the current branch, task and recent commits. Read frontmatter rather than inferring lifecycle from a filename.

- Require `status: implemented`. Also accept `status: reviewed` when a review layer has advanced the same completed plan.
- Require every sibling `phase-<n>.md` declared by `plan.md` to exist and carry `status: done`.
- Record the feature directory as `plan_directory` and its `plan.md` as `plan_file`.
- Do **not** rename or move `plan.md`, the phase files, or their directory. The directory is the durable task record.
- Ignore another feature directory merely because its `plan.md` is implemented. If no unique match can be established, ask: *"Which feature directory in `aidd_docs/tasks/` contains the plan for this work?"*
- Legacy compatibility only: an existing `*.processed.md` may be read as a completed legacy plan, but never require or create `.pending.md`/`.processed.md` for a modern directory plan.

If the matching plan is `pending`, `in-progress`, or `blocked`, stop before merge and report that `aidd-dev:02-implement` must complete it; `endtask` never writes the plan lifecycle status.

### Step 2c — Detect issue number

Attempt to resolve `issue_number` from the following sources in priority order. Stop at the first match.

1. **Argument** — a number passed directly by the user (e.g. `endtask 42`).
2. **Branch name** — extract from `current_branch`: patterns `issue-42`, `#42`, `-42-`, or a leading numeric segment (e.g. `42-my-feature`). Ignore date-like segments (`YYYY`, `MM`, `DD`).
3. **Plan file frontmatter** — read `plan_file`; look for `issue_number:` or `tracker_id:`.
4. **Plan file content** — scan for `Fixes #42`, `Closes #42`, `**Issue:** #42`, `Ref: #42`.
5. **Recent commits** — run `git log --oneline -10`; scan messages for `#42`, `fix #42`, `close #42`.
6. **No match** — set `issue_number = none`. Do not ask.

### Step 3 — Verify the durable plan record

Confirm that `plan_directory`, `plan_file`, every declared phase and an optional `review.md` are tracked by Git. No archive rename is performed: `status: implemented` in `plan.md` is the completion marker.

### Step 4 — Capture learnings (auto-validate)

Invoke `/aidd-context:10-learn` on `plan_directory`, using `plan.md` as the primary source and its phase/review files only as supporting evidence.

**Auto-validate all proposed learnings without asking for confirmation** — save every entry that the skill surfaces. Do not pause or prompt the user at this step.

### Step 5 — Merge and push

**If `has_plan_branch = true`** (dedicated branch):
- `git checkout <target_branch>`
- `git pull`
- `git merge --no-ff <current_branch>` — if conflict, stop and ask user to resolve before continuing.
- `git push`
- `git branch -D <current_branch>`

**If `has_plan_branch = false`** (working directly on target branch):
- `git push`

### Step 6 — Changelog

Invoke `/overcode:changelog`: updates `CHANGELOG.md` from git history, commits the file, and creates an annotated tag for the new version.

### Step 7 — Push tags

```bash
git push --follow-tags
```

### Step 8 — Close issue

If an issue number was provided: close the issue using the tracker (GitHub or GitLab) and add a closing comment referencing the tag or commit.

If no issue number: skip this step silently.

### Step 9 — Report

| Field | Value |
|---|---|
| Commit | `<sha> <message>` |
| Plan completed | `<plan_directory>/plan.md` (`status: implemented|reviewed`) |
| Branch mode | `plan branch merged into <target>` or `direct commit on <target>` |
| Branch deleted | `<current_branch>` *(only if has_plan_branch)* |
| Tag | `<tag>` pushed |
| Issue closed | `#<n> <url>` or `—` |
