# Server target

Reconcile one framework aware production facade and project contract without executing delivery.

## Input

- Verified local setup, sniff classification, named `server` target, phase, lifecycle guard, secret names, exclusions, proof, and recovery.

## Output

One package manager facade, one project owned script, and a matching secret free contract, or a no write gap.

## Process

1. **Load.** Read [facade reconciliation](../references/command-facade.md), [framework strategies](../references/frameworks.md), and [data rules](../references/data-layers.md).
2. **Select.** Resolve the exact target id, phase, independent lock and invocation. Resolve static output, Node service, or framework server strategy from project configuration and stop on ambiguity or an unknown adapter.
3. **Profile.** Establish artifact filesystem provenance from the resolved path plus available Windows-path and mount evidence. Treat `/mnt/<letter>` as a signal rather than sole proof. A DrvFs source may proceed only through native-Linux artifact staging or explicit destination-mode normalization that disables permission, owner, and group preservation.
4. **Reconcile.** Preserve an identical facade and add one project script when absent.
   - Report a divergent user owned `deploy:prod` and request arbitration without overwriting it.
5. **Scope.** Keep artifact code, SQL schema, server data, browser data and managed media distinct. IndexedDB migrations ship in code and never transfer browser records.
6. **Authorize.** Production permits code and declared SQL migrations but refuses local server data or media. Staging permits a local mirror only with proven export/import or manifest inventory, preview, backup, confirmation and recovery.
7. **Contract.** Write `deploy/contract.json` with exact native command, directory, named target, invocation, lifecycle guard, source, operations and secret names.
8. **Verify.** Run build, dry run, facade and contract checks without contacting the target. Require the delivery script to execute post-transfer mode proof for at least one directory, one newly created file, and one updated file during a real delivery. Configuration verifies that the mechanism exists and is fail-closed; it does not claim the remote observations already ran. Then reread the complete current owned script and describe its control flow as a normalized observation: source path and digest, ordered success/failure events, mutations, checks, cleanup, and failure propagation. Bind every contract `proof` and `recovery` to event ids in that observation. Reject absent/unreachable events and any cleanup that removes recovery before its declared availability window ends. Do not infer arbitrary TypeScript semantics from tokens: the observation must cite the inspected script behavior. Propagate all failures and repeat reconciliation.

## Test

| Case | Pass |
| --- | --- |
| pnpm owns a supported fixture | `pnpm deploy:prod` invokes exactly one versioned project script |
| a user command has conflicting semantics | no overwrite or second facade is intended and arbitration is requested |
| IndexedDB is detected | only client migration code is delivered and no browser data transfer exists |
| SQL migration is defined without data copy | no data transfer command is invented |
| reconciliation runs twice unchanged | the second intended-write set is empty |
| several targets exist and none is named | no target, lock or invocation is selected |
| production data or media copy is requested | no transfer command is intended |
| DrvFs source preserves permissions, owner, or group | no remote command is intended and the unsafe fields are named |
| DrvFs source normalizes destination modes | dry-run is allowed only when directory, new-file, and updated-file mode proofs are declared |
| proof names no reachable checking event | reconciliation stops with a no-write gap naming the unbound proof |
| recovery cleanup precedes its promised window | reconciliation stops with a no-write gap naming the early removal |
