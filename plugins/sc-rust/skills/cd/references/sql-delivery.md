# Rust SQL delivery

Only apply a strategy whose crate/configuration is present:

- SQLx: use the project's checked migration directory and installed invocation.
- Diesel: use the project's Diesel migration configuration and CLI strategy.
- rusqlite: require a project-owned migration mechanism; the crate alone provides no deploy command.

Compilation, artifact transfer, migration and service switch are independent gates. `deploy:db` means reviewed schema migration with backup/recovery, not local data upload. A non-zero migration prevents the selected target's pointer switch and preserves its prior running release.

Production business data and persistent files remain authoritative to each target; local uploads and target-to-target copies are refused. A staging target may declare scoped local mirrors only with deterministic data export/import or a reliable file manifest, resumable delta, preview, backup, confirmation and final proof.
