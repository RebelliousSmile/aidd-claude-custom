# Automata

Validate the Rust project facade and delegate a thin automation envelope.

## Input

- A current project contract, proven project facade, selected provider, and available sc-tiers capability.

## Output

A validated handoff containing the exact Rust facade, directory, operations, source, proof, and recovery.

## Process

1. **Validate.** Reject command, directory, target, source, operation, proof, or recovery drift before delegation.
2. **Require.** Stop without writing when sc-tiers is unavailable.
3. **Delegate.** Pass the unchanged contract to `sc-tiers:cd automata` while keeping build and release semantics in project code.
4. **Trigger.** Use manual delivery by default and preserve push only when explicitly declared.

## Test

| Case | Pass |
| --- | --- |
| local facade and contract agree | automation uses the same versioned command and working directory |
| contract target or command is stale | no workflow or provider file is intended and the drift is named |
| sc-tiers is absent | no fallback or plugin installation is intended |
| delegated facade exits non-zero | the envelope is required to preserve the failing status |
