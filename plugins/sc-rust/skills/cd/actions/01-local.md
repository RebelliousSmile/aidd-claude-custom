# Local

Reconcile a repeatable Rust toolchain, workspace command, and required local services.

## Input

- Cargo manifests, lockfile, workspace topology, toolchain, features, binary targets, task configuration, and sniff signals.

## Output

An idempotent local check and run procedure for the exact package, binary, features, and services.

## Process

1. **Detect.** Preserve the pinned toolchain, lockfile, workspace topology, and existing task mechanism.
2. **Reconcile.** Add or preserve example variables and only required SQL or broker services.
3. **Specify.** Document the exact package, binary, features, and local run command.
4. **Verify.** Run the nonproduction check and local probe, then repeat reconciliation without contacting production.

## Test

| Case | Pass |
| --- | --- |
| workspace fixture is detected | package, binary, features, target, and toolchain match Cargo evidence |
| existing task mechanism is present | no global tool or competing facade is intended |
| unsupported topology is encountered | the gap is named and no delivery field is written |
| reconciliation runs twice unchanged | the second intended-write set is empty |
