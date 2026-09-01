# Promote

Accept a valid page wireframe and prepare its official `design:harness` handoff.

## Input

- Exact wireframe HTML plus current green static and rendered reports.
- Explicit reviewer identity and approval.
- New receipt and handoff paths, and `tabletPolicy = desktop-derived|mobile-derived|defer`.

## Process

1. On explicit approval, run `${DESIGN_PLUGIN_ROOT}/tools/wireframes-review.py accept` with artifact, both reports, reviewer and a distinct receipt path.
2. Run `${DESIGN_PLUGIN_ROOT}/tools/wireframes-handoff.py` with the same three files, receipt, tablet policy and a new output directory.
3. Refuse absent, revoked or stale receipts; non-page units without `parentPage`/`parentZone`; missing page harness metadata; duplicate, missing or unresolved state dispositions.
4. Use only each page's `initialState` as the harness body. Keep other states in the handoff inventory according to their declared disposition.
5. With `defer`, stop after the three-file bundle. Otherwise generate the harness with its public generator and `pages.json`, apply `migration-payload.json` through `harness-apply.py`, then run the harness proofs.

## Output

A detached immutable-evidence receipt and atomic bundle containing `pages.json`, `migration-payload.json`, and `handoff.json`. Human acceptance is never embedded in or inferred from the HTML.

## Test

Accepted current evidence promotes; missing/revoked/stale evidence, orphan fragments, unresolved states and missing tablet policy write no bundle. All three tablet policies are explicit, and only `defer` sets `invokeHarness` false.
