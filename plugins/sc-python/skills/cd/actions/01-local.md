# Local

Reconcile a repeatable Python environment, application process, workers, and local services.

## Input

- Python manifests, lockfiles, interpreter constraint, environment commands, and sniff signals for runtime, workers, ORM, and SQL.

## Output

An idempotent install and local run procedure using the existing environment manager.

## Process

1. **Detect.** Preserve uv, Poetry, Pipenv, or the documented virtual environment workflow and stop on ambiguous manager evidence.
2. **Reconcile.** Add or preserve dependency installation, example variables, and only required SQL or broker services.
3. **Separate.** Document independent application and worker commands from proven entrypoints.
4. **Verify.** Start and probe the local application without production access, then repeat reconciliation.

## Test

| Case | Pass |
| --- | --- |
| fixture has a manager and lockfile | both remain the selected environment workflow |
| requirements only fixture lacks a runner decision | no manager or task runner file is intended and user agreement is requested |
| application and worker are present | each receives a separate documented command |
| reconciliation runs twice unchanged | the second intended-write set is empty |
