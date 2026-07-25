---
name: plan
description: Lot 4 - the fidelity gate requires the per-property oracle; deviations become a structured source with status and expiry; a tolerated exception must reference an existing deviation with its expected value.
argument-hint: N/A
objective: "Conformity is asserted from the per-property oracle only, and every tolerated exception references an existing deviation entry carrying its expected value."
success_condition: "Prerequisite, since measure.py drives a real browser: Playwright and its Chromium are installed, and the two oracle fixtures each ship a self-contained local HTML page served over file:// or a local static server, so no network is involved. Then, with FCONF=plugins/design/skills/enforce/fixtures/oracle/conformant and FUNK=plugins/design/skills/enforce/fixtures/oracle/unknown-deviation: python plugins/design/adapters/measure/measure.py --config $FCONF/measure.config.json --ledger-registry $FCONF/deviations.json --out <tmp>/conformant.json writes a report whose jq -r .summary.verdict equals CLOSED AND python plugins/design/adapters/measure/measure.py --config $FUNK/measure.config.json --ledger-registry $FUNK/deviations.json --out <tmp>/unknown.json writes a report whose jq -r .summary.verdict equals OPEN AND invoking measure.py without --ledger-registry exits 2 with a message naming that argument, instead of measuring AND grep -rniE '\bwp\b|_in_wp|\bmaq\b' plugins/design/adapters/measure/measure.py plugins/design/adapters/measure/config-gen.py returns nothing AND python plugins/design/tools/migrate-contract.py --ledger $FLED --dry-run, with FLED=plugins/design/skills/enforce/fixtures/oracle/ledger-1x, prints one report line per identifier found in the Markdown source, with no identifier missing AND running python plugins/design/tools/generate.py twice over deviations.json produces byte-identical Markdown ledger views (diff exits 0) AND jq -r .version plugins/design/.claude-plugin/plugin.json equals 2.3.0 and matches .claude-plugin/marketplace.json and index.json"
iteration: 0
created_at: "2026-07-23T21:00:57Z"
---

# Instruction: Lot 4 - mandatory oracle, structured ledger

## Feature

- **Summary**: the fidelity gate stops accepting a global pixel comparison as proof. It requires the per-property oracle wired. A global pixel diff remains allowed as a coarse detector. Deviations become a structured source: identifier, status, oracle target, expected value, date, optional expiry. Both the structured source and its Markdown view land here: the Lot 2 generator is extended with a fourth artifact, since the source it derives from does not exist before this lot. An exception tolerated by the oracle must reference an existing deviation carrying its expected value, otherwise the run fails instead of tolerating. Active deviations and historical decisions are separated.
- **Stack**: `Markdown (Claude Code skills) · Python 3.11+ (measure, config-gen, migrate-contract, generate) · Playwright with Chromium, required by measure.py only · JSON contract artifacts`
- **Branch name**: `feat/design-2-0/lot-4-oracle`
- **Parent Plan**: `2026_07_23-design-2-0-guarantees-alignment-master.md`
- **Sequence**: `5 of 7`
- Confidence: 9/10
- Time to implement: 2 work units

## Architecture projection

### Files to modify

