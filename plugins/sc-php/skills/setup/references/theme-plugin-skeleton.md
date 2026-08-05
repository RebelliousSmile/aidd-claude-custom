# Squelette thème FSE + plugin custom

Placeholders : `{{THEME_SLUG}}`, `{{THEME_NAME}}`, `{{PLUGIN_SLUG}}`, `{{PLUGIN_NAME}}`.

## Arborescence à créer

```
wp-content/
  themes/{{THEME_SLUG}}/
    style.css
    theme.json
    templates/
      index.html
      single.html
      page.html
    parts/
      header.html
      footer.html
    functions.php
  plugins/{{PLUGIN_SLUG}}/
    {{PLUGIN_SLUG}}.php
    includes/
    assets/
      js/
      css/
```

**Aucun des cinq fichiers `.html` ne peut rester vide.** Un thème block dont `templates/index.html` est vide rend une page HTTP 200 sans aucun contenu : `<body>` ne porte que les scripts du core, `.wp-site-blocks` est absent, le texte rendu fait zéro caractère. Mesuré sur WordPress 7.0.2. Le contenu ci-dessous est le minimum qui rend un site navigable — il est fait pour être remplacé, pas pour être omis.

## `style.css` (en-tête thème, obligatoire pour que WP le reconnaisse)

```css
/*
Theme Name: {{THEME_NAME}}
Theme URI:
Author:
Description: Thème block-based (FSE) scaffoldé par sc-php:setup.
Version: 0.1.0
Requires at least: 6.6
Requires PHP: 8.0
*/
```

`Requires at least` est lié au `"version"` de `theme.json` ci-dessous : le schéma **v3 exige WordPress 6.6** (« *Updating to version 3 is recommended when your minimum supported WordPress version reaches 6.6* », dev-note core du 2024-06-19). Descendre le minimum à 6.5 sans redescendre le schéma à `2` livre un `theme.json` que la version annoncée ne sait pas lire.

## `theme.json` (squelette minimal — à enrichir selon la charte design du projet)

```json
{
  "$schema": "https://schemas.wp.org/trunk/theme.json",
  "version": 3,
  "settings": {
    "appearanceTools": true,
    "layout": {
      "contentSize": "720px",
      "wideSize": "1200px"
    }
  },
  "templateParts": [
    { "name": "header", "title": "Header", "area": "header" },
    { "name": "footer", "title": "Footer", "area": "footer" }
  ]
}
```

`templateParts` n'est pas décoratif : sans lui, `parts/header.html` et `parts/footer.html` fonctionnent au rendu mais ne sont rattachées à aucune zone, et l'éditeur de site les présente comme des parties génériques.

## `parts/header.html`

```html
<!-- wp:group {"tagName":"header","layout":{"type":"constrained"}} -->
<header class="wp-block-group">
	<!-- wp:group {"layout":{"type":"flex","justifyContent":"space-between"}} -->
	<div class="wp-block-group">
		<!-- wp:site-title /-->
		<!-- wp:navigation /-->
	</div>
	<!-- /wp:group -->
</header>
<!-- /wp:group -->
```

## `parts/footer.html`

```html
<!-- wp:group {"tagName":"footer","layout":{"type":"constrained"}} -->
<footer class="wp-block-group">
	<!-- wp:paragraph {"align":"center"} -->
	<p class="has-text-align-center">&copy; <!-- wp:site-title {"isLink":false} /--></p>
	<!-- /wp:paragraph -->
</footer>
<!-- /wp:group -->
```

## `templates/index.html`

```html
<!-- wp:template-part {"slug":"header","tagName":"header"} /-->

<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main class="wp-block-group">
	<!-- wp:query {"query":{"inherit":true}} -->
	<div class="wp-block-query">
		<!-- wp:post-template -->
			<!-- wp:post-title {"isLink":true} /-->
			<!-- wp:post-excerpt /-->
		<!-- /wp:post-template -->

		<!-- wp:query-pagination -->
			<!-- wp:query-pagination-previous /-->
			<!-- wp:query-pagination-next /-->
		<!-- /wp:query-pagination -->

		<!-- wp:query-no-results -->
			<!-- wp:paragraph -->
			<p>Aucun contenu.</p>
			<!-- /wp:paragraph -->
		<!-- /wp:query-no-results -->
	</div>
	<!-- /wp:query -->
</main>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","tagName":"footer"} /-->
```

## `templates/single.html`

```html
<!-- wp:template-part {"slug":"header","tagName":"header"} /-->

<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main class="wp-block-group">
	<!-- wp:post-title {"level":1} /-->
	<!-- wp:post-content {"layout":{"type":"constrained"}} /-->
</main>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","tagName":"footer"} /-->
```

## `templates/page.html`

```html
<!-- wp:template-part {"slug":"header","tagName":"header"} /-->

<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main class="wp-block-group">
	<!-- wp:post-title {"level":1} /-->
	<!-- wp:post-content {"layout":{"type":"constrained"}} /-->
</main>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","tagName":"footer"} /-->
```

## `functions.php` du thème

```php
<?php
if (!defined('ABSPATH')) {
    exit;
}

add_action('after_setup_theme', function () {
    add_theme_support('wp-block-styles');
    add_theme_support('editor-styles');
});
```

## `{{PLUGIN_SLUG}}.php` (en-tête plugin, obligatoire)

```php
<?php
/**
 * Plugin Name: {{PLUGIN_NAME}}
 * Description: Plugin custom scaffoldé par sc-php:setup.
 * Version: 0.1.0
 * Requires PHP: 8.0
 */

if (!defined('ABSPATH')) {
    exit;
}
```

## Notes

- Le thème contient uniquement le rendu/templates (FSE). Toute la logique métier (formulaires, blocs SSR, intégrations tierces) va dans le plugin — jamais dans `functions.php` du thème au-delà du setup de base. C'est la séparation observée sur les projets WP FSE matures : le thème reste remplaçable, le plugin porte les fonctionnalités.
- Les cinq fichiers `.html` ci-dessus sont un **plancher navigable**, pas une maquette : le contenu FSE réel se construit ensuite avec l'éditeur, ou via `design:enforce`/`design:diffuse` si le pivot design est utilisé.
