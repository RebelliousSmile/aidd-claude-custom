# Automata

## Inputs

- Current static project contract and installed `sc-tiers`.

## Process

1. Revalidate facade, working directory, build output, source proof and recovery.
2. Stop without files or plugin installation when `sc-tiers` is absent.
3. Delegate the exact contract to `sc-tiers:cd automata`; keep build/cache semantics in the project script.
4. Use manual trigger by default and explicit push only.

## Outputs

A thin provider envelope created by sc-tiers.

## Test

Confirm it invokes the exact facade, publishes only the declared output and relays failures.
