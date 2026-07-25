---
name: review-functional
description: Functional review of Lot 1 (design 2.0 contract split) against its plan
argument-hint: N/A
---

# Functional Review: design 2.0 — Lot 1, split contract and version identity

- **Plan**: `aidd_docs/tasks/2026_07/2026_07_23-design-2-0-guarantees-alignment-part-2.md`
- **Diff scope**: `git diff main` restricted to the plan perimeter (`plugins/design/`, `aidd_docs/internal/decisions/005-*`, three version registers, `README.md`, `aidd_docs/memory/design-plugin.md`) — 45 tracked files + 20 untracked
- **Date**: 2026-07-24

## Verdict

PARTIAL — the whole `success_condition` reproduces on disk and 27/31 criteria are Met, but three documented facts contradict what the shipped tools do (`oracle.json` optionality, exhaustiveness of the redistribution table, an invariant cross-reference), and two files the plan enumerated were never touched. No blocker.

## Scoring Matrix

### `success_condition`

| Criterion | Files | Status | Severity | Notes |
| --- | --- | --- | --- | --- |
| SC1 — `migrate-contract.py --dry-run` exits 0 on `nominal-1x`, `no-layer-3`, `version-skew` | `plugins/design/tools/migrate-contract.py` | Met | — | Re-run: 0 / 0 / 0. Anomalies reported for the two degenerate cases, none for nominal |
| SC2 — exits 2 on `mode-undeclared` naming `--mode`, 0 with `--mode` passed | `migrate-contract.py:183` | Met | — | Message names `--mode bem\|utility-first` and states why it refuses to guess |
| SC3 — eight fixtures reproduce `0 1 0 1 0 1 0 1` after migration | `skills/enforce/adapters/lint-core.mjs`, `fixtures/**` | Met | — | Re-run in the master's enumeration order with `--contract` per family: exactly `0 1 0 1 0 1 0 1` |
| SC4 — `nominal-1x` exits 3 with the migration command; missing argument still exits 2; three registers read 2.0.0 | `lint-core.mjs:127`, `plugin.json`, `marketplace.json`, `index.json` | Met | — | Exit 3 prints both dry-run and write commands with absolute paths; bare call and unreadable file both exit 2; the three registers agree on `2.0.0` |

### Phase 1 — specify the four artifacts

| Criterion | Files | Status | Severity | Notes |
| --- | --- | --- | --- | --- |
| Every field of the redistribution table appears exactly once in the new schema | `references/contract-schema.md` | Partial | 🟡 major | The table is present and complete, but the script emits two targets the table does not name (see Finding 2) |
| Every field carries one tag, every executable tag names a consumer | `references/contract-schema.md`, `adjust/references/manifest-schema.md` | Met | — | Four field tables, every row carries `exécutable · <consumer>` or `informationnel`; deferred consumers name their lot |
| No field is documented in two places | `contract-schema.md`, `manifest-schema.md` | Met | — | `manifest-schema.md` reduced to `components.json`; `contract-schema.md` carries a skeleton and delegates the field detail |
| `manifest-schema.md` reduced, `design-system-contract.md` rewritten around four artifacts | both files | Met | — | `manifest-schema.md` −276 lines net; six invariants instead of seven |
| Invariant 5 (version parity) declared gone | `manifest-schema.md:53`, `contract-schema.md:73` | Met | — | Restated as data, not violation, in both places and in ADR 005 §3 |

### Phase 2 — migration fixtures

| Criterion | Files | Status | Severity | Notes |
| --- | --- | --- | --- | --- |
| Four fixture directories exist, named by class of case | `skills/enforce/fixtures/migration/` | Met | — | `nominal-1x`, `no-layer-3`, `version-skew`, `mode-undeclared`, plus the expected output `nominal-2x` |
| The nominal pair covers every field of the redistribution table | `fixtures/migration/nominal-1x`, `nominal-2x` | Met | — | Dry-run mapping emits all nine rows of the table, adapters included |
| No fixture contains a project name, a real URL or a stack-specific selector | `fixtures/migration/**` | Met | — | Project-name grep over `git ls-files` hits only `CHANGELOG.md`, `audits/`, `adapters/measure/configs/mentions-legales.json` — the two master exemptions plus the Lot 4 deferral |

### Phase 3 — migration script

