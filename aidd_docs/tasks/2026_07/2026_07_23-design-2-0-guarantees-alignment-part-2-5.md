---
name: plan
description: Lot 1.5 - sweep the exception paths Lot 1 fixed twice without fixing everywhere. A structurally invalid artifact exits 2 naming the field, never 1 and never a false green. Hardening only, no public surface changes.
argument-hint: N/A
objective: "Every tool that reads a contract artifact refuses a structurally invalid one the same way: exit 2, naming the artifact and the field, without crashing and without producing a green verdict on a set it silently mis-derived."
success_condition: "With MAL=plugins/design/skills/enforce/fixtures/malformed, node plugins/design/skills/enforce/adapters/lint-core.mjs $MAL/<case>/markup.html --contract $MAL/<case> exits 2 and prints the artifact filename, the offending field and the value received, for <case> in component-not-object, base-not-string and utility-prefixes-not-array, AND python plugins/design/tools/migrate-contract.py --contract $MAL/<case> --dry-run exits 2 likewise for <case> in 1x-root-not-object and 1x-component-not-object, AND no exception trace reaches stdout or stderr in any of those five runs, AND the eight fixtures taken in the master's fixture enumeration order still reproduce the exit-code baseline 0 1 0 1 0 1 0 1, AND python plugins/design/tools/migrate-contract.py --contract plugins/design/skills/enforce/fixtures/migration/oracle-contract-level --dry-run exits 0 and prints a mapping line for $.oracle, AND python plugins/design/tools/status.py --contract plugins/design/skills/enforce/fixtures prints the contract directory on stderr while stdout still carries the rung alone, AND jq -r .version plugins/design/.claude-plugin/plugin.json equals 2.0.1 and matches .claude-plugin/marketplace.json and index.json"
iteration: 0
created_at: "2026-07-24T00:00:00Z"
---

# Instruction: Lot 1.5 - sweep the exception paths

## Feature

- **Summary**: Lot 1 established that a required decision a tool refuses to guess exits 2, and applied it twice — undeclared `mode`, missing contract argument. It did not sweep the rest. Five read paths across the two tools still meet a structurally invalid artifact and either raise an uncaught exception (exit 1, indistinguishable from a lint violation) or, worse, carry on with a silently wrong derived set and return a green verdict. This lot closes the class rather than the two instances of it. No rule is added, no rule is removed, no CLI surface changes.
- **Stack**: `Node 20+ (lint-core.mjs, zero dependency) · Python 3.11+ (migrate-contract.py, status.py) · JSON contract artifacts`
- **Branch name**: `feat/design-2-0/lot-1-5-exception-paths`
- **Parent Plan**: `2026_07_23-design-2-0-guarantees-alignment-master.md`
- **Sequence**: `2.5 of 8`
- **Version**: 2.0.1 (PATCH)
- Confidence: 9/10
- Time to implement: 1 work unit

## Why PATCH and not MINOR

The master opens a breaking window at Lot 1 that Part 7 closes, inside which a shipped CLI may change incompatibly under a MINOR bump. This lot does not use that window. Nothing it changes is a behaviour a caller could have relied on: the inputs concerned either crash today or produce a verdict the tool had no basis to emit. 2.1.0 is already assigned to Lot 2 in the master's table; taking MINOR here would shift every version downstream for a hardening lot.

**Explicitly deferred to Lot 2**: renaming `config-gen.py --wp-url` / `--maquette-url`. Those two flags name a platform and an abbreviation in a tool the plugin declares stack-agnostic, which breaches the master's clause binding identifiers to the criterion. Renaming them *is* a CLI break, so it belongs to a lot that takes the window. Lot 2 already touches `config-gen.py` — it carries the rename.

## The defect class

Lot 1 named the rule: *a required decision the tool refuses to guess exits 2*. Its dual is unstated and unenforced: **a structurally invalid artifact is not a decision to guess either**. Five sites take the shape on faith.

