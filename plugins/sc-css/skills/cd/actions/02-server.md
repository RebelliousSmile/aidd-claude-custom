# Server target

Reconcile one project-owned static production facade without executing it.

## Input

- Verified static ownership, deterministic output, named `server` target, phase, lifecycle guard, cache policy, proof, and recovery.

## Output

One manager-native facade, one owned script, and a matching secret-free project contract, or a no-write gap.

## Process

1. **Load.** Read [static delivery](../references/static-delivery.md) and stop when output, exclusions, cache, proof, or recovery is unknown.
2. **Select.** Resolve the exact target id, invocation, lifecycle revision and independent lock. Preserve identical fields and add one `deploy:prod` facade that calls one versioned project script.
   - Report a divergent user-owned command and request arbitration without overwriting it.
3. **Bound.** Build a clean declared artifact and describe transfer, identity proof, target cache behavior and target-scoped prior-artifact recovery. Versioned images and fonts stay inside code.
4. **Refuse.** Stop requests for databases, mutable records or user media and name the application runtime that must own them. Stop on unknown output or cache policy.
5. **Contract.** Write `deploy/contract.json` with exact native command, directory, named target, invocation, lifecycle guard, proof, recovery and secret names only.
6. **Verify.** Run build, dry-run, artifact, facade and contract checks without contacting the target, then repeat reconciliation.

## Test

| Case | Pass |
| --- | --- |
| static fixture has complete delivery evidence | one facade, one script, and one matching contract are intended |
| output or cache policy is unknown | no facade, target, script, or contract is intended |
| an existing command conflicts | it remains unchanged and arbitration is requested |
| reconciliation runs twice unchanged | the second intended-write set is empty |
| several targets exist and none is named | no destination, lock or cache policy is selected |
| user media is requested | no data or media operation is owned by sc-css |
