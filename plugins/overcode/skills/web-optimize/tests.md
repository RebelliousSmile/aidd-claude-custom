# web-optimize — smoke tests

> Run these before trusting `web-optimize` on a new stack or after editing `SKILL.md` / `framework-mapping.md`.
> Purpose: verify the **detection step** produces the expected stack label and points to the right checklist source.

## How to use

For each case below:
1. `cd` into a project matching the description (or a minimal fixture).
2. Run the Quick Start detection commands from `SKILL.md`.
3. Compare the detected stack + chosen checklist against the **Expected** column.
4. If mismatch → fix `SKILL.md` Step 1 detection logic OR `framework-mapping.md` pivots.

> The **Expected checklist source** column below covers the `source` field of the provenance header only. The second field, `pivot`, is not fixed by the project shape: it depends on what `.claude/rules/07-quality/` holds in the fixture at run time. A run is correct only if **both** fields are emitted — matching this column while omitting `pivot` is a failure, not a pass.

## Test matrix

| # | Project shape (files present)                                         | Expected stack             | Expected checklist source                                                                  |
|---|------------------------------------------------------------------------|----------------------------|---------------------------------------------------------------------------------------------|
| 1 | `package.json` with `"nuxt": "^3.x"` or `"^4.x"`, `nuxt.config.ts`     | `nuxt`                     | `aidd_docs/templates/dev/perf_checklist_nuxt.md` (existing template)                        |
| 2 | `package.json` with `"vue": "^3.x"` + `vite.config.ts`, **no** `nuxt`  | `vue-spa`                  | Generate `perf_checklist_vue-spa.md` (propose to user)                                      |
| 3 | `manage.py` + `requirements.txt` with `Django==`                       | `django`                   | Generate `perf_checklist_django.md`                                                         |
| 4 | `manage.py` + `<script src=".../alpinejs">` in templates               | `django+alpine` (hybrid)   | Load Django pivots **+** section `## Django + Alpine.js (hybride classique)`                |
| 5 | `composer.json` with `"laravel/framework"` + `artisan`                 | `php-laravel`              | Generate `perf_checklist_php-laravel.md`                                                    |
| 6 | `composer.json` with `"symfony/framework-bundle"` + `bin/console`      | `php-symfony`              | Generate `perf_checklist_php-symfony.md`                                                    |
| 7 | `wp-config.php` present                                                | `wordpress`                | Use section `## PHP vanilla / WordPress / autres`                                           |
| 8 | `astro.config.mjs` + `package.json` with `"astro"`                     | `astro`                    | Generate `perf_checklist_astro.md` (use Static section pivots)                              |
| 9 | `package.json` Laravel + `<script ... alpinejs>` in `*.blade.php`      | `php+alpine` (hybrid)      | Load Laravel pivots **+** Alpine pivots from `## Django + Alpine.js (hybride classique)`    |
|10 | None of the above (e.g. Go + htmx)                                     | `other` (fallback)         | Trigger fallback flow — ask user 3 infos, build from 10 generic sections                    |
|11 | `Cargo.toml` **in a subfolder** (`app/`, `engine/core/`) with `axum`   | `rust-axum`                | `perf-pivots-axum.md` if installed, else recommend `sc-rust`, `/sc-rust:sniff`              |
|12 | `Cargo.toml` in a subfolder, **no** `axum`/`actix-web`/`rocket`        | `rust-vanilla`             | `no provider` — no line in `pivot-providers.md`; generation is the only remedy              |
|13 | `Cargo.toml` carrying `[workspace]` **not at the root** (`engine/`)    | monorepo halt              | STOP and list the workspace members among the candidates offered to the user                |
|14 | `manage.py` + `rest_framework` in `INSTALLED_APPS`                     | `django` **+** `drf`       | Load `perf-pivots-django.md` **+** `perf-pivots-drf.md` — `drf` concatenates, it never replaces `django` |
|15 | `main.py` holding `FastAPI()`, no `manage.py`                          | `fastapi`                  | `perf-pivots-fastapi.md` if installed, else recommend `sc-python`, `/sc-python:sniff`       |
|16 | Django project + `celery.py` + `CELERY_BROKER_URL`                     | `django` **+** `celery`    | Two slugs, two provenance pairs — a run reporting `celery` alone has mis-detected the stack |
|17 | Any backend + `httpx` in the dependency manifest                       | stack slug **+** `httpx`   | `perf-pivots-httpx.md` if installed, else recommend `sc-python`, `/sc-python:sniff`         |
|18 | `vite.config.ts` **outside** a Nuxt/Astro project                      | stack slug **+** `vite`    | `perf-pivots-vite.md` if installed, else recommend `sc-js`, `/sc-js:sniff`                  |

## Failure modes to catch

- **False Nuxt match**: Vue SPA project misidentified as Nuxt because `nuxt` appears in a transitive dep — detection must grep the **direct** deps section, not all of `package.json`
- **Missed hybrid**: Django + Alpine project audited as pure Django (Alpine pivots skipped) — Step 1.4 must trigger BOTH-layer load
- **Silent fallback**: skill picks `perf_checklist_nuxt.md` for a non-Nuxt stack instead of stopping to propose generation
- **DEC dependency leak**: skill writes to `aidd_docs/internal/decisions/` on a project where that folder doesn't exist (must be conditional per Rule 7)
- **Rust missed for depth**: a crate under `app/` or `engine/core/` reported as "no stack" because `Cargo.toml` was looked for at the root only — the search is bounded at depth 3, not at depth 0
- **`target/` flood**: the Rust probe matching hundreds of vendored manifests because `-not -path '*/target/*'` was dropped
- **Additive layer swallowing the stack**: a Django + Celery project reported as `celery` alone, or a Vue + Vite project as `vite` alone — a layer adds to a stack, it never is one, so the run must emit one pair per slug
- **Additive layer dropped**: the same project reported as `django` alone, `perf-pivots-celery.md` never loaded although installed — the layer is silently lost and nothing in the output says so
- **Rust folded into `other`**: a crate without a web framework labelled `other` instead of `rust-vanilla`. Both emit `no provider` today, so the output looks right — but `other` says "unknown stack" where `rust-vanilla` says "known stack, unserved", and only the second stays true when `sc-rust` ships another `perf` pivot

## When to update

- After adding a new pivot in `framework-mapping.md` → add a row here covering the new stack
- After fixing a detection bug → add the failing project shape as a regression case
