# Wireframe contract

This reference is the normative contract for `design:wireframes`. A wireframe is a standalone HTML board used to validate layout, hierarchy and usage before `design:harness` turns accepted pages into a measurable reference. It is not a design-contract artifact and never changes `design/release.json`.

## Proof layers

1. **Static** checks the embedded manifest, governed shell and author DOM.
2. **Rendered** checks computed geometry and visibility in Chromium.
3. **Review** records that a human understood and accepted the rendered artifact.

No layer may claim another layer's conclusion. A valid candidate has zero static and rendered errors. Promotion additionally requires a current accepted review receipt.

## Canonical board

Every output is one UTF-8 HTML document with no network or adjacent-file dependency. It owns one embedded manifest (`script#wireframe-manifest[type="application/json"]`), one visible section per declared unit and stable `data-wireframe-*` links for units, states, elements and viewports. The shell and manifest are generator-owned; markup, styles and optional helper interactions live only in marked author regions.

All units and decision-relevant states stay present in the document. Controls may aid inspection but cannot be the sole way to expose an essential state. A board may scroll vertically; declared frames may not scroll horizontally.

Executable/display dependencies must be embedded: external scripts, stylesheets, CSS imports, fonts, images, video, audio and poster resources are errors. Ordinary navigation links and provenance strings inside the manifest are not display dependencies.

## Mandatory core

### Layout and hierarchy

- Every expected element has one manifest declaration and one matching rendered element in every state that lists it.
- Parent relationships, DOM order and the declared primary action express hierarchy without relying on colour alone.
- No declared element is clipped, horizontally overflowing or colliding with an unrelated peer.
- Ancestor/descendant box intersections are structural, not collisions. Peer intersections are allowed only by an exact `allowedOverlaps` entry for that unit and state.

### Usage and states

- Each control has a label or conventional accessible role.
- Every decisive interaction has an `initialState`, a target state and a declared transition.
- Decision-relevant states are simultaneously visible; executable helpers reproduce rather than replace them.
- Generic loading, empty, error, success and disabled states are required only when the brief declares them or they alter layout.

## Optional pillars

Only declared pillars apply.

- `responsive`: exactly `desktop` 1440 px and `mobile` 390 px for every unit; no tablet or hidden viewport.
- `representative-content`: named scenarios, credible values, no lorem ipsum or generic placeholder labels.
- `existing-context`: at least one state renders the new element with the neighbouring existing interface needed to judge insertion.
- `brand`: every claimed brand colour, font, shape, logo or component cites a readable reference; neutral board chrome is excluded.

Without `responsive`, a unit declares exactly one context: `desktop`, `mobile`, or `intrinsic`. Intrinsic units declare a numeric container width.

## Annotations

The default is zero. A unit may contain at most two `[data-wireframe-annotation]` nodes, each at most 60 characters, with no list or paragraph. An annotation cannot replace visible UI, describe implementation, or explain something the layout/state could show. The last three judgements belong to review; count and shape belong to static lint.

## Rendered checks

Rendered collision candidates are declared elements at the same hierarchy level. Zero-area boxes and ancestor/descendant pairs are excluded. Every remaining intersection needs an exact allowed-overlap pair. Chromium also checks frame width, clipping, horizontal overflow and visibility without interaction. Animations and transitions are disabled before measurement.

## Exit space

- `0`: applicable checks completed with zero errors.
- `1`: readable candidate with one or more violations.
- `2`: invalid invocation, unreadable/invalid input, or required validation environment unavailable.

Warnings never turn an error into success. Static success alone is a candidate, never a valid wireframe.
