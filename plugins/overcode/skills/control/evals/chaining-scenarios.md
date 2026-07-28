# Control — Routing Graph, Chaining Contract & Halting Cases Behavioural Test Scenarios

<!--
One suite = one durable regression spec for ONE aspect of ONE target.
This suite pins the GRAPH and the CONTRACT that travels along its edges: who
routes, who may not launch, who recomputes nothing, which edges do not exist,
and the cases where an action must stop rather than produce a ranking.
It does NOT test what a phase or a domain is (phase/domains-scenarios), nor
whether a batch may be confirmed at once (confirmations-scenarios).
-->

Behavioural tests for **overcode:control** (`plugins/overcode/skills/control/SKILL.md`, all six actions) — verifies the routing graph and the contract carried by each edge. The decisive properties: `05-stats` is the entry point, routes, and **launches nothing**; no state survives between two runs; **the one who names hands over, the one who receives does not recompute**; `01-write` is the sink and every confirmed gap crosses it **one at a time, the number constraint re-evaluated between each**; `02-audit` has **no edge** to `01-write`; `03-configure` is reachable and terminal; `scope` + `domain` together halts; no test file found → no ranking at all; and saturation is answered with a narrower `scope`, **never with a `domain`**.

This suite is **distinct** from:
- `phase-scenarios.md` — `03-configure` taking none of the three parameters (there: as a parameter rule; here: as a graph position).
- `confirmations-scenarios.md` — whether an act may be confirmed as a batch.
- `measurement-scenarios.md` — the degenerate measurement cases and their order.
- **this file** — which edges exist, what travels along them, and where a run stops.

> **Fixture / preconditions.** Run against a **populated** Python repo, **READ-ONLY**.
>
> **No double, of any kind.** No mocked filesystem, no mocked coverage report, no synthesised project tree, no fixture `testing.md`, no stand-in for `aidd-dev:06-test`. The first real read of a real repository is the test — a suite that passes against a double proves the double.
>
> Reference fixtures:
> - **`app`** — `C:\Users\fxgui\Documents\Perso\Projects\suddenly\_code\app`. 80 test files; `.coverage` present; gate `make check`; document `aidd_docs/memory/TESTING.md`. Large enough that `04-strengthen` with `top_n=5` plausibly saturates — that is the S9 material.
> - **`ai-hub`** — `C:\Users\fxgui\Documents\Perso\Projects\suddenly\_code\ai-hub`. 60 test files under `tests/{muses,pipelines,e2e}/`; **no coverage report**. Carries `scripts/` — five `.py` files with **no corresponding test tree** — which makes the "no test file found" case (S8) exercisable on a real path rather than a hypothetical.
>
> State the fixture and its relevant state in every run. A precondition the fixture lacks → **N/A**, never FAIL.

## Scenarios

