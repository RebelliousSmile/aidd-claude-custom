# Legacy deployment pipeline migration

`setup wire-deploy` historically generated `scripts/deploy.mjs`, `scripts/deploy-targets.mjs` and a pnpm `deploy` script. New delivery is owned by `sc-php:cd`; this reference exists only to recognize and migrate that shape.

Migration preserves existing target facts, exclusions, custom hooks and the `COMPOSE_PROJECT_NAME` guard. It reconciles them behind one Composer `deploy:prod` facade and writes the common `deploy/contract.json`. It never creates a parallel implementation or overwrites divergent user code silently.

Legacy database export is not promoted into code deployment. WordPress database, content and media operations follow `sc-php:cd/references/wordpress-sync.md`: explicit scope and direction, backup, dry-run/review, production confirmation, proof and recovery. Secret values never enter target or contract files.

Compatibility setup and verification never contact a remote target. An actual production deployment occurs only after an explicit user request through the project facade.
