# Local

## Inputs

- Static/CSS source, existing manager, build and preview configuration.
- Evidence of any application-language owner.

## Process

1. If JS, PHP, Python or Rust owns the application, reconcile only the declared CSS scope and route root setup to that owner.
2. For a pure static site, preserve its manager and identify deterministic build, preview, output and URL.
3. Reconcile the smallest local commands and verify the output is regenerated from source.

## Outputs

A bounded contributor record or an idempotent static local procedure. No production access occurs.

## Test

Build and preview twice. Confirm a composite fixture gains no second root script.
