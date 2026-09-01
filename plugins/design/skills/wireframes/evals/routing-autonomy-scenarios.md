# Wireframes — Routing autonomy Behavioural Test Scenarios

Authority: `SKILL.md`, `actions/01-scaffold.md`, `actions/03-lint.md`, `references/wireframe-contract.md` and `references/wireframe-manifest-schema.md`.

## Scenarios

| # | Situation (input) | Expected behaviour | Pass criteria |
|---|---|---|---|
| S1 | Generate a responsive component board from the bundled valid fixture. | Select `scaffold`; generate, apply and statically lint. | Distinct output; desktop/mobile and both states exist; static exit 0; rendered/review remain unclaimed. |
| S2 | Lint a board with three annotations. | Select `lint` and fail the candidate. | Exit 1 and `annotation-count`; no rewrite. |
| S3 | Ask for safe repair of a unique element id missing its data attribute. | Select `lint --fix` with a distinct output. | Only the derived attribute changes and full re-lint runs. |
| S4 | Ask to normalize arbitrary existing HTML. | Do not route yet. | No absent normalize tool is promised or invoked. |
| S5 | Ask for a free component prototype without a board/manifest/pillars. | Bypass wireframes for `diffuse/prototype`. | No wireframes action or artifact is selected. |

## How to run

Agent-as-wireframes, dry-run plus deterministic bundled selftest. Record action, intended paths, exit, active pillars and claimed proof layers.

**Decisive observables:** one action; distinct writes; no external dependency; static success never claims rendered/review success; absent later routes stay absent.
