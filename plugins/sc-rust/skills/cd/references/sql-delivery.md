# Rust SQL delivery

Only apply a strategy whose crate/configuration is present:

- SQLx: use the project's checked migration directory and installed invocation.
- Diesel: use the project's Diesel migration configuration and CLI strategy.
- rusqlite: require a project-owned migration mechanism; the crate alone provides no deploy command.

Compilation, artifact transfer, migration and service switch are independent gates. `deploy:db` means reviewed schema migration with backup/recovery, not local data upload. A non-zero migration prevents the pointer switch and preserves the prior running release. Mutable data transfer requires a separate explicit scoped operation and confirmation.
