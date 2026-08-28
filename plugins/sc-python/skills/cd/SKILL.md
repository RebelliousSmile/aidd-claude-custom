---
name: cd
description: Standardize local setup and production delivery for Python projects while preserving uv, Poetry, Pipenv, or the existing environment workflow, with framework-aware SQL handling and delegation of CI or PaaS envelopes to sc-tiers. Use for cd local, cd server, cd automata, deploy:prod, deploy:db, or deploy:sync. Not for staging or converting package managers.
---

Read [host portability](../../references/host-portability.md), [the common contract](../../references/cd-contract.md), and [the project schema](../../references/cd-project-contract.schema.json).

# Python delivery

Keep one project-owned facade and preserve the existing manager and lockfile. Python has no universal package-script surface, so use the proven native invocation documented in [command-facade](references/command-facade.md); never convert a project silently.

## Actions

| Action | Déclencheur | Route | Result |
| --- | --- | --- | --- |
| `local` | `cd local`, Python local setup | [01-local](actions/01-local.md) | Reconciles environment, services and application processes. |
| `server` | `cd server`, `deploy:prod`, `deploy:db`, `deploy:sync` | [02-server](actions/02-server.md) | Reconciles the native facade and production contract. |
| `automata` | `cd automata`, delivery CI or PaaS | [03-automata](actions/03-automata.md) | Validates and hands the exact facade to sc-tiers. |

Reuse `sc-python:sniff` for framework and dependency classification. Consult [python-frameworks](references/python-frameworks.md) and [sql-delivery](references/sql-delivery.md). Unknown combinations are reported as gaps with no write.
