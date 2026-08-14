# Domain layout — generic working-directory convention

The generic model used by `overcode:research`. It is **domain-agnostic**: a JDR game domain is a profile of this model, not the base. A novel, a technical-documentation knowledge base, or any other subject area is just as valid a domain.

> **Local paths, discovered anchor — no global hardcoding.** A domain is a self-contained directory in `Documents/`; everything it needs lives beneath it in **relative** paths. Move it anywhere and the skill still works.

## Domain `R`

`R` = a **subcategory** directory in the tree: `(Perso|Pro)/<Category>/<Subcategory>/`. There are **many `R` per category** (e.g. `Perso/RPG/engrenages/`, `Perso/RPG/archipels/`, or `Perso/Creative/mon-roman/`). `R` is located by the Documents tree anchor — walk up to a `Perso`/`Pro` segment; the subcategory level is `R`. **No domain marker is required** to locate `R`. A profile may add a marker-based shortcut; see the JDR profile below.

## Working-dir buckets

Inside `R`, durable resources live in **working-dir buckets** `R/_<bucket>/` (the `_` prefix is `tree` invariant I1; the content inside is **not** prefixed). Bucket names are **free** and catalogued by `R/bank.yml` — the skill never hardcodes a bucket name in the generic core. The JDR profile happens to name them `_univers`, `_systeme`, `_subsystems`, `_pjs`, and `_campagnes`.

## Manifest

`R/bank.yml` = the generic manifest (cache) of `R`'s durable resources, maintained by `obs:tree` when that companion skill is installed. An optional top-level **`profile:`** key declares a layout profile (e.g. `profile: jdr`). Research can still use the fallback detection below when no manifest exists.

## Path variables (all relative to `R`)

| Variable | Generic | JDR profile |
|----------|---------|-------------|
| `R` | subcategory domain, **discovered** | `Perso/RPG/<jeu>/` |
| raw ingested material | `<bucket\|projet>/sources/<source>/` | `_univers/<u>/sources/`, `_systeme/sources/` |
| synthesized durable knowledge | `<bucket>/reference/` | `canon/` + `mj/` (provenance split) |
| research reports | `<scope-root>/research/<slug>-<date>.md` | idem |
| work unit (project) | `R/<AAAA>/<MM>/<projet>/` — holds `_brief/`, `_output/`, `research/`, `sources/` | idem (+ `_ecrits/`) |

## Provenance — `reference/` (generic) vs `canon/`+`mj/` (JDR)

The generic core has a **single `reference/`** bucket-subdirectory for synthesized durable knowledge. The JDR profile **refines** it into a provenance split: `canon/` (official, source-derived) vs `mj/` (homemade or authored). A non-JDR domain does not need the split.

## Research scopes

Generic scopes, determined **before** writing (never a default): **`shared`** (R-level, durable, reused across work units) vs **`project`** (specific to one work unit). The JDR profile adds a third scope, **`campagne`** (specific to one game).

## Profile detection

A domain uses a **profile** when:

1. `R/bank.yml` declares `profile: <name>` — **explicit and authoritative**; or
2. as a zero-configuration fallback, `R` contains the profile's signature buckets — for JDR, `_univers/` or `_systeme/`.

Without a profile, apply the **generic core** (`sources/` + `reference/`, scopes `shared`/`project`).

## Generic vs JDR profile — summary

- **Generic:** `R` = subcategory · `R/_<bucket>` working directories · optional `bank.yml` · `sources/` (raw) + `reference/` (synthesized) · scopes `shared`/`project` · discovery via the `tree` anchor.
- **JDR profile:** bucket names `_univers`/`_systeme`/`_subsystems`/`_pjs`/`_campagnes` · `canon/`+`mj/` provenance split · `campagne` scope · marker-based shortcut.
