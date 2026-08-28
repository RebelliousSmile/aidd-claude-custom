# Automata

## Inputs

- Valid current `deploy/contract.json`, chosen supported automation platform and provisioned secret names.

## Process

1. Refuse absent, unknown-version or stale contracts before writing.
2. Select [the CI adapter](../references/ci-adapters.md) and install the stack/runtime with lockfile-aware commands.
3. Set the exact contract working directory and invoke its command textually. Do not inline deployment, migration or provider logic.
4. Generate a manual trigger when `trigger` is absent or `manual`; generate push only for explicit `push`.
5. Let a non-zero project exit fail the job. Surface source identity, proof and recovery from the contract in the job/report.

## Outputs

One thin GitHub, GitLab, Railway or Heroku automation envelope containing secret references only.

## Test

Compare command and directory byte-for-byte to the contract, assert default manual triggering, inject a failing facade and confirm the job remains failed.
