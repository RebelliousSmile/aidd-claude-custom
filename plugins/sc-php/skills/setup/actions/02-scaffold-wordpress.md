# Action 02 — scaffold-wordpress

Scaffold un projet WordPress FSE + Docker/wp-env depuis zéro.

## Inputs

- `project_root` (répertoire de travail courant, doit être vide ou quasi-vide — voir action 01).
- Slug du thème et du plugin custom (demander à l'utilisateur si non fournis ; dériver du nom du dossier projet en fallback).
- Port HTTP local souhaité (défaut `8888`).

## Process

1. Lire `references/wp-env-json.md` et écrire `.wp-env.json` à la racine, en substituant `{{THEME_SLUG}}`, `{{PLUGIN_SLUG}}`, `{{PORT}}`.
2. Lire `references/theme-plugin-skeleton.md` et créer l'arborescence thème + plugin décrite, en substituant les placeholders.
3. Lire `references/compose-project-name-guard.md` et écrire `scripts/start.ps1` / `scripts/stop.ps1`, avec `{{START_COMMAND}}` = `pnpm dlx @wordpress/env start` et `{{STOP_COMMAND}}` = `pnpm dlx @wordpress/env stop`.
4. Écrire un `package.json` minimal si absent, avec les scripts `"start": "powershell -File scripts/start.ps1"`, `"stop": "powershell -File scripts/stop.ps1"`.
5. Écrire un `.gitignore` couvrant au minimum : `node_modules/`, `wp-content/uploads/`, `dump.sql`.
6. Ne PAS lancer `wp-env start` automatiquement — le confirmer à l'utilisateur, il choisit quand démarrer les conteneurs.
7. Rappeler explicitement la règle wp-cli (`references/pitfalls.md` #3) : toujours `pnpm dlx @wordpress/env run cli wp`, jamais un binaire local.

## Outputs

```
.wp-env.json
wp-content/themes/{{THEME_SLUG}}/...
wp-content/plugins/{{PLUGIN_SLUG}}/...
scripts/start.ps1
scripts/stop.ps1
package.json
.gitignore
```

## Test

`pnpm run start` démarre wp-env sans erreur de nom de projet Docker Compose, et `pnpm dlx @wordpress/env run cli wp core version` retourne une version WordPress.
