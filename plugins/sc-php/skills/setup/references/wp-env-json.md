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
  "testsEnvironment": false,
  "config": {
    "WP_DEBUG": true,
    "SCRIPT_DEBUG": true
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

## Pas d'environnement de tests, et pas de bloc `env`

`"testsEnvironment": false` n'est pas une économie de confort, c'est ce qui rend le scaffold **cohabitable**. L'environnement de tests de wp-env écoute par défaut sur le port fixe **8889**, indépendant de `{{PORT}}` : deux projets scaffoldés par cette skill sur une même machine entrent en collision, même avec des ports HTTP distincts.

La collision ne dégrade pas, elle bloque — mesuré : `Bind for 0.0.0.0:8889 failed: port is already allocated`, et l'échec du conteneur de tests fait échouer `wp-env start` **en entier**, alors que le conteneur de développement a démarré. Toute commande ultérieure rend `Environment not initialized. Run wp-env start first.` Un port qui ne sert pas le site rend le site inutilisable.

Le bloc `env` est par ailleurs déprécié par wp-env, qui l'annonce à chaque démarrage : *« The "env", "testsPort", and "testsEnvironment" options are also deprecated. Use the --config option with a separate config file for test environments instead. »* `WP_DEBUG` et `SCRIPT_DEBUG` remontent donc dans le `config` racine, où ils s'appliquent à l'environnement unique.

`testsEnvironment` est nommée dans ce message, mais **la garder seule n'émet aucun avertissement** — mesuré sur `@wordpress/env` 11.12.0 : template ci-dessus, démarrage complet, zéro ligne de dépréciation. C'est le bloc `env` qui déclenche l'avertissement. Le jour où `testsEnvironment` disparaîtra vraiment, l'absence d'environnement de tests deviendra le défaut et la clé pourra simplement être retirée.

**Quand un projet a réellement besoin de PHPUnit**, la voie n'est pas de rouvrir `env` : c'est un fichier de config séparé passé à `--config`, avec un port choisi par le projet et non hérité.

## `WP_DEFAULT_THEME` n'y est pas, volontairement

La constante ne choisit le thème qu'au moment de `wp core install`. wp-env installe WordPress avant de résoudre `themes`, donc le site démarre sur le thème par défaut du core quoi qu'elle dise — mesuré : `WP_DEFAULT_THEME` valant le slug scaffoldé, et `get_stylesheet()` rendant `twentytwentyfive`, thème scaffoldé `Inactive`.

L'activation est une **étape explicite** du scaffold (`02-scaffold-wordpress.md`), pas une constante de configuration.