| Site | Input that breaks it | Today | Should be |
| ---- | -------------------- | ----- | --------- |
| `lint-core.mjs:253` `validClasses.add(comp.base)` | a component that is not an object | `null` raises, exit 1; a string or number adds `undefined` to the valid set — **no crash, wrong set, green verdict** | exit 2, naming `components.json` and the component |
| `lint-core.mjs:255-256` `Object.values(comp.elements \|\| {})` | `elements` a string | `Object.values("ab")` yields `['a','b']` — characters enter the valid class set | exit 2, same |
| `lint-core.mjs:322` `utilityPrefixes.some(...)` | `$utilityPrefixes` not an array | `.some` undefined, raises, exit 1 | exit 2, naming `policies.json` and the field |
| `migrate-contract.py:176` `manifest.get("mode")` / `:144` `manifest.items()` | a `components.json` whose root is not an object | `AttributeError`, exit 1 | exit 2, naming the file |
| `migrate-contract.py:113` `comp.items()` | a component that is not an object | `AttributeError`, exit 1 | exit 2, naming the component |

The false-green rows matter more than the crashing ones. An exit 1 is at least visible; a valid-class set quietly seeded with `undefined` or with the characters of a string produces a lint that passes on markup it should have rejected — the exact failure mode the whole chantier exists to remove.

None of these is reachable from a well-formed contract, and no current fixture reaches any of them. All assume an artifact edited by hand or emitted by a broken generator — which is precisely what a migration lot invites.

## Architecture projection

### Files to modify

