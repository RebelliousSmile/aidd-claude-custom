# Server

## Inputs

- Verified local runtime, deployment target facts and the existing manager.
- Build, process, SQL migration, proof and recovery requirements.

## Process

1. Select a proven invocation from [command-facade](../references/command-facade.md); preserve existing task configuration.
2. Reconcile one versioned project script that performs preflight, build/package, bounded release, proof and recovery.
3. Separate application release from [SQL migrations and data transfer](../references/sql-delivery.md). Add `deploy:db` only for a defined operation.
4. Ensure the command is non-interactive unless an explicit production confirmation is required before mutation.
5. Write `deploy/contract.json` with exact command, directory, source and secret names; validate it against the native invocation.

## Outputs

One native facade and a secret-free contract. Never run production delivery merely because it was configured.

## Test

Execute the script against a fixture/dry-run for the detected manager, validate contract parity, and confirm a second reconciliation is unchanged.
