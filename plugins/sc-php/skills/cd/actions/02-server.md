# Server

Reconcile one project-native root facade with explicit WordPress or PHP delivery scopes.

## Input

- Verified local setup, framework strategy, production target facts and capabilities, requested scope, proof, and recovery.

## Output

One root facade, one owned implementation, and a matching secret free contract, or a no write refusal.

## Process

1. **Load.** Read [facade reconciliation](../references/command-facade.md), [framework strategies](../references/php-frameworks.md), and [WordPress synchronization](../references/wordpress-sync.md).
2. **Detect.** Identify the existing root package-manager command and its owning script before choosing a facade. PHP or WordPress does not by itself make Composer the deployment owner.
3. **Reconcile.** Preserve targets and custom behavior behind that one existing facade. Create a Composer facade only when Composer already owns root project operations or no deployment facade exists and Composer is the detected project manager.
   - Report conflicting semantics and request arbitration without adding a second producer.
4. **Profile.** Record commands available on the actual host. Prefer the strongest verified transport without assuming that two shared hosts expose the same SSH, shell, archive, rsync, WP-CLI, database, or scheduler capabilities.
5. **Scope.** Keep `deploy:prod` code only unless another surface is explicitly selected with direction and deletion policy.
6. **Guard.** Require backup, dry run or review, explicit confirmation, proof, and recovery before database, content, or media mutation.
7. **Contract.** Write `deploy/contract.json` with the exact root command, manager, directory, source, operations, host capability assumptions, and secret names.
8. **Verify.** Run local dry-run and contract checks without contacting production. Run a read-only remote capability or proof probe only when the user explicitly requests remote verification, then repeat reconciliation.

## Test

| Case | Pass |
| --- | --- |
| normal WordPress code release is configured | database, uploads, caches, and secrets are excluded |
| sync scope or direction is absent | zero remote commands and zero project writes are intended |
| database backup or confirmation is absent | no migration, import, transfer, or remote command is intended |
| existing pnpm/PowerShell or Composer pipeline is present | its one root facade remains and custom targets are preserved |
| host offers more capabilities than another known host | verified capabilities select the procedure; the provider name does not cap it |
| reconciliation runs twice unchanged | the second intended-write set is empty |
