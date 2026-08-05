# Docker Compose — Laravel

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
      DB_HOST: db
      DB_DATABASE: "{{APP_SLUG}}"
      DB_USERNAME: laravel
      DB_PASSWORD: laravel

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
      MYSQL_USER: laravel
      MYSQL_PASSWORD: laravel
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
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        fastcgi_pass app:9000;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }
}
```

## Provisioning

1. `composer create-project laravel/laravel .` (ou dans un dossier temporaire puis déplacer le contenu si le dossier cible n'est pas vide).
2. Écrire les trois fichiers ci-dessus.
3. Copier `.env.example` vers `.env`, aligner `DB_HOST=db`, `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD` sur les valeurs du service `db`.
4. `docker compose up -d --build`, puis `docker compose exec app php artisan key:generate` et `docker compose exec app php artisan migrate`.

## Portée volontairement plus légère que WordPress

Ce flow s'appuie sur l'installeur officiel (`composer create-project`) et un Docker Compose standard PHP-FPM/nginx/MySQL — il n'a pas (encore) de retour d'expérience production équivalent au flow WordPress de cette skill, né d'un déploiement réel. Signaler tout piège rencontré en usage réel pour enrichir cette référence.
