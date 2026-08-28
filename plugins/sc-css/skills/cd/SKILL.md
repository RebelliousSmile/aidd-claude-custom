---
name: cd
description: Standardize local preview and production delivery for pure static or CSS-owned sites, while limiting CSS to a bounded contributor when a language plugin owns the application facade, and delegating CI or hosting envelopes to sc-tiers. Use for cd local, cd server, cd automata, or deploy:prod on static sites. Not for taking ownership from a JS, PHP, Python, or Rust application.
---

Read [host portability](../../references/host-portability.md), [the common contract](../../references/cd-contract.md), and [the project schema](../../references/cd-project-contract.schema.json).

# Static delivery

First determine ownership. A pure static site may be owned by sc-css. If a language runtime owns the root build or delivery, register only a bounded CSS/static contribution and route the root request to that plugin; never write a competing facade.

## Actions

| Action | Déclencheur | Route | Result |
| --- | --- | --- | --- |
| `local` | `cd local`, static preview | [01-local](actions/01-local.md) | Reconciles deterministic build and preview commands. |
| `server` | `cd server`, `deploy:prod` for a static site | [02-server](actions/02-server.md) | Reconciles the native static facade and project contract. |
| `automata` | `cd automata`, static delivery CI or host | [03-automata](actions/03-automata.md) | Validates and hands the exact facade to sc-tiers. |

Use [static-delivery](references/static-delivery.md). Unknown build output or cache semantics are a gap with no target written.
