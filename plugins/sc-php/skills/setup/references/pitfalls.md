# Pièges connus — scaffold PHP + Docker

Généralisés depuis un déploiement WordPress réel. L'entrée 1 est générique à tout projet Docker Compose (WordPress, Laravel, Symfony) ; les entrées 2 et 3 sont spécifiques à WordPress/wp-env.

## 1. Nom de dossier invalide pour Docker Compose (générique — tous frameworks)

Docker Compose dérive par défaut le nom du projet du nom du dossier courant (`wp-env` fait de même en interne pour WordPress, mais un `docker-compose.yml` brut pour Laravel/Symfony a exactement le même comportement). Docker Compose interdit certaines séquences de caractères dans un nom de projet (notamment un tiret suivi d'un underscore, `-_`) — un nom de projet invalide produit une image mal nommée et le démarrage échoue silencieusement ou avec une erreur peu claire.

**Symptôme** : `docker compose up` (ou `wp-env start`) échoue, ou les conteneurs ne démarrent jamais, sans message d'erreur exploitable au premier abord.

**Solution** : ne jamais laisser Docker Compose dériver le nom automatiquement si le dossier contient des caractères à risque. Forcer explicitement `COMPOSE_PROJECT_NAME` à une valeur assainie (alphanumérique + tirets simples uniquement, déterministe, unique par projet pour éviter les collisions entre projets voisins), posée en tête de tout script qui pilote Docker Compose — scripts de démarrage/arrêt ET scripts Node/CI qui invoquent Docker en sous-main. Voir `references/compose-project-name-guard.md` pour l'implémentation.

## 2. Cache navigateur qui masque les modifications CSS de bloc

En développement WP_DEBUG actif, le CSS des blocs Gutenberg est servi avec un nom de fichier stable — le navigateur le garde en cache même après une modification du fichier source. Une modification CSS peut donc sembler "ne pas s'appliquer" alors que le fichier est correct.

**Solution** : buster le cache via `filemtime()` sur l'URL de l'asset quand `WP_DEBUG` est actif (timestamp du fichier en query string), pour que chaque sauvegarde invalide le cache navigateur automatiquement.

## 3. wp-cli : ne jamais appeler le binaire local

Si PHP et wp-cli sont installés localement sur la machine hôte (ex. `php wp-cli.phar`), les commandes wp-cli ciblent la configuration WordPress trouvée sur le PATH local — qui peut pointer vers une base de données complètement différente de celle visible dans le navigateur (servie par les conteneurs Docker de wp-env).

**Symptôme classique** : une commande wp-cli semble s'exécuter sans erreur, mais le résultat n'apparaît jamais sur le site ouvert dans le navigateur — parce qu'elle a modifié la mauvaise base de données.

**Solution** : toujours invoquer wp-cli via le wrapper `scripts/wp.ps1` du projet, donc `pnpm wp <commande>` — jamais le binaire local, et jamais `pnpm dlx @wordpress/env run cli wp` nu, qui route bien vers Docker mais perd le garde `COMPOSE_PROJECT_NAME` (cf. `compose-project-name-guard.md`). Documenter cette règle en tête de toute mémoire projet issue de ce scaffold.
