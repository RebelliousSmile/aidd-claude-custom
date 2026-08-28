# Local

## Inputs

- Python manifests, lockfiles, interpreter constraint and existing environment commands.
- Framework, ASGI/WSGI server, worker, ORM and SQL signals from `sc-python:sniff`.

## Process

1. Preserve uv, Poetry, Pipenv or the documented virtual-environment workflow.
2. Reconcile dependency installation, example variables and only the local SQL/broker services actually required.
3. Document separate application and worker commands using the detected framework/runtime.
4. Start and probe the local application without contacting production.

## Outputs

An idempotent install/start procedure and explicit gaps. Do not add a manager to a requirements-only project without user agreement.

## Test

Execute the documented non-interactive command in the manager's environment and reconcile twice with no second diff.
