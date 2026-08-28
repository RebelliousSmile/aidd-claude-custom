# Server

Reconcile one identifiable, gated, and reversible Rust release procedure.

## Input

- Verified topology, build host and target, service facts, release directory, source identity, migration strategy, proof, and recovery.

## Output

One project facade, one identifiable artifact procedure, and a matching secret free contract, or a no write gap.

## Process

1. **Load.** Read [facade selection](../references/command-facade.md), [release invariants](../references/releases.md), and [SQL delivery](../references/sql-delivery.md).
2. **Reconcile.** Preserve the existing project mechanism or add a versioned xtask and Cargo alias when that strategy is proven.
   - Report a divergent user owned alias or runner and request arbitration without overwriting it.
3. **Identify.** Bind artifact package, binary, features, profile, target, source, and checksum and stop on unproven cross compilation.
4. **Gate.** Separate build, checksum, transfer, detected migration, pointer switch, restart, health proof, and recovery.
5. **Contract.** Write `deploy/contract.json` with the exact facade, directory, source, operations, and secret names.
6. **Verify.** Exercise argument and exit propagation plus failure paths on a fixture without remote mutation, then repeat reconciliation.

## Test

| Case | Pass |
| --- | --- |
| supported workspace release is configured | facade and contract identify the exact artifact and preserve a previous release |
| cross target lacks a proven builder | no artifact target, transfer, service, or contract is intended |
| migration exits non-zero | no pointer switch or restart follows |
| health check fails after switch | the previous pointer and service are restored |
| reconciliation runs twice unchanged | the second intended-write set is empty |
