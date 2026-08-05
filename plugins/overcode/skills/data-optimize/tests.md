# data-optimize — smoke tests

> Run these before trusting `data-optimize` on a new stack or after editing `SKILL.md` / `api-mapping.md`.
> Purpose: verify the **detection step** produces the expected stack label and points to the right checklist source.

## How to use

For each case below:
1. `cd` into a project matching the description (or a minimal fixture).
2. Run the Quick Start detection commands from `SKILL.md`.
3. Compare the detected stack + chosen checklist against the **Expected** column.
4. If mismatch → fix `SKILL.md` Step 1 detection logic OR `api-mapping.md` pivots.

> The **Expected checklist source** column below covers the `source` field of the provenance header only. The second field, `pivot`, is not fixed by the project shape: it depends on what `.claude/rules/07-quality/` holds in the fixture at run time. A run is correct only if **both** fields are emitted — matching this column while omitting `pivot` is a failure, not a pass.

## Test matrix

| #  | Project shape (files present)                                                  | Expected stack             | Expected checklist source                                                                  |
|----|--------------------------------------------------------------------------------|----------------------------|---------------------------------------------------------------------------------------------|
| 1  | `package.json` with `"firebase": "^10.x"` + `firebase.json` + `firestore.rules`| `firebase`                 | `aidd_docs/templates/dev/data_checklist_firebase.md` (existing template)                    |
| 2  | `package.json` with `"@supabase/supabase-js"` + `supabase/config.toml`         | `supabase`                 | Generate `data_checklist_supabase.md` (propose to user)                                     |
| 3  | `package.json` with `"@prisma/client"` + `prisma/schema.prisma`                | `prisma`                   | Generate `data_checklist_prisma.md`                                                         |
| 4  | `package.json` with `"drizzle-orm"` + `drizzle.config.ts`                      | `drizzle`                  | Generate `data_checklist_drizzle.md`                                                        |
| 5  | `package.json` with `"mongoose"` (no other ORM)                                | `mongoose`                 | Generate `data_checklist_mongoose.md`                                                       |
| 6  | `package.json` with `"@aws-sdk/client-dynamodb"` + `serverless.yml`            | `dynamodb`                 | Generate `data_checklist_dynamodb.md`                                                       |
| 7  | `manage.py` + `<app>/models.py` defining `models.Model` subclasses             | `django-orm`               | Generate `data_checklist_django-orm.md`                                                     |
| 8  | `composer.json` with `"laravel/framework"` + `app/Models/*.php`                | `laravel-eloquent`         | Generate `data_checklist_laravel-eloquent.md`                                               |
| 9  | `composer.json` with `"doctrine/orm"` (Symfony or standalone)                  | `doctrine`                 | Generate `data_checklist_doctrine.md`                                                       |
| 10 | `package.json` with `"@apollo/client"` + `*.gql` operations                    | `graphql-apollo`           | Generate `data_checklist_graphql-apollo.md`                                                 |
| 11 | `package.json` with `"@trpc/client"` + `@trpc/server`                          | `trpc`                     | Generate `data_checklist_trpc.md`                                                           |
| 12 | Hasura `metadata/` directory + `query_collections.yaml`                        | `hasura`                   | Generate `data_checklist_hasura.md`                                                         |
| 13 | Firebase + Prisma both in `package.json` (e.g. Firestore for users + PG for analytics) | `firebase-prisma` (hybrid) | Load Firebase pivots **+** Prisma pivots — no new combined template generated     |
| 14 | Plain `fetch`/`axios` calls to a documented REST API, no ORM/SDK markers       | `rest-vanilla`             | Generate `data_checklist_rest-vanilla.md`                                                   |
| 15 | Exotic DB without standard driver (e.g. SurrealDB, EdgeDB, FaunaDB, raw libpq) | `other` (fallback)         | Trigger fallback flow — ask user 3 infos, build from 11 generic sections                    |
| 16 | `Cargo.toml` **in a subfolder** (`app/rust-backend/`) with `rusqlite`          | `rusqlite`                 | `data-pivots-rusqlite.md` if installed, else recommend `sc-rust`, `/sc-rust:sniff`          |
| 17 | `Cargo.toml` in a subfolder with `diesel` + `diesel.toml` + `migrations/`      | `diesel`                   | `data-pivots-diesel.md` if installed, else recommend `sc-rust`, `/sc-rust:sniff`            |
| 18 | `Cargo.toml` in a subfolder with `sqlx` + `.sqlx/` query cache                 | `sqlx`                     | `data-pivots-sqlx.md` if installed, else recommend `sc-rust`, `/sc-rust:sniff`              |
| 19 | `Cargo.toml` in a subfolder with `sea-orm`                                     | `sea-orm`                  | `no provider` — no line in `pivot-providers.md`; generation is the only remedy              |
| 20 | `Cargo.toml` with serde/tokio only, **no** ORM or driver                       | no data stack              | `1quater` fallback — dump direct deps, ask which one talks to the store                     |
| 21 | `alembic/` + `models/` carrying `declarative_base()` or `DeclarativeBase`      | `sqlalchemy`               | `data-pivots-sqlalchemy.md` if installed, else recommend `sc-python`, `/sc-python:sniff`    |
| 22 | `load_dataset(` in the sources + `datasets` in the dependency manifest         | `datasets`                 | `data-pivots-datasets.md` if installed, else recommend `sc-python`, `/sc-python:sniff`      |

