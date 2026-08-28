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
