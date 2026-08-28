# Local

Reconcile WordPress, Laravel, or Symfony locally without destructive container or database effects.

## Input

- Composer and package manifests, framework sentinels, local examples, database engine, and existing container wrappers.

## Output

An idempotent local start, stop, CLI, and verification procedure for the detected framework.

## Process

1. **Detect.** Reuse existing sniff signals to resolve WordPress, Laravel, or Symfony and stop on an unsupported combination.
2. **Reconcile.** Preserve existing containers, volumes, variables, and framework commands.
   - For WordPress, reuse wp-env, the Compose project name guard, and the `pnpm wp` wrapper.
3. **Verify.** Check the framework CLI, local URL, and rendered application without reset, destroy, import, or production access.
4. **Repeat.** Reconcile unchanged inputs a second time and report each check explicitly.

## Test

| Case | Pass |
| --- | --- |
| WordPress fixture is verified | the wrapper reports WP CLI, active theme or plugin, URL, and rendered content |
| Laravel or Symfony fixture is verified | the native framework CLI and welcome route are checked |
| database volume is populated | no reset, destroy, import, or deletion command is intended |
| reconciliation runs twice unchanged | the second intended-write set is empty |
