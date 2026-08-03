# Install

Write third-party SaaS consumption rule files to the current project's `.claude/rules/`.

## Process

Read each reference file listed below and write its content verbatim to the target path in the current project. Create parent directories as needed.

### Coding rules

| Reference file | Target path |
|---|---|
| `references/03-firebase-resources.md` | `.claude/rules/03-frameworks-and-libraries/03-firebase-resources.md` |
| `references/04-firebase-auth-listeners.md` | `.claude/rules/04-tooling/04-firebase-auth-listeners.md` |
| `references/4-firebase-hosting-trailing-slash.md` | `.claude/rules/04-tooling/4-firebase-hosting-trailing-slash.md` |
| `references/05-playwright-firebase-auth.md` | `.claude/rules/05-testing/05-playwright-firebase-auth.md` |
| `references/09-klaviyo.md` | `.claude/rules/03-frameworks-and-libraries/09-klaviyo.md` |
| `references/10-gtm-consent-meta.md` | `.claude/rules/03-frameworks-and-libraries/10-gtm-consent-meta.md` |
| `references/11-clarity.md` | `.claude/rules/03-frameworks-and-libraries/11-clarity.md` |
| `references/12-pagespeed-insights.md` | `.claude/rules/07-quality/12-pagespeed-insights.md` |

### Data pivots (consumed by `data-optimize`)

| Reference file | Target path |
|---|---|
| `references/08-data-pivots-firebase.md` | `.claude/rules/07-quality/data-pivots-firebase.md` |

Only the stacks with a reference file above are covered. A stack absent from this table has no
sc-tiers rule to install — say so, do not invent a target path for it.

## Output

Report what was written, not what the tables above list. Count and enumerate the targets you
actually touched; a reference file that does not resolve is reported as missing, never as
written. Never claim "installed" when nothing was written.

```
✅ sc-tiers rules installed — <n> files written to .claude/rules/
  Coding rules (<n>):
    + .claude/rules/03-frameworks-and-libraries/03-firebase-resources.md   (written)
    ✓ .claude/rules/04-tooling/04-firebase-auth-listeners.md               (skipped — identical)
    … one line per target actually processed
  Data pivots (<n>):
    + .claude/rules/07-quality/data-pivots-firebase.md                     (written)
```

If a reference file listed above is missing from the plugin, report it and continue with the
rest:

```
❌ references/<name>.md — missing from the plugin, nothing written for this target
```

If every reference file is missing, the header is `❌ sc-tiers rules — nothing written`.
