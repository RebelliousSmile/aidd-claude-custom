# Reasoned WordPress synchronization

Treat these as separate surfaces: code, configuration, schema/migrations, full database, editorial content, and media. Every operation states its scope and direction.

- `deploy:prod`: local-to-production code release by default; excludes secrets, caches, uploads and local database state.
- `deploy:db`: reviewed schema migration in production, or an explicit local-authoritative database mirror in staging. It is never a hidden part of code deployment.
- `deploy:sync`: staging-only local mirror whose exact data/content/media scope and deletion policy are named. Production refuses this operation for mutable surfaces.
- `pull:*` and every target-to-target copy are outside this delivery contract and are refused.

WP-CLI search-replace must account for serialized data. Before staging mutation, require a fresh backup, stable preview, explicit confirmation and recovery. Media inventory uses normalized relative paths and content hashes: report additions, changes, deletions and transferable bytes; unchanged uploads transfer zero bytes. Prefer proven rsync, otherwise use the manifest fallback with safe partials, atomic replacement and final inventory verification. Never silently send a complete archive when comparison is unavailable.

Production receives code and explicitly safe declarative migrations only. Its database, editorial content and uploads remain untouched and authoritative.

## Remote capability profile

Choose the procedure from observed host capabilities, not from the provider name or from a lowest-common-denominator WordPress recipe. Probe only when remote verification is authorized; otherwise use documented target facts and mark unverified assumptions.

Record at least:

- SSH transport and interactive/non-interactive shell availability;
- `tar`, `rsync`, `scp`/SFTP, `unzip`, and deletion semantics;
- WP-CLI availability and whether PHP permits process execution;
- direct `mysql`/`mysqldump` access and whether a fresh remote backup can be produced;
- cron, deploy hooks, symlinks/releases, writable paths, and rollback options.

A more capable host may use atomic releases, rsync, remote WP-CLI, server-side backups, or automation. A restricted host may legitimately retain archive-over-SSH, SFTP, or direct database-client workarounds. Preserve either implementation when it satisfies the same scoped safety contract; never downgrade a capable host merely because another deployment target is more constrained.
