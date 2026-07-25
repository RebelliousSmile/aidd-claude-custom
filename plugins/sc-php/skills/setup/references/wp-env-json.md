# Template `.wp-env.json`

Placeholders à substituer : `{{THEME_SLUG}}`, `{{PLUGIN_SLUG}}`, `{{PORT}}` (port HTTP local, défaut `8888` si non précisé par l'utilisateur).

```json
{
  "core": null,
  "phpVersion": "8.2",
  "plugins": [
    "./wp-content/plugins/{{PLUGIN_SLUG}}"
  ],
  "themes": [
    "./wp-content/themes/{{THEME_SLUG}}"
  ],
  "port": {{PORT}},
  "env": {
    "development": {
      "config": {
        "WP_DEBUG": true,
        "SCRIPT_DEBUG": true
      }
    },
    "tests": {
      "port": 8889
    }
  },
  "config": {
    "WP_DEFAULT_THEME": "{{THEME_SLUG}}"
  },
  "mappings": {
    "wp-content/uploads": "./wp-content/uploads"
  }
}
```

## Notes

- `phpVersion` : aligner sur la cible d'hébergement réelle (vérifier la version PHP supportée par l'hébergeur avant de la figer).
- `mappings.wp-content/uploads` : persiste les médias uploadés en dehors du volume Docker éphémère, pour survivre à un `wp-env destroy`.
- Ne jamais committer de vrai contenu dans `wp-content/uploads/` — ajouter au `.gitignore` du projet scaffoldé.
