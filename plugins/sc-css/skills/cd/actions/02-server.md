# Server

## Inputs

- Confirmed pure-static ownership, deterministic output and production target facts.

## Process

1. Read [static-delivery](../references/static-delivery.md); stop if output, exclusions, cache or recovery cannot be determined.
2. Reconcile one manager-native `deploy:prod` facade that calls a project-owned script.
3. Build into a clean artifact, transfer only the declared output, verify source identity/content and retain or document the prior artifact recovery.
4. Write a secret-free `deploy/contract.json` matching the command and working directory.

## Outputs

One static facade and project contract, or a no-write gap. Configuration does not itself deploy.

## Test

Build/dry-run, validate artifact and contract, then reconcile twice with no diff.
