# Host portability

Resolve `SC_CSS_PLUGIN_ROOT` from the loaded `<root>/skills/<skill>/SKILL.md` as `Path(SKILL_FILE).resolve().parent.parent.parent`. Set that task-local variable before using plugin-root paths. `PLUGIN_ROOT` and `CLAUDE_PLUGIN_ROOT` are optional hints only.

Use `$sc-css:<skill>` on Codex and `/sc-css:<skill>` on Claude Code. Persist project instructions in `AGENTS.md` on Codex and `.claude/rules/` on Claude Code; keep both equivalent when both hosts are in use.
