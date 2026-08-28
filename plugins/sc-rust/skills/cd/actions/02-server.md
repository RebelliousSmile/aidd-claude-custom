# Server

## Inputs

- Verified local topology, build host/target, service target and release directory facts.
- Version/commit identity, migration strategy, health proof and recovery requirements.

## Process

1. Reconcile a proven project facade from [command-facade](../references/command-facade.md).
2. Apply [releases](../references/releases.md): build exact package/binary/features/target, checksum the artifact and bind it to commit/version.
3. Keep configuration external and transfer into a new immutable release directory.
4. Apply only detected [SQL](../references/sql-delivery.md) strategy. Build, checksum, transfer, migration, switch and restart remain separate gates.
5. Switch atomically only after pre-switch gates pass; verify health and retain the prior release for recovery.
6. Write and validate `deploy/contract.json` against the runnable project facade.

## Outputs

One native facade, an identifiable artifact procedure and a secret-free contract. Configuration does not itself deploy.

## Test

Prove argument/exit propagation, artifact checksum, failed-migration no-switch behavior, health failure recovery, and idempotent reconciliation.
