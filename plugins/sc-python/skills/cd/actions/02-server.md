# Server target

Reconcile one native Python delivery facade while keeping migrations and mutable data separate.

## Input

- Verified local runtime, existing manager, a named `server` target, selected `deploy:*` operation, process ordering, SQL strategy, proof, and recovery.

## Output

One manager native facade, one versioned project script, and a matching secret free contract, or a no write gap.

## Process

1. **Load.** Read [facade selection](../references/command-facade.md), [runtime strategies](../references/python-frameworks.md), and [SQL delivery](../references/sql-delivery.md).
2. **Select.** Resolve the target by exact id, validate its phase, lifecycle revision and independent lock, then use its proven invocation. Stop on an ambiguous target, entrypoint, task-runner decision, or stale guard.
3. **Reconcile.** Preserve an identical command and add one versioned deployment script when absent.
   - Report a divergent user owned command and request arbitration without overwriting it.
4. **Separate.** Keep artifact release, schema migration, mutable data transfer, and worker ordering as distinct operations.
5. **Protect.** In production, allow declarative schema migration but refuse local data or managed-media transfer. In staging, use manifest-based differential sync only for a proven inventoriable store and require preview, backup, confirmation and recovery before mirror deletions.
6. **Contract.** Write `deploy/contract.json` with exact command, directory, named target, invocation, source, operations, lifecycle guard, proof, recovery and secret names.
7. **Verify.** Execute only fixture or dry run checks, validate target-specific contract parity, and repeat reconciliation. Propagate every facade, migration, media, health or restart failure.

## Test

| Case | Pass |
| --- | --- |
| uv, Poetry, or Pipenv fixture is supported | its existing manager invokes one versioned deployment script |
| requirements only fixture lacks a runner decision | no conversion or deployment facade is intended |
| migration is defined without data copy | no local database upload or mutable data transfer is invented |
| production import lacks scope, backup, or confirmation | no remote SQL command is intended |
| reconciliation runs twice unchanged | the second intended-write set is empty |
| two server targets exist | only the explicitly named target is locked and invoked |
| production media or data push is requested | no transport or remote mutation is intended |
