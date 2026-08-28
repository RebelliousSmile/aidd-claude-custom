---
name: cd
description: Standardize local setup and production delivery for WordPress, Laravel, and Symfony through a Composer facade, including scoped WordPress synchronization and delegation of CI or PaaS envelopes to sc-tiers. Use for cd local, cd server, cd automata, deploy:prod, deploy:db, or deploy:sync. Not for staging or generic PHP scaffolding.
---

Read [host portability](../../references/host-portability.md), [the common contract](../../references/cd-contract.md), and [the project schema](../../references/cd-project-contract.schema.json).

# PHP delivery

`cd` is the delivery authority. Keep one root facade owned by the application stack; JS and CSS are bounded contributors in WordPress projects. Prefer `composer deploy:prod`; existing WordPress pnpm wrappers remain implementation commands, not a second facade.

## Actions

| Action | Déclencheur | Route | Result |
| --- | --- | --- | --- |
| `local` | `cd local`, WordPress/Laravel/Symfony local setup | [01-local](actions/01-local.md) | Reconciles wp-env or Compose without destructive side effects. |
| `server` | `cd server`, `deploy:prod`, `deploy:db`, `deploy:sync` | [02-server](actions/02-server.md) | Reconciles the Composer facade and scoped production contract. |
| `automata` | `cd automata`, delivery CI or PaaS | [03-automata](actions/03-automata.md) | Validates and hands the exact facade to sc-tiers. |

Use [framework strategies](references/php-frameworks.md), [WordPress synchronization](references/wordpress-sync.md), and [facade reconciliation](references/command-facade.md). Never deploy during setup, reset WordPress, destroy containers, or import a database as a side effect.
