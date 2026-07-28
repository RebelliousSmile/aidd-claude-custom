# Marketplace — état courant

Source de vérité : `plugins/<nom>/.claude-plugin/plugin.json`, recopié dans `.claude-plugin/marketplace.json`. Ce fichier en est la lecture, pas une archive datée.

| Plugin | Rôle |
|---|---|
| `overcode` | Extensions AIDD projet-agnostiques : alias, behave, control, harvest, status, taste, foresee, baby, readme, changelog, decompose, journey, reconcile-normative, seo-optimize, data/web/ap-optimize |
| `design` | Entonnoir design system 5 verbes (define→destructure→adjust→enforce→diffuse) + detail et harness hors entonnoir |
| `game-writer` | Contenu narratif jeu vidéo (bank, dialogic-draft, dialogic-review) |
| `sc-godot` | Godot/GDScript — coquille (skills à porter) |
| `sc-js` | Écosystème JS (Nuxt/Vue/Svelte/Vite/Astro) + design-bridge, wp-blocks |
| `sc-css` | Écosystème CSS + design-bridge |
| `sc-php` | Écosystème PHP (WP/Laravel/Symfony) + log-analysis, bruno, setup, design-bridge, builder-coverage |
| `sc-python` | Écosystème Python (Django/FastAPI/Flask) |
| `sc-rust` | Écosystème Rust (Axum/Actix + SQLx/Diesel) |
| `sc-tiers` | SaaS tiers (Firebase/Firestore, Klaviyo, GTM, Clarity, PSI) |
| `obs` | Notes Obsidian, arbre Documents/, filler, research, extract-pdf |

## Plugins supprimés ou renommés

| Ancien | Devenu |
|---|---|
| `aidd-overlay` | `overcode` (renommé en 3.0.0) |
| `obsidian` | `obs` (renommé) |
| `gamedesign` | `game-writer` (renommé) |
| `doc-writer` | `writing` (fusion), puis `writing` retiré du marketplace |
| `rpg-writer` | `writing` (craft narratif) + `obs` (skills JDR + assemblage intrants) |
| `tabula-rasa` | — (supprimé, système de reset abandonné) |

## Skills supprimées

| Skill | Plugin | Remplacée par |
|---|---|---|
| `dig` | `overcode` | output style natif Learning (blocs ★ Insight) — le rappel actif noté /20 n'a pas d'équivalent |

## Séparation des responsabilités (BREAKING v3)

- **`obs`** assemble les intrants : `brief` (construit `_brief/`), `forge` (concept), `research` (données), `lore-extract`, `rules-keeper`, `extract-pdf`.
- La production éditoriale à partir d'un brief ne remonte jamais vers `R` ni `bank.yml`.
