# Wireframes — Routing autonomy Behavioural Test Scenarios

Authority: `SKILL.md`, its four actions, and the shared wireframe contract, normalization and handoff references.

## Scenarios

| # | Situation (input) | Expected behaviour | Pass criteria |
|---|---|---|---|
| S1 | Generate a responsive component board from the bundled valid fixture. | Select `scaffold`; generate, apply and statically lint. | Distinct output; desktop/mobile and both states exist; static exit 0; rendered/review remain unclaimed. |
| S2 | Lint a board with three annotations. | Select `lint` and fail the candidate. | Exit 1 and `annotation-count`; no rewrite. |
| S3 | Ask for safe repair of a unique element id missing its data attribute. | Select `lint --fix` with a distinct output. | Only the derived attribute changes and full re-lint runs. |
| S4 | Normalize an author HTML document or fragment. | Select `normalize`; analyze first, rebuild in a fresh shell. | Source digest stays unchanged; reviewed inventory is complete; new board passes both lints. |
| S5 | Normalize a source with two defensible journeys. | Select `normalize` and stop after analysis. | Inventory names the semantic decision; no board, manifest or payload is written. |
| S6 | Promote a reviewed page with current green evidence and `desktop-derived`. | Select `promote`; sign then hand off. | Receipt and three linked bundle files exist; initial state alone becomes the page body; `invokeHarness` is true. |
| S7 | Promote with stale or revoked review evidence. | Select `promote` and refuse before output. | Exit 2; no handoff directory. |
| S8 | Promote with `defer`. | Select `promote`; emit bundle only. | `invokeHarness` is false and no harness is created. |
| S9 | Ask for a free component prototype without a board/manifest/pillars. | Bypass wireframes for `diffuse/prototype`. | No wireframes action or artifact is selected. |

## How to run

Agent-as-wireframes, dry-run plus deterministic bundled selftest. Record action, intended paths, exit, active pillars and claimed proof layers.

**Decisive observables:** one action; distinct writes; immutable source; no silent external dependency; static/rendered/review conclusions stay separate; promotion is receipt-bound and tablet-explicit.