- `plugins/design/skills/enforce/actions/05-fidelity-gate.md` - require the per-property oracle; demote the global pixel diff to a coarse detector
- `plugins/design/adapters/measure/measure.py` - `--ledger-registry` becomes required instead of optional, so an exception can never be honoured without a registry to validate it against; read `deviations.json` instead of the Markdown ledger; honour status and expiry; rename the platform-named API surface by role, `--side wp|maq` becoming `--side implementation|mockup` and every `*_in_wp` report field becoming `*_in_implementation`, which also removes the French abbreviation from an otherwise English tool
- `plugins/design/adapters/measure/config-gen.py` - read `oracle.json` instead of the oracle hints previously embedded in the component file; carry the same renaming, the two tools sharing one vocabulary
- `plugins/design/references/visual-diff-procedure.md` - the pixel diff is a detector, never a proof of conformity
- `plugins/design/references/deviation-ledger-template.md` - the generated view of the structured source
- `plugins/design/tools/migrate-contract.py` - add the `--ledger` pass, idempotent and replayable
- `plugins/design/tools/generate.py` - the Markdown ledger view derives from `deviations.json`
- `plugins/design/references/contract-schema.md` - reference `deviations.json` from the release root
- `plugins/design/skills/enforce/evals/scenarios.json` - scenario covering the oracle requirement
- `plugins/design/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `index.json`, `README.md`, `plugins/design/README.md`, `plugins/design/CHANGELOG.md` - 2.3.0
- `aidd_docs/memory/design-plugin.md` - oracle and ledger topology

### Files to create

- `plugins/design/references/deviations-schema.md` - identifier, status, oracle target, expected value, date, optional expiry, separation of active and historical entries
- `plugins/design/adapters/measure/configs/example.json` - the stack-agnostic sample configuration: generic local address, generic selectors, generic documentation string
- `plugins/design/skills/enforce/fixtures/oracle/conformant/` - contract, `deviations.json`, `measure.config.json` and a self-contained local HTML page whose rendered properties match the contract, producing a CLOSED verdict
- `plugins/design/skills/enforce/fixtures/oracle/unknown-deviation/` - same shape, with a page that diverges on one property and an exception referencing an identifier absent from `deviations.json`, producing an OPEN verdict
- `plugins/design/skills/enforce/fixtures/oracle/ledger-1x/` - a Markdown ledger for the `--ledger` migration pass

### Files to delete

- `plugins/design/adapters/measure/configs/mentions-legales.json` - the only shipped sample configuration, carrying a project-specific page name and a project address. It is deleted, not neutralized in place; `example.json` replaces it.

## Applicable rules

| Tool   | Name                  | Path                                                    | Why it applies |
| ------ | --------------------- | ------------------------------------------------------- | -------------- |
| repo   | contributing          | `CONTRIBUTING.md`                                        | MINOR bump in three places, CHANGELOG, verifiable Test per action |
| repo   | guideline-readme      | `memory/guideline-readme.md`                             | both READMEs restate what proves conformity |
| repo   | dec-002               | `aidd_docs/internal/decisions/002-design-funnel-hybrid-pivot.md` | the oracle is a WHAT-side instrument; rendering stays with the pivots |
| claude | global-conventions    | `C:\Users\fxgui\.claude\CLAUDE.md`                       | rtk prefix, no commit without explicit request |
| claude | plugins-marketplace   | `C:\Users\fxgui\.claude\rules\plugins-marketplace.md`    | edit the source, never the runtime cache |

## User Journey

```mermaid
---
title: Lot 4 - a divergence is either a violation or a referenced deviation
---
flowchart TD
  Run["Fidelity gate runs"]
  Wired{"Per-property oracle wired"}
  Refuse["Refuse to assert conformity"]
  Measure["Measure per property"]
  Diff{"Divergence found"}
  Closed["Verdict closed"]
  Ack{"Exception references a deviation id"}
  Known{"Id exists with an expected value"}
  Expired{"Deviation active and not expired"}
  Tolerated["Divergence tolerated, traced"]
  Open["Verdict open"]
  Pixel["Global pixel diff"]
  Detector["Coarse detector only, never a proof"]

  Run --> Wired
  Wired -- no --> Refuse
  Wired -- yes --> Measure
  Measure --> Diff
  Diff -- no --> Closed
  Diff -- yes --> Ack
  Ack -- no --> Open
  Ack -- yes --> Known
  Known -- no --> Open
  Known -- yes --> Expired
  Expired -- no --> Open
  Expired -- yes --> Tolerated
  Pixel -.-> Detector
