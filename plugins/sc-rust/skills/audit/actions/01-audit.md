# Audit

Orchestrate a Rust code quality review: detect applicable pivots, load them from the plugin, and delegate analysis to `aidd-dev:04-audit`.

## Transversal rules

- Invoke `01-scan` only — never `02-install-pivots`. Audit is read-only.
- Never install any file to `.claude/rules/` or any project path.
- All knowledge is read from `${SC_RUST_PLUGIN_ROOT}/skills/sniff/references/capabilities/` at runtime.

## Process

### Step 1 — Detect stack (invoke 01-scan only)

Run sniff `01-scan` on the project to detect the stack and obtain the pivot manifeste.

**Important**: invoke `01-scan` only — do not invoke `02-install-pivots`. Audit never triggers side effects.

If `Cargo.toml` is absent and no workspace is found, abort with:
```
❌ sc-rust audit — no Rust project detected. Run from the project root.
```

### Step 2 — Load capability pivots

Always load `rust/idioms.md` (applies to all Rust projects). For each additional capability in the manifeste, load the corresponding pivot:

```
${SC_RUST_PLUGIN_ROOT}/skills/sniff/references/capabilities/<pivot-path>
```

Collect all loaded pivot contents into an acceptance criteria document:

```
Rust Code Quality Criteria — sc-rust 0.4.0

## Rust idioms and best practices
<content of rust/idioms.md>

## SQLx async query conventions   (only if data/sqlx.md was in the manifeste)
<content of data/sqlx.md>

[...additional capability pivots from manifeste...]
```

### Step 3 — Identify review targets

From the `01-scan` output, identify Rust source directories:
- Axum/Actix-web: `src/handlers/`, `src/routes/`, `src/middleware/`, `src/models/`
- Generic: all `*.rs` files under `src/`; exclude `target/`, `tests/`, `benches/`

These form the `review_target` for the AIDD audit.

### Step 4 — Delegate to aidd-dev:04-audit

Resolve `aidd-dev:04-audit` from the host's available-skills catalogue and read its complete
`SKILL.md`. Invoke its `code-quality` pillar with:

- the Rust review targets identified in Step 3 as the audit scope;
- the capability pivots loaded in Step 2 as supplementary, stack-specific lenses;
- an instruction that every loaded pivot be accounted for either by a concrete finding, a
  "reviewed — no finding" coverage note, or an "unscannable" coverage note with its reason.

Preserve the AIDD audit's own report schema and artifact path. Do not spawn the retired
Do not introduce a retired reviewer agent type or impose a second scoring rubric on the delegated report.

If the package, canonical skill, or `code-quality` pillar is unavailable, stop the delegation,
name the missing capability, and return no substitute generic audit.

### Step 5 — Present results

Read the resulting `code-quality.md` artifact. Return its path and a compact delegation receipt
that maps every loaded pivot to `finding`, `reviewed — no finding`, or `unscannable`. Do not
copy the report into a competing local report format.

## Output format

```text
🔍 sc-rust audit — Rust code quality

Pivots loaded: <n>
Review scope: src/handlers/, src/models/, src/services/
Delegated to: aidd-dev:04-audit / code-quality
Artifact: <aidd_docs/tasks/.../code-quality.md>

Pivot receipt:
  <pivot-path>  <finding | reviewed — no finding | unscannable>
```
