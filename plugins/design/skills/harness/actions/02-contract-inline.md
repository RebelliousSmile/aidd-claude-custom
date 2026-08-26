# Contract-inline

## Input

- The scaffold inputs.
- A frozen contract directory supplied through `--contract`.

## Output

A standalone HTML file containing the already generated contract stylesheet and copied policy guidance without modifying the contract.

## Process

1. **Validate.** Require `release.json`, readable policies, and a declared readable stylesheet adapter.
2. **Ground.** Copy `policies.json § mode` and valid `usage.rules[]` into the LLM framing; do not derive, rewrite, or enforce new rules.
3. **Generate.** Run `${DESIGN_PLUGIN_ROOT}/adapters/harness/harness.py` with `--contract` and the scaffold arguments.
4. **Verify.** Run `${DESIGN_PLUGIN_ROOT}/tools/harness-runtime-check.mjs` on the generated file and return its public exit code.

## Test

| Case | Pass |
| --- | --- |
| a valid frozen contract is supplied | the stylesheet is inlined and the runtime check exits 0 |
| the contract declares usage rules | their identifiers and descriptions are copied into the LLM framing |
| `release.json` is absent | the action exits 3 and names the migration path |
| the stylesheet closes the style context | the action exits 2 and writes no unsafe output |
