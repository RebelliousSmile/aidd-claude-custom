# JavaScript command facade

Preserve the lockfile owner. With pnpm, expose `deploy:prod` as a `package.json` script that invokes one versioned project script such as `node scripts/deploy.mjs prod`; do not put the whole procedure inline. Use the equivalent native script command for npm, Yarn, or Bun rather than adding pnpm.

Reconciliation rules:

1. Inspect the existing script and owned file before editing.
2. If absent, add the smallest facade and project script.
3. If semantically identical, leave it unchanged.
4. If user-owned and divergent, show the conflict and request arbitration; never overwrite silently.
5. Match `deploy/contract.json.command` and `workingDirectory` exactly to the runnable facade.

The project script owns preflight, exclusions, source identity, provider call, proof and recovery. An envelope only calls it and relays its exit status.

The facade accepts a target id and `deploy:*` operation. Provider and mode live in target metadata, so switching a target between server and automata does not create a second script or change operation semantics. Every target has its own invocation, lifecycle revision and lock; an error never falls through to another target.

## Permission boundary

Do not use `rsync -a` as shorthand when the artifact originates on DrvFs: archive mode includes permission preservation. A safe DrvFs transport disables permission, owner, and group preservation and applies explicit destination modes for directories and files (for example through an appropriate `--chmod` policy). Executable paths are declared separately so the project can retain only the execute bits its runtime actually needs. Staging the built artifact on a native Linux filesystem is also valid when that provenance is established.

The owned script must fail when post-transfer inspection disagrees with the declared policy. Its proof samples at least one directory, one newly created file, and one updated file so an umask-only success cannot mask permissive existing paths. During skill configuration, verify the proof mechanism and dry-run shape without contacting the target; record actual mode observations only during delivery.
