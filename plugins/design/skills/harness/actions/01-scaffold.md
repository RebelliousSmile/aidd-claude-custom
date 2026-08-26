# Scaffold

## Input

- An explicit output path.
- Optional title, language, and page list or pages JSON. Page objects may carry `route`, `source`, and `theme` grounding metadata.

## Output

A standalone HTML file exposing `window.setPage(key)` and `window.setViewport(mode)`.

## Process

1. **Resolve.** Normalize the page list and reject empty, duplicate, non-slug, or JavaScript-colliding keys. Preserve supplied route, source, and theme metadata.
2. **Generate.** Run `${DESIGN_PLUGIN_ROOT}/adapters/harness/harness.py` with the supplied output and page arguments.
3. **Verify.** Run `${DESIGN_PLUGIN_ROOT}/tools/harness-runtime-check.mjs` on the generated file and return its public exit code.

## Test

| Case | Pass |
| --- | --- |
| valid pages are supplied | the file exists and the runtime check exits 0 |
| route, source, and theme metadata are supplied | the LLM framing maps every page to its evidence and the runtime applies its theme |
| two keys map to the same JavaScript function | generation exits 2 and writes no invalid file |
| no contract is supplied | no contract file is read or changed |
