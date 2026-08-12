# Host portability

The plugin root is derived from the loaded artifact, never assumed from the current working directory or a host-specific environment variable.

## Root resolution

For every design skill, resolve `DESIGN_PLUGIN_ROOT` from the loaded file
`<root>/skills/<skill>/SKILL.md` with the explicit operation
`Path(SKILL_FILE).resolve().parent.parent.parent`. In shell terms, starting from the directory
that contains `SKILL.md`, this is `../..`. Before executing a command that uses
`${DESIGN_PLUGIN_ROOT}`, set that task-local variable to the resolved absolute path or substitute
that absolute path directly. Never count parents from the file path implicitly: the formula above
is the executable contract.

`PLUGIN_ROOT` and `CLAUDE_PLUGIN_ROOT` may be used only as optional hints when a host supplies them. Their absence must not change behavior.

## Subagents

When an action names a leaf contract under `agents/`, load that file and pass its instructions to the host's native subagent primitive. Use the host's default model and bounded available concurrency. If subagents are unavailable, apply the same leaf contract sequentially. Never require a product-specific `Agent`, `Workflow`, or model tier.

## Persistent project instructions

- Codex projects: write the smallest applicable section in `AGENTS.md`.
- Claude Code projects: write the corresponding rule under `.claude/rules/`.
- Projects using both: keep both surfaces semantically equivalent.
- Optional profiles follow the same routing; their source filename does not prescribe the host
  destination.
- Never patch an installed plugin skill to persist a consuming project's rule.
