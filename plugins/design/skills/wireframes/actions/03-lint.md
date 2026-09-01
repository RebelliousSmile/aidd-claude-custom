# Lint

Statically validate an existing canonical wireframe candidate.

## Input

- A readable wireframe HTML path.
- Optional `--fix` intent and a distinct fix output path.

## Process

1. Run `${DESIGN_PLUGIN_ROOT}/tools/wireframes-lint.py <html> --report <report>`.
2. Report format, mandatory-core and active-pillar results separately.
3. When explicitly requested, run `--fix --fix-out <distinct-output>`; accept only safe attribute/id repairs derivable from the manifest.
4. Re-run the complete static lint on the fixed output. Never repair layout, content, states, pillars, references or review decisions.
5. Return `0` for zero static errors, `1` for violations, `2` for invalid input/invocation.

## Output

A deterministic JSON report and optional distinct mechanically repaired candidate. Never claim rendered or human validity.

## Test

An excessive annotation exits 1; an unreadable file exits 2; a missing `data-wireframe-element` on a unique matching id can be repaired to a distinct file and is then fully re-linted.
