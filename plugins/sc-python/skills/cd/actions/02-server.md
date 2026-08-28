# Server

Reconcile one native Python delivery facade while keeping migrations and mutable data separate.

## Input

- Verified local runtime, existing manager, target facts, process ordering, SQL strategy, proof, and recovery.

## Output

One manager native facade, one versioned project script, and a matching secret free contract, or a no write gap.

## Process

1. **Load.** Read [facade selection](../references/command-facade.md), [runtime strategies](../references/python-frameworks.md), and [SQL delivery](../references/sql-delivery.md).
2. **Select.** Use the proven invocation for the existing manager and stop when an entrypoint or task runner decision is missing.
3. **Reconcile.** Preserve an identical command and add one versioned deployment script when absent.
   - Report a divergent user owned command and request arbitration without overwriting it.
4. **Separate.** Keep artifact release, schema migration, mutable data transfer, and worker ordering as distinct operations.
5. **Contract.** Write `deploy/contract.json` with exact command, directory, source, operations, and secret names.
6. **Verify.** Execute only fixture or dry run checks, validate contract parity, and repeat reconciliation.

## Test

| Case | Pass |
| --- | --- |
| uv, Poetry, or Pipenv fixture is supported | its existing manager invokes one versioned deployment script |
| requirements only fixture lacks a runner decision | no conversion or deployment facade is intended |
| migration is defined without data copy | no local database upload or mutable data transfer is invented |
| production import lacks scope, backup, or confirmation | no remote SQL command is intended |
| reconciliation runs twice unchanged | the second intended-write set is empty |