| #   | Situation (input) | Expected behaviour | Pass criteria | Judge load path | Page rule pinned |
|-----|-------------------|--------------------|---------------|-----------------|------------------|
| S1  | `05-stats` on `app`. The measurement surfaces an untested module and a config gap. | Report, and **name** the action that would treat each finding. Launch neither. | Intended writes: **∅**. No `04-strengthen` output, no `03-configure` output appears in the run. Suggesting is permitted; invoking is an automatic FAIL. | `SKILL.md` + `actions/05-stats.md` | `### Le contrat de chaînage` › *`05-stats` n'écrit rien et ne propose rien* |
| S2  | `05-stats` on `ai-hub`, then `04-strengthen` on `ai-hub` in a fresh run with no argument carried over. | The second run re-reads the project document; it does **not** rely on anything the first run "knows". | Nothing from run 1 is assumed present in run 2. If the second run behaves as though a phase or a domain answered in run 1 still holds, that is retained state → **FAIL**. | `SKILL.md` + `actions/05-stats.md` + `actions/04-strengthen.md` | `### Le contrat de chaînage` › *ne garde aucun état entre deux exécutions* |
| S3  | `05-stats` on `app` computes a density figure, then routes to `02-audit`. | `02-audit` uses the figure it was handed. It does not recompute a density of its own. | One measurement, one value, cited once. Two independently computed figures for the same measure — even if they agree — is a FAIL: the failure mode is divergence in silence, not disagreement today. | `SKILL.md` + `actions/05-stats.md` + `actions/02-audit.md` | `### Le contrat de chaînage` › *celui qui nomme passe la main, celui qui reçoit ne recalcule pas* |
| S4  | `05-stats` on `ai-hub` where a `domain` term resolves to nothing. | Raise a flag that names the action treating it, reports the term, and gives **both readings** — divergent spelling, or non-existent domain — deciding neither. | Both readings appear. A flag that picks one reading, or that reports the term with no owning action, is a FAIL. | `SKILL.md` + `actions/05-stats.md` | `### Le contrat de chaînage` › *rapporte le terme et les deux lectures* |
| S5  | `04-strengthen` on `app` confirms three gaps. | Pass them to `01-write` **one at a time**, re-evaluating the number constraint between each, with the total announced before the first. | Three separate passages, with a re-evaluation between them. A single batched handover of three is a FAIL — each addition moves the arithmetic for the next. Announcing the total is not submitting it for approval. | `SKILL.md` + `actions/04-strengthen.md` + `actions/01-write.md` | `## Les confirmations` › *Un lot que l'utilisateur nomme lui-même* (the derived form) |
| **S6** | `02-audit` on `app`. During the audit, a removal candidate reveals an untested behaviour worth a test. | Report the observation. Do **not** originate a test, and do **not** route to `01-write`. | No proposed test appears in `02-audit`'s output and no `01-write` invocation is intended. The edge does not exist. This is the deliberate absence, not an oversight — an audit removes, it never originates. | `SKILL.md` + `actions/02-audit.md` | `## Le chaînage` › *`02-audit` n'a aucune arête vers lui* |
| S7  | `05-stats` on `ai-hub`, which has **no coverage report** and thus no denominator. | Route to `03-configure`, naming it as what changes this. `03-configure` then routes onward to nothing. | `03-configure` is reached from `05-stats` and produces no onward routing of its own. An unreachable `03-configure` is a FAIL; one that routes to `04-strengthen` afterwards is also a FAIL. | `SKILL.md` + `actions/05-stats.md` + `actions/03-configure.md` | `## Le chaînage` › *atteignable et terminale* |
| S8  | `04-strengthen` on `ai-hub` with `scope=scripts/` — five source files, no corresponding test tree, therefore no test file in the resolved universe. | Report the finding, refer to the strategy document (or its absence), and **stop**. | No ranking is produced. Ranking the whole source tree instead is a FAIL: it denies the number constraint and turns the skill into the mass campaign it exists to avoid. | `SKILL.md` + `actions/04-strengthen.md` | `## Les cas limites du classement` › *aucun classement* |
| **S9** | `04-strengthen` on `app` with `top_n=5`, where qualified gaps far exceed 5. | Report the total, say the ranking cannot be relevant at that population size, and propose a **narrower `scope`**. | The remedy offered is a `scope`. A proposed `domain` is an automatic FAIL — it reorders the same population and leaves it exactly as large, producing a table that only *looks* shorter. | `SKILL.md` + `actions/04-strengthen.md` | `## Les cas limites du classement` › *Ne jamais proposer un `domain` comme remède* |
| S10 | `02-audit` on `app` with both `scope=tests/games/` and `domain=federation`. | Halt and say why. | The action halts before any classification. Applying either parameter, or preferring one silently, is a FAIL — there is no implicit precedence. | `SKILL.md` + `actions/02-audit.md` | `## Les paramètres` › *`scope` et `domain` sont exclusifs* |
| S11 | `04-strengthen` on `app` with `scope=tests/games/` (a path inside the test tree). | Resolve **symmetrically**: the universe is the pair — those tests **and** the source they correspond to. | The universe contains both sides. A universe holding only test files is a FAIL; so is a refusal to accept a test-tree path. Same expectation for `02-audit`, `05-stats`, `06-align`. | `SKILL.md` + `actions/04-strengthen.md` | `## Les paramètres` › *La résolution est symétrique* |
| S12 | A session where `02-audit` removes tests on `tests/games/` and `04-strengthen` runs afterwards on the same path, with **no demonstrated change of risk**. | `04-strengthen` does not re-propose a test on that path. | No re-proposal on the just-removed path. Without this bound the two actions ping-pong on the same file from run to run — the failure only shows across runs, which is why the scenario is a pair and not a single invocation. Whether the net figure is framed as an observation is scored in `confirmations-scenarios.md` S12, not here. | `SKILL.md` + `actions/02-audit.md` + `actions/04-strengthen.md` | `### La balance nette` › *ne repropose pas un test sur un chemin que `02-audit` vient de faire retirer* |
| S13 | `01-write` on `app` for three behaviours the tier table settles differently: one `contract`, one `e2e`, one `skip`. | Delegate to `aidd-dev:06-test` — `01-test` and `02-test-journey` respectively — for the first two, and to **nothing** for the third. | The invocation set holds exactly two delegations. A delegation on `skip` is a FAIL: `skip` is a tier decision that no test is written, and routing it onward turns the sink's own classification into a formality. Delegating before the outcome block is reported is also a FAIL — the user overrides or cancels *before* the edge is taken, not after. | `SKILL.md` + `actions/01-write.md` | `## Le chaînage` › *`01-write` est le puits* + `## Les quatre autorités` (row **Table des tiers**, `skip`) |

