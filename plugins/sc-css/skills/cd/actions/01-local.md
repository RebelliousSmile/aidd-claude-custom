# Local

Reconcile a deterministic static build and preview without crossing the application ownership boundary.

## Input

- Static source, existing manager, build and preview configuration, and evidence of any application owner.

## Output

An idempotent static local procedure or a bounded CSS contributor record.

## Process

1. **Classify.** Determine whether sc-css owns a pure static root or contributes to a language-owned application.
   - For a composite application, limit the intended writes to the declared CSS scope and route root setup to its owner.
2. **Detect.** Read the configured manager, build, preview, output, and local URL without assuming conventional paths.
3. **Reconcile.** Add or preserve only the smallest local commands and bounded example configuration.
4. **Verify.** Build and preview without contacting production, then repeat reconciliation over unchanged inputs.

## Test

| Case | Pass |
| --- | --- |
| pure static fixture runs build and preview twice | both commands resolve and the second reconciliation produces no diff |
| composite fixture already has a language owner | no second root script or owner is intended |
| any local verification is inspected | no production command or credential access occurs |
