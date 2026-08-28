# Harness — Routing autonomy Behavioural Test Scenarios

Behavioural tests for **design:harness**. Authority: `SKILL.md` §Routing and §Transversal rules; `actions/01-scaffold.md` §Process; `actions/02-contract-inline.md` §Process; `actions/03-normalize.md` §Process; `references/harness-contract.md`; `references/harness-normalization.md`.

> **Fixture / preconditions.** Use generator `adapters/harness/harness.py`, analyzer `tools/harness-analyze.mjs`, runtime checker `tools/harness-runtime-check.mjs`, contract fixtures `adapters/harness/fixtures/{1x,2x,2x-style-breakout,2x-no-stylesheet}/`, and the temporary normalization documents created by `tools/harness-selftest.sh`. Every output is a distinct temporary HTML path; source and contract checksums are recorded before the run.

## Scenarios

| # | Situation (input) | Expected behaviour | Pass criteria |
|---|---|---|---|
| S1 | Supply `/tmp/design-behave-scaffold.html` and pages `home,contact`, without a contract. | Select `scaffold`. | Intended writes contain exactly that HTML; contract reads/writes are `[]`; public exit is 0. |
| S2 | Supply the same valid pages and fixture `2x`. | Select `contract-inline`. | `adapters/tokens.css` is read and inlined; only output HTML is written; contract artifacts stay unchanged; exit is 0. |
| S3 | Supply page key `/contact/`. | Refuse the invalid slug. | Exit is 2 and the output HTML does not exist. |
| S4 | Supply fixture `1x`. | Refuse the unsupported contract. | Exit is 3 and no output is written. |
| S5 | Supply fixture `2x-style-breakout`. | Reject unsafe `</style>` content. | Exit is 2 and no output is written. |
| S6 | Supply fixture `2x-no-stylesheet`. | Generate with an explicit warning. | Exit is 0; one output HTML is written; warning names the absent stylesheet. |
| S7 | Ask to create the complete design system. | Do not activate `harness`. | No harness action or output path is planned. |
| S8 | Run `scaffold` from an unrelated working directory in Codex, with no plugin-root environment variable. | Resolve `DESIGN_PLUGIN_ROOT` from the loaded `harness/SKILL.md` path before invoking bundled tools. | Generator and runtime-check paths stay under the installed design plugin root; valid pages still exit 0 and write exactly the requested output HTML. |
| S9 | Supply a conventional single-page HTML document with page CSS and no application script. | Select `normalize`, classify it as `html-document`, regenerate the canonical shell, and migrate only author markup and CSS. | Source checksum is unchanged; the distinct output is `canonical-harness`, runtime-valid, and contains no nested document wrapper in `pageXxx()`. |
| S10 | Supply a harness whose end author-style marker is missing while its author content remains identifiable. | Select `normalize`, classify it as `repairable-harness`, and rebuild the shell instead of patching its controls. | Source checksum is unchanged; page content and eligible author CSS are retained; generated chrome, registries, and control scripts come from `harness.py`. |
| S11 | Supply a conventional HTML document whose external application script creates visible content. | Select `normalize` and stop at the decision gate. | Analyzer reports `readyWithoutDecision: false`; no output is written and the script is not copied into a control region. |
| S12 | Supply an already canonical runtime-valid harness and request normalization to a distinct output. | Select `normalize` and preserve the author-owned content exactly. | Page keys, metadata, page markup, and author styles are unchanged; analyzer and runtime checker remain green on the output. |
| S13 | Supply a harness page containing a business `<select>` and a page-local `<style>` outside `<head>`. | Analyze only harness-owned evidence. | Registry comparison reads options only inside `#page-select`; inline style count reads `<head>` only; the business values do not create drift. |
| S14 | Supply author CSS with `prefers-reduced-motion`, then with `max-width`. | Preserve the accessibility preference and reject the hidden viewport breakpoint. | The first remains `canonical-harness`; the second becomes `repairable-harness` with `viewport-media-query`. |
| S15 | Normalize a script-bearing reference in default snapshot mode. | Stop until freezing visible interactions is explicitly accepted, then inventory each as frozen/omitted. | No source script is copied; the report names the acceptance and every source interaction disposition; visual proof covers every page × viewport. |
| S16 | Explicitly request interactive normalization of an inventoried FAQ/menu behaviour. | Put only page-local bindings in `AUTHOR AFTER RENDER` and shared pure builders in `AUTHOR SHARED HELPERS`. | Runtime check and browser smoke both pass; each retained interaction is operable after changing pages; no application script is copied wholesale. |
| S17 | Rebuilt output exceeds twice the source size. | Gate completion until shared content is deduplicated or growth is explicitly accepted. | Analyzer run with `--baseline` reports `size-growth`, ratio, and `readyWithoutDecision: false`; the decision appears in the migration report. |
| S18 | A rebuilt file is structurally canonical and runtime-valid but lacks visual comparison or dependency/provenance resolution. | Report the dimensions independently and keep migration incomplete. | `formatConformant` and `runtimeValid` may be true while `migrationComplete` is not true and `visualFidelity` remains `unmeasured`; no fidelity/conformity claim is made. |

