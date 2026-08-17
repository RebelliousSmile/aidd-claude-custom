---
name: sniff
description: >-
author: François-Xavier Guillois
version: 0.5.0
vibe_version: ">=1.0.0"
permissions:
  - bash
  - files
tags:
  - frontend
  - audit
  - css
---

Read [host portability](../../references/host-portability.md) before resolving plugin files, invoking sibling skills, or persisting project guidance.

# sc-css:sniff

Détecteur d'architecture CSS et producteur de pivot manifeste.

## Actions disponibles

| # | Action | Rôle | Input |
|---|--------|------|-------|
| 01 | `scan` | Détecter architecture + stack, émettre pivot manifeste | chemins des fichiers CSS/SCSS du projet |

## Default flow

Action unique : `scan`. Le skill **n'installe rien** — `sc-css` ne fournit aucun fichier de pivot
sous `.claude/rules/07-quality/`. Le manifeste décrit l'état détecté ; il ne déclenche pas d'écriture.

## Modèle conceptuel

- **Architecture** : le style d'organisation des règles (BEM, utility-first, SMACSS, ITCSS, ad-hoc).
- **Stack** : outils en place (préprocesseur, linter, bundler CSS).
- **Maturité** : degré d'adoption de custom properties et cascade layers — indicateurs d'une base modernisable.
- **Pivot manifeste** : document JSON émis en fin de scan, consommé par audit et improve pour charger les patterns pertinents.

## Indicateurs de détection

| Signal | Détection |
|--------|-----------|
| `package.json` → `sass`, `postcss`, `less` | préprocesseur |
| `.stylelintrc*`, `biome.json` | linter CSS |
| Fichiers `*.module.css`, `*.module.scss` | CSS Modules |
| Classes `tw-`, `text-`, `flex`, `grid` systématiques | Tailwind / utility-first |
| Classes `__`, `--` systématiques | BEM |
| `@layer` dans les fichiers | cascade layers adoptés |
| `--` custom properties omniprésentes | design tokens en custom props |
| Aucune des structures ci-dessus | architecture ad-hoc |

## Règles transversales

- Si aucun fichier CSS/SCSS/Less n'est trouvé, arrêter avec un message explicite.
- Le scan est **read-only** : il écrit le manifeste, rien d'autre. Ne jamais annoncer l'installation
  d'un fichier de règle — le plugin n'en fournit aucun.
- Signaler les gaps : pattern détecté dont le traitement relève d'un skill (`improve`, `legacy`) —
  en nommant le skill, jamais un fichier à installer.
- Rapport en plain-text avec `✅ / ❌` par item — pas de tableaux Markdown.
