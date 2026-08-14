# Host portability

Resolve `OVERCODE_PLUGIN_ROOT` from the loaded `<root>/skills/<skill>/SKILL.md` as `Path(SKILL_FILE).resolve().parent.parent.parent`. Set that task-local variable before using plugin-root paths. `PLUGIN_ROOT` and `CLAUDE_PLUGIN_ROOT` are optional host hints only.

Use native host capabilities for plans, tools, browser work, and subagents. On Codex, invoke skills as `$plugin:skill`; on Claude Code, use `/plugin:skill`. If subagents are unavailable, run the same bounded work sequentially.

For persistent project guidance, write the smallest applicable `AGENTS.md` section on Codex and the corresponding `.claude/rules/` file on Claude Code. Resolve `PROJECT_RULES_ROOT` to `.agents/rules` on Codex and `.claude/rules` on Claude Code. On Codex, search `.agents/rules` first and always fall back to an existing `.claude/rules` cross-host pivot interchange when no native match exists. Never assume Codex auto-loads either directory; an `AGENTS.md` section must point to any rule intended as persistent Codex guidance.