**Rule for distinguishing 14 vs 15:** `rest-vanilla` = HTTP/JSON client without a data-access library (no ORM, no SDK, no GraphQL client). `other` = a DB or service exists but uses a non-mainstream driver/client absent from the api-mapping pivots. If the project uses `fetch` to talk to its own REST endpoints AND a recognized stack handles the server side, audit BOTH (hybrid).

## Failure modes to catch

- **False Firebase match**: project with `firebase-tools` (CLI only, deploy hosting) misidentified as Firestore user — detection must require `firebase`/`firebase-admin` SDK in dependencies, not just `firebase-tools` in devDeps
- **Missed hybrid**: Firestore + Prisma project audited as pure Firebase (Prisma pivots skipped) — Step 1.4 must trigger BOTH-layer load when both SDKs are direct deps
- **Silent fallback**: skill picks `data_checklist_firebase.md` for a non-Firebase stack instead of stopping to propose generation
- **DEC dependency leak**: skill writes to `aidd_docs/internal/decisions/` on a project where that folder doesn't exist (must be conditional per Rule 7)
- **Mistaking GraphQL transport for stack**: tRPC + GraphQL backend (Hasura behind tRPC procedures) — must audit BOTH (transport ergonomics + DB layer)
- **ORM transitive dep**: `prisma` appearing as transitive (e.g. via `@trigger.dev/sdk`) misidentified as primary stack — detection must grep direct deps only
- **Rust missed for depth**: an ORM under `app/rust-backend/` reported as "no data layer" because `Cargo.toml` was looked for at the root only — the search is bounded at depth 3, not at depth 0
- **`target/` flood**: the Rust probe matching hundreds of vendored manifests because `-not -path '*/target/*'` was dropped
- **`alembic.ini` read as SQLAlchemy**: a project carrying the migration tool alone labelled `sqlalchemy` — the ORM is proven by `declarative_base()` / `DeclarativeBase` in the models, Alembic can front a schema it does not map
- **HuggingFace `datasets` read as a generic word**: a `data/` folder or a `datasets` variable taken for the library — the marker is the dependency manifest plus `load_dataset(`
- **Slug pasted into the filename**: `laravel-eloquent` resolved to `data-pivots-laravel-eloquent.md` (which does not exist) instead of `data-pivots-eloquent.md`, or `graphql-urql` to a file of its own instead of the shared `data-pivots-graphql.md` — the pivot is read off `pivot-providers.md`, never composed

## When to update

- After adding a new pivot in `api-mapping.md` → add a row here covering the new stack
- After fixing a detection bug → add the failing project shape as a regression case
