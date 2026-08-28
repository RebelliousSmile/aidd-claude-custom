# Server

Reconcile one project-owned static production facade without executing it.

## Input

- Verified static ownership, deterministic output, target facts, cache policy, proof, and recovery.

## Output

One manager-native facade, one owned script, and a matching secret-free project contract, or a no-write gap.

## Process

1. **Load.** Read [static delivery](../references/static-delivery.md) and stop when output, exclusions, cache, proof, or recovery is unknown.
2. **Reconcile.** Preserve identical fields and add one `deploy:prod` facade that calls one versioned project script.
   - Report a divergent user-owned command and request arbitration without overwriting it.
3. **Bound.** Build a clean declared artifact and describe transfer, identity proof, cache behavior, and prior-artifact recovery.
4. **Contract.** Write `deploy/contract.json` with the exact native command and working directory and secret names only.
5. **Verify.** Run build, dry-run, artifact, facade, and contract checks without contacting production.

## Test

| Case | Pass |
| --- | --- |
| static fixture has complete delivery evidence | one facade, one script, and one matching contract are intended |
| output or cache policy is unknown | no facade, target, script, or contract is intended |
| an existing command conflicts | it remains unchanged and arbitration is requested |
| reconciliation runs twice unchanged | the second intended-write set is empty |
