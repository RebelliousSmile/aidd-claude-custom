---
name: setup
model: sonnet
description: >-
  Scaffolds a brand-new PHP project from scratch (WordPress FSE, Laravel, or
  Symfony) with Docker Compose ready for local dev, and optionally wires an
  SSH-based deploy pipeline (rsync + optional DB export, alwaysdata/Scriptami-style
  hosting). Detects/asks the target framework first — mirrors the three frameworks
  sc-php:sniff already knows how to detect (composer.json + wp-config.php / artisan /
  bin/console). Use when the user asks to: scaffold a new PHP project, set up
  WordPress/Laravel/Symfony with Docker, init wp-env, create a fresh project with
  local dev + deploy. The WordPress flow is the most complete (born from a real
  production deployment); Laravel/Symfony flows wrap the official installers
  (composer create-project) with a standard Docker Compose. Do NOT use on an
  already-configured project — prefer sc-php:sniff then sc-php:audit there. Do NOT
  use for generic PHP without one of these three frameworks (no scaffold path exists
  for that yet).
---

# sc-php Setup

Scaffold-from-zero counterpart to `sc-php:sniff` (which detects/audits an already-configured project). Covers exactly the three frameworks `sniff` detects: WordPress, Laravel, Symfony.

## Available actions

| # | Action | Role | Input |
|---|--------|------|-------|
| 01 | `detect-framework` | Resolve which framework to scaffold (explicit request, ask if ambiguous), abort if project already configured | project root, user request |
| 02 | `scaffold-wordpress` | WordPress FSE theme + custom plugin + Docker/wp-env | resolved framework = wordpress |
| 03 | `scaffold-laravel` | Laravel via composer create-project + Docker Compose | resolved framework = laravel |
| 04 | `scaffold-symfony` | Symfony via composer create-project + Docker Compose | resolved framework = symfony |
| 05 | `wire-deploy` | Optional SSH deploy pipeline (rsync + optional DB export) | framework, target(s) info from user |
| 06 | `verify` | Post-scaffold sanity checks | framework, project root |

## Default flow

`01` → (`02` | `03` | `04` depending on resolved framework) → `06`. `05` is optional, proposed after scaffold but never assumed — only run it if the user wants a deploy target wired now.

Trigger-to-action mapping for `01`:
- Framework named explicitly ("scaffold a WordPress", "set up Laravel with Docker") → skip the question, go straight to the matching scaffold action.
- No framework named, or ambiguous → ask (WordPress / Laravel / Symfony), never guess.

## References

- `references/pitfalls.md` — Docker Compose project-naming trap (generic, all frameworks), WP-specific CSS cache-busting and wp-cli-via-Docker rules.
- `references/compose-project-name-guard.md` — `start.ps1`/`stop.ps1` template shared by all three scaffolds.
- `references/wp-env-json.md`, `references/theme-plugin-skeleton.md` — WordPress scaffold content.
- `references/docker-compose-laravel.md`, `references/docker-compose-symfony.md` — Docker Compose content for the other two frameworks.
- `references/deploy-pipeline.md` — `deploy.mjs`/`deploy-targets.mjs` content for `wire-deploy`.

## Transversal rules

- Never scaffold onto an already-configured project — `01` aborts and redirects to `sniff`/`audit` if `composer.json` or a sentinel file already exists.
- Never invent deploy target credentials (host, user, path) — ask, or leave a commented example.
- Never auto-run a database import against a remote target — that step stays manual and explicit, always.
- Never let Docker Compose derive its project name implicitly — every scaffold wires the `COMPOSE_PROJECT_NAME` guard from `compose-project-name-guard.md`.
- WordPress is the reference-quality flow (real production lineage); Laravel/Symfony are thinner (official installer + standard compose) — say so rather than implying equal depth.
- Report every file written, per action, same as `sniff`/`sc-tiers:setup` do.
