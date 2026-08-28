# Automata

Validate the static facade and delegate a thin automation envelope.

## Input

- A current static project contract, declared provider, and available sc-tiers capability.

## Output

A validated handoff containing the exact static facade and contract facts.

## Process

1. **Validate.** Compare facade, working directory, output, source proof, operations, and recovery to the project contract.
2. **Require.** Stop without writing or installing anything when sc-tiers is unavailable.
3. **Delegate.** Pass the exact contract to `sc-tiers:cd automata` while leaving build and cache logic in the project script.
4. **Trigger.** Use manual delivery by default and preserve push only when the contract explicitly declares it.

## Test

| Case | Pass |
| --- | --- |
| contract and native facade agree | the handoff preserves command, directory, output, proof, and recovery byte-for-byte |
| sc-tiers is absent | no provider, workflow, fallback, or plugin installation is intended |
| trigger is absent | the handoff resolves it to manual |
| delegated facade exits non-zero | the envelope is required to preserve the failing status |