| Criterion | Files | Status | Severity | Notes |
| --- | --- | --- | --- | --- |
| `--dry-run` writes nothing to disk | `migrate-contract.py:236` | Met | — | Verified on a scratch copy: no file created, no mtime changed |
| Each degenerate fixture produces the documented outcome and exit code | `migrate-contract.py` | Met | — | 0 / 0 / 2 as the master's table assigns; anomaly text names the capping charter and the version skew |
| Running the script twice produces identical output and no diff | `migrate-contract.py:161` | Met | — | Second run prints `NO-OP release.json present`, exit 0, zero diff |
| The derived adapter table lists every adapter present with a declared consumer | `migrate-contract.py:88`, `contract-schema.md:137` | Met | — | Extension→role map; `unknown` is raised as an anomaly, never silently written |
| The four status literals appear in `status.py` and nowhere else under `tools/` | `plugins/design/tools/status.py:28` | Met | — | Grep over `tools/*.py` returns `status.py` only |
| Round-trip against the expected output | `fixtures/migration/nominal-2x` | Met | — | Byte-identical on all five files except `provenance.producedAt`, which `--now` pins |

### Phase 4 — migration action

| Criterion | Files | Status | Severity | Notes |
| --- | --- | --- | --- | --- |
| The action carries a verifiable Test section | `skills/adjust/actions/03-migrate.md:84` | Met | — | Eight checkboxes, each observable |
| The action contains no logic the script already implements | `03-migrate.md:7` | Met | — | Explicitly forbids replaying the redistribution by hand and points at `contract-schema.md` |
| The eval scenario routes a migration request to `03-migrate` | `skills/adjust/evals/scenarios.json:9-11` | Met | — | Three prompts, including the exit-3 trigger |
| Non-regression check specified | `03-migrate.md` Étapes 1 and 5 | Met | — | Reference verdict taken before any write, and the case where it cannot be taken is declared rather than skipped |

### Phase 5 — linter read path

| Criterion | Files | Status | Severity | Notes |
| --- | --- | --- | --- | --- |
| Reads the four artifacts | `lint-core.mjs:100-160` | Met | — | Declared-artifact presence and parseability both checked; a declared-but-absent artifact exits 2 |
| Mode taken from `policies.json`, no inference from an empty component set | `lint-core.mjs` | Met | — | Removing `mode` from `policies.json` exits 2 with `Expected "bem" or "utility-first". The tool does not infer it.` |
| The 1.x read path is removed entirely | `lint-core.mjs` | Met | — | No 1.x parse branch survives; the only 1.x mentions are the diagnosis and its comments |
| Absence of `release.json` exits 3 with the migration command | `lint-core.mjs:127` | Met | — | Verified against `fixtures/migration/nominal-1x` |
| A missing or unreadable argument still exits 2 | `lint-core.mjs:39-57` | Met | — | Bare call, unreadable markup file, unknown option, `--contract` without value: all 2 |
| The eight fixtures reproduce the baseline | `fixtures/**` | Met | — | `0 1 0 1 0 1 0 1` |
| No hard-coded design value introduced | `lint-core.mjs` | Met | — | No hex, no px, no token name literal; every rule derives from the artifacts |

### Phase 6 — version, ADR and release

| Criterion | Files | Status | Severity | Notes |
| --- | --- | --- | --- | --- |
| The three version registers agree on 2.0.0 | `plugin.json`, `marketplace.json`, `index.json` | Met | — | Identical description string in the three, which the CHANGELOG names as a deliberate fix |
| The CHANGELOG names the break and the migration command | `plugins/design/CHANGELOG.md` | Met | — | `BREAKING` heading, `Migrer` block with both commands, redistribution table, exit-code table |
| ADR 005 exists and references DEC-002 as unchanged | `aidd_docs/internal/decisions/005-design-2-0-contract-split.md:58` | Met | — | Dedicated section; three rejected alternatives recorded |
| No `trois couches / three layers / layer 3 / couche 3` residue in the perimeter | `plugins/design/{skills,references,agents,adapters}` | Met | — | Grep returns zero matches |
| Both READMEs and `aidd_docs/memory/design-plugin.md` updated | `README.md:12`, `plugins/design/README.md`, `aidd_docs/memory/design-plugin.md` | Met | — | Memory carries version, artifact table, breaking list and the migration invocation |

