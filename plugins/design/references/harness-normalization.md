# Normalizing existing HTML into a harness

Normalization adopts author work without adopting an arbitrary document shell. The generated harness remains the sole owner of preview chrome, page and metadata registries, viewport controls, and the two control scripts.

## Classification

Run `tools/harness-analyze.mjs <input.html>` before writing. It returns one of four classes:

| Class | Meaning | Migration |
| --- | --- | --- |
| `canonical-harness` | all static invariants and the runtime check pass | regenerate only when an explicit new output is requested; preserve author regions exactly |
| `repairable-harness` | harness signals exist but the shell or runtime is damaged | generate a fresh shell and migrate identifiable author regions |
| `html-document` | a conventional document owns `<html>`, `<head>`, and `<body>` | migrate body content as page markup and eligible page CSS as author styles |
| `html-fragment` | only page-level markup is present | require or infer one explicit page key and migrate the fragment as that page |

The analyzer aggregates evidence; a nonconformant but readable HTML input still exits 0. Exit 2 is reserved for invalid invocation or an unreadable/empty input. Its `classification` and compatibility field `conformant` describe the harness **format**, not the success of a migration. The `outcome` object keeps runtime validity, migration completeness, and visual fidelity separate; the latter two stay `null` / `unmeasured` until the normalization workflow supplies their evidence.

Pass `--baseline <source.html>` when inspecting a rebuilt output. A size ratio above 2 is a migration blocker until repeated content is moved to `AUTHOR SHARED HELPERS` or the growth is explicitly accepted with its cause. The ratio is a diagnostic threshold, not a compression target.

## Modes

| Mode | Default | Behaviour |
| --- | --- | --- |
| `snapshot` | yes | captures the rendered state of each page; visible interactions are frozen only after explicit acceptance and are listed as omitted/frozen |
| `interactive` | no | preserves only inventoried interactions with an explicit mapping into `AUTHOR AFTER RENDER`; browser smoke proof is mandatory |

Do not silently choose snapshot when JavaScript changes visible content. Do not choose interactive merely because scripts exist: analytics, loaders, hydration frameworks and unrelated application state never migrate. The report names each source interaction and one disposition: `retained`, `frozen`, `omitted`, or `unresolved`.

After generating a fresh shell, pass reviewed author content through `tools/harness-apply.py`; do not synthesize page-function source with ad hoc regex or string replacement. The JSON payload defines exactly one page representation: `pages` maps keys to rendered HTML, while `pageBodies` maps keys to reviewed JavaScript function bodies that may call `sharedHelpers`. Prefer `pageBodies` whenever rendering would duplicate shared layout, icons, or embedded assets across pages. It may also carry `styles`, pure `sharedHelpers`, and interactive `afterRender`. The applicator accepts only untouched generated placeholders, escapes rendered strings, rejects script-closing sequences in raw bodies, confines raw JavaScript to governed zones, and publishes the output atomically.

## Ownership boundary

Always regenerate these elements from `adapters/harness/harness.py`:

- `.preview-bar`, `.preview-stage`, and `.preview-frame`;
- `#page-select`, its options, and the three viewport buttons;
- the `pages` and `pageMetadata` registries;
- `window.setPage`, `window.setViewport`, and both control scripts;
- contract stylesheet and copied policy framing when `--contract` is used.

Only these elements may cross from the source:

- page content into a declared `pageXxx()` body;
- page-owned CSS into the `AUTHOR PAGE STYLES` region;
- repeated pure markup builders into `AUTHOR SHARED HELPERS`;
- explicitly retained page-local behaviour into `AUTHOR AFTER RENDER` in interactive mode;
- explicit route, source, theme, label, and group metadata through pages JSON.

Never migrate document wrappers, preview chrome, analytics, third-party loaders, source control scripts, or a second page registry.

## Decisions that block an automatic write

Stop before creating the output when any of these changes the meaning of the result:

- several page candidates have no explicit key-to-content mapping;
- inline or external JavaScript creates visible content or required interaction;
- a stylesheet dependency cannot be read and its absence would materially change the reference;
- an asset URL is relative but the static serving base is unknown;
- a viewport media query cannot be mapped honestly to the fixed desktop, tablet, and mobile device samples.

Preference/accessibility media queries (`prefers-reduced-motion`, `prefers-contrast`, `forced-colors`, `prefers-color-scheme`) are preserved. They are not responsive breakpoints.

Do not solve these gaps by copying scripts into the harness, inventing content, or treating contract tokens as a visual repair instruction. Record the evidence and the missing decision.

## Completion proof

A normalization is complete only when all four dimensions have evidence:

1. the input checksum is unchanged;
2. **format** — the output analyzer class is `canonical-harness` and the page registry, `#page-select` options, and metadata keys agree;
3. **runtime** — `harness-runtime-check.mjs` exits 0 for every declared page, and interactive mode also passes browser smoke tests;
4. **migration** — every content block, asset, dependency and interaction has a disposition; no unresolved item remains; absolute `source` paths are readable or deliberately replaced with portable provenance; an inlined token snapshot names its frozen contract;
5. **visual delta** — before/after screenshots cover every page × desktop/tablet/mobile with animations disabled and dependencies resolved; changed-pixel measurements and accepted deviations are reported;
6. the response lists preserved, transformed, omitted, frozen, and unresolved items, the output/input size ratio, and any explicit acceptance;
7. no claim of **design-contract conformity** is made from normalization evidence. That distinct conclusion belongs to `design:enforce`.

`canonical-harness` plus a green runtime is therefore necessary but insufficient. A report with `visualFidelity: "unmeasured"`, unresolved dependencies, missing provenance, or a non-empty interaction inventory cannot state that migration is complete.
