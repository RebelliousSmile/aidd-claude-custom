# PHP framework strategies

| Framework | Local | Production unit |
| --- | --- | --- |
| WordPress | wp-env/Docker through project wrappers | reviewed theme/plugin code and explicitly selected synchronization scopes |
| Laravel | existing Docker Compose and Artisan | built application, Composer dependencies and reviewed Artisan migrations |
| Symfony | existing Docker Compose and Console | built application, Composer dependencies and reviewed Doctrine migrations |

Detect configuration rather than assuming document roots, public paths or process managers. Unknown hosting constraints are a gap and cause no write. SQL migrations never imply copying mutable production content.
