# Automata

## Inputs

- Current validated project contract and installed `sc-tiers`.

## Process

1. Execute the facade's non-mutating validation and reject command, directory, target or source drift.
2. Stop without writing if `sc-tiers` is missing.
3. Delegate the exact command and contract to `sc-tiers:cd automata`; keep compilation and release semantics in the project.
4. Default to manual and accept push only when explicitly declared.

## Outputs

A thin provider envelope that relays the project's exit code.

## Test

Confirm local and CI invoke the same versioned command with the same working directory and no secret values.