```

## Risk register

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| Making the oracle mandatory blocks projects that never wired it | the gate becomes unrunnable | the gate refuses to assert conformity rather than failing the build; the refusal names the wiring step |
| The Markdown ledger loses entries during migration | a sanctioned deviation silently becomes a violation | the `--ledger` pass reports one entry per identifier, and the dry-run report is validated before writing |
| Expiry turns into silent tolerance | an expired deviation keeps passing | expiry is evaluated at run time and an expired entry produces an open verdict |
| The pixel diff keeps being used as proof | the coarse detector reasserts itself as the gate | the procedure reference states the demotion, and the gate asserts closure only from the per-property verdict |
| The shipped sample measurement configuration carries a project name and address | the plugin stops being agnostic | the file is deleted and replaced by a generic `example.json`; the substitution happens here rather than at Lot 0 because this lot rewrites the configuration format anyway |
| The oracle fixtures depend on a network or on a project page | the success condition stops being reproducible | each fixture ships its own self-contained HTML page, loaded locally, with no external asset |
| Historical and active entries stay mixed | the source cannot be read as a state | the schema separates them, and only active entries can sanction a divergence |
| Renaming the oracle API breaks existing callers | a wired project loses its fidelity gate | the rename happens inside the migration window the master opens at Lot 1, is announced under a Breaking heading in the CHANGELOG, and is executed in one pass covering the tools, the configuration, the fixtures and every caller, so no half-renamed state ships |

## Implementation phases

### Phase 1: Specify the structured deviation source

> A deviation is data before it is prose.

#### Tasks

1. Write `deviations-schema.md`: identifier, status, oracle target, expected value, date, optional expiry.
2. Separate active entries from historical decisions.
3. Reference `deviations.json` from the release root in `contract-schema.md`.

#### Acceptance criteria

- [x] Every field of the existing Markdown entry format maps to a schema field.
- [x] Active and historical entries are distinct in the schema.
- [x] Only an active entry can sanction a divergence.

### Phase 2: Ledger migration pass

> Existing sanctions survive the format change.

#### Tasks

1. Add the `--ledger` pass to `migrate-contract.py`, independent from the `--contract` pass.
2. Parse the Markdown ledger and emit `deviations.json`.
3. Report one line per identifier in dry-run, with anomalies for entries that cannot be mapped.
4. Make the pass idempotent and replayable.
5. Add the Markdown ledger fixture.

#### Acceptance criteria

- [x] The dry-run report accounts for every identifier present in the source.
- [x] A second run produces no diff.
- [x] An unmappable entry is reported, never dropped.

### Phase 3: Oracle sources and generated view

> The oracle reads its own artifact; the Markdown view is produced.

#### Tasks

1. Point `config-gen.py` at `oracle.json`.
2. Make `--ledger-registry` a required argument of `measure.py` and point it at `deviations.json`. Omitting it exits 2, the code the master assigns to a missing argument.
3. Honour status and expiry when validating an exception.
4. Set `summary.verdict` to `OPEN` when an exception references an unknown identifier or an entry without an expected value.
5. Extend `generate.py` with the Markdown ledger view derived from `deviations.json`, appended to the artifact set specified at Lot 2 without altering the three artifacts already emitted there.
6. Requalify `deviation-ledger-template.md` as the output template of that view.
7. Build the two oracle fixtures, each with its own self-contained local HTML page.
8. Rename the platform-named API of `measure.py` and `config-gen.py` by role: the two comparison sides become `implementation` and `mockup`, and every report field built on the old names follows. Update the shipped configuration, the fixtures and every caller in the same pass, so no file keeps the old vocabulary.

#### Acceptance criteria

- [x] The conformant fixture report reads `summary.verdict` equal to `CLOSED`.
- [x] The unknown-deviation fixture report reads `summary.verdict` equal to `OPEN`.
- [x] A fixture whose referenced entry is expired reads `summary.verdict` equal to `OPEN`.
- [x] Omitting `--ledger-registry` exits 2 naming the argument, and measures nothing.
- [x] Two consecutive generations of the Markdown view are byte-identical.
- [x] The Lot 2 drift check still passes on the three artifacts it already covered.
- [x] `grep -rniE '\bwp\b|_in_wp|\bmaq\b' plugins/design/adapters/measure/measure.py plugins/design/adapters/measure/config-gen.py` returns nothing, and the same grep over `plugins/design/` returns matches only in `CHANGELOG.md` and under `audits/`.
- [x] Every caller of the renamed arguments, in the actions, the references and the fixtures, uses the new names; none uses both.

### Phase 4: Gate semantics

> Proof comes from the oracle; the pixel diff only points.

#### Tasks

1. Rewrite `05-fidelity-gate.md` to require the wired per-property oracle before asserting conformity.
2. State that closure is asserted from the per-property verdict only.
3. Rewrite `visual-diff-procedure.md` to present the pixel diff as a coarse detector.
4. Delete `configs/mentions-legales.json` and create `configs/example.json` in its place: generic local address, generic selectors, generic documentation string.
5. Update the eval scenario.

#### Acceptance criteria

- [x] No document presents a global pixel comparison as proof of conformity.
- [x] The gate refuses to assert conformity when the oracle is not wired, and names the wiring step.
- [x] `plugins/design/adapters/measure/configs/` contains `example.json` and no other file.
- [x] `example.json` contains no project name, no external address and no stack-specific selector.

### Phase 5: Version and release

#### Tasks

1. Set 2.3.0 in the three version registers.
2. Write the CHANGELOG entry covering the ledger format change and the oracle requirement, with a Breaking heading listing the three incompatible changes this lot ships: `--ledger-registry` becoming required, the `--side` values renamed, and the sample configuration replaced.
3. Update both READMEs and `aidd_docs/memory/design-plugin.md`.

#### Acceptance criteria

- [x] The three version registers agree on 2.3.0.
- [x] The CHANGELOG carries a Breaking heading naming the three incompatible changes.

### Phase 6: Transverse writing criterion

> Exhaustive, agnostic, fewest words.

#### Acceptance criteria

- [x] No project name appears in the schema, the fixtures, the sample configuration or the gate action.
- [x] No stack is presupposed by the oracle documents.
- [x] Every field of the previous Markdown format is still covered after compression.
- [x] No duplication between `05-fidelity-gate.md`, `visual-diff-procedure.md` and `deviations-schema.md`.

## Amendments

- **`generate.py` généralisé par rôle, pas seulement étendu.** Le plan (Phase 3 §5) demandait « d'ajouter » la vue ledger. L'implémentation a exigé un changement structurel : `generate.py` codait `tokens.json` comme source unique de tout émetteur. Ajout de `source_for(role)` (rôle `deviation ledger` → `deviations.json`, tous les autres → `tokens.json`) et d'un cache de sources dans `produce()`, sans toucher les trois émetteurs de tokens (drift-check Lot 2 resté vert). Sans cela, la vue aurait dérivé du mauvais artefact.
- **`screenshot.py` renommé au-delà du gate grep.** Le gate strict ne scanne que `measure.py`+`config-gen.py`, et `screenshot.py` ne le déclenchait pas (occurrences collées à `_`). Mais il pilotait `maq_viewport` quand `config-gen.py` émet `mockup_viewport` — un décalage silencieux de viewport SPA. Renommé pour un vocabulaire unique, hors périmètre strict du gate mais dans l'intention de la Phase 3 §8 (« every caller … uses the new names »).
- **`copycat-checklist-schema.md` génériqué.** Résidu Phase 6 non listé dans les fichiers à modifier : un exemple de schéma portait `"page": "mentions-legales"` / `out/mentions-legales.json`. Remplacé par `pricing` — un nom de projet dans un schéma viole le critère d'agnosticité.

## Log

- Phase 1 — schéma `deviations.json` : `active`/`historical` distincts, seul `active` sanctionne, chaque champ du format Markdown a une correspondance. `references/deviations-schema.md`.
- Phase 2 — passe `--ledger` de `migrate-contract.py` : dry-run rend une ligne par identifiant (DEV-001/002/003), anomalie signalée pour l'entrée sans `expected` (DEV-003), jamais silencieuse. Idempotente.
- Phase 3 — `--ledger-registry` requis (absence → exit 2) ; statut+expiry honorés ; verdict `OPEN` sur id inconnu ou sans `expected` ; vue ledger dans `generate.py` (rôle `deviation ledger`, source `deviations.json`) octet-identique ; template requalifié en sortie ; deux fixtures oracle autoportantes (HTML local `file://`) ; renommage `maq|wp` → `mockup|implementation` propagé à tous les appelants.
- Phase 4 — `05-fidelity-gate.md` réécrit (oracle câblé requis, refus nommé, diff pixel = détecteur jamais preuve) ; `visual-diff-procedure.md` réécrit ; `mentions-legales.json` supprimée, `example.json` générique créée ; scénario d'éval ajouté (2 prompts).
- Phase 5 — 2.3.0 dans les trois registres ; CHANGELOG avec en-tête Breaking nommant les trois incompatibilités ; deux READMEs (contrat = cinq artefacts, topologie registre) et `design-plugin.md` (section Lot 4 + péremption des alias 2.1.0) mis à jour.
- Phase 6 — aucun nom de projet dans schéma/fixtures/example/gate (résidu `copycat-checklist-schema.md` corrigé) ; aucun stack présupposé par les docs oracle ; format Markdown intégralement couvert ; pas de duplication entre les trois références (renvois croisés).

