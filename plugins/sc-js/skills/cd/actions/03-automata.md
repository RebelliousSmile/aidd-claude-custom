# Automata

## Inputs

- A current, valid `deploy/contract.json` produced by `server`.
- An installed `sc-tiers` plugin and the chosen CI or PaaS provider.

## Process

1. Revalidate the contract against the native package script; reject stale command, directory, source identity, proof, or recovery.
2. Require `sc-tiers`. If unavailable, name the prerequisite and stop without writing a fallback or installing anything.
3. Delegate provider and CI envelope generation to `sc-tiers:cd automata`, passing the exact command, working directory, operations, trigger and secret names.
4. Keep `manual` as the default trigger; accept `push` only when explicitly present in the project contract.

## Outputs

A validated handoff to sc-tiers. JavaScript deployment logic remains in the project facade.

## Test

Confirm the generated envelope calls the command textually, relays its exit status, and contains secret names but no secret values.
