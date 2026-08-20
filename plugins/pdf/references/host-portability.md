# Host portability

Resolve `PDF_PLUGIN_ROOT` from the loaded `<root>/skills/<skill>/SKILL.md` as `Path(SKILL_FILE).resolve().parent.parent.parent`. Set that task-local variable before using plugin-root paths. `PLUGIN_ROOT` and `CLAUDE_PLUGIN_ROOT` are optional host hints only.

Use the host's native tools by capability rather than product-specific tool names. Use `$pdf:<skill>` for explicit Codex invocation and `/pdf:<skill>` for Claude Code.

When persisting project instructions, update the smallest applicable section of `AGENTS.md` on Codex and the matching file under `.claude/rules/` on Claude Code. Keep both semantically equivalent when both surfaces exist.
