# Scaffold-wordpress

Scaffold un projet WordPress FSE + Docker/wp-env depuis zéro.

## Inputs

- `project_root` (répertoire de travail courant, doit être vide ou quasi-vide — voir action 01).
- Slug **et nom lisible** du thème et du plugin custom — quatre valeurs, pas deux : `{{THEME_SLUG}}`, `{{THEME_NAME}}`, `{{PLUGIN_SLUG}}`, `{{PLUGIN_NAME}}` (demander à l'utilisateur si non fournis ; en fallback, slug dérivé du nom du dossier projet et nom dérivé du slug en Title Case). Les noms lisibles ne sont pas cosmétiques : ils sont l'en-tête `Theme Name:` / `Plugin Name:` sans lequel WordPress ne reconnaît ni l'un ni l'autre.
- Port HTTP local souhaité (défaut `8888`).

## Process

1. Lire `references/wp-env-json.md` et écrire `.wp-env.json` à la racine, en substituant `{{THEME_SLUG}}`, `{{PLUGIN_SLUG}}`, `{{PORT}}`.
2. Lire `references/theme-plugin-skeleton.md` et créer l'arborescence thème + plugin décrite, en substituant les placeholders.
3. Lire `references/compose-project-name-guard.md` et écrire `scripts/start.ps1`, `scripts/stop.ps1` **et `scripts/wp.ps1`**, avec `{{START_COMMAND}}` = `pnpm dlx @wordpress/env start` et `{{STOP_COMMAND}}` = `pnpm dlx @wordpress/env stop`. Les trois portent le même garde ; `wp.ps1` est ce qui le rend disponible aux commandes tapées à la main.
4. Écrire un `package.json` minimal si absent, avec les scripts `"start": "powershell -File scripts/start.ps1"`, `"stop": "powershell -File scripts/stop.ps1"`, `"wp": "powershell -File scripts/wp.ps1"`.
5. Écrire un `.gitignore` couvrant au minimum : `node_modules/`, `wp-content/uploads/`, `dump.sql`.
6. Ne PAS lancer `wp-env start` automatiquement — le confirmer à l'utilisateur, il choisit quand démarrer les conteneurs.
7. Rappeler explicitement la règle wp-cli (`references/pitfalls.md` #3) : toujours par `pnpm wp <commande>`, jamais un binaire local — et jamais `pnpm dlx @wordpress/env run cli wp` nu, qui perd le garde `COMPOSE_PROJECT_NAME` et rend `service "cli" is not running` alors que les conteneurs tournent.
8. **Énoncer ce que le scaffold ne fait pas** : aucun type de contenu n'est enregistré, et aucun ne peut l'être ici — cette action tourne sur un dossier vide, avant la référence. Si le projet part d'une maquette, dire explicitement que le modèle de contenu se dérive ensuite (`sc-php:design-bridge`, `references/content-model-fse.md`), avant tout rendu de patterns. Sans cet énoncé, `includes/` vide et trois templates génériques se lisent comme un état complet.
9. **Prescrire l'activation du thème comme première commande après le démarrage** : `pnpm wp theme activate {{THEME_SLUG}}`. Rien ne l'active à la place — `WP_DEFAULT_THEME` ne s'applique qu'à l'installation, que wp-env a déjà faite (voir `references/wp-env-json.md`). Sans cette commande, le site sert le thème par défaut du core, et le thème scaffoldé n'est jamais exercé.
10. Vérifier que `assets/css/design/index.css` est référencé par `wp_enqueue_style()`,
    `add_editor_style()` **et** `enqueue_block_assets` ; ce dernier enrôle effectivement la même entrée
    dans le canvas iframe. Un point d'entrée présent sur une seule surface est un scaffold incomplet.

## Outputs

```
.wp-env.json
wp-content/themes/{{THEME_SLUG}}/...
wp-content/plugins/{{PLUGIN_SLUG}}/...
wp-content/themes/{{THEME_SLUG}}/assets/css/design/index.css
scripts/start.ps1
scripts/stop.ps1
scripts/wp.ps1
package.json
.gitignore
```

## Test

`pnpm run start` démarre wp-env sans erreur de nom de projet Docker Compose, puis `pnpm wp theme status {{THEME_SLUG}}` rend `Status: Active`, **et la page d'accueil rend du contenu** :

```
pnpm wp eval "echo get_stylesheet();"
curl -s http://localhost:{{PORT}}/ | Select-String -Quiet 'wp-site-blocks'
curl -s http://localhost:{{PORT}}/ | Select-String -Quiet '{{THEME_SLUG}}-design-css'
```

La première commande doit rendre `{{THEME_SLUG}}`, les deux suivantes `True`. Vérifier aussi via
`pnpm wp eval` que `get_theme_support('editor-styles')` contient `assets/css/design/index.css`.

**Exercer les scripts depuis un autre répertoire**, sinon le garde de répertoire n'est jamais testé : tout lancement fait à la racine passe avec ou sans lui. `& <racine>\scripts\stop.ps1` tapé depuis un dossier tiers doit arrêter les conteneurs. Mesuré sans le `Push-Location` : `Environment not initialized. Run wp-env start first.` alors que les trois conteneurs tournaient — le script rend la main en échec et **laisse le projet debout**.

**Ne pas se contenter de `wp core version`.** Ce test-là passe sur un site entièrement blanc : il atteste que WordPress répond, pas que le scaffold a produit quelque chose de navigable. Mesuré — thème actif, HTTP 200, `.wp-site-blocks` absent, zéro caractère rendu. Un test qui ne peut pas échouer sur le défaut qu'il est censé couvrir n'est pas un test.