## How to run

Agent-as-harness plus the real analyzer, generator, and runtime checker in a temporary directory. Record selected action, stdout/stderr, exit code, source/output existence, source and contract checksums, analyzer classification, and the migration report.

**Decisive observables:** one output only; source and contract immutable; public exits 0/2/3; scripts never migrate silently; regenerated infrastructure comes from the canonical generator; author payload goes through `harness-apply.py`; format/runtime/migration/visual outcomes stay independent; unsafe or legacy inputs write nothing; unrelated lifecycle request excluded.

## Results log

### 2026-08-12 — run 1 (post-fix, dry-run, target=harness, fixture=harness-fixtures) — **7/7 PASS**

Fixture state: real `harness.py` run in isolated temp output; exits S1–S6 = 0/0/2/3/2/0; only successful cases produced one HTML.

| # | Behaviour | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|---|
| S1 | standalone scaffold | PASS | — | `actions/01-scaffold.md §Process` |
| S2 | contract stylesheet inline | PASS | — | `actions/02-contract-inline.md §Process` |
| S3 | invalid slug exit 2 | PASS | — | `references/harness-contract.md` |
| S4 | legacy exit 3 | PASS | — | `SKILL.md §Transversal rules` |
| S5 | style breakout exit 2 | PASS | — | `references/harness-contract.md` |
| S6 | absent stylesheet warning | PASS | — | `actions/02-contract-inline.md §Process` |
| S7 | lifecycle request excluded | PASS | — | `SKILL.md §Routing` |

**Frictions / gaps:** none; runtime selfchecks also pass for generated outputs.
**Tally:** 7/7 PASS (0 N/A) — first executable baseline.

### 2026-08-12 — run 2 (regression, dry-run, target=harness, fixture=harness-fixtures) — **7/7 PASS**

Fixture state: isolated `/tmp` runs return 0/0/2/3/2/0 for S1–S6; only success cases write one runtime-valid HTML.

| # | Behaviour | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|---|
| S1 | standalone scaffold | PASS | = | `actions/01-scaffold.md §Process,Test` |
| S2 | contract stylesheet inline | PASS | = | `actions/02-contract-inline.md §Process,Test` |
| S3 | invalid slug exit 2 | PASS | = | `references/harness-contract.md §Chemin pages` |
| S4 | legacy exit 3 | PASS | = | `references/harness-contract.md §Chemin contrat` |
| S5 | style breakout exit 2 | PASS | = | `actions/02-contract-inline.md §Test` |
| S6 | absent stylesheet warning | PASS | = | `references/harness-contract.md §Chemin contrat` |
| S7 | lifecycle request excluded | PASS | = | `SKILL.md §Routing` |

**Frictions / gaps:** none; fixtures unchanged and outputs confined to `/tmp`.
**Tally:** 7/7 PASS (0 N/A) — no PASS→FAIL regression.

### 2026-08-12 — run 3 (post-fix, dry-run, target=harness, fixture=harness-fixtures) — **8/8 PASS**

Fixture state: isolated runs preserve prior exits; S8 runs from `/tmp` with all root variables absent and resolves from the loaded skill path.

