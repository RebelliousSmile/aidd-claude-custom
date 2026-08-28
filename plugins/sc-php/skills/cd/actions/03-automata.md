# Automata

## Inputs

- A valid, current `deploy/contract.json` and installed `sc-tiers`.

## Process

1. Compare contract command and directory to Composer, then verify source, operations, proof and recovery.
2. Stop without writing if `sc-tiers` is absent.
3. Delegate provider/CI envelope generation to `sc-tiers:cd automata` with the contract unchanged.
4. Default to manual. Permit push only when explicitly declared; keep high-risk WordPress database/content/media operations manual and confirmed.

## Outputs

A provider envelope that invokes the exact Composer facade and relays failures, without duplicating PHP or WordPress logic.

## Test

Inspect the envelope for exact command/directory, no secret values, and a non-zero exit path.
