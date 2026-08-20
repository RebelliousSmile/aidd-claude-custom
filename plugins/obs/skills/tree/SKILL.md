---
name: tree
description: Keeps the Documents/ tree navigable as it evolves — maintains a cache (map of the real arborescence), verifies it against a small set of portability invariants, fixes drift safely, and exports a routing map. Runs as a deterministic script, no model call. Use to check whether a directory is well-organised, to tidy it, or to place loose files.
author: fxgui
version: 0.38.0
vibe_version: ">=1.0.0"
permissions:
  - bash
tags:
  - documentation
  - obsidian
  - notes
---

Read [host portability](../../references/host-portability.md) before resolving plugin files, invoking sibling skills, or persisting project guidance.

# Tree

Keeps `Documents/` **navigable while it keeps changing**. Rather than enforcing a frozen layout, `tree` maintains a **cache** (a map of the *actual* arborescence) and uses it to verify drift, fix it, and place loose items.

Everything this skill does is done by `${OBS_PLUGIN_ROOT}/scripts/tree.py`. Run the command, read its output, relay it. Do not re-implement its behaviour in prose, and do not move or rename files by hand alongside it.

**Local paths, discovered anchor — no global hardcoding.** The script works relative to a **target directory** (the CWD by default, or a path passed as argument). It finds the schema **anchor** by walking up to a `Perso`/`Pro` segment; it never hardcodes `C:\Users\…\Documents`. The cache lives at `<anchor>/_tree/cache.json` and is fully regenerable.

## Commands

| Command | Role | Invocation |
| --- | --- | --- |
| `index` | Scan the real tree → refresh `<anchor>/_tree/cache.json` + each domain's `R/bank.yml` | `python tree.py index [<target>] [--managed-root] [--apply]` |
| `check` | Verify invariants + drift vs the cached convention; report only | `python tree.py check [<target>] [--managed-root]` |
| `fix` | Rename/move to correct confirmed anomalies; `--drift` also realigns on the learned convention | `python tree.py fix [<target>] [--drift] [--apply]` |
| `sort` | Place loose items into the tree, using the cache | `python tree.py sort <items…> [--into <target>] [--apply]` |
| `destinations` | Export the durable tree as a `destinations.txt` routing map | `python tree.py destinations [<target>] [--out <path>] [--apply]` |

## Default flow

- "index the tree", "scan", "refresh the map", "rebuild cache" → `index`
- "check organisation", "is this tidy", "vérifier l'arbo", "what's out of place" → `check`
- "fix the tree", "tidy", "ranger", "corriger l'arbo" → `fix`
- "where does this go", "sort these files", "trier", "classe ça" → `sort`
- "export destinations", "routing map email" → `destinations`

`check`/`fix`/`sort`/`destinations` refresh the cache themselves when it is missing or stale.

Always run without `--apply` first and show the plan. Only re-run with `--apply` once the user has seen it and agreed.

## What the script guarantees

- **Discovered anchor only.** No hardcoded absolute path. No anchor found → the script says so and offers `--managed-root` to treat the target as its own root.
- **Target scope is strict, not anchor-wide.** `check`/`fix` bound their report to `<target>`. Resolving the anchor locates the shared cache; it does not widen the blast radius to sibling domains.
- **Cache is regenerable.** It accelerates navigation; the disk is the source of truth.
- **Invariants vs drift.** I1–I4 are enforced (see reference); everything else is soft drift judged against the domain's learned convention, and only touched under `--drift`.
- **Never destructive.** Rename and move only, after a dry-run, never a delete, never an overwrite — a collision is reported, not resolved.
- **Links are not rewritten.** `fix` and `sort` rename and move, nothing more: incoming `[[…]]` wikilinks, `![[…]]` embeds and relative attachment paths keep their old target, and assets are not co-moved. Read the dry-run before applying — renaming a note breaks every link pointing at it. `filler sort` does rewrite them; `tree` does not.
- **Credentials are never read.** A file matching a credential pattern (`.env`, `credentials.*`, `*.key`, `*.pem`, `*password*`, …) has its path signalled, never its content. Files under a `_code/` directory are silently skipped.
- **`.git` and dotfiles never move alone.** They travel only with their parent directory.
- **Media are never read.** Images, audio and video are excluded from every content-reading operation.
- **Learn, don't impose.** A domain that diverges has its effective convention recorded in the cache.
- `index` and `check` never modify user content; `index` only writes derived caches (`_tree/cache.json`, per-domain `R/bank.yml`), and `bank.yml` is merged, never clobbered — curated summaries survive.

## External data

- `${OBS_PLUGIN_ROOT}/scripts/tree.py` — the implementation. `--help` on any subcommand.
- `${OBS_PLUGIN_ROOT}/references/tree-convention.md` — invariants, default pattern, cache format, anchor resolution.
- `${OBS_PLUGIN_ROOT}/references/destinations-template.md` — `destinations.txt` format for the `email-to-markdown` router.
- `<anchor>/_tree/cache.json` — the navigation cache.
- `R/bank.yml` — per-domain resource manifest; format in `${OBS_PLUGIN_ROOT}/references/bank-yml.md`.
