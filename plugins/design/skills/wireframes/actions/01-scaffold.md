# Scaffold

Generate a standardized wireframe board from a brief and explicit output path.

## Input

- A brief naming one or more pages, fragments or components.
- An explicit output HTML path.
- Readable references for each requested contextual pillar.

## Process

1. **Model.** Produce a manifest conforming to `${DESIGN_PLUGIN_ROOT}/references/wireframe-manifest.schema.json`; select the mandatory core and evidence-backed optional pillars.
2. **Gate.** Stop before writing on contradictory brief elements, unresolved pillar choice, or unreadable required reference.
3. **Generate.** Run `${DESIGN_PLUGIN_ROOT}/adapters/wireframes/wireframes.py --manifest <manifest> --out <fresh-shell>`.
4. **Compose.** Prepare reviewed state markup with `data-wireframe-element` links, author CSS and helper-only interactions as a JSON payload.
5. **Apply.** Run `${DESIGN_PLUGIN_ROOT}/tools/wireframes-apply.py --shell <fresh-shell> --payload <payload> --out <output>`.
6. **Check.** Run `${DESIGN_PLUGIN_ROOT}/tools/wireframes-lint.py <output> --report <static-report>` and return its public exit.

## Output

A distinct standalone HTML candidate, its manifest/payload working inputs and static report. State explicitly that rendered proof and review remain outstanding.

## Test

A responsive two-state component produces one board with both states and exactly desktop/mobile frames, no external display dependency, a static exit 0, and no design contract write.
