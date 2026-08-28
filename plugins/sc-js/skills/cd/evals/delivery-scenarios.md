# JavaScript delivery scenarios

| Scenario | Expected behavior |
| --- | --- |
| Nuxt SSR with pnpm | Preserve pnpm, detect the configured adapter, and expose one `pnpm deploy:prod` facade. |
| Vite static site | Use the configured build output, never an assumed directory. |
| Existing custom deploy script | Preserve it when compatible; surface a conflict before any overwrite otherwise. |
| SQL ORM | Keep migrations distinct from production content and require backup/recovery. |
| IndexedDB | Ship tested client migration code; transfer no browser data. |
| Composite PHP application | Register a bounded JS contributor and create no second root facade. |
| Missing sc-tiers | Stop automata with a named prerequisite and write nothing. |
| Named Node targets | Use one package-manager facade with separate server and automata invocations and locks. |
| Nuxt staging store | Mirror server data/media only when export/import or manifest inventory is proven. |
| Nuxt production store | Apply schema migration while preserving target-authoritative rows and media. |
| Static target | Deliver its configured artifact without inventing a database or media store. |
