# Wireframe to harness handoff

Promotion is a governed handoff, not shell reuse. The wireframe remains author evidence; `design:harness` remains sole owner of preview chrome, page registry, three viewport controls and runtime scripts.

## Preconditions

- Static and rendered reports are current and green.
- A detached review receipt is `accepted` and its SHA-256 digests match the exact HTML and both reports.
- Every promoted unit is a `page`, or a fragment/component has explicit `parentPage` and `parentZone`.
- Every non-initial state has a resolved disposition.

## Handoff bundle

One explicit output directory receives three atomic files tied to the receipt's artifact digest:

- `pages.json`: harness page metadata (`key`, optional `label`, `group`, `route`, `source`, `theme`);
- `migration-payload.json`: initial-state bodies, page-owned styles, reviewed shared helpers and retained interactive `afterRender` mappings;
- `handoff.json`: provenance, source digest, state dispositions, fragment mappings, omissions/reasons and tablet policy.

The initial state becomes the page's initial body. Other states never remain juxtaposed in harness chrome: `retained-interactive` maps a declared trigger to `afterRender`; `reference-only` and `omitted` require reasons and stay in the inventory; `unresolved` blocks.

## Tablet decision

Wireframes own only desktop and mobile. Promotion requires `tabletPolicy`:

- `desktop-derived` or `mobile-derived`: an explicit reviewer decision that the named layout seeds the harness tablet sample;
- `defer`: emit the bundle but do not invoke harness normalization.

Missing policy is invalid input. `defer` is a successful handoff, not a successful harness. Only a non-deferred policy allows the official harness normalization action to run; its format, runtime, migration and visual proofs remain independently required.

The receipt signs the exact bytes of the HTML, static report and rendered report with SHA-256. Revocation is a new detached receipt that retains the original reviewer, timestamp and digests; neither acceptance nor revocation rewrites the board. The handoff recalculates all three digests before creating its output directory.
