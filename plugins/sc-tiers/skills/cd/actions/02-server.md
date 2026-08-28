# Server

## Inputs

- Valid project contract, selected SSH/Railway/Heroku provider and non-secret target facts.

## Process

1. Validate contract version, root ownership, command parity, operations, source, proof and recovery.
2. Resolve the supported provider in [providers](../references/providers.md); stop on missing CLI/primitive or unsupported provider.
3. Reconcile non-secret provider metadata and declare required secret names/source only.
4. Never read, print, collect or version a secret value. Never run the project command merely while configuring a provider.

## Outputs

Bounded provider configuration and a list of secret names the maintainer must provision out of band.

## Test

Scan generated files for secret values and prove missing primitives fail before mutation.
