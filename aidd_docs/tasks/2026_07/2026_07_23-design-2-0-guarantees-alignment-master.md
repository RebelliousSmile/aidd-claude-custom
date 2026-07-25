---
name: master_plan
description: Parent plan orchestrating the design plugin 2.0 chantier - align guarantees with promises
argument-hint: N/A
---

# Master Plan: design 2.0 - align guarantees with promises

## Overview

- **Goal**: every normative statement of the `design` plugin has an implemented consumer; the contract carries its own version identity; generated artifacts are reproducible; unenforceable rules are declared instead of implied; and the funnel states, from inside, which sequence applies to which case.
- **Risk Score**: 11 (breaking public API +3, contract schema migration +3, 5+ modules +3, major refactoring +2)
- **Branch**: `feat/design-2-0/`

## Problem statement

Four distinct gaps, all verified on disk:

1. **Doc to code**: `skills/adjust/references/manifest-schema.md` documents background rules, a11y rules, layer-concordance checks and per-theme WCAG contrast as `enforce` behaviour. `skills/enforce/adapters/lint-core.mjs` implements five rules, none of them these. The `.lintrc.json` template in `skills/enforce/actions/01-build-linter.md` declares severities (`a11yRole`, `backgroundMismatch`) for rules that are never emitted.
2. **Word to guarantee**: "vocabulaire ferme" names an open-by-default scanner (`lint-core.mjs` line 152, `if (!strict) continue;`); "fige" names a contract whose a11y was never verified; "generated" names non-reproducible LLM output.
3. **Surface**: the gate sees one markup file at a time. CSS, theme.json, database-stored content and adapters are out of scope by construction, yet the plugin presents `lint-core.mjs` as the system gate.
4. **Entry point**: six verbs, no map. Which verb applies to which entry signature, in which order, under which gate, and where a platform takes over is knowledge held outside the plugin. A consumer either knows the funnel or reads six `SKILL.md` to reconstruct it.

## Structuring decision

Assumed breaking change: the monolithic contract is split into four artifacts plus a tooled migration. MAJOR bump, and migration of every frozen 1.x contract.

## Child Plans

| #   | Plan                          | Lot   | Version  | File            | Status  | Validated |
| --- | ----------------------------- | ----- | -------- | --------------- | ------- | --------- |
| 1   | Truth of the discourse        | Lot 0 | 1.17.0   | `./2026_07_23-design-2-0-guarantees-alignment-part-1.md` | done | [x] |
| 2   | Split contract, version identity | Lot 1 | 2.0.0 | `./2026_07_23-design-2-0-guarantees-alignment-part-2.md` | done | [x] |
| 2.5 | Sweep the exception paths     | Lot 1.5 | 2.0.1  | `./2026_07_23-design-2-0-guarantees-alignment-part-2-5.md` | done | [x] |
| 3   | Deterministic generation      | Lot 2 | 2.1.0    | `./2026_07_23-design-2-0-guarantees-alignment-part-3.md` | done | [x] |
| 4   | Distributed enforcement       | Lot 3 | 2.2.0    | `./2026_07_23-design-2-0-guarantees-alignment-part-4.md` | done | [x] |
| 5   | Mandatory oracle, structured ledger | Lot 4 | 2.3.0 | `./2026_07_23-design-2-0-guarantees-alignment-part-5.md` | done | [x] |
| 6   | Maturity at freeze            | Lot 5 | 2.4.0    | `./2026_07_23-design-2-0-guarantees-alignment-part-6.md` | done | [x] |
| 7   | Migration of frozen contracts | ops   | unchanged | `./2026_07_23-design-2-0-guarantees-alignment-part-7.md` | done | [x] |
| 8   | Verb 0 `detail`, map and workflow router | Lot 6 | 2.5.0 | `./2026_07_23-design-2-0-guarantees-alignment-part-8.md` | done | [x] |

<!-- Status values: pending, in-progress, done, blocked -->
<!-- RULE: Plan N+1 blocked until Plan N checkbox checked -->