| # | Behaviour | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|---|
| S1 | standalone scaffold | PASS | = | `actions/01-scaffold.md §Process,Test` |
| S2 | contract stylesheet inline | PASS | = | `actions/02-contract-inline.md §Process,Test` |
| S3 | invalid slug exit 2 | PASS | = | `references/harness-contract.md §Chemin pages` |
| S4 | legacy exit 3 | PASS | = | `references/harness-contract.md §Chemin contrat` |
| S5 | style breakout exit 2 | PASS | = | `actions/02-contract-inline.md §Test` |
| S6 | absent stylesheet warning | PASS | = | `references/harness-contract.md §Chemin contrat` |
| S7 | lifecycle request excluded | PASS | = | `SKILL.md §Routing` |
| S8 | root resolution without host env | PASS | new | `host-portability.md §Root resolution`; `actions/01-scaffold.md §Process` |

**Frictions / gaps:** none; generated outputs confined to `/tmp`.
**Tally:** 8/8 PASS (0 N/A) — portable root resolution confirmed.

### 2026-08-28 — run 4 (post-fix, dry-run, target=harness, fixture=harness-normalization) — **12/12 PASS**

Fixture state: prior contract and page cases replayed; analyzer exercised against a generated canonical harness, a conventional document, a damaged harness, a script-bearing document, and an empty input. Analyzer exits are 0/0/0/0/2; runtime checker is green on the canonical result; all source fixtures and contract checksums remain unchanged.

| # | Behaviour | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|---|
| S1 | standalone scaffold | PASS | = | `actions/01-scaffold.md §Process,Test` |
| S2 | contract stylesheet inline | PASS | = | `actions/02-contract-inline.md §Process,Test` |
| S3 | invalid slug exit 2 | PASS | = | `references/harness-contract.md §Chemin pages` |
| S4 | legacy exit 3 | PASS | = | `references/harness-contract.md §Chemin contrat` |
| S5 | style breakout exit 2 | PASS | = | `actions/02-contract-inline.md §Test` |
| S6 | absent stylesheet warning | PASS | = | `references/harness-contract.md §Chemin contrat` |
| S7 | lifecycle request excluded | PASS | = | `SKILL.md §Routing` |
| S8 | root resolution without host env | PASS | = | `host-portability.md §Root resolution` |
| S9 | conventional HTML normalization | PASS | new | `actions/03-normalize.md §Process`; `harness-normalization.md §Ownership boundary` |
| S10 | damaged harness reconstruction | PASS | new | `actions/03-normalize.md §Process`; analyzer class `repairable-harness` |
| S11 | application-script decision gate | PASS | new | analyzer `readyWithoutDecision: false`; output absent |
| S12 | canonical input idempotence | PASS | new | `harness-normalization.md §Completion proof` |

**Frictions / gaps:** arbitrary application behaviour remains an explicit decision, never an automatic migration; visual conformity remains outside this action.
**Tally:** 12/12 PASS (0 N/A) — normalization boundary and reconstruction path confirmed.

### 2026-08-28 — run 5 (regression, dry-run, target=harness, fixture=jeveuxtravailler-harness) — **18/18 PASS**

Fixture state: populated 29-page reference `/home/tnn/MEGA/Projets/jeveuxtravailler/2026/08/jeveuxtravailler-harness.html`, inspected read-only. It contains business selects, visible FAQ/menu/icon/reveal behaviour, external Google Fonts, accessibility media queries, repeated shared content, and stale absolute Windows provenance. Deterministic fixtures in `harness-selftest.sh` replay analyzer and applicator edge cases without writing to the real fixture.