## How to run

Agent-as-`overcode:control` (dry-run, READ-ONLY on the fixture): for each scenario, load **only** the files in its *Judge load path*, plus this suite. Reason out the response, the exact set of intended writes, **and the set of actions the run would invoke**, then judge against the pass criteria.

**The invocation set is a first-class observable here.** Half this suite turns on the difference between *naming* an action and *launching* it. Record, for every run, the list of actions the skill would actually execute — a suite that only reads the prose will score S1 as a PASS on the strength of the word "suggests".

**S2 requires two runs and is judged on the Δ.** Run 1 answers the phase question out loud; run 2 is a clean invocation. Anything carried into run 2 that was never written to the project document is retained state.

**Decisive observables** (write-scoped):

- **`05-stats` intended writes = ∅ and invocations = ∅.** Named actions only.
- **No `02-audit` → `01-write` edge**, in either the prose or the invocation set.
- **One measurement, one computation.** A value recomputed downstream is a FAIL even when the two agree.
- **`scope` + `domain` → halt.** Any output past that point is a FAIL.
- **Saturation remedy = `scope`.** A `domain` offered as the remedy is an automatic FAIL.
- **No edge out of `skip`.** The invocation set is counted per tier, not read from the prose.

## Results log

<!-- append run results here per behave/references/harness-conventions.md › Results log format -->

### 2026-07-28 — run 1 (initial, dry-run, target=`control`@HEAD, fixture=app+ai-hub) — **10/13 PASS, 3 FAIL**

Pre-alignment state of the skill, materialised read-only from `HEAD` (`git archive`); both fixtures untouched.

| # | Verdict | Δ vs prior | Note (instruction cited) |
|---|---|---|---|
| S1 | PASS | — | `actions/05-stats.md` › *Flags* — an untested module routes to `04-strengthen`, a config gap to `03-configure`. |
| S2 | PASS | — | No state is carried between runs; the second run re-resolves everything. |
| S3 | PASS | — | A density figure routes to `02-audit` and is judged no further in `05-stats`. |
| S4 | PASS | — | A domain term resolving to nothing routes to `06-align`, deciding neither reading. |
| S5 | PASS | — | Three confirmed gaps chain into `01-write`, one at a time. |
| S6 | PASS | — | A removal candidate revealing an untested behaviour hands over rather than writing in place. |
| S7 | **FAIL** | — | `ai-hub` has no coverage report, so there is no denominator. At HEAD the degenerate order is stated in `test-density.md` but `05-stats` does not route the outcome — the run reports "not measurable" and stops, naming no action. `03-configure` is what changes that. |
| S8 | **FAIL** | — | `scope=scripts/` resolves to five source files and **no test file**. Nothing at HEAD says what an empty resolved scope means: an empty result and a scope that matched nothing are reported identically, and only one of the two is good news. |
| S9 | PASS | — | `top_n=5` truncates and says how many were dropped. |
| S10 | PASS | — | `scope` and `domain` together: the run stops and asks which was meant. |
| S11 | **FAIL** | — | `scope=tests/games/` on `04-strengthen` — a path *inside* the test tree, given to the action that looks for untested *source*. At HEAD nothing tells the action to read the scope against the source glob and say the scope cannot yield a gap. |
| S12 | PASS | — | `04-strengthen` after `02-audit` on the same path re-measures rather than assuming the prior removal. |
| S13 | PASS | — | Three behaviours, three tiers; `skip` delegates to nothing. |

**Frictions / gaps:**
- S7, S8 and S11 are one family: a degenerate or ill-posed input that produced a truthful-but-terminal answer with no route out. Each of the three names a different degenerate shape — no denominator, an empty scope, a scope pointed at the wrong tree.

**Tally:** 10/13 PASS (0 N/A) — no prior run.

### 2026-07-28 — run 2 (post-fix, dry-run, target=`control`@worktree, fixture=app+ai-hub) — **13/13 PASS**

Post-alignment state (parts 1–3 applied); both fixtures untouched, byte-identical to run 1.

| # | Verdict | Δ vs prior | Note |
|---|---|---|---|
| S7 | PASS | **▲** | The missing denominator is reported *and* routed — `03-configure` is named as what changes it. |
| S8 | PASS | **▲** | An empty resolved scope is distinguished from a scope that matched nothing, and each is said. |
| S11 | PASS | **▲** | A scope inside the test tree is read against the source glob and reported as unable to yield a gap. |
| S1–S6, S9, S10, S12, S13 | PASS | = (×10) | Unchanged. |

**Frictions / gaps:** none.
**Tally:** 13/13 PASS (0 N/A) — no PASS→FAIL. Three FAIL→PASS, all three on the degenerate-input family.
