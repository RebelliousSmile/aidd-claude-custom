# Action 03 — bump-plugin

Bumps a plugin version across the **three** manifests that carry it — `plugin.json`, `index.json` and `marketplace.json` — commits, and pushes to the marketplace.

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

Replace `"version"` in `plugins/<name>/.claude-plugin/plugin.json` with the new version. **This file is the source of truth** for both `version` and `description`; Steps 3 and 4 propagate from it, never the reverse.

### Step 3 — Update index.json

In the marketplace root `index.json`, update the entry whose `"id"` matches the plugin name:
- `"version"` → the new version;
- `"description"` → copied verbatim from `plugin.json` if it differs.

If the entry is absent, append a new one built from `plugin.json`.

### Step 4 — Update marketplace.json

In `.claude-plugin/marketplace.json`, update the entry whose `"name"` matches the plugin name — same two fields, same source:
- `"version"` → the new version;
- `"description"` → copied verbatim from `plugin.json` if it differs.

If the entry is absent, append a new one: `name`, `version`, `source` (`./plugins/<name>`), `description`, `recommended: false`.

> **Why all three.** The version lives in three files and `CONTRIBUTING.md` requires them coherent. Skipping any one of them leaves a divergence that no tool reports and that only surfaces when a user installs the plugin and gets a version the repo does not claim.

### Step 5 — Verify before committing

Re-read the three files and assert that `version` **and** `description` are identical across them for `<name>`. If any differs, stop and report rather than committing a partial bump.

### Step 6 — Commit

Stage `plugins/<name>/.claude-plugin/plugin.json`, `index.json` and `.claude-plugin/marketplace.json`. Commit:
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
- Three manifests aligned (version + description)
- Commit SHA
- Push confirmed
