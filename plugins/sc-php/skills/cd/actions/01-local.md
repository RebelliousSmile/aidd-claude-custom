# Local

## Inputs

- Existing Composer/package manifests and framework sentinels.
- Local environment examples, database engine and current container wrappers.

## Process

1. Detect WordPress, Laravel, or Symfony using existing `sniff` signals.
2. For WordPress, reuse setup's wp-env configuration, `COMPOSE_PROJECT_NAME` guard and `pnpm wp` wrapper; verify the active theme/plugin, URL and WP-CLI.
3. For Laravel or Symfony, reconcile the existing Docker Compose services and native framework command.
4. Preserve databases and volumes. Never invoke reset, destroy or import while reconciling or verifying.

## Outputs

An idempotent local start/stop/CLI procedure and a report of prerequisites. No production access occurs.

## Test

Start twice, run the application CLI and check rendered content. Report each check as ok, failed or not applicable.
