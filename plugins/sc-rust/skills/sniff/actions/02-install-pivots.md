# Install-pivots

Install perf and data pivots to `.claude/rules/07-quality/` for consumption by `web-optimize` and `data-optimize`. Does not install capability pivots — those are loaded on demand by `/sc-rust:audit`.

## Process

Read the pivot manifeste emitted by `01-scan`. For each perf or data pivot listed:

### Perf pivots — install to `.claude/rules/07-quality/`

| Source (in plugin) | Target (in project) |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/skills/sniff/references/capabilities/perf/axum.md` | `.claude/rules/07-quality/perf-pivots-axum.md` |

### Data pivots — install to `.claude/rules/07-quality/`

| Source (in plugin) | Target (in project) |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/skills/sniff/references/capabilities/data/sqlx.md` | `.claude/rules/07-quality/data-pivots-sqlx.md` |
| `${CLAUDE_PLUGIN_ROOT}/skills/sniff/references/capabilities/data/diesel.md` | `.claude/rules/07-quality/data-pivots-diesel.md` |
| `${CLAUDE_PLUGIN_ROOT}/skills/sniff/references/capabilities/data/rusqlite.md` | `.claude/rules/07-quality/data-pivots-rusqlite.md` |

### Install rules

For each pivot in the manifeste:

1. If the target file does not exist → **install**: read source, write to target; create parent directories as needed
2. If the target file exists and content matches source → **skip** (already up-to-date)
3. If the target file exists and content differs → **update**: overwrite silently

### Scope constraint

This action installs ONLY to `.claude/rules/07-quality/`. It NEVER installs capability pivots (those are loaded at audit time by `/sc-rust:audit`).

## Output

Pick the header by what actually happened — never claim "installed" when nothing was written.

Report what was written, not what the tables above list. Count and enumerate the targets you
actually processed. **The blocks below are shapes, not contents — do not copy their lines.** Only the
pivots the manifeste lists are processed, so an axum + sqlx crate emits two lines:
`data-pivots-diesel.md` and `data-pivots-rusqlite.md` never appear, not even as `skipped`.
Emitting the two tables in full is the failure this note names.

### Case A — at least one pivot was installed or updated

```
✅ sc-rust sniff — pivots installed

  Perf pivots:
    + .claude/rules/07-quality/perf-pivots-axum.md   (installed)
    … one line per target actually processed

  Data pivots:
    + .claude/rules/07-quality/data-pivots-sqlx.md   (installed)
    … one line per target actually processed

  Capability pivots: not installed (loaded on demand by /sc-rust:audit)

→ /web-optimize and /data-optimize are ready for detected pivots.
→ Run /sc-rust:audit to review Rust code quality against capability pivots.
```

### Case B — nothing to install (no applicable perf/data pivot)

Use this header verbatim when the manifeste lists no perf and no data pivot — the common case for
Rust: a CLI, a library crate, or an embedded target has neither `axum` nor a SQL crate. Do **not**
write `pivots installed` when nothing was written.

```
✅ sc-rust sniff — nothing to install

  Perf pivots:
    — none applicable (no axum server detected)

  Data pivots:
    — none detected

  Capability pivots: not installed (loaded on demand by /sc-rust:audit)

→ /web-optimize and /data-optimize have no pivot to load for this project.
→ Run /sc-rust:audit to review Rust code quality against capability pivots.
```

### Case C — pivots were applicable but all already up-to-date

Header `✅ sc-rust sniff — pivots up-to-date`; list each pivot with `✓ … (skipped — up-to-date)`.
