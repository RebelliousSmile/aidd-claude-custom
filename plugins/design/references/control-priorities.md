# Control priorities

This is the canonical classification for design evidence. A lower-value workflow convenience never outweighs an unmeasured or failing user outcome.

| Priority | Question answered | Examples | Verdict effect |
| --- | --- | --- | --- |
| P0 outcome | does the rendered experience work for the user | visual fidelity when a reference exists, responsive behavior, rendered contrast, semantics, keyboard and focus behavior, required interaction states, unresolved critical deviations | failure or missing required evidence blocks |
| P1 system | does the implementation remain governed by the declared system | token and component vocabulary, target coverage, generated-artifact freshness, native pivot results, contract maturity | failure or missing required evidence blocks |
| P2 workflow | is enforcement conveniently integrated into the development workflow | generated rules, plan success conditions, pre-commit wiring, optional automatic imports | failure warns and never invalidates design by itself |

## Evidence rules

- An unavailable measurement is `missing evidence`, never a pass.
- A control with no applicable target is `not applicable`, never a pass.
- P0 fidelity is applicable only when an external visual reference exists.
- A P2 warning remains visible in reports but does not change exit code 0 to 1.
- Exit 4 remains reserved for a contract below the maturity threshold, even when violations are also present.
