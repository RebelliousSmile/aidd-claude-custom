---
name: cd
description: Standardize local setup and production delivery for JavaScript projects through pnpm scripts, with framework-aware server delivery and delegation of CI or PaaS envelopes to sc-tiers. Use for cd local, cd server, cd automata, deploy:prod, deploy:db, or deploy:sync. Not for staging or generic CI unrelated to delivery.
---

Read [host portability](../../references/host-portability.md), then [the common contract](../../references/cd-contract.md) and [the project schema](../../references/cd-project-contract.schema.json).

# JavaScript delivery

Keep one project-owned root facade. Prefer the detected package manager, with `pnpm deploy:prod` as the standard when pnpm owns the project. Never create a staging environment.

## Actions

| Action | Déclencheur | Route | Result |
| --- | --- | --- | --- |
| `local` | `cd local`, local setup | [01-local](actions/01-local.md) | Reconciles a repeatable local runtime. |
| `server` | `cd server`, `deploy:prod`, `deploy:db`, `deploy:sync` | [02-server](actions/02-server.md) | Reconciles the native production facade and project contract. |
| `automata` | `cd automata`, delivery CI or PaaS | [03-automata](actions/03-automata.md) | Validates the facade, then delegates its envelope to sc-tiers. |

Detect the stack through the existing `sniff` skill or its references; do not create a competing taxonomy. Read [framework strategies](references/frameworks.md), [data rules](references/data-layers.md), and [facade reconciliation](references/command-facade.md) only as needed.

Before writing, decide whether sc-js owns the root or contributes a bounded workspace. If ownership or a safe strategy is unknown, report the gap and make no delivery changes. Setup alone never performs an external deployment.