## Validation flow demonstration

Exécutée avec le venv `adapters/measure/.venv`, `FCONF=skills/enforce/fixtures/oracle/conformant`, `FUNK=skills/enforce/fixtures/oracle/unknown-deviation`, `FLED=skills/enforce/fixtures/oracle/ledger-1x`. `jq` indisponible → verdicts extraits en Python.

| # | Étape | Commande | Résultat mesuré |
|---|-------|----------|-----------------|
| 1 | Migration ledger dry-run, une ligne par identifiant | `migrate-contract.py --ledger $FLED --dry-run` | ENTRIES 3 · DEV-001/002/003 listés · DEV-003 anomalie (pas d'`expected`) · exit 0 ✓ |
| 2 | Source structurée, seconde passe sans diff | `generate.py` ×2 sur `ledger-view` puis `diff -r` | diff exit 0 (octet-identique) ✓ |
| 3 | Conformant → `CLOSED` | `measure.py --config $FCONF/… --ledger-registry $FCONF/deviations.json` | `summary.verdict = CLOSED`, exit 0 ✓ |
| 4 | Exception vers id inconnu → `OPEN` | `measure.py --config $FUNK/… --ledger-registry $FUNK/deviations.json` | `OPEN — ledger id DEV-999 absent des écarts actifs` ✓ |
| 5 | Entrée expirée → `OPEN` | registre dérivé, `DEV-001.expires=2020-01-01` | `OPEN — ledger id DEV-001 expiré le 2020-01-01` ✓ |
| 6 | Sans `--ledger-registry` → refus, pas de mesure | `measure.py --config $FCONF/… --out …` | exit 2, `error: the following arguments are required: --ledger-registry`, rien mesuré ✓ |
| 7 | Vue Markdown générée deux fois, octet-identique | `generate.py` ×2 → `diff -r` | diff exit 0 ✓ |
| 8 | Trois registres à 2.3.0 | lecture `plugin.json`/`marketplace.json`/`index.json` | 2.3.0 · 2.3.0 · 2.3.0 ✓ |

Gate grep confirmé : `grep -rniE '\bwp\b|_in_wp|\bmaq\b'` sur `measure.py`+`config-gen.py` → aucun match (exit 1) ; le même scan sur `plugins/design/` ne matche que `CHANGELOG.md` et `audits/`. Drift-check Lot 2 sur le contrat de base et sur `ledger-view` → exit 0 (pas de dérive). L'usage de `measure.py` affiche `--side {mockup,implementation}` (renommage effectif).
