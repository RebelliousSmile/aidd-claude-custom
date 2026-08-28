# Automata

Generate a thin provider or CI envelope from the validated producer contract.

## Input

- A current project contract, selected supported automation platform, and provisioned secret names.

## Output

One thin GitHub, GitLab, Railway, or Heroku envelope that invokes the exact producer facade.

## Process

1. **Validate.** Refuse an absent, unknown version, or stale contract before writing.
2. **Load.** Read [CI adapters](../references/ci-adapters.md) and select the supported platform without redetecting the application stack.
3. **Generate.** Install locked dependencies, set the exact working directory, and call the contract command textually without copying deployment logic.
4. **Trigger.** Generate manual delivery when the trigger is absent or manual and generate push only for explicit push.
5. **Relay.** Preserve nonzero status and expose the contract source, proof, and recovery without secret values.

## Test

| Case | Pass |
| --- | --- |
| valid manual contract generates GitHub or GitLab automation | command and directory match byte-for-byte and the trigger is manual |
| contract explicitly declares push | push rules are generated without changing command or directory |
| contract is absent or stale | no workflow or provider file is intended |
| facade exits non-zero | no ignored error or success reinterpretation exists |
| envelope is scanned | secret names may appear but secret values and duplicated deployment logic do not |
