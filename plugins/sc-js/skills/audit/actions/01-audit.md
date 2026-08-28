# Audit

Orchestrate a JS code quality review: detect applicable pivots, load them from the plugin, and delegate analysis to `aidd-dev:04-audit`.

## Transversal rules

- Invoke `01-scan` only — never `02-install-pivots` or `03-clean`. Audit is read-only.
- Never install any file to `.claude/rules/` or any project path.
- All knowledge is read from `${SC_JS_PLUGIN_ROOT}/skills/sniff/references/capabilities/` at runtime.

## Process

### Step 1 — Detect stack (invoke 01-scan only)

Run sniff `01-scan` on the project to detect the stack and obtain the pivot manifeste.

**Important**: invoke `01-scan` only. Do not invoke `02-install-pivots` or `03-clean`. Audit never triggers side effects.

Output: pivot manifeste listing applicable capability reference paths (e.g. `state/pinia.md`, `icons/lucide-vue.md`, `code-splitting/dynamic-import.md`, etc.)

If `package.json` is not found, abort with:
```
❌ sc-js audit — no package.json found. Run from the project root.
```

### Step 2 — Load capability pivots

For each pivot path in the manifeste, read the corresponding reference file:

```
${SC_JS_PLUGIN_ROOT}/skills/sniff/references/capabilities/<pivot-path>
```

Example: for `state/pinia.md` → read `${SC_JS_PLUGIN_ROOT}/skills/sniff/references/capabilities/state/pinia.md`

Collect all loaded pivot contents into an acceptance criteria document. Structure it as:

```
JS Code Quality Criteria — sc-js capability pivots

## Vue component scope
<content of components/shared-scope.md>

## Pinia state management
<content of state/pinia.md>

## Code splitting
<content of code-splitting/dynamic-import.md>
<content of code-splitting/defineAsyncComponent.md>

## CSS transitions
<content of styling/css-transitions.md>

## Icons (lucide-vue-next)
<content of icons/lucide-vue.md>

[...additional pivots from manifeste...]
```

### Step 3 — Identify review targets

Pick targets by the stack `01-scan` detected — do not assume a framework layout. Use the rows that match; combine when several apply.

| Stack (from `01-scan`) | Typical review targets |
|---|---|
| Vue / Nuxt | `src/`, `components/`, `pages/`, `stores/`, `composables/`, `app.vue`, `nuxt.config.*`, `vite.config.*` |
| SvelteKit / Svelte | `src/`, `src/routes/`, `src/lib/`, `*.svelte`, `svelte.config.*`, `vite.config.*` |
| Alpine.js | `src/`, the HTML templates carrying `x-data`, the bundler entry |
| **Vanilla web (no framework)** | `index.html` + other `*.html`, `lib/` / `js/` / `src/` JS, `css/`, the build config (`gulpfile.*`, bundler config) |
| Node backend | `src/`, `routes/`, `controllers/`, `services/`, server entry |
| Any stack — always include | linter config (`eslint.config.*`, `biome.json`), test config (`vitest.config.*`, `playwright.config.*`), and `tests/` when present |

These form the `review_target` for the AIDD audit. For vanilla web, **do not skip inline styles/scripts inside `*.html` and JS-generated DOM** — pivots like `css-transitions` and `images` apply to inline/dynamic markup, not just `.css` files.

### Step 4 — Delegate to aidd-dev:04-audit

Resolve `aidd-dev:04-audit` from the host's available-skills catalogue and read its complete
`SKILL.md`. Invoke its `code-quality` pillar with:

- the JS review targets identified in Step 3 as the audit scope;
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
🔍 sc-js audit — JS code quality

Pivots loaded: <n>
Review scope: src/, components/, stores/, pages/
Delegated to: aidd-dev:04-audit / code-quality
Artifact: <aidd_docs/tasks/.../code-quality.md>

Pivot receipt:
  <pivot-path>  <finding | reviewed — no finding | unscannable>
```