| File | Change |
| ---- | ------ |
| `plugins/design/skills/enforce/adapters/lint-core.mjs` | validate artifact shape before deriving rules; exit 2 on failure |
| `plugins/design/tools/migrate-contract.py` | same, before reading the manifest and each component |
| `plugins/design/tools/status.py` | name the contract directory in the verdict line |
| `plugins/design/references/contract-schema.md` | state that a shape violation exits 2, next to the exit-code table |
| `plugins/design/CHANGELOG.md` | 2.0.1 entry |
| `plugins/design/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `index.json` | 2.0.1 |

### Files to create

| File | Purpose |
| ---- | ------- |
| `plugins/design/skills/enforce/fixtures/malformed/component-not-object/` | a component whose value is a string |
| `plugins/design/skills/enforce/fixtures/malformed/base-not-string/` | `base` absent or not a string |
| `plugins/design/skills/enforce/fixtures/malformed/utility-prefixes-not-array/` | `$utilityPrefixes` an object |
| `plugins/design/skills/enforce/fixtures/malformed/root-not-object/` | a 1.x `components.json` whose root is an array |
| `plugins/design/skills/enforce/fixtures/migration/oracle-contract-level/` | a 1.x contract carrying a top-level `$.oracle` |

Each malformed fixture is minimal: the smallest contract that reaches the site, nothing else. They are inputs, never expected outputs.

## Applicable rules

- The master's exit-code space is fixed and this lot reassigns nothing: 0 no violation · 1 at least one violation or drift · 2 invocation or environment error, **including a required decision the tool refuses to guess** · 3 contract in 1.x format · 4 below conformity threshold. A shape violation is an environment error, not a lint violation.
- No message may print an exception trace. The refusal names the artifact file and the field; the stack is not the user's problem.
- No hard-coded design value enters any tool.
- Transverse writing criterion: exhaustive, stack-agnostic, fewest words; no duplication between a `SKILL.md` and its actions; DRY through `${CLAUDE_PLUGIN_ROOT}/references/`.

## Risk register

| Risk | Mitigation |
| ---- | ---------- |
| Validation drifts into a schema validator, growing a dependency the linter forbids | validate only the fields the five sites consume, in the function that consumes them; no generic validator, no library |
| A tightened check rejects a contract that used to pass | the eight-fixture baseline `0 1 0 1 0 1 0 1` is an acceptance criterion of every phase, not just the last |
| Validation duplicated between the two tools drifts apart | each tool validates only what it reads; the shared statement lives once in `references/contract-schema.md`, not copied into either |

## Implementation phases

### Phase 1: Malformed fixtures

> The refusal is only real once a fixture reaches it.

#### Tasks

1. Create the five fixture directories listed above, each a complete contract minimal enough to reach exactly one site.
2. `root-not-object` and `oracle-contract-level` are 1.x contracts (no `release.json`); the other three are 2.0.
3. Record in each directory which site it reaches, in a one-line `README` or an in-file comment field — not in a separate index.

#### Acceptance criteria

- [ ] Each of the five fixtures reaches its site today, verified by running the tool and observing the current wrong behaviour before any fix.
- [ ] No malformed fixture is picked up by the eight-fixture enumeration; the baseline `0 1 0 1 0 1 0 1` is unchanged by their existence.
- [ ] No fixture carries a project name, a client name or a platform name.

### Phase 2: `lint-core.mjs` shape refusal

> A wrong valid-class set is worse than a crash.

#### Tasks

1. Before deriving the valid class set, check each component is an object and its `base` is a string; `elements` and `modifiers`, when present, are objects.
2. Before the utility-prefix test, check `$utilityPrefixes` is an array of strings.
3. On failure, print the artifact filename, the path to the offending field, and what was expected; exit 2.
4. Fail on the first violation. The tool is not a validator producing a report; it refuses and names one reason.

#### Acceptance criteria

- [ ] `component-not-object`, `base-not-string` and `utility-prefixes-not-array` each exit 2.
- [ ] Each message names the artifact file and the field path.
- [ ] No exception trace reaches stdout or stderr.
- [ ] The eight fixtures reproduce the baseline `0 1 0 1 0 1 0 1`.
- [ ] The 1.x fixture still exits 3 with the migration command; a missing or unreadable argument still exits 2.

### Phase 3: `migrate-contract.py` shape refusal

> Migration is where malformed artifacts actually arrive.

#### Tasks

1. Check the manifest root is an object before `manifest.get` / `manifest.items`.
2. Check each component is an object before `comp.items()`.
3. On failure, print the file and the offending key; exit 2. No traceback.
4. Apply the check in the dry-run path as well — a dry run that crashes is not a dry run.

#### Acceptance criteria

- [ ] `root-not-object` and `component-not-object` exit 2 under `--dry-run` and without it.
- [ ] Each message names the file and the component key.
- [ ] No traceback reaches stdout or stderr.
- [ ] The four existing migration fixtures behave exactly as Lot 1's success_condition specifies: `nominal-1x`, `no-layer-3`, `version-skew` exit 0; `mode-undeclared` exits 2 naming `--mode`, and exits 0 when `--mode` is passed.
- [ ] A dry run still writes nothing, verified by hash snapshot of the fixture tree.

### Phase 4: `$.oracle` contract-level branch

> A branch with no fixture is a claim, not a behaviour.

#### Tasks

1. Add the `oracle-contract-level` fixture: a 1.x contract with a top-level `oracle` key and no per-component `oracle`.
2. Verify the branch that maps `$.oracle` to `oracle.contract` and emits its warning line is reached, and that `oracle.json` is written and declared in `release.json`.

#### Acceptance criteria

- [ ] The fixture exits 0 under `--dry-run` and prints a mapping line for `$.oracle`.
- [ ] The warning naming the contract-level form as having no reader is printed.
- [ ] Migrating it for real produces an `oracle.json` carrying `contract`, declared by `release.json`.

### Phase 5: `status.py` verdict names its subject

> A rung with no contract named is unciteable evidence.

#### Tasks

1. Print the contract directory alongside the rung.

#### Acceptance criteria

- [ ] The output names the contract directory and the rung, on one line.
- [ ] Exit codes are unchanged: 0 on success, 2 when the directory is not found.
- [ ] `migrate-contract.py`, which imports this module, is unaffected — it consumes `compute`/`observe`, not the printed line.

### Phase 6: Statement, version and CHANGELOG

#### Tasks

1. State in `references/contract-schema.md`, next to the exit-code table, that an artifact whose shape does not match its declaration exits 2 — one sentence, not a copy of the site table.
2. Bump the three registers to 2.0.1.
3. Write the CHANGELOG entry: the defect class, why exit 1 was wrong, and the false-green rows named explicitly.
4. Record in the CHANGELOG that the `config-gen.py` flag rename is carried by Lot 2, so the deferral is traceable rather than forgotten.

#### Acceptance criteria

- [ ] The three registers read 2.0.1 and agree.
- [ ] The CHANGELOG names the false-green paths, not only the crashing ones.
- [ ] The statement exists once; neither tool's documentation restates the site table.
- [ ] No `SKILL.md` and its actions carry the same sentence.

## Reserves carried but not treated here

Named so they are traceable, deliberately out of scope:

| Reserve | Why not here | Where it belongs |
| ------- | ------------ | ---------------- |
| `config-gen.py --wp-url` / `--maquette-url` name a platform | renaming is a CLI break; this lot is PATCH | Lot 2 (already touches the file, takes the window) |
| `README.md:18` funnel diagram calls `enforce` a *verrou* | prose in a diagram, consistent with "gate"; no tool reads it | none — noted, not a defect |
| `contract-schema.md` tagging | re-verified during the Lot 1 audit; every field row carries a tag. The apparent misses were headers and the artifact/rule/mode comparison tables | closed, no action |
| `.lintrc.json` template severities · Part 7 grep over `git ls-files` | already corrected in Lot 0 | closed, no action |

## Amendments

Three, all found while implementing, all recorded before the phases were closed.

1. **Fixture names collide.** The plan listed one `component-not-object` used by both tools. They cannot share a directory: `lint-core.mjs` requires `release.json`, `migrate-contract.py` requires its absence. The 1.x cases are prefixed: `1x-root-not-object`, `1x-component-not-object`.

2. **`status.py` writes the contract directory to stderr, not on the rung's line.** The plan said "on one line", written before `adjust/02-freeze.md:143` was identified as a consumer — it copies stdout *verbatim* into `release.json § status`. Anything added to that line would have been written into the contract, which is the exact failure this lot removes. stdout keeps the rung alone; stderr carries the subject.

3. **The defect was worse than diagnosed.** The plan predicted exit 1 with an uncaught exception at the three `lint-core.mjs` sites. Measured on fixtures before any fix, all three exited **0**. A contract whose components are all malformed declares an empty vocabulary, every class is treated as a utility, and the run passes on any markup. The two Python sites behaved as predicted (exit 1 + traceback). The CHANGELOG records the measured behaviour, not the predicted one.

## Log

- 2026-07-24 — Phases 1 to 6 implemented and verified. The five malformed fixtures were run against the unmodified tools first, to observe the defect before fixing it; that run is what produced amendment 3.

## Verification run

| Clause | Result |
| ------ | ------ |
| 3 lint-core cases exit 2, artifact + field + value named | ✅ |
| 2 migrate cases exit 2 under `--dry-run` and without it, no traceback | ✅ |
| Eight-fixture baseline `0 1 0 1 0 1 0 1` | ✅ unchanged |
| 1.x contract still exits 3, missing argument still exits 2 | ✅ |
| Four Lot 1 migration fixtures unchanged (`0 0 0`, `2`, `0` with `--mode`) | ✅ |
| `oracle-contract-level` exits 0, maps `$.oracle`, writes `oracle.json § contract` declared by `release.json` | ✅ |
| `status.py` stdout = rung alone, stderr = contract directory, exit 0 / 2 unchanged | ✅ |
| Three registers at 2.0.1 | ✅ |

## Validation flow demonstration

Run the success_condition verbatim. Every clause is a command with an observable exit code or a string in the output; none is a judgement.
