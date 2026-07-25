# Docker Compose — Symfony

Placeholders : `{{APP_SLUG}}`, `{{PHP_VERSION}}` (défaut `8.3`), `{{APP_PORT}}` (défaut `8000`).

## `docker-compose.yml`

```yaml
services:
  app:
    build:
      context: .
      dockerfile: docker/php.Dockerfile
      args:
        PHP_VERSION: "{{PHP_VERSION}}"
    volumes:
      - .:/var/www/html
    depends_on:
      - db
    environment:
      DATABASE_URL: "mysql://symfony:symfony@db:3306/{{APP_SLUG}}?serverVersion=8.0"

  nginx:
    image: nginx:stable-alpine
    ports:
      - "{{APP_PORT}}:80"
    volumes:
      - .:/var/www/html
      - ./docker/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - app

  db:
    image: mysql:8
    environment:
      MYSQL_DATABASE: "{{APP_SLUG}}"
      MYSQL_USER: symfony
      MYSQL_PASSWORD: symfony
      MYSQL_ROOT_PASSWORD: root
    volumes:
      - db-data:/var/lib/mysql

volumes:
  db-data:
```

## `docker/php.Dockerfile`

```dockerfile
ARG PHP_VERSION=8.3
FROM php:${PHP_VERSION}-fpm-alpine

RUN docker-php-ext-install pdo pdo_mysql

WORKDIR /var/www/html
```

## `docker/nginx.conf`

```nginx
server {
    listen 80;
    index index.php;
    root /var/www/html/public;

    location / {
        try_files $uri /index.php$is_args$args;
    }

    location ~ ^/index\.php(/|$) {
        fastcgi_pass app:9000;
        fastcgi_split_path_info ^(.+\.php)(/.*)$;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param DOCUMENT_ROOT $document_root;
    }
}
```

## Provisioning

1. `composer create-project symfony/skeleton:"7.*" .` (variante `symfony/website-skeleton` si un starter Twig+assets complet est voulu plutôt que l'API minimale).
2. Écrire les trois fichiers ci-dessus.
3. Aligner `DATABASE_URL` dans `.env.local` (jamais committer ce fichier) sur la valeur du service `db`.
4. `docker compose up -d --build`, puis `docker compose exec app php bin/console doctrine:database:create` et `docker compose exec app php bin/console doctrine:migrations:migrate`.

## Portée volontairement plus légère que WordPress

Même remarque que pour Laravel : flow basé sur l'installeur officiel + Docker Compose standard, sans retour d'expérience production équivalent au flow WordPress de cette skill.