Sequence is strictly linear: 1 -> 2 -> 2.5 -> 3 -> 4 -> 5 -> 6 -> 7. No parallel execution.

Plan 2.5 is a hardening lot inserted after Lot 1 shipped. It takes a PATCH (2.0.1) and no version downstream moves. It closes a defect class Lot 1 fixed in two instances without sweeping: a structurally invalid artifact exits 1, or worse produces a green verdict on a silently mis-derived set. It carries no feature and opens no window; plan 3 is blocked on its checkbox like any other.

Plan 8 is the single exception to that linearity: it shares no artifact with plan 7, so it unblocks on plan 6 and may run before, after, or between the project migrations. It cannot run earlier — it describes the 2.x state.

Part 1 is deliverable alone: it ships as 1.17.0 and is valuable even if the rest is never executed.

## Transverse acceptance criterion (all eight plans)

Skills are written exhaustive, stack-agnostic, and as concise as possible: best coverage, fewest words.

- **Perimeter of the criterion**: every file under `plugins/design/` and under the three `sc-*` pivots, with exactly three exemptions, `CHANGELOG.md`, `plugins/design/audits/`, and the ADR files under `aidd_docs/internal/decisions/`. The three exemptions share one property: they are dated records of a past state, not instructions read at run time. The perimeter is stated as a directory rule, never as a list of file kinds, so `agents/`, `adapters/`, `evals/` and `fixtures/` are covered by construction.
- No project name appears anywhere in that perimeter, including in a code comment or a docstring. Project names are allowed in plans, CHANGELOG, audits and ADR only.
- **Stack-specific material is relocated, not rewritten.** A file whose subject is one platform does not belong under `plugins/design/`; it moves to the pivot that owns that platform. Relocation is assigned to Lot 3, which already opens the three pivots.
- **The criterion binds identifiers, not only prose.** A CLI flag value, a JSON key, a report field and a function name are read at run time and are inside the perimeter. `--side wp` names a platform as surely as a sentence does, and an abbreviation in a language other than the surrounding code (`maq`) is a second ambiguity on top. Public API surfaces are named by role, never by the platform or project that first motivated them.
- Degenerate inputs are written as classes of case (`layer 3 absent`, `artifact versions skewed`, `mode undeclared`), never as named projects.
- No rule, example or schema presupposes a specific stack. Stack specifics live in the `sc-*` pivots and in the per-project adapter map.
- No defensive prose, no narrative justification inside an instruction body, no duplication between a `SKILL.md` and its actions. Rationale goes to CHANGELOG or ADR. DRY through `${CLAUDE_PLUGIN_ROOT}/references/`.
- Concision does not mean gaps: every field, rule and status stays covered. Density rises, perimeter does not fall.

## Cross-cutting definitions

**Fixture enumeration.** Wherever a plan pins the exit-code baseline `0 1 0 1 0 1 0 1`, the eight fixtures are enumerated in this order, which is the ascending lexicographic order of their file names under `plugins/design/skills/enforce/fixtures/`:

`clean.html · dirty.html · retrofit-clean.html · retrofit-dirty.html · themed-clean.html · themed-dirty.html · utility-clean.html · utility-dirty.html`

**Exit-code space.** Fixed once here; no lot may reassign a code.

The table binds every tool the plugin ships, not a subset: `lint-core.mjs`, `run-gates.py`, `generate.py`, `migrate-contract.py`, `status.py`, `measure.py`, `config-gen.py`. No plan may write "exits non-zero" where one of these codes applies.

| Code | Meaning | Emitter |
| ---- | ------- | ------- |
| 0 | No violation, or the requested operation succeeded | every tool |
| 1 | At least one violation, or a drift detected | `lint-core.mjs`, `run-gates.py`, `generate.py --check` |
| 2 | Invocation or environment error: missing, unreadable or unusable argument; required runtime absent; a required decision the tool refuses to guess | every tool |
| 3 | Contract in 1.x format, migration required | `lint-core.mjs` (Lot 1), `run-gates.py` (Lot 3) |
| 4 | Contract below the conformity threshold, conformity not asserted, violations still reported | `run-gates.py` (Lot 5) |

