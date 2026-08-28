# Local

## Inputs

- Named third-party provider and existing project emulator configuration.

## Process

1. Check [providers](../references/providers.md) for a proven local emulator or CLI mode.
2. If supported, reconcile only its local configuration and example variable names.
3. Otherwise return `not applicable` with the remote boundary; do not fake the provider or access production.

## Outputs

A supported local adapter or an explicit N/A. Secret values are neither requested nor written.

## Test

Start/probe the emulator when available and prove a second reconciliation is unchanged.
