# Server

Reconcile one framework aware production facade and project contract without executing delivery.

## Input

- Verified local setup, sniff classification, target facts, secret names, exclusions, proof, and recovery.

## Output

One package manager facade, one project owned script, and a matching secret free contract, or a no write gap.

## Process

1. **Load.** Read [facade reconciliation](../references/command-facade.md), [framework strategies](../references/frameworks.md), and [data rules](../references/data-layers.md).
2. **Classify.** Resolve static output, Node service, or framework server strategy from project configuration and stop on an unknown adapter.
3. **Reconcile.** Preserve an identical facade and add one project script when absent.
   - Report a divergent user owned `deploy:prod` and request arbitration without overwriting it.
4. **Scope.** Add `deploy:db` or `deploy:sync` only when its direction, preconditions, proof, and recovery are defined.
5. **Contract.** Write `deploy/contract.json` with the exact native command, working directory, source, operations, and secret names.
6. **Verify.** Run build, dry run, facade, and contract checks without contacting production, then repeat reconciliation.

## Test

| Case | Pass |
| --- | --- |
| pnpm owns a supported fixture | `pnpm deploy:prod` invokes exactly one versioned project script |
| a user command has conflicting semantics | no overwrite or second facade is intended and arbitration is requested |
| IndexedDB is detected | only client migration code is delivered and no browser data transfer exists |
| SQL migration is defined without data copy | no data transfer command is invented |
| reconciliation runs twice unchanged | the second intended-write set is empty |
