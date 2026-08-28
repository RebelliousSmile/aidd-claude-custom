# Automata

Validate the native Python facade and delegate a thin automation envelope.

## Input

- A current project contract, proven noninteractive facade, selected provider, and available sc-tiers capability.

## Output

A validated handoff containing the exact Python command, directory, operations, and trigger.

## Process

1. **Validate.** Reject an interactive, missing, or stale command and compare source, proof, recovery, and operations.
2. **Require.** Stop without writing or installing anything when sc-tiers is unavailable.
3. **Delegate.** Pass the exact contract to `sc-tiers:cd automata` without copying Python, process, or migration logic.
4. **Trigger.** Use manual delivery by default and preserve push only when explicitly declared.

## Test

| Case | Pass |
| --- | --- |
| native facade and contract agree | command and working directory are preserved byte-for-byte |
| command is interactive or stale | no workflow or provider file is intended and the defect is named |
| sc-tiers is absent | no fallback or plugin installation is intended |
| delegated facade exits non-zero | the envelope is required to preserve the failing status |
