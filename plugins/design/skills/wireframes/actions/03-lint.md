# Lint

Validate an existing canonical wireframe candidate at the static and rendered levels.

## Input

- A readable wireframe HTML path.
- Optional `--fix` intent and a distinct fix output path.
- Playwright 1.60.0 and a launchable Chromium executable for rendered proof.

## Process

1. Run `${DESIGN_PLUGIN_ROOT}/tools/wireframes-lint.py <html> --report <report>`.
2. Report format, mandatory-core and active-pillar results separately.
3. When explicitly requested, run `--fix --fix-out <distinct-output>`; accept only safe attribute/id repairs derivable from the manifest.
4. Re-run the complete static lint on the fixed output. Never repair layout, content, states, pillars, references or review decisions.
5. Once static lint passes, run `${DESIGN_PLUGIN_ROOT}/adapters/wireframes/render-check.py <html> --report <render-report>` in Chromium.
6. Keep `static`, `rendered`, and `review` conclusions distinct. Missing Playwright or Chromium is unverified and exits `2`, never green.
7. Return `0` only when static and rendered checks pass, `1` for violations, `2` for invalid input, invocation, or unavailable rendered proof.

## Output

Deterministic static and rendered JSON reports, plus an optional distinct mechanically repaired candidate. Never infer human acceptance from either report.

## Test

An excessive annotation exits 1; an unreadable file exits 2; a missing `data-wireframe-element` on a unique matching id can be repaired to a distinct file and is then fully re-linted. Browser fixtures prove a valid board, an unapproved overlap, horizontal overflow, and a hidden declared element.
