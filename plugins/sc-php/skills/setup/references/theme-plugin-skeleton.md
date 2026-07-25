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

## `style.css` (en-tête thème, obligatoire pour que WP le reconnaisse)

```css
/*
Theme Name: {{THEME_NAME}}
Theme URI:
Author:
Description: Thème block-based (FSE) scaffoldé par sc-php:setup.
Version: 0.1.0
Requires at least: 6.5
Requires PHP: 8.0
*/
```

## `theme.json` (squelette minimal — à enrichir selon la charte design du projet)

```json
{
  "$schema": "https://schemas.wp.org/trunk/theme.json",
  "version": 3,
  "settings": {
    "layout": {
      "contentSize": "720px",
      "wideSize": "1200px"
    }
  }
}
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
- `templates/index.html` et `parts/header.html`/`footer.html` sont laissés minimaux (contenu FSE réel à construire avec l'éditeur ou `design:enforce`/`design:diffuse` si le pivot design est utilisé).
