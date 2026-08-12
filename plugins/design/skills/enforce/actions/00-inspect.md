# Inspect

## Input

- A component, page, rendered application, or source tree.
- Optional visual reference and target viewports.

## Output

A read-only diagnostic grouped by P0 outcome, P1 system consistency, and P2 workflow integration. The report states `conformity: not assessed` and lists every unavailable measurement as missing evidence.

## Process

1. **Resolve.** Identify the supplied target, any visual reference, and the evidence that can actually be read or measured.
2. **Inspect.** Evaluate the applicable rows of [control-priorities.md](../../../references/control-priorities.md) without inventing a contract or a passing result for unavailable evidence.
3. **Classify.** Rank observed findings as P0, P1, or P2 and separate observations from missing evidence.
4. **Report.** Emit the diagnostic, the measurements used, the blind spots, and `conformity: not assessed`, then stop.

## Test

| Case | Pass |
| --- | --- |
| no contract exists | the output contains no green gate, maturity level, or conformity claim |
| a visual reference is absent | fidelity is listed as unavailable evidence rather than passed |
| a P2 integration is missing | it is a warning and is not presented as a design failure |
