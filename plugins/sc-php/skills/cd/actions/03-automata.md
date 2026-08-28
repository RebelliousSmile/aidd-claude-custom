# Automata

Validate the Composer facade and delegate a thin automation envelope.

## Input

- A current project contract, Composer facade, selected provider, and available sc-tiers capability.

## Output

A validated handoff containing the exact facade and scoped operations.

## Process

1. **Validate.** Compare the contract command, directory, source, operations, proof, and recovery to Composer and the project.
2. **Require.** Stop without writing when sc-tiers is unavailable.
3. **Delegate.** Pass the unchanged contract to `sc-tiers:cd automata` without duplicating PHP or WordPress logic.
4. **Trigger.** Use manual delivery by default and keep database, content, and media operations manual and confirmed.

## Test

| Case | Pass |
| --- | --- |
| contract and Composer agree | the handoff preserves command and directory byte-for-byte |
| risky WordPress operation is present | no automatic push trigger is introduced |
| sc-tiers is absent | no workflow, provider file, fallback, or plugin installation is intended |
| delegated facade exits non-zero | the envelope is required to preserve the failing status |
