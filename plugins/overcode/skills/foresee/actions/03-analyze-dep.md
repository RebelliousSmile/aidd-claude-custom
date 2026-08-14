# Analyze-dep

Runs the installed AIDD dependency audit first, then adds only the repository-specific abandonment and migration horizon that the audit does not own.

## Inputs

- `$ARGUMENTS` (required): `<package | manifest> [--all] [--discuss | --plan]`
- `package`: one dependency present in the project manifest.
- `manifest`: `package.json`, `composer.json`, `pyproject.toml`, or `Cargo.toml`.
- `--all`: explicit opt-in to horizon analysis for every dependency returned by the audit instead of the default top five.

## Output

Write `aidd_docs/foresee/YYYY-MM-DD-HHMMSS-dep-<slug>.md`:

```md
# Dependency horizon — <target>

Baseline audit: <AIDD report path>
Scope: <single | N of M audit-prioritized dependencies>

| Dependency | Continuity | Isolation | Exit options | Coverage | Horizon |
|---|---:|---:|---:|---:|---|
| <name> | <1-10 or unknown> | <1-10 or unknown> | <1-10 or unknown> | <known>/3 | <risk summary> |

## Evidence

| Dependency | Signal | Observation | Source | Observed at |
|---|---|---|---|---|

## Persistence

| Signal | Status | Evidence |
|---|---|---|
```

Do not copy vulnerability, licence, outdated-version, transitive-depth, or compatibility findings from the baseline audit into local scores. Link to them instead.

## Process

1. Parse the target and flags. Read `@../../../references/aidd-delegation.md`.
2. Resolve and run `aidd-dev:04-audit` with pillar `dependencies`. If it fails or no report is produced, return its failure receipt and stop; no horizon score is valid without the baseline.
3. Select the local horizon scope:
   - named package → that package only;
   - manifest → at most the five dependencies ranked highest by the AIDD report;
   - manifest with `--all` → announce the number of dependencies and cost before continuing. The explicit flag is consent; do not add another confirmation.
4. For each selected dependency, load only the context in `@../assets/context-map.md` and evaluate only signals in `@../references/dep-risk-signals.md`. Use native host concurrency when useful; sequential bounded execution is equally valid. Never prescribe a model or subagent type.
5. Score the three dimensions with `@../assets/scoring-rubrics.md`. A missing observation is `unknown`, excluded from the denominator. Display coverage as known dimensions over `3`; do not produce a composite when fewer than two dimensions are known.
6. Compare only local horizon signals with the newest prior timestamped report for the same dependency and classify them `Resolved`, `Persistent`, or `New`. Do not compare or restate the AIDD audit's findings.
7. Persist the report with second-resolution timestamp and target slug, then return it with the delegation receipt (`local_follow_up: dependency horizon`).
8. Apply common `--discuss` and `--plan` behavior to the completed horizon report.

## Test

- A manifest without `--all` analyzes no more than five dependencies selected by the AIDD report.
- Missing metadata yields `unknown`, reduces coverage, and cannot improve the score.
- The local report contains no CVE, licence, outdated-version, or transitive-depth rescore.
- Two runs in the same day have distinct filenames.
