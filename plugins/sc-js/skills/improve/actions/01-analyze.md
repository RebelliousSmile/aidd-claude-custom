# Action 01 — analyze

Read the JS/TS codebase, identify anti-patterns and improvement opportunities per category, emit structured findings.

## Process

### Step 1 — Detect project context

Read `package.json` to identify:
- Framework (Nuxt, Vue SPA, Alpine, Vite, Astro) — from dependencies
- TypeScript usage — presence of `tsconfig.json`
- Runtime target (Node, browser, SSR)

### Step 1.5 — Stack-specific anti-patterns from capability pivots

Re-detect capabilities from `package.json` (same conditions as `sniff/01-scan`). For each condition met, load the pivot from `${CLAUDE_PLUGIN_ROOT}/skills/sniff/references/capabilities/<path>` and use its anti-patterns as **additional detection criteria** in Step 2. Report findings under a `Stack-specific` category.

| Capability | Condition | Pivot |
|---|---|---|
| TypeScript patterns | `typescript` or `vue-tsc` in devDependencies, or Nuxt 3 detected | `typescript.md` |
| Pinia store patterns | `pinia` in dependencies | `state/pinia.md` |
| Vue component scope | Vue or Nuxt detected | `components/shared-scope.md` |
| Alpine.store patterns | Alpine.js detected | `state/alpine-store.md` |
| Svelte store patterns | `svelte` or `@sveltejs/kit` in dependencies | `state/svelte-stores.md` |
| SSR storage guards | Nuxt or SvelteKit detected | `ssr/storage-guards.md` |
| Nitro server imports | Nuxt detected | `server/nitro-imports.md` |
| Vite dynamic imports | Vite detected (any framework with vite) | `code-splitting/dynamic-import.md` |
| Vue async components | Vue or Nuxt detected | `code-splitting/defineAsyncComponent.md` |

Apply the same TS guard as the TypeScript type coverage category above: do not load `typescript.md` if no `tsconfig.json` and no `typescript` in devDependencies.
If a loaded pivot has a `## Anti-patterns` section, extract it directly. Otherwise read the full pivot and infer violations.
Skip this step if no `package.json` is found.

### Step 2 — Scan for anti-patterns

For each category, search the codebase and record findings with file + line references.

#### Async and promises

- Callbacks where async/await is applicable — flag `then().catch()` chains that can be flattened
- Missing `await` on async calls (common in event handlers)
- `async` functions that never `await` — pointless async wrapper
- Promesses potentiellement non gérées — un appel `async` sans `try/catch`/`.catch()` visible. **🟡, jamais 🔴** : « non géré » n'est pas décidable au scan statique — la rejection peut être captée par un handler global (`process.on('unhandledRejection')`, `window.onunhandledrejection`), par un `await` en amont, ou l'appel peut être *fire-and-forget* intentionnel. Et le fix (injecter `await`/`.catch`) **change le flux de contrôle** : awaiter là où on ne le faisait pas altère l'ordre/timing. Signaler pour décision humaine, pas comme bug prouvé à corriger d'office.
- `Promise.all` vs `Promise.allSettled` : **ne pas trancher au grep**. Lequel est « plus sûr » dépend de la sémantique voulue (échec-rapide vs collecte de tous les résultats), qui n'est pas dans le texte de l'appel. `🟡` question, jamais une réécriture automatique dans un sens ou l'autre.

#### TypeScript type coverage

**Skip this category entirely if no `tsconfig.json` is found AND `typescript` is absent from devDependencies.** Flagging type coverage on a vanilla JS project produces irrelevant findings.

- Implicit `any` — untyped function parameters, return types, variables
- Type assertions (`as X`) that bypass safety — flag without justification comment
- Missing interface/type for component props not using `defineProps<T>()`
- `unknown` used where a proper type exists

#### Vue / Nuxt patterns

- Options API components where Composition API is available — flag for migration consideration
- Direct `$store` / Vuex usage in a Pinia project
- Prop drilling beyond 2 levels — suggest composable or Pinia store
- Watchers on computed values — use `computed` directly
- Missing `defineEmits` type annotation
- `ref` used where `reactive` is more appropriate and vice versa
- Mutating props directly — should emit instead

#### Module and imports

- CommonJS `require()` — **le système de module se mesure par fichier, pas par projet**. Un `.cjs`/`.cts`, ou un fichier dont le `package.json` le plus proche n'a pas `"type": "module"`, est légitimement CommonJS même dans un dépôt à dominante ESM. Ne flaguer que si la résolution effective du fichier (extension + `type` du `package.json` le plus proche) est ESM. Sinon `info`, pas une violation.
- Circular imports — detect via grep for mutual references
- Wildcard imports (`import * as`) — le fait qu'ils « cassent le tree-shaking » est un **comportement de bundler**, pas une propriété du source. Les bundlers modernes (Vite/Rollup/esbuild) gèrent les imports de namespace. Ne l'affirmer que si le bundler mesuré (dans les deps) est connu pour ne pas le faire ; sinon `🟢`/`info`, jamais un verdict de perf.

#### General JS

- `var` declarations — should be `const` or `let`
- Mutable `let` that is never reassigned — should be `const`
- `==` comparisons — should be `===`
- `console.log` left in production code

### Step 3 — Emit findings

For each finding, record:
- Category
- File and line
- Anti-pattern name
- Severity: 🔴 (likely bug) / 🟡 (maintainability) / 🟢 (style)
- Problematic snippet (≤3 lines)
- Proposed fix (≤3 lines)

## Output

```
📋 sc-js improve — analysis

Framework: Nuxt 3 + TypeScript

Findings (N total — N 🔴, N 🟡, N 🟢):

🟡 Promesse possiblement non gérée — src/composables/useData.ts:42
   Current:  fetchData()
   Note:     vérifier handler global / fire-and-forget voulu avant d'injecter await/.catch (change le flux)

🟡 Options API component — src/components/UserCard.vue:1
   Current:  export default { data() {...}, methods: {...} }
   Improved: <script setup lang="ts"> with defineProps<T>()

🟢 var declaration — src/utils/format.ts:7
   Current:  var formatter = new Intl.DateTimeFormat(...)
   Improved: const formatter = new Intl.DateTimeFormat(...)

→ proceed to 02-plan
```

## Test

Invoke on a project with at least one `.vue` or `.ts` file; verify findings include file paths, severity indicators, and before/after snippets.

### Non-régression (faux positifs corrigés)

Sur un fichier de test couvrant chaque cas, rejouer `analyze` et vérifier :

- Un appel async non awaité (`fetchData()`) sort en **🟡** avec note « vérifier handler global / fire-and-forget » — **jamais 🔴** ni routé en Priorité 1 auto-fix.
- `require('./x')` dans un fichier `.cjs` (ou `.js` sous un `package.json` sans `"type": "module"`) → **aucun** finding CommonJS→ESM.
- `import * as utils from './utils'` sans bundler mesuré → au plus `🟢`/`info`, pas un verdict de tree-shaking cassé.
- `Promise.all([...])` → pas de réécriture automatique vers `allSettled` (ni l'inverse).
