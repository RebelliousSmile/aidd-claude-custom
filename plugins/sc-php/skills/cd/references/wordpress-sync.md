# Reasoned WordPress synchronization

Treat these as separate surfaces: code, configuration, schema/migrations, full database, editorial content, and media. Every operation states its scope and direction.

- `deploy:prod`: local-to-production code release by default; excludes secrets, caches, uploads and local database state.
- `deploy:db`: local-to-production database operation only when explicitly designed, backed up, dry-run/reviewed and confirmed. It is never a hidden part of code deployment.
- `deploy:sync`: local-to-production synchronization whose exact content/media/configuration scope is named. An unqualified sync request is rejected.
- `pull:*`: production-to-local operation, kept distinct from deployment and protected from overwriting local work.

WP-CLI search-replace must account for serialized data. Media transfer must state deletion behavior; default to no remote deletion. Before production mutation record a backup and recovery command, then require confirmation. Afterward prove URL, active theme/plugin and the changed scope only.

## Remote capability profile

Choose the procedure from observed host capabilities, not from the provider name or from a lowest-common-denominator WordPress recipe. Probe only when remote verification is authorized; otherwise use documented target facts and mark unverified assumptions.

Record at least:

- SSH transport and interactive/non-interactive shell availability;
- `tar`, `rsync`, `scp`/SFTP, `unzip`, and deletion semantics;
- WP-CLI availability and whether PHP permits process execution;
- direct `mysql`/`mysqldump` access and whether a fresh remote backup can be produced;
- cron, deploy hooks, symlinks/releases, writable paths, and rollback options.

A more capable host may use atomic releases, rsync, remote WP-CLI, server-side backups, or automation. A restricted host may legitimately retain archive-over-SSH, SFTP, or direct database-client workarounds. Preserve either implementation when it satisfies the same scoped safety contract; never downgrade a capable host merely because another deployment target is more constrained.
