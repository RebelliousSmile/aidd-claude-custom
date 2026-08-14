---
name: setup
description: >-
  Installs third-party SaaS consumption guidance in the host-native project surface:
  AGENTS.md plus .agents/rules/ on Codex, or .claude/rules/ on Claude Code.
  Use when integrating Firebase, Klaviyo, GTM/Meta Pixel (or other SaaS) and the consumption rules are missing.
  Covers: Firestore query limits, security rules, quota awareness,
  Auth listener cleanup, Hosting trailing slash and cache headers,
  Playwright Firebase auth patterns, Klaviyo API patterns,
  GTM Consent Mode v2, Meta Pixel consent integration,
  Microsoft Clarity (best-effort, consent-gated, E2E patterns),
  PageSpeed Insights / Lighthouse (PSI variance, deterministic metrics, Nuxt checklist).
  Do NOT use to update a single rule — edit it directly instead.
---

Read [host portability](../../references/host-portability.md) before resolving plugin files, invoking sibling skills, or persisting project guidance.

# sc-tiers Setup

Installs third-party SaaS consumption rules in the current project. On Codex, it writes the references under `.agents/rules/` and maintains a bounded `## SC Tiers` index in `AGENTS.md`; on Claude Code, it writes the corresponding `.claude/rules/` files.

## Available actions

| # | Action | Role | Input |
|---|--------|------|-------|
| 01 | `install` | Write SaaS rules to the host-native instruction surface | current project path |
| 02 | `verify` | Audit the project code against installed SaaS rules | current project (auto-detected) |
| 03 | `help` | Provide integration context for a specific service to a calling skill | service name |

## Default flow

Trigger-to-action mapping:

- "install", "setup", "add rules", default invocation → `install`
- "verify", "audit", "check", "validate", "compliance" → `verify`
- "help", "how to integrate", "rules for", "guide for" + service name → `help`

## References

### Coding rules

- `references/03-firebase-resources.md` — Firestore query limits, count(), batch reads, security rules, quotas
- `references/04-firebase-auth-listeners.md` — onAuthStateChanged one-shot cleanup pattern
- `references/4-firebase-hosting-trailing-slash.md` — trailingSlash: false, cache headers glob
- `references/05-playwright-firebase-auth.md` — Firebase auth patterns in Playwright (networkidle, admin flow, custom claims)
- `references/09-klaviyo.md` — Klaviyo API patterns : 2-step subscribe, 409→PATCH, listes séparées par type, lazy loading, test cleanup
- `references/10-gtm-consent-meta.md` — GTM Consent Mode v2 : format gtag() vs Array, ensureGtag(), Meta Pixel consent, taxonomie pushEvent/pushGtmEvent, déduplication sessionStorage
- `references/11-clarity.md` — Microsoft Clarity : modèle best-effort, consent behavior, queue init, dual push GTM+Clarity, tests E2E (smoke, résilience, garde-fou perf)
- `references/12-pagespeed-insights.md` — PSI / Lighthouse : variance ±29 pts, signal déterministe, protocole 5 runs, checklist Nuxt 3 (LCP/CLS/INP/TBT/bundle/cache/SSR), anti-patterns

### Data pivots (consumed by `data-optimize`)

- `references/08-data-pivots-firebase.md` — Firestore reads accounting, real-time listeners, security rules

## Transversal rules

- Detect the active host before choosing targets; never assume `.claude/rules/` is loaded by Codex.
- Write files atomically — do not skip any rule.
- Preserve frontmatter (paths: globs) verbatim from each reference file.
- If a target file already exists, overwrite it without confirmation.
- Report each written file path at the end.
