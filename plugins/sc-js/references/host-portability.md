# Host portability

Resolve `SC_JS_PLUGIN_ROOT` from the loaded `<root>/skills/<skill>/SKILL.md` as `Path(SKILL_FILE).resolve().parent.parent.parent`. Set that task-local variable before using plugin-root paths. `PLUGIN_ROOT` and `CLAUDE_PLUGIN_ROOT` are optional hints only.

Use `$sc-js:<skill>` on Codex and `/sc-js:<skill>` on Claude Code. Persist general project instructions in `AGENTS.md` on Codex and `.claude/rules/` on Claude Code. Quality pivot files may remain under `.claude/rules/07-quality/` as a cross-host interchange because consuming skills read them explicitly; Codex does not auto-load that directory.

## Windows and WSL artifact provenance

Treat Unix mode bits read through DrvFs as synthetic transport input, not as production authority. A path under `/mnt/<letter>` is a DrvFs signal, not sufficient proof by itself: correlate it with a converted Windows path and, when available, mount information or another verifiable filesystem declaration. Never assume that DrvFs always reports `777`.

For a Linux destination, the delivery profile must classify the artifact as either:

- `drvfs`, whose permissions, owner, and group must not be preserved and whose destination modes must be explicit; or
- `linux-native`, prepared on a native Linux filesystem before transfer.

If provenance cannot be established, stop before forming a remote command and report a no-write gap.
