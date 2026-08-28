# Reasoned WordPress synchronization

Treat these as separate surfaces: code, configuration, schema/migrations, full database, editorial content, and media. Every operation states its scope and direction.

- `deploy:prod`: local-to-production code release by default; excludes secrets, caches, uploads and local database state.
- `deploy:db`: local-to-production database operation only when explicitly designed, backed up, dry-run/reviewed and confirmed. It is never a hidden part of code deployment.
- `deploy:sync`: local-to-production synchronization whose exact content/media/configuration scope is named. An unqualified sync request is rejected.
- `pull:*`: production-to-local operation, kept distinct from deployment and protected from overwriting local work.

WP-CLI search-replace must account for serialized data. Media transfer must state deletion behavior; default to no remote deletion. Before production mutation record a backup and recovery command, then require confirmation. Afterward prove URL, active theme/plugin and the changed scope only.
