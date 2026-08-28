---
name: cd
description: Standardize local setup and reversible production releases for Rust crates, workspaces, services, and binaries through a project-owned Cargo or task-runner facade, with SQL-aware sequencing and delegation of CI or PaaS envelopes to sc-tiers. Use for cd local, cd server, cd automata, deploy:prod, or deploy:db. Not for staging or publishing crates to a registry.
---

Read [host portability](../../references/host-portability.md), [the common contract](../../references/cd-contract.md), and [the project schema](../../references/cd-project-contract.schema.json).

# Rust delivery

Keep one versioned project facade that runs identically locally and in CI, forwards arguments and preserves exit codes. Do not invent a Cargo subcommand or install a global task runner without explicit agreement.

## Actions

| Action | Déclencheur | Route | Result |
| --- | --- | --- | --- |
| `local` | `cd local`, Rust local setup | [01-local](actions/01-local.md) | Reconciles toolchain, services and run commands. |
| `server` | `cd server`, `deploy:prod`, `deploy:db`, Rust release | [02-server](actions/02-server.md) | Reconciles a reproducible, reversible release facade. |
| `automata` | `cd automata`, delivery CI or PaaS | [03-automata](actions/03-automata.md) | Validates and hands the exact facade to sc-tiers. |

Reuse `sc-rust:sniff` signals. Consult [command facade](references/command-facade.md), [release invariants](references/releases.md), and [SQL sequencing](references/sql-delivery.md). Unsupported targets or stacks produce a gap and no deployment changes.
