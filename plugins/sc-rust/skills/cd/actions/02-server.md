# Server target

Reconcile one identifiable, gated, and reversible Rust release procedure.

## Input

- Verified topology, named `server` target, phase, lifecycle guard, build host and target, service facts, target-scoped release directory, source identity, migration strategy, proof, and recovery.

## Output

One project facade, one identifiable artifact procedure, and a matching secret free contract, or a no write gap.

## Process

1. **Load.** Read [facade selection](../references/command-facade.md), [release invariants](../references/releases.md), and [SQL delivery](../references/sql-delivery.md).
2. **Select.** Resolve the exact target id, phase, invocation, lifecycle revision and independent lock. Preserve the existing project mechanism or add a versioned xtask and Cargo alias when that strategy is proven.
   - Report a divergent user owned alias or runner and request arbitration without overwriting it.
3. **Identify.** Bind artifact package, binary, features, profile, compilation target, source and checksum for this invocation; stop on an unknown target or unproven cross compilation.
4. **Gate.** Separate build, checksum, transfer, detected schema migration, target pointer switch, restart, health proof and target-scoped recovery. Any non-zero result stops the sequence.
5. **Authorize.** Production permits schema migration but refuses local business data and persistent-file transfer. Staging permits defined mirror operations only under the shared differential protocol.
6. **Contract.** Write `deploy/contract.json` with exact facade, directory, named target, invocation, lifecycle guard, source, operations and secret names.
7. **Verify.** Exercise arguments, exit propagation, concurrent independent locks and failure paths on fixtures without remote mutation, then repeat reconciliation.

## Test

| Case | Pass |
| --- | --- |
| supported workspace release is configured | facade and contract identify the exact artifact and preserve a previous release |
| cross target lacks a proven builder | no artifact target, transfer, service, or contract is intended |
| migration exits non-zero | no pointer switch or restart follows |
| health check fails after switch | the previous pointer and service are restored |
| reconciliation runs twice unchanged | the second intended-write set is empty |
| one target migration fails | neither its pointer nor any other target is mutated |
| target is switched to automata | alias and target arguments remain byte-for-byte identical |
