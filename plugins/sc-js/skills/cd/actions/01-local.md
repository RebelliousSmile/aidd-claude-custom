# Local

## Inputs

- Repository manifests, lockfile, existing scripts and environment examples.
- Framework, rendering mode, adapter, SQL/ORM and IndexedDB signals from `sc-js:sniff`.

## Process

1. Preserve the detected package manager and install command; do not replace a lockfile.
2. Reconcile environment examples, framework dev command, and only the SQL services the project actually requires.
3. Verify a fresh clone can install, start, and reach its documented local URL. Never contact production.
4. On a composite repository, limit changes to the declared JS scope and leave the root facade to its owner.

## Outputs

A documented, idempotent local command plus any reconciled examples or service definition. Report missing prerequisites without guessing credentials.

## Test

Run install and the shortest non-interactive framework check twice. Confirm the second reconciliation produces no diff.