Code 2 keeps and widens its pre-existing meaning; the 1.x diagnosis takes 3 so that a malformed invocation can never be read as an unmigrated contract. Three refusals therefore exit 2 and not something else: an undeclared `mode` with no `--mode` passed, a `measure.py` call with no `--ledger-registry`, and a `run-gates.py` run finding no Node runtime.

**Invocation shape.** `--contract` carries the contract directory as its value in every tool that accepts it, never a bare mode flag: `--contract <dir>`. Passes are selected by their own flag, `--contract` naming what they operate on. A plan writing an invocation writes it runnable, with every path supplied.

`lint-core.mjs` predates the rule and shipped the contract directory as a second positional. It now accepts both: `--contract <dir>` is the form every documented invocation uses, the positional keeps working so the pre-commit hooks already installed in consuming projects run unmodified, and supplying both with divergent values exits 2. No other tool takes a positional contract directory.

**Breaking window.** Lot 1 opens a single migration window that Part 7 closes. Inside it, lots 2 to 5 may change a shipped CLI in an incompatible way — a required argument added, a flag value renamed, a sample file removed — while carrying a MINOR bump, because no consumer is expected to settle on an intermediate 2.x. Each such change is named in its own CHANGELOG entry under a Breaking heading. Outside the window the ordinary SemVer rule of `CONTRIBUTING.md` applies unchanged.

## Cross-cutting decisions

- **Migration perimeter**: six frozen 1.x contracts, not two. `migrate-contract.py` accepts degenerate inputs and refuses to guess a `mode`.
- **Initial maturity status**: `normalized`, no grandfathering. A migrated contract has never been verified on contrast or states. A contract with layer 3 absent starts lower.
- **Adapter names**: no normalization. A correspondence table in `policies.json`, derived by the migration script from the adapters actually present, declares artifact and real consumer for each. The hash drift gate reads that table.
- **Aggregation runner language**: Python, aligned with the rest of the tooling. Consequence, to be stated explicitly in Lot 3 and in `references/gate-wiring.md`: Python becomes a pre-commit prerequisite on every consuming project, including pure-JS ones. `lint-core.mjs` stays Node and is invoked by the Python runner.
- **1.x/2.0 breakage window**: Lot 1 removes the 1.x read path. `lint-core.mjs` detects a 1.x contract by the absence of `release.json` and exits 3 with the migration command. No degraded read, no dual path.
- **Maturity status lifecycle**: one implementation, extended twice, never duplicated. `tools/status.py` ships at Lot 1 and computes from the facts a migration can observe: charter layer present or absent, checks run or not run. Lot 5 extends the same tool with the contrast and declarative-state inputs, and makes the result opposable. No lot recomputes a status outside `status.py`.
- **Ledger split placement**: the structured deviation source and its generated Markdown view both belong to Lot 4. Lot 2 generates the token stylesheet, the platform theme file and the stack adapters only — it cannot generate a view whose source does not exist yet.
- **Out of scope**: strict DTCG rewrite of the token schema; rework of the design / sc-* pivot boundary (DEC-002 kept as is); automatic migration of consumer project source beyond the contract script.

## Validation Protocol

1. Complete Plan 1, run its `success_condition`
2. [x] Checkpoint 1: user confirms, 1.17.0 published
3. Unblock Plan 2, repeat through Plan 6
4. [ ] Checkpoint 6: 2.4.0 published, fixtures green
5. Unblock Plan 7, one human validation per project migrated
6. Unblock Plan 8 as soon as Plan 6 is validated, independently of Plan 7
7. [x] Final: every frozen contract reads under 2.x, no contract left in 1.x (all six carry `release.json`, linter can no longer exit 3), and the funnel carries its own map (`detail` verb, 2.5.0)

## Estimations

- **Confidence**: 9/10
- **Duration**: 8 work units, 7 of them sequential; Lot 1 and Lot 2 carry most of the effort
