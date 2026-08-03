# Install-pivots

Install perf and data pivots to `.claude/rules/07-quality/` for consumption by `web-optimize` and `data-optimize`. Does not install capability pivots — those are loaded on demand by `/sc-php:audit`.

## Process

Read the pivot manifeste emitted by `01-scan`. For each perf or data pivot listed:

### Perf pivots — install to `.claude/rules/07-quality/`

| Source (in plugin) | Target (in project) |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/skills/sniff/references/capabilities/perf/laravel.md` | `.claude/rules/07-quality/perf-pivots-laravel.md` |
| `${CLAUDE_PLUGIN_ROOT}/skills/sniff/references/capabilities/perf/symfony.md` | `.claude/rules/07-quality/perf-pivots-symfony.md` |
| `${CLAUDE_PLUGIN_ROOT}/skills/sniff/references/capabilities/perf/wordpress.md` | `.claude/rules/07-quality/perf-pivots-wordpress.md` |
| `${CLAUDE_PLUGIN_ROOT}/skills/sniff/references/capabilities/perf/htmx.md` | `.claude/rules/07-quality/perf-pivots-htmx.md` |

### Data pivots — install to `.claude/rules/07-quality/`

| Source (in plugin) | Target (in project) |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/skills/sniff/references/capabilities/data/eloquent.md` | `.claude/rules/07-quality/data-pivots-eloquent.md` |
| `${CLAUDE_PLUGIN_ROOT}/skills/sniff/references/capabilities/data/doctrine.md` | `.claude/rules/07-quality/data-pivots-doctrine.md` |

### Install rules

For each pivot in the manifeste:

1. If the target file does not exist → **install**: read source, write to target; create parent directories as needed
2. If the target file exists and content matches source → **skip** (already up-to-date)
3. If the target file exists and content differs → **update**: overwrite silently

### Scope constraint

This action installs ONLY to `.claude/rules/07-quality/`. It NEVER installs capability pivots (those are loaded at audit time by `/sc-php:audit`). It never writes to `.claude/rules/capabilities/` or any other path.

## Output

Pick the header by what actually happened — never claim "installed" when nothing was written.

### Case A — at least one pivot was installed or updated

```
✅ sc-php sniff — pivots installed

  Perf pivots:
    + .claude/rules/07-quality/perf-pivots-laravel.md   (installed)
    ✓ .claude/rules/07-quality/perf-pivots-symfony.md   (skipped — not applicable)
    ✓ .claude/rules/07-quality/perf-pivots-wordpress.md (skipped — not applicable)
    ✓ .claude/rules/07-quality/perf-pivots-htmx.md      (skipped — not applicable)

  Data pivots:
    + .claude/rules/07-quality/data-pivots-eloquent.md  (installed)
    ✓ .claude/rules/07-quality/data-pivots-doctrine.md  (skipped — not applicable)

  Capability pivots: not installed (loaded on demand by /sc-php:audit)

→ /web-optimize and /data-optimize are ready for detected pivots.
→ Run /sc-php:audit to review PHP code quality against capability pivots.
```

### Case B — nothing to install (no applicable perf/data pivot)

Use this header verbatim when the manifeste lists no perf and no data pivot (e.g. a PHP library or
a CLI tool with neither framework nor ORM). Do **not** write `pivots installed` when nothing was
written.

```
✅ sc-php sniff — nothing to install

  Perf pivots:
    — none applicable (no framework with a perf pivot detected)

  Data pivots:
    — none detected

  Capability pivots: not installed (loaded on demand by /sc-php:audit)

→ /web-optimize and /data-optimize have no pivot to load for this project.
→ Run /sc-php:audit to review PHP code quality against capability pivots.
```

### Case C — pivots were applicable but all already up-to-date

Header `✅ sc-php sniff — pivots up-to-date`; list each pivot with `✓ … (skipped — up-to-date)`.
