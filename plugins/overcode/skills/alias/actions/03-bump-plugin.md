# Bump-plugin

Bumps a plugin version across the **two** manifests that carry it — `plugin.json` and `marketplace.json` — verifies with the repo's own consistency gate, commits, and pushes to the marketplace.

## Context required

- Plugin name (e.g. `sc-js`, `overcode`, `writing`).
- Version or bump type (`major`, `minor`, `patch`). If absent, ask: *"Which plugin and what version bump?"*

## Prompt

### Step 0 — Locate marketplace root

Find automatically:
- a. Read `~/.claude/plugins/known_marketplaces.json` (or `%USERPROFILE%\.claude\plugins\known_marketplaces.json`). Use the `path` of the entry whose `source.source` is `"directory"`.
- b. If absent, search for `index.json` containing a `"plugins"` array in `~/Documents`, `~/Projects`, `~/Projets` (one level deep).
- c. If still not found, ask: *"Where is your marketplace repo?"*

### Step 1 — Resolve version

Read `plugins/<name>/.claude-plugin/plugin.json`. If bump type given, compute new semver (e.g. `0.1.0` + `minor` → `0.2.0`).

### Step 2 — Bump plugin.json

Replace `"version"` in `plugins/<name>/.claude-plugin/plugin.json` with the new version. **This file is the source of truth** for both `version` and `description`; Step 3 propagates from it, never the reverse.

### Step 3 — Update marketplace.json

In `.claude-plugin/marketplace.json`, update the entry whose `"name"` matches the plugin name:
- `"version"` → the new version;
- `"description"` → copied verbatim from `plugin.json` if it differs.

If the entry is absent, append a new one: `name`, `version`, `source` (`./plugins/<name>`), `description`, `recommended: false`.

> **Why this one too.** `marketplace.json` is what Claude Code reads at install time. Skipping it leaves a divergence that only surfaces when a user installs the plugin and gets a version the repo does not claim.

### Step 4 — Register in index.json if absent

`index.json` carries **no version and no description** — only `{ "id", "name" }` per plugin, which is what makes it unable to drift. Add the entry if the plugin is new; otherwise leave the file untouched.

### Step 5 — Verify before committing

If the marketplace ships a consistency gate — a `test` script, `tools/eval/consistency.mjs` — run it and prefer its verdict:

```bash
node tools/eval/consistency.mjs
```

Otherwise, re-read `plugin.json` and `marketplace.json` and assert that `version` **and** `description` are identical for `<name>`.

Either way, a failure stops the action: report rather than commit a partial bump.

### Step 6 — Commit

Stage `plugins/<name>/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` (plus `index.json` if Step 4 added an entry). Commit:
```
chore(<name>): bump version <old> → <new>
```

### Step 7 — Push

```bash
git push origin main
```

### Step 8 — Activation

Output to user:
> ```
> /plugin update
> /reload-plugins
> ```

### Step 9 — Report

- Marketplace path
- Plugin: `<name>` `<old>` → `<new>`
- `consistency.mjs` green
- Commit SHA
- Push confirmed
