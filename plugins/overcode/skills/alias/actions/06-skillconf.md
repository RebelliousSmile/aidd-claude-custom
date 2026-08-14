# Skillconf

Audit the skills active in the current host and compare their implicit-invocation policy with the curated CORE allowlist in `assets/skillconf-core.json`.

## Host boundary

- **Codex:** invocation policy is shipped per skill in `agents/openai.yaml` as `policy.allow_implicit_invocation`. Project `config.toml` can enable or disable a skill, but it cannot turn implicit invocation into explicit-only invocation. Audit and report drift; change plugin source only when the user explicitly asks to update policy, then validate and reinstall the plugin.
- **Claude Code:** invocation policy is project-configurable through `skillOverrides` in `.claude/settings.json`; after confirmation, this action may update that key only.

Never claim that one host's configuration changes the other.

## Process

1. Resolve and read `assets/skillconf-core.json`. Its `core` array is the single curated source of truth.
2. Inventory the skills actually visible in the current session. Use namespaced `plugin:skill` keys where applicable.
3. Classify each skill with `CORE.includes(skillKey) ? "auto" : "explicit-only"`. Do not infer exceptions from the current project's stack.
4. Read the active host baseline:
   - Codex: each installed skill's `agents/openai.yaml`; missing policy means implicit invocation is allowed.
   - Claude Code: project `.claude/settings.json`; missing file means `{}`.
5. Emit a classification table with skill, current policy, proposed policy, rationale, and host surface.
6. Apply only after explicit confirmation:
   - Codex: edit the source skill's `agents/openai.yaml`, not cache copies or project config; create a valid `interface` block when adding the file, validate the skill and plugin, then use the plugin update/reinstall flow.
   - Claude Code: merge `skillOverrides` in the project `.claude/settings.json`, preserving every unrelated key.
7. Report changed, unchanged, and CORE counts plus the exact files touched. Tell the user to start a new session after policy changes.

## Safety

- Never edit global Codex or Claude settings from this action.
- Never patch an installed cache copy.
- On Codex, if the source plugin cannot be resolved, stop after the audit and report the missing source rather than pretending a project override exists.
- Keep the CORE allowlist short and hand-maintained.
