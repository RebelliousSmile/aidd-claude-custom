---
name: cd
description: Configure hosting-provider prerequisites and generate thin CI or PaaS delivery envelopes from an existing validated deploy/contract.json for SSH, Railway, Heroku, GitHub Actions, or GitLab CI. Use for cd local, cd server, cd automata, or connecting a project-owned deploy command to a provider. Not for inventing application deployment logic or working without a producer contract.
---

Read [host portability](../../references/host-portability.md), [the common contract](../../references/cd-contract.md), and [the project schema](../../references/cd-project-contract.schema.json).

# Provider delivery adapters

sc-tiers owns provider configuration and automation envelopes, never the deployment procedure. Require a current `deploy/contract.json` from the root language/static owner. Copy its command, working directory, operations, source, proof and recovery exactly; do not redetect the stack.

## Actions

| Action | Déclencheur | Route | Result |
| --- | --- | --- | --- |
| `local` | `cd local` for a third-party service | [01-local](actions/01-local.md) | Configures a supported emulator or returns explicit N/A. |
| `server` | `cd server`, SSH/Railway/Heroku provider setup | [02-server](actions/02-server.md) | Reconciles provider prerequisites without deploying. |
| `automata` | `cd automata`, GitHub/GitLab/Railway/Heroku delivery | [03-automata](actions/03-automata.md) | Generates a thin envelope from the validated contract. |

Read [providers](references/providers.md) or [CI adapters](references/ci-adapters.md) as needed. Unsupported providers, absent/stale contracts or divergent commands stop before any write.
