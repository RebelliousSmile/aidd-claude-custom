# Server

Reconcile one Composer facade with explicit WordPress or PHP delivery scopes.

## Input

- Verified local setup, framework strategy, production target facts, requested scope, proof, and recovery.

## Output

One Composer facade, one owned implementation, and a matching secret free contract, or a no write refusal.

## Process

1. **Load.** Read [facade reconciliation](../references/command-facade.md), [framework strategies](../references/php-frameworks.md), and [WordPress synchronization](../references/wordpress-sync.md).
2. **Reconcile.** Preserve targets and custom behavior while placing an existing legacy implementation behind one Composer facade.
   - Report conflicting semantics and request arbitration without adding a second producer.
3. **Scope.** Keep `deploy:prod` code only unless another surface is explicitly selected with direction and deletion policy.
4. **Guard.** Require backup, dry run or review, explicit confirmation, proof, and recovery before database, content, or media mutation.
5. **Contract.** Write `deploy/contract.json` with the exact Composer command, directory, source, operations, and secret names.
6. **Verify.** Run safe dry run and contract checks without contacting production, then repeat reconciliation.

## Test

| Case | Pass |
| --- | --- |
| normal WordPress code release is configured | database, uploads, caches, and secrets are excluded |
| sync scope or direction is absent | zero remote commands and zero project writes are intended |
| database backup or confirmation is absent | no migration, import, transfer, or remote command is intended |
| legacy pipeline is present | one Composer facade remains and custom targets are preserved |
| reconciliation runs twice unchanged | the second intended-write set is empty |
