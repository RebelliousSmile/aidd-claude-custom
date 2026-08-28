# Host portability

Resolve `SC_TIERS_PLUGIN_ROOT` from the loaded `<root>/skills/<skill>/SKILL.md` as `Path(SKILL_FILE).resolve().parent.parent.parent`. Set that task-local variable before using plugin-root paths. `PLUGIN_ROOT` and `CLAUDE_PLUGIN_ROOT` are optional hints only.

Use `$web-tiers:setup` on Codex and `/web-tiers:setup` on Claude Code. On Codex, install the SaaS consumption guidance as bounded, named sections in the nearest `AGENTS.md`; on Claude Code, write the mapped files under `.claude/rules/`. Keep the quality pivot as an explicit cross-host interchange file when an optimizer consumes it.
