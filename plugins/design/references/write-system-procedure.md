# Write-system procedure (shared)

Followed by `define/04-write-material` (in draft mode). Writes the canonical design-system artifacts from a finalized token set. Read alongside `design-system-contract.md` (layout + sections) and `token-schema.md` (token shapes + adapter rules).

## Inputs

- A finalized token set (schema-shaped) with a responsive strategy and a component list.
- Provenance metadata: origin (reference description / brief summary), date, version.

## Process

1. **Create the design home** `design/` if absent (or the recorded sub-package root).
2. **Write `design/tokens.json`** — W3C DTCG, every required group from `token-schema.md`, `{alias}` references for semantic→ramp links. This is the source of truth.
3. **Detect the consumers the project actually has, and record them** — see § Adapter emission rule below. No adapter file is written here.
4. **Write `design/design-system.md`** with the contract's required sections:
   - Provenance (origin, date, `version:` line).
   - Foundations (narrative; point to `tokens.json` for values, don't restate every number).
   - Responsive strategy (named breakpoints; mobile core / enriched-only / mobile-only — aligned with the `08-design` rules).
   - Component inventory table (component · purpose · options/variants · **background tokens** · **foreground tokens** · responsive divergence · spec file). State in this section that the inventory is **candidate prose**, and that once `adjust` promotes it to the manifest the resulting vocabulary is **open by default** — pointing to `skills/adjust/references/manifest-schema.md § Invariant 1`, the canonical statement, rather than restating the rule.

     The two colour columns are the pairing, and they are the reason this table is not decoration. A colour carries text because a component says so; no name convention says it, and nothing downstream can recover it once the reference or the brief is closed. They become `components.json § .foregrounds × .backgrounds`, which is what the contrast check reads at freeze — a component that shows text and leaves the foreground column empty makes its own text colour untestable, and a contract where *no* component fills it does not freeze at all (`skills/adjust/references/manifest-schema.md § Invariant 7`). A purely structural component (grid, spacer) leaves both empty, which is a statement and not an omission.
   - Open questions (assumptions, unresolved choices).
5. **Do not author component spec files here** — list them in the inventory. Specs are produced on demand by `diffuse/01-define-element`, after the freeze, so that they are written against a versioned contract rather than against draft material.

## Adapter emission rule

**Canonical statement. Every other document conditions adapter emission by pointing here.**

Detection here, emission elsewhere. `tools/generate.py` is the only producer of an adapter file; it runs at freeze time and emits one artifact per `policies.json § adapters[]` entry declaring a `consumer`. This procedure decides **which entries that table will hold**.

One entry per consumer **present in the project**, never per consumer the plugin knows how to write — read the project's declared dependencies and configuration files, not habit.

| Consumer detected | `consumer` role | Condition |
|---|---|---|
| A stylesheet pipeline of any kind (always true for a browser-rendered project) | `stylesheet` | default; the only artifact every consuming stack can read |
| A pre-processed stylesheet source in the build | `stylesheet source` | the pre-processor is a declared dependency |
| A build step consuming tokens as a module | `build configuration` | the tool is a declared dependency |
| A runtime platform with its own design-token file format | `platform token file` | the platform is the project's runtime |

- No detected consumer beyond the stylesheet → one `stylesheet` entry alone. This is a complete result, not a degraded one.
- Never declare a consumer the project does not have: an unread generated file drifts silently and is indistinguishable from a maintained one.
- A detected consumer whose role is not in the table is recorded **without** a `consumer`. It is then declared and not emitted — the honest state for an artifact nobody knows how to produce.
- Record in `design-system.md § Provenance` which consumers were detected and, for each, on what evidence. That record is the input `adjust` promotes into `policies.json § adapters[]`.

## Atomicity

- `tokens.json` is written here alone; no adapter exists yet to fall out of step with it. The pair exists from the freeze onward, kept consistent by `generate.py --check`.
- If `design/tokens.json` already exists, diff against it: bump the version per the contract's rule and summarize what changed instead of silently overwriting.

## Report

- List every written/regenerated path.
- State the version and a one-line provenance.
- Surface unresolved Open questions for the user to close.
- Suggest the next capability: invoke `design:destructure` (challenge the direction) or
  `design:adjust` (freeze the contract) through the current host.

## Test

`design/tokens.json` and `design/design-system.md` exist; **no file was written under `design/adapters/`**; § Provenance names every detected consumer and its evidence; `design-system.md` has all five required sections and a `version:` line.
