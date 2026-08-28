# Server

## Inputs

- A verified local setup, framework strategy and production SSH facts.
- Explicit requested scopes: code, configuration, migration, database, content, or media.

## Process

1. Reconcile [the Composer facade](../references/command-facade.md), migrating the legacy setup pipeline without losing custom targets or code.
2. Keep `deploy:prod` code-only unless the project contract explicitly says otherwise.
3. For WordPress, apply [wordpress-sync](../references/wordpress-sync.md). An ambiguous sync request stops before mutation and asks for scope and direction.
4. For SQL operations require a fresh backup, dry-run where possible, explicit production confirmation, proof and recovery before import or migration.
5. Write and validate `deploy/contract.json` against the schema and Composer script. Store secret names only.

## Outputs

One Composer facade, one owned implementation, and scoped operations only where safe strategies exist. External execution requires an explicit deployment request.

## Test

Run code dry-run and contract validation twice. For risky fixtures, prove that missing scope, backup or confirmation causes zero remote commands.
