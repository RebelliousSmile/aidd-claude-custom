# Detect-framework

Détermine le framework cible à scaffolder avant de dispatcher vers l'action correspondante. Cette action gère la sélection ; elle ne scaffold rien elle-même.

## Inputs

- Répertoire de travail courant (project root).
- Requête utilisateur (peut nommer explicitement le framework : "monte-moi un WordPress", "scaffold un Laravel", etc.).

## Process

1. **Projet déjà configuré ?** Si `composer.json` ou un fichier sentinelle (`wp-config.php`, `artisan`, `bin/console`) existe déjà à la racine, arrêter : ce n'est plus un scaffold depuis zéro. Rediriger vers `sc-php:sniff` puis `sc-php:audit` — ne jamais écraser un projet existant.
2. **Framework nommé explicitement dans la requête** → utiliser directement, passer à l'action correspondante (pas de question).
3. **Framework ambigu ou non nommé** → poser la question à l'utilisateur : WordPress (FSE + Docker/wp-env), Laravel (+ Docker Compose), ou Symfony (+ Docker Compose). Ne jamais deviner silencieusement.
4. **Mapping vers l'action suivante** :
   - WordPress → `02-scaffold-wordpress`
   - Laravel → `03-scaffold-laravel`
   - Symfony → `04-scaffold-symfony`

## Outputs

`framework` résolu (`wordpress` | `laravel` | `symfony`), consommé par l'action de scaffold correspondante.

## Test

Le framework choisi correspond soit à ce que l'utilisateur a nommé explicitement, soit à sa réponse à la question posée — jamais une valeur devinée.
