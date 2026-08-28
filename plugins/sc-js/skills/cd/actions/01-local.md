# Local

Reconcile a repeatable JavaScript runtime with the detected manager, framework, and local services.

## Input

- Repository manifests, lockfile, scripts, environment examples, and sniff signals for framework, rendering, adapter, SQL, and IndexedDB.

## Output

An idempotent local install and run procedure limited to the owned JavaScript scope.

## Process

1. **Detect.** Preserve the lockfile owner and consume the existing sniff classification.
2. **Reconcile.** Add or preserve environment examples, framework development commands, and only required local SQL services.
3. **Bound.** Limit intended writes to the declared JavaScript workspace when another stack owns the root.
4. **Verify.** Install, start, and probe the documented local URL without contacting production, then repeat reconciliation.

## Test

| Case | Pass |
| --- | --- |
| project has an existing lockfile | its package manager and lockfile remain unchanged |
| fresh clone follows the documented procedure | install, start, and the local probe succeed |
| composite fixture has another root owner | no second root facade or owner is intended |
| reconciliation runs twice unchanged | the second intended-write set is empty |
