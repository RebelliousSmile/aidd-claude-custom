# Server

## Inputs

- A working `local` setup and the detected build/runtime strategy.
- Production target facts, secret names, exclusions, proof and recovery procedure.

## Process

1. Read [command-facade](../references/command-facade.md), then classify static output, Node service, or framework SSR using [frameworks](../references/frameworks.md).
2. Reconcile one project-owned deployment script and its package-manager facade. Preserve an existing `deploy:prod`; stop for arbitration if its semantics conflict.
3. Add `deploy:db` or `deploy:sync` only when [data-layers](../references/data-layers.md) establishes a safe operation.
4. Make the script perform preflight, build, bounded transfer/release, proof, and an explicit recovery path. Dry-run before any mutation when supported.
5. Write `deploy/contract.json`; validate command and working directory against `package.json` and the portable schema.

## Outputs

An idempotent native facade, its owned script, and a secret-free project contract. No deployment is run unless the user explicitly requests it.

## Test

Run build, dry-run, schema/facade checks, and reconciliation twice. Confirm `pnpm deploy:prod` invokes exactly one owned script.