### Phase 7 — transverse writing criterion

| Criterion | Files | Status | Severity | Notes |
| --- | --- | --- | --- | --- |
| No project name in the schema, fixtures, action or script messages | perimeter | Met | — | See Phase 2 grep |
| Degenerate cases named as classes of case | `fixtures/migration/` | Met | — | `no-layer-3`, `version-skew`, `mode-undeclared` |
| No stack presupposed by the contract or the script | `contract-schema.md`, `migrate-contract.py` | Met | — | Adapter consumers are roles (`stylesheet`, `build configuration`), never platforms |
| No duplication between `adjust/SKILL.md` and `03-migrate.md`; shared material in `references/contract-schema.md` | both files | Met | — | `SKILL.md` carries two routing lines; the action delegates the redistribution |

## Missing behaviors

- [ ] `plugins/design/skills/harness/SKILL.md` — enumerated in the plan's "Files to modify" (line 49) as one of the files describing the contract shape; never touched. Line 136 still reads « Harness ne modifie pas le contrat tokens/components », a 1.x description of the contract. 🟢 minor.
- [ ] `plugins/design/skills/adjust/actions/01-arbitrate.md` — enumerated in the same list; never touched. Line 28 still instructs the re-freeze path to « lire aussi `design/components.json` existant pour n'opérer que sur le delta », which no longer covers `policies.json` or `oracle.json`. A delta re-freeze can therefore silently drop the policy and oracle sides of an existing contract. 🟡 major.

Both hand off to `aidd-dev:02-implement`.

## Unplanned behaviors

All are recorded in the 2.0.0 CHANGELOG but none appears as an Amendment in the plan.

