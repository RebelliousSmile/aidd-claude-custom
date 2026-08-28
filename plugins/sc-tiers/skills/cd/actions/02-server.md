# Server

Reconcile supported provider prerequisites without running the project deployment command.

## Input

- A valid project contract, selected SSH, Railway, or Heroku provider, and nonsecret target facts.

## Output

Bounded provider metadata and the required out of band secret names, or a no write refusal.

## Process

1. **Validate.** Check contract version, root ownership, facade parity, operations, source, proof, and recovery.
2. **Load.** Read [supported providers](../references/providers.md) and stop on a missing primitive, missing fact, or unsupported provider.
3. **Reconcile.** Preserve or add only versionable provider identifiers and references to declared secret names.
4. **Verify.** Scan intended files for secret values and confirm that the project command never runs during provider setup.

## Test

| Case | Pass |
| --- | --- |
| supported provider and facts are complete | only bounded nonsecret metadata and secret name references are intended |
| provider primitive or required fact is absent | no provider file or remote command is intended |
| contract is stale or invalid | no provider write is intended and producer correction is named |
| generated metadata is scanned | no secret value is present and the project command has not run |
