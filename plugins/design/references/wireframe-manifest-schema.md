# Wireframe manifest schema

The machine authority is [`wireframe-manifest.schema.json`](wireframe-manifest.schema.json). This page explains cross-field invariants that JSON Schema cannot express compactly.

## Identity and ordering

`schemaVersion` is `1`. Unit, element, state and reference ids are non-empty slugs and unique within their scope. `units[]` order is user-flow order, or brief order when no flow exists. Each unit type is `page`, `fragment` or `component`.

`primaryAction` is an element id or `null`. `initialState` names exactly one declared state. Every state's `elementIds` resolves inside the unit. Each transition resolves `from`, `to` and `controlId`; the control appears in its source state.

`allowedOverlaps` is an unordered pair of distinct element ids in one state. Both elements must appear in that state and share the same declared parent. Duplicate/reversed pairs are invalid.

## Context and pillars

`pillars` contains any subset of `responsive`, `representative-content`, `existing-context`, and `brand`.

- With `responsive`, every unit uses context `responsive`; the shell creates desktop and mobile frames.
- Without it, each unit uses exactly one of `desktop`, `mobile`, `intrinsic`; intrinsic requires `containerWidth`.
- Representative content requires at least one `contentScenario` per unit.
- Existing context requires at least one `contextReferenceIds` entry and a state marked `showsExistingContext`.
- Brand requires at least one `brandReferenceIds` entry. Every id resolves in top-level `references`.

References declare provenance and authority rank. A URL may document provenance but cannot become a runtime/display dependency of the standalone HTML.

## Harness metadata

Only a `page` may carry `harness`. Its `key` is a harness-compatible slug; the optional fields map directly to `label`, `group`, `route`, `source` and `theme`.

Each non-initial state gets a disposition:

- `retained-interactive`: requires a transition trigger and an explicit `afterRender` mapping;
- `reference-only`: remains in the handoff inventory and requires a reason;
- `omitted`: does not migrate and requires a reason;
- `unresolved`: blocks harness normalization.

Fragments/components must declare `parentPage` and `parentZone` before promotion. No tool invents a page wrapper.

## Review is deliberately absent

Human acceptance never lives in this manifest. It is recorded in a detached receipt governed by [`wireframe-review.schema.json`](wireframe-review.schema.json), so accepting a board never changes the bytes that were reviewed.