- [ ] `plugins/design/adapters/measure/config-gen.py` — new `--oracle`, defaults to the sibling of `--components`. Not in the plan's file list; a necessary consequence of `oracle` leaving `components.json`. Justified.
- [ ] `plugins/design/references/gate-natures.md` (new) — canonical statement of the two gate natures, deduplicating three divergent tables. Not in the plan's file list; a Lot 0-class deduplication landed in Lot 1.
- [ ] `lint-core.mjs` — `migrate-contract.py` path resolution fixed (was `../../../tools/`, dead once the linter is installed in a consumer's `design/lint/`), plus `status.py` import failure requalified from a Python traceback (exit 1) to exit 2. Real defect fixes, outside every phase.
- [ ] `lint-core.mjs` — a `release.json` declaring fewer than the three rule-bearing artifacts now exits 2 instead of silently running rules against an empty vocabulary. Real defect fix, outside every phase.
- [ ] `plugins/design/skills/enforce/fixtures/{,retrofit/,themed/,utility/}{policies,oracle,release}.json` — twelve new fixture files. Implied by Phase 5 task 5, never enumerated.
- [ ] `aidd_docs/internal/decisions/001-pivot-authoring-conventions.md` — modified; belongs to the `sc-*` pivot chantier, not to Lot 1.
- [ ] Roughly 110 files under `plugins/sc-{js,php,python,rust,css,tiers}` and `plugins/overcode`, plus ADR 006–010 and `aidd_docs/tasks/2026_07/2026_07_24-sc-pivots-organisation-arbitrages.md` — a different chantier whose own plan states « Branche : à créer depuis `main`, **hors de** `feat/design-2-0/*` ». It is nonetheless uncommitted in the same working tree as Lot 1. 🟡 major, scope hygiene.

## Flow / edge-case gaps

- [ ] **`oracle.json` is documented optional in three places and emitted unconditionally in two.** `contract-schema.md:48` states « `oracle.json` n'est déclaré que si le contrat en produit un » ; the CHANGELOG states « `oracle.json` reste facultatif : il n'est écrit que si le brief produit des cibles de mesure » ; `02-freeze.md:80` states « écrit seulement si le brief en produit ». But `02-freeze.md:227` Test requires that `release.json` « déclare **les quatre** artefacts, tous présents sur disque », and `migrate-contract.py:212` always writes `oracle.json` (empty `{"components":{}}` when there are no hints) and always declares it in `artifacts`. A freeze that legitimately skips `oracle.json` fails its own Test; a migration that produces no hints contradicts the schema. Verified: `no-layer-3` migrates to a `release.json` declaring all four artifacts. 🟡 major.
- [ ] **`contract-schema.md:210` claims the redistribution table is applied exactly.** « Exhaustive. Rien n'est inventé, rien n'est perdu. `tools/migrate-contract.py` applique exactement cette table. » The script has two targets the table does not name: `$.oracle` (contract-level hints) → `oracle.json.contract` (`migrate-contract.py:138`), and any unknown top-level key → `policies.json.<key>` (`:144`). Both are reported as anomalies, so nothing is lost — but `oracle.json.contract` is absent from the `oracle.json` schema, and the word « exactement » is the same class of unbacked claim Lot 0 was written to purge. 🟡 major.
- [ ] **`manifest-schema.md:37` sends `.a11y.role` to « (Invariant 5) ».** Invariant 5 is now « Contraste par thème » and says nothing about ARIA roles or attributes. The pointer was added by this chantier (it does not exist on `main`) and survived the 7→6 renumbering. There is no longer any invariant covering the a11y fields; the honest form is « aucun invariant ne le couvre ». 🟡 major.
- [ ] **`release.json` example diverges from the tool's output.** `contract-schema.md:37` shows `"from": "contrat 1.x"`; `migrate-contract.py:215` writes `"from": "1.x contract"`. 🟢 minor.
- [ ] **`migrate-contract.py:242` — `backup.mkdir(exist_ok=True)`.** A `.contract-1x/` left by an earlier aborted run is silently merged into, so a partial backup can be presented as a complete one. No pre-existence check, no warning. 🟢 minor.
- [ ] **`status.read_charter` is called from the migration path without a release root** (`migrate-contract.py:195`), so it can only look for the default `design-system.md`. A 1.x contract whose charter is named otherwise migrates with `charter.present: false` and a status capped at `extracted`. Acceptable for 1.x, which had no way to declare a charter path, but the anomaly message asserts the charter is absent rather than not-found-at-the-default-name. 🟢 minor.
- [ ] **The plan document does not record its own execution.** `iteration: 0`, all 27 acceptance checkboxes unchecked, `## Amendments` and `## Log` empty — while the master plan marks Lot 1 `done`. Part 1, by contrast, carries six amendments and a full log. Every deviation listed under *Unplanned behaviors* above is traceable only through the CHANGELOG. 🟡 major, process.
- [ ] **Nothing is committed.** `git log main..HEAD` is empty; the 189 working-tree entries carry Lot 0, Lot 1 and the unrelated `sc-*` chantier at once. Lot 0 is already checkpointed as published in the master plan, which is not true of any register a consumer can read.

## Summary

- **Criteria covered**: 27/31 Met, 4 Partial (Phase 1 field-uniqueness, plus the two untouched files and the plan-record gap counted under gaps)
- **Blockers**: 0
- **Follow-up actions**:
  1. Decide `oracle.json`'s optionality once, then align `contract-schema.md:48`, `02-freeze.md:80` and `:227`, the CHANGELOG, and `migrate-contract.py:212` on that decision — hand to `aidd-dev:07-refactor` for the docs, `aidd-dev:08-debug` if the script is the side that must change.
  2. Add `$.oracle → oracle.json.contract` and the unknown-key fallthrough to the redistribution table of `contract-schema.md`, and document `oracle.json.contract` in the oracle schema — or drop the word « exactement ».
  3. Fix the `.a11y.role` cross-reference in `manifest-schema.md:37`.
  4. Update `harness/SKILL.md:136` and `adjust/actions/01-arbitrate.md:28` to the four-artifact contract — the second one changes behaviour, not only prose.
  5. Backfill the Lot 1 plan: check the boxes, record the six unplanned changes as amendments, write the Log.
  6. Separate the `sc-*` pivot chantier from `feat/design-2-0/lot-0-truth`, as its own plan requires, before committing either.
- **Additional notes**: the `success_condition` was re-executed in full for this review, not read from the plan. Migration round-trip, idempotence, backup, exit-code space (0/1/2/3) and the eight-fixture baseline all reproduce. The two "Corrigé" sections of the 2.0.0 CHANGELOG describe defects found and fixed outside any phase; both are of the class the master plan targets, and both are correctly recorded — they are listed as unplanned only because the plan document was never amended.
