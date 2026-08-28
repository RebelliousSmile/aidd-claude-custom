# Automata

## Inputs

- A current valid project contract and installed `sc-tiers`.

## Process

1. Re-run the native facade check and reject an interactive, missing or stale command.
2. Stop without writing or installing anything when `sc-tiers` is unavailable.
3. Delegate the exact command, directory, operations, trigger and secret names to `sc-tiers:cd automata`.
4. Keep manual triggering as the default; accept push only when the contract explicitly declares it.

## Outputs

A provider envelope only; all Python, process and migration logic remains behind the project facade.

## Test

Prove the envelope calls the developer command textually and returns its non-zero exit status.
