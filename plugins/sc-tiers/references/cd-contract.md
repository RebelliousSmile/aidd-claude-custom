# SC CD contract

Canonical maintenance source: `tools/sc-cd/contract.md`. This file is copied byte-for-byte to every `sc-*` plugin so each plugin remains independently installable.

## Environments

- `local` is the only development environment.
- `production` is the only remote delivery environment.
- A skill must not invent another environment.

## Public actions

- `local` reconciles a reproducible local runtime owned by the active stack.
- `server` reconciles the production procedure and target without mutating the remote target unless the user separately authorizes that execution.
- `automata` connects an installed production procedure to CI or a managed provider. It never reimplements deployment.

## Command direction

- Every `deploy:*` operation moves an explicitly named scope from local to production.
- Every production-to-local operation uses `pull:*`.
- `deploy:prod` is the normal code or release delivery.
- `deploy:db` and `deploy:sync` exist only when the stack defines their exact scope, preconditions, proof, and recovery.

## Single procedure

- One project has one root deployment facade and one owning script.
- Package-manager commands expose that script; they do not contain a second procedure.
- CI and providers invoke the exact command declared by the project contract and preserve its exit code.
- Composite projects may declare scoped contributors, but contributors do not create another root facade.

## Reconciliation

- Detect before writing and report unsupported combinations without inventing files.
- Create absent owned fields, preserve identical fields, and update only bounded generated regions.
- Never silently replace a user-owned command or target. Report the conflict and ask for arbitration.
- A second run over unchanged inputs produces no diff.

## Production safety

- Never store secret values in versioned configuration; declare only required secret names and their expected source.
- Display the target, source revision, dirty-worktree state, and operation scope before a production mutation.
- A dirty local source requires an explicit project policy and confirmation; it is never silently treated as a clean revision.
- Every mutation declares preconditions, an observable post-delivery proof, and a recovery path.
- Database or content replacement requires a fresh backup and explicit confirmation.
- No setup, verification, fixture, or dry-run contacts a real production target.

## Automation

- Automation requires a valid `deploy/contract.json` whose command matches the native package-manager facade.
- The default trigger is manual. A push trigger is emitted only when the project contract explicitly requests it.
- Missing provider support or a missing `sc-tiers` capability stops without writing a fallback workflow.
