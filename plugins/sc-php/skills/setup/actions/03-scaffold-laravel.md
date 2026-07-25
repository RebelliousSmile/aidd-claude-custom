# Action 03 — scaffold-laravel

Scaffold un projet Laravel + Docker Compose depuis zéro.

## Inputs

- `project_root` (doit être vide ou quasi-vide — voir action 01).
- Slug applicatif (nom de la base de données), version PHP cible.

## Process

1. `composer create-project laravel/laravel .` (si le dossier n'est pas totalement vide, créer dans un dossier temporaire puis déplacer le contenu).
2. Lire `references/docker-compose-laravel.md` et écrire `docker-compose.yml`, `docker/php.Dockerfile`, `docker/nginx.conf`, en substituant les placeholders.
3. Lire `references/compose-project-name-guard.md` et écrire `scripts/start.ps1` / `scripts/stop.ps1`, avec `{{START_COMMAND}}` = `docker compose up -d --build` et `{{STOP_COMMAND}}` = `docker compose down`.
4. Copier `.env.example` vers `.env`, aligner `DB_HOST`, `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD` sur les valeurs du service `db` du docker-compose.
5. Ne PAS lancer `docker compose up` automatiquement — le confirmer à l'utilisateur.

## Outputs

```
docker-compose.yml
docker/php.Dockerfile
docker/nginx.conf
scripts/start.ps1
scripts/stop.ps1
.env
```

## Test

`pnpm run start` (ou exécution directe de `scripts/start.ps1`) démarre les conteneurs sans erreur de nom de projet Docker Compose, et `docker compose exec app php artisan --version` répond.
