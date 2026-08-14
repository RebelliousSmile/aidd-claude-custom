# Bump-plugin

Bump a plugin version across its Claude Code and Codex manifests and both marketplace catalogs, validate the result, then commit and push when authorized by the parent alias.

## Context required

Require a plugin name and an exact version or bump type (`major`, `minor`, `patch`). Ask if either is missing.

## Process

1. **Locate the source marketplace repository.** Prefer the current repository when it contains `index.json`, `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`, and `plugins/`. Otherwise inspect the host's configured marketplace list (`codex plugin marketplace list` on Codex or Claude Code's known marketplaces) and ask if no unambiguous local source exists. Never edit an installed cache.
2. **Resolve the version.** Read `plugins/NAME/.claude-plugin/plugin.json` as the semantic-version source of truth and calculate the requested bump.
3. **Update both plugin manifests.** Write the semantic version to `.claude-plugin/plugin.json`. Write the same version to `.codex-plugin/plugin.json`; a Codex build suffix is allowed only when the existing repository convention requires a cachebuster.
4. **Update catalogs.** In `.claude-plugin/marketplace.json`, synchronize `version` and `description`. Ensure `.agents/plugins/marketplace.json` contains the plugin's local source entry and required policy/category metadata; this Codex catalog intentionally carries no duplicated version or description.
5. **Update `index.json` only if the plugin is new.** It carries only `{ "id", "name" }`.
6. **Validate before committing.** Run the repository's consistency gate and the official plugin validator. Re-read both manifests and both catalogs; any mismatch stops the action.
7. **Commit and push.** Stage only the plugin manifests, affected catalogs, and `index.json` when changed. Commit as `chore(NAME): bump version OLD → NEW`, then push the intended branch.
8. **Activation.** Report that Claude Code and Codex require their native plugin refresh/update flow and a new session. Do not emit commands for the wrong host.

## Report

Return the marketplace path, old and new versions, validator results, commit SHA, push status, and the host-specific activation instruction.
