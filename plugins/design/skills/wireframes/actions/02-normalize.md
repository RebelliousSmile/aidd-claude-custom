# Normalize

Rebuild existing author HTML into a fresh canonical wireframe without changing the source.

## Input

- Readable source HTML, brief/evidence, destination manifest, payload, inventory, and board paths. If the source comes from a published claude.ai Artifact, see [wireframe-artifact-sourcing.md](../../../references/wireframe-artifact-sourcing.md) before analysis: extract the author's document out of the viewer chrome first.
- The applicable optional pillars and any references they require.

## Process

1. Record the source SHA-256, then run `${DESIGN_PLUGIN_ROOT}/tools/wireframes-analyze.py <source> --out <inventory>`.
2. Stop before board generation when classification is `ambiguous` or any named decision can change meaning, journey order, or business content.
3. Review every inventory block into `preserved`, `transformed`, or `omitted`; retain a reason for omissions and never adopt external dependencies or hidden-content scripts silently.
4. Create a manifest and payload from the reviewed inventory. Generate a new shell with `adapters/wireframes/wireframes.py`. For a `page` unit, set `harness.key`/`label`/`group` only when the source unambiguously names a route or screen identity; otherwise leave `harness` absent. `promote` refuses missing page harness metadata (see [`04-promote.md`](04-promote.md)) — an absent `harness` here means a human completes it before promotion, `normalize` never invents one.
5. Apply only through `tools/wireframes-apply.py --inventory <reviewed-inventory>` to a distinct output.
6. Run static and rendered lint. Verify the original SHA-256 is unchanged and every inventoried block has a final disposition.

## Output

A new canonical board, detached migration inventory, and both validation reports. The source remains byte-identical. An ambiguous analysis produces no board.

## Test

Document, fragment, annotation-heavy source and canonical source classify distinctly; ambiguous unit/state mapping exits `1` before a board is written; missing or stale inventory exits `2`.
