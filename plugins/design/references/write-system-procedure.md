# Write-system procedure (shared)

Followed by `define/04-write-material` (in draft mode). Writes the canonical design-system artifacts from a finalized token set. Read alongside `design-system-contract.md` (layout + sections) and `token-schema.md` (token shapes + adapter rules).

## Inputs

- A finalized token set (schema-shaped) with a responsive strategy and a component list.
- Provenance metadata: origin (reference description / brief summary), date, version.

## Process

1. **Create the design home** `design/` if absent (or the recorded sub-package root).
2. **Write `design/tokens.json`** — W3C DTCG, every required group from `token-schema.md`, `{alias}` references for semantic→ramp links. This is the source of truth.
3. **Generate the adapters the project actually consumes** — see § Adapter emission rule below. Shapes and naming: `token-schema.md`. Every generated file carries the "GENERATED — do not edit" banner.
4. **Write `design/design-system.md`** with the contract's required sections:
   - Provenance (origin, date, `version:` line).
   - Foundations (narrative; point to `tokens.json` for values, don't restate every number).
   - Responsive strategy (named breakpoints; mobile core / enriched-only / mobile-only — aligned with the `08-design` rules).
   - Component inventory table (component · purpose · options/variants · responsive divergence · spec file). State in this section that the inventory is **candidate prose**, and that once `adjust` promotes it to the manifest the resulting vocabulary is **open by default**: a class whose block is not declared is treated as a utility and passes the gate. Declaring a component is what makes its own elements and modifiers enforceable — nothing else.
   - Open questions (assumptions, unresolved choices).
5. **Do not author component spec files here** — list them in the inventory; `component` writes the specs on demand.

## Adapter emission rule

**Canonical statement. Every other document conditions adapter emission by pointing here.**

One adapter is emitted per consumer **present in the project**, never per consumer the plugin knows how to write. Detect from the project's declared dependencies and configuration files, not from habit.

| Consumer detected | Artifact | Condition |
|---|---|---|
| A stylesheet pipeline of any kind (always true for a browser-rendered project) | `design/adapters/tokens.css` | default; the only adapter every consuming stack can read |
| A utility-CSS framework consuming a theme declaration | its own theme artifact, in the form and major version installed (`token-schema.md § Adapter: Tailwind`) | the framework is a declared dependency |
| A platform with its own design-token file format | that platform's file, written by the pivot that owns the platform | the platform is the project's runtime |

- No detected consumer beyond CSS → emit `tokens.css` alone. This is a complete result, not a degraded one.
- Never emit an adapter for a stack the project does not use: an unread generated file drifts silently and is indistinguishable from a maintained one.
- Record in `design-system.md § Provenance` which adapters were emitted and, for each, on what evidence.

## Atomicity

- Write `tokens.json` and regenerate **every emitted** adapter in the same pass; never leave them inconsistent.
- If `design/tokens.json` already exists, diff against it: bump the version per the contract's rule and summarize what changed instead of silently overwriting.

## Report

- List every written/regenerated path.
- State the version and a one-line provenance.
- Surface unresolved Open questions for the user to close.
- Suggest next step: `/design:destructure` (challenge the direction) or `/design:adjust` (freeze the contract).

## Test

`design/tokens.json`, `design/adapters/tokens.css` and `design/design-system.md` exist; every adapter listed in § Provenance exists and no other adapter file was written; the adapters' values match `tokens.json`; `design-system.md` has all five required sections and a `version:` line.