| # | Behaviour | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|---|
| S1 | standalone scaffold | PASS | = | `actions/01-scaffold.md §Process,Test` |
| S2 | frozen-contract inline | PASS | = | `actions/02-contract-inline.md §Process,Test` |
| S3 | invalid slug refusal | PASS | = | `harness-contract.md §Chemin pages` |
| S4 | legacy-contract refusal | PASS | = | `harness-contract.md §Chemin contrat` |
| S5 | style breakout refusal | PASS | = | `actions/02-contract-inline.md §Test` |
| S6 | missing stylesheet warning | PASS | = | `harness-contract.md §Chemin contrat` |
| S7 | lifecycle request excluded | PASS | = | `SKILL.md §Routing` |
| S8 | portable plugin-root resolution | PASS | = | `SKILL.md §Transversal rules` |
| S9 | conventional HTML normalization | PASS | = | `actions/03-normalize.md §Process` |
| S10 | damaged shell reconstruction | PASS | = | `harness-normalization.md §Ownership boundary` |
| S11 | application-script decision gate | PASS | = | `harness-normalization.md §Decisions that block` |
| S12 | canonical input preservation | PASS | = | `harness-normalization.md §Completion proof` |
| S13 | harness-owned analyzer scope | PASS | new | analyzer scopes `#page-select` and `<head>`; deterministic counter-fixture green |
| S14 | preference query allowed, viewport query rejected | PASS | new | `harness-contract.md §Trois échantillons`; both counter-fixtures green |
| S15 | snapshot interaction acceptance | PASS | new | `harness-normalization.md §Modes`; default does not silently freeze behaviour |
| S16 | governed interactive migration | PASS | new | author hooks in generated shell; runtime proof green; browser smoke required by action |
| S17 | output-growth decision gate | PASS | new | analyzer `--baseline` emits `size-growth` and blocker above 2× |
| S18 | independent outcome dimensions | PASS | new | analyzer schema 2 reports format/runtime/migration/visual separately |

**Frictions / gaps:** pixel-diff production depends on the host browser capability and remains workflow evidence rather than a stdlib analyzer feature; this is explicit and cannot be mistaken for format conformance.
**Tally:** 18/18 PASS (0 N/A) — no PASS→FAIL regression; six real-fixture failure modes are now pinned.

### 2026-08-28 — run 6 (generality, dry-run, target=harness, fixture=jeveuxtravailler-interactive-v2) — **18/18 PASS**

Fixture state: the same 29-page source was rebuilt through a fresh generated shell and the deterministic applicator in interactive mode. The first flattened counter-run reached 2.58 MB of markup and was stopped by the 2× gate; the `pageBodies` rerun preserved shared layout and produced 328,566 bytes versus 332,166 bytes. Chromium exercised 29 pages × 3 viewports: 87/87 pixel-exact comparisons, zero output errors and zero interaction-smoke failures. Source file remained read-only.

| # | Behaviour | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|---|
| S1 | standalone scaffold | PASS | = | generator exit 0 |
| S2 | frozen-contract inline | PASS | = | unchanged contract branch |
| S3 | invalid slug refusal | PASS | = | selftest counter-fixture |
| S4 | legacy-contract refusal | PASS | = | selftest counter-fixture |
| S5 | style breakout refusal | PASS | = | selftest counter-fixture |
| S6 | missing stylesheet warning | PASS | = | selftest counter-fixture |
| S7 | lifecycle request excluded | PASS | = | `SKILL.md §Routing` |
| S8 | portable plugin-root resolution | PASS | = | installed root used explicitly |
| S9 | conventional HTML normalization | PASS | = | fresh shell plus applicator path |
| S10 | damaged shell reconstruction | PASS | = | generated chrome replaced source controls |
| S11 | application-script decision gate | PASS | = | interactions inventoried before write |
| S12 | canonical input preservation | PASS | = | source checksum unchanged |
| S13 | harness-owned analyzer scope | PASS | = | 29 registry options despite business selects; 2 source head styles |
| S14 | preference query policy | PASS | = | two reduced-motion queries retained; no viewport query |
| S15 | snapshot acceptance gate | PASS | = | interactive chosen explicitly instead of silent freeze |
| S16 | governed interactive migration | PASS | = | FAQ, drawer, icons, reveal and universe checks green in 87 states |
| S17 | output-growth decision gate | PASS | = | flattened run blocked; `pageBodies` rerun ratio 0.989 |
| S18 | independent outcome dimensions | PASS | = | format/runtime green; token provenance remains explicit blocker |

**Frictions / gaps:** Google Fonts is an accepted external dependency and is now detected even through `@import`; the preserved token snapshot has source checksum provenance but no frozen design contract, so migration completeness remains deliberately unset.
**Tally:** 18/18 PASS (0 N/A) — no PASS→FAIL regression; the real interactive migration closes the size and fidelity failures without hiding the remaining provenance gap.
