# Previously

Project snapshot (tests, git activity, working tree, lint) prefixed with a status summary and, when requested, a synchronized documentary backlog. If a status report from the last 7 days exists, use it; otherwise run the explicit `status report` action first.

## Context required

Accepted syntax after the `previously` action selector:

```text
previously [<depth>] [--backlog <file.md>] [--milestone <title> | --ml <title>]
```

- `<depth>` is the existing optional first positional value: a positive commit count or a duration such as `7d`. Default: 15 commits.
- `--backlog` accepts exactly one non-empty Markdown file path. `--milestone` and `--ml` are strict synonyms, accepted at most once and only with `--backlog`.
- Parse and validate the whole argument list before any file lookup, command, sibling action, or sub-agent. Reject an unknown option, extra positional value, duplicate option, missing value, orphan milestone filter, or depth placed after named options. On rejection, do no work.
- Preserve the selected spelling and values verbatim when forwarding the backlog request; do not reinterpret the filter as a native provider option.

## Prompt

### Step 1 — Parse arguments

Apply `Context required`. Keep the resolved depth, optional backlog file, and optional filter as separate values. With no `--backlog`, the remaining steps are the historical flow apart from their renumbering and the explicit `status report` spelling.

### Step 2 — Optional backlog synchronization

When `--backlog` is present, invoke the sibling `status` skill's `backlog` action before looking for a recent status report:

```text
status backlog <file.md> [--milestone <title> | --ml <title>]
```

Forward the file, option spelling and filter value verbatim as separate arguments. This step runs on every invocation carrying `--backlog`, including when a recent status report already exists.

- On success, retain only this compact receipt for the final output: `Backlog: updated <file.md> (inserted|replaced)`. Do not repeat the detailed backlog report, its issue count, headings, or issue lines.
- On failure, relay the useful cause and `File unchanged.`, then stop. Do not search for a status report and do not spawn snapshot agents.

### Step 3 — Status check

```bash
find aidd_docs/tasks/status -name "*.md" -mtime -7 2>/dev/null | sort -r | head -1
```

### Step 4a — Recent status exists

Read the returned file. Extract the **Project Summary** table and **Quick Wins** list. If Step 2 produced a backlog receipt, display it once immediately before this status block. Display:

```text
## Project Status (from <yyyy-mm-dd>)
| Metric | Value |
|--------|-------|
| Branch | `<branch>` |
| Tests | ✅/❌ N tests |
| Coverage | N% lines |
| Open issues | N |
| Quick wins | N |
```

### Step 4b — No recent status

Invoke the sibling action explicitly as `status report`, never bare `status`. Once complete:

```bash
ls -t aidd_docs/tasks/status/*.md 2>/dev/null | head -1
```

Read that file and display the same status block as Step 4a. If Step 2 produced a backlog receipt, display it once immediately before this status block. The `Open issues` count in this status block is the only issue count added by `previously`.

### Step 5 — Project snapshot

Spawn 3 haiku sub-agents in parallel (background: true). Use the resolved depth; default to 15 commits.

**Agent "git"** — branch, activity, working tree:
- `git branch --show-current`
- `git log --oneline -<N>` → group by theme; preserve a `#N` already present in a commit summary as a plain reference, without resolving it remotely
- `git status -s` → categorize: staged / unstaged / untracked
- Return: `{ branch, activity[], working_tree{ staged[], unstaged[], untracked[] } }`

**Agent "tests"** — test & coverage:
- Infer the test command from applicable `AGENTS.md`, `CLAUDE.md`, or `package.json` (common: `pnpm test`, `vitest run`).
- Extract: pass/fail, test count, duration, line/branch/function coverage %, below-threshold files.
- If unavailable: return `{ test_status: "N/A" }`.
- Return: `{ test_status, test_count, duration_s, lines_pct, branches_pct, functions_pct, below_threshold[] }`

**Agent "lint"** — lint health:
- Infer the lint command from applicable `AGENTS.md`, `CLAUDE.md`, or `package.json` (common: `pnpm lint`).
- Run `<lint command> 2>&1 | tail -5`, extract pass/fail. If unavailable: `{ lint_status: "N/A" }`.
- Return: `{ lint_status }`

### Step 6 — Fill and display snapshot

Merge all agent data, fill `@../assets/previously.md`, display exactly once immediately after the status block. Do not synthesize a second issue list from commit references.
