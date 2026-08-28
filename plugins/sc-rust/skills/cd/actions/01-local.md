# Local

## Inputs

- Cargo manifests, workspace topology, toolchain file, features, binary targets and existing task configuration.
- Framework, SQL crate and external service signals from `sc-rust:sniff`.

## Process

1. Preserve the pinned Rust toolchain and existing Cargo/task-runner workflow.
2. Reconcile example variables and only required SQL or broker services.
3. Document the exact package, binary, features and local run command for crates or workspaces.
4. Compile/check and probe the application without contacting production.

## Outputs

An idempotent local procedure and explicit unsupported combinations.

## Test

Run the documented Cargo check/run command twice and confirm the second reconciliation has no diff.
