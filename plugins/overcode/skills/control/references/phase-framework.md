# Project phase framework

A test suite does not prove the same thing at every moment of a product's life. The same uncovered function is a foundation worth securing while the domain model still moves, and an acceptable gap once the model is frozen and nobody is using the product yet. This reference gives `control` the missing dimension: **when in the product's life** the arbitration is happening.

**The phase classifies, second and never alone.** Domains resolve first and set a level; the phase reads that level into a `phase x domain-level` cell (`references/decision-matrix.md`), and the cell states a required proof and a ceiling. The tier (`contract` / `e2e` / `skip`) is that cell's output name, not a decision the phase takes on its own reasoning - a test is never refused "because we are in production" outside the cell that names the requirement. Density and the pivot's *Risk signals* keep the older boundary: they prioritise and report, never classify - the phase is the one exception, having become the classifying authority in series with domains.

What the phase does govern is the **analysis strategy**, and it is **four things, not three**: which criteria weigh heavily right now, **which files enter the reading of the coverage report**, in which order the result is restituted, and — **at a phase switch only** — the qualification of a batch of tests as now obsolete (`## Net balance by phase`, and `06-align` step 10).

It fixes a **ceiling now, never a threshold**. A per-phase coverage *percentage* threshold would still turn the number into a target and still break the rule that coverage is a symptom, never a goal - that prohibition is unconditional and holds whichever phase is in force. What the `phase x domain-level` cell fixes instead is a ceiling on required proof: a fixed count a case cannot be pushed past. A floor degenerates into a target the moment it is displayed - something to sit just above; a ceiling cannot, it can only be met or exceeded. The two are not interchangeable, and this reference names both so neither is mistaken for the other.

### Bounding by saying so

**The phase may reduce the analysed universe. It may never do so in silence: every file it sets aside is listed, with the phase motive that set it aside.**

This is the only form of restriction the model admits, and the reason is the one that already bounds the domains — a false positive costs one line of noise, a silent false negative costs the gap this skill exists to prevent. A **declared** restriction is not a false negative: it is a decision that can be re-read and contested. An undeclared one is indistinguishable from an area that came out clean.

### What the phase does not decide

**It bounds what enters a reading; it never changes what a datum means once read.** A file absent from the coverage report means *not covered* in every phase alike. What the phase legitimately changes is how high that file ranks — in `scaffolding` a mass of never-imported files is the expected state and ranks low, in `sustaining` the same mass is the finding. Same fact read twice, never two facts.

Entering the universe and meaning something are two different questions, and only the first is the phase's.

## The phases

Four of them sit on one axis: growing exposure, then sedimentation. Each boundary is a question with a binary answer, so a phase can be declared without debate. Two more sit off that axis — `default` and `undetermined` — and both proceed on the neutral weighting.

### `scaffolding` — does the domain model still move?

**Yes.** Entities are being renamed, split, merged; a schema change is a normal week.

- What the suite must prove: that the foundations hold their own contract — model invariants, validation rules, the transformations everything else is built on. Broad, shallow coverage of the shapes that everything downstream assumes.
- What it assumes it does not cover: client journeys, error paths of integrations that are not wired yet, anything whose shape is going to change before anyone depends on it. A test written here against a shape that moves next week costs more than the regression it would have caught.

### `hardening` — is the model frozen, with no real users yet?

**Yes.** The shapes have stopped moving; nobody outside the team depends on the system, and no data in it would be painful to lose.

- What the suite must prove: that the assembled whole behaves — the paths that cross several modules, the branches nobody exercised by hand, the error handling that was postponed while the model moved.
- What it assumes it does not cover: production-grade edge cases nobody has met yet. Guessing at them here produces tests calibrated on imagination rather than on incidents.

### `production` — are there real users, and data that cannot be reconstituted?

**Yes.** Someone outside the team depends on the system, and a wrong write cannot simply be replayed.

- What the suite must prove: the client-facing acts — sign-in, registration, payment, booking, form submission, anything irreversible or business-critical — and the boundaries with third parties the product now genuinely depends on.
- What it assumes it does not cover: internal refactoring detail. Here the suite protects the user's path, not the developer's comfort.

### `sustaining` — has significant new code stopped arriving?

**Yes.** Commits are mostly fixes and dependency bumps; the feature set is settled.

- What the suite must prove: that nothing regresses on what is already in use, and that the **external contracts** the product depends on still behave as assumed — because they keep moving after the product has stopped.
- What it assumes it does not cover: new-feature coverage that nothing produces any more. This is the phase where the suite's cost is most visible and its internal yield lowest.

### `default` — is neutrality what the project wants?

**Yes.** The project wants to use the actions without any ranking bias and without any removal batch, and it wants that on the record rather than re-litigated at every run.

- What the suite must prove: whatever the resolved `phase x domain-level` cell requires, nothing more (`@decision-matrix.md`). No required proof is raised, none is lowered.
- What it assumes it does not cover: nothing in particular. `default` expresses no expectation about the suite, which is precisely its point.

`default` is **declared**, exactly like the four positional phases. Its effects are entirely subtractive: neutral criteria weighting, **no expected axis order**, and **no removal batch** — because `default` raises and lowers nothing that a test could have been justified by, so nothing it wrote can have become obsolete.

**What it is exempt from is the removal side, not the switch itself, and the two directions differ** (`@../actions/06-align.md`, step 10, which states the rule in full and is the authority for it):

| Movement | Outgoing batch | Incoming ranking |
|---|---|---|
| **to** `default` | none — a declaration, net balance zero | none |
| **from** `default` to a real phase | **empty set** — nothing was written under a bias that could now be obsolete | **the entering phase's**, through `04-strengthen` |

Saying that a project moving *from* `default` is not switching would withhold the entering phase's incoming ranking — the one thing declaring a real phase is for.

### `undetermined`

Not a fallback dressed up as a value: a first-class answer. It means the question was put to the user and left unanswered - never that a deduction came up short, because none is attempted. `control` says so, states what it asked, and proceeds on the neutral weighting.

**`undetermined` and `default` are not the same value wearing two names.** They share the neutral weighting and nothing else:

| | `default` | `undetermined` |
|---|---|---|
| Origin | a declared choice | a question left unanswered |
| The question is asked again | never | at every run |
| `05-stats` routes to `06-align` for it | no, **once declared** | yes |
| Removal batch | none, by definition | whatever the real phase says, once known |
| Phase switch applies | no removal batch, in either direction; the **incoming** ranking does apply on leaving it | yes, as soon as a phase is declared |

The distinction is worth the extra value because the two states call for opposite handling: one is settled, the other is an open question that every run must keep surfacing.

## Resolution order

**The phase is never deduced.** It is declared by a human, and this skill's only job is to know where that declaration came from. Three sources, in order:

1. An explicit `phase` argument on the invocation - the answer for this run only.
2. A phase **declared in the project's own documentation** - conventionally its test strategy document, `aidd_docs/memory/testing.md`. This is the normal source, and the one worth establishing once.
3. **Ask the user, and wait.** No action proceeds on an undeclared phase by guessing one. The question is asked before any ranking, any table, any proposal - because the answer changes their order.

`undetermined` remains a legitimate value, and it means exactly one thing: the question was asked and not answered. It is never the result of a failed deduction, because no deduction is attempted.

### Value and provenance are two axes, not one

Every action reports **two** things about the phase, and they are never merged into a single line:

| Axis | Answers | Possible values |
|---|---|---|
| **value** | *which phase is in force* | `scaffolding` · `hardening` · `production` · `sustaining` · `default` · `undetermined` |
| **provenance** | *where that value came from* | `argument` · `declared <path>` · `answered` · `unanswered` |

The provenance axis is worded as the `answered` / `unanswered` pair on purpose. Naming its last value `undetermined` would have been the obvious shortcut and the wrong one: `undetermined` is a phase, and reusing it as a provenance made the same word mean *which phase* on one line and *where it came from* on the other. The confusion stayed invisible while the two coincided; `default` is what made it legible, since a `default` arriving by argument, by declaration or by an answer are three different situations that a merged line cannot tell apart.

**One pairing is forced, and only one**: provenance `unanswered` always carries value `undetermined`, and value `undetermined` always carries provenance `unanswered` - they are the two faces of the same non-event. Every other combination is free.

`default` travels through the same three sources as any other phase - it is a declarable value, not a mode. Declaring it is what makes it different from `undetermined`: once written down, the question stops being asked, and `05-stats` stops routing to `06-align` over it.

When the argument and the declaration diverge, the argument wins **for this run** and the divergence is reported - a one-off override does not silently rewrite what the project has written down. The phase is an attribute of the project, overridable on an explicitly requested `scope`; there is no automatic per-zone split, because no reliable source of truth exists for one.

**A phase this skill resolved by asking is recorded nowhere by that act alone.** An answer given in conversation is worth one run. `06-align` is what turns it into a declaration, in the project's own document - after which nobody, human or skill, has to answer again.

## What the repository can and cannot tell you

A repository carries traces. It carries no users.

That distinction is the whole reason the phase is declared rather than measured. A project that is finished but not yet open, and the same project serving thousands of paying clients, leave **exactly the same traces**: a frozen model, regular tags, a wired deployment, a green pipeline. Nothing in the code says whether anyone is on the other side - and that is precisely the difference that decides what the suite must protect first. Where nobody is using it yet, a failure is repaired and forgotten; where real clients are, a failure takes someone's money or cancels their booking, and there is no undo.

So the signals below are **material for the question, never an answer to it**. They are offered alongside the question so the user answers in one word instead of investigating; they never produce a value, and no action may proceed on them alone.

| Observation | What it is worth saying out loud |
|---|---|
| Churn on model/schema/entity files | high churn: the domain model is still moving; flat: it has settled |
| Data migrations, ordered | the model was frozen at some point |
| Version tags | regular tags suggest something is being released to someone |
| Deployment configuration | it goes somewhere real, automatically |
| Commit volume over 90 days, against the repository's total age | near zero on a long history: little new is arriving; near zero on a short one: the project stopped, which is not the same thing |
| `fix:` outweighing `feat:` | the work has shifted from building to keeping alive |

Present what is relevant, then ask the question these observations do not settle - most often: **are real people using this today?**

## Risk criteria weighting

The phase re-weights the risk criteria `04-strengthen` already ranks by. It adds no ranking mechanism of its own. What it does change is the **output name**, and only through the matrix cell it reads: the required proof of the resolved `phase x domain-level` cell (`@decision-matrix.md`) is what `proposed_tier` names. A re-weighting alone never moves a name; a cell does.

| Criterion | `scaffolding` | `hardening` | `production` | `sustaining` |
|---|---|---|---|---|
| Consequence | normal | raised | **dominant** | raised |
| Branching | raised | **dominant** | normal | lowered |
| Churn | **dominant** | raised | normal | lowered |
| Blast radius | raised | raised | normal | normal |
| Absence of any other net | normal | raised | raised | normal |
| **External contract dependency** | lowered | normal | raised | **dominant** |

`default` and `undetermined` have no column: both use the **neutral** weighting, which is the criterion order as `04-strengthen` states it, with nothing raised and nothing lowered. Adding a column of six `normal` cells would only invite the reader to look for a difference that does not exist.

"Development" is deliberately absent from the phase list. What it describes — test the recent code, prove non-regression — is the **churn** criterion, which already exists. A phase modulates its weight; it does not need to become one.

## External contract dependency

The five pre-existing criteria are all **internal**: churn, branching, blast radius, consequence, absence of another net. None of them fires when the thing that breaks is the vendor. A Meta Pixel or Conversions API integration, a GTM container, Brevo, Klaviyo, a payment SDK, an outgoing webhook — any of these can break without a single line of the repository moving. That blind spot is why this criterion exists.

### What a test can and cannot prove here

Writing this down is what keeps the criterion from manufacturing false assurance.

- **Provable in process, at `contract` tier, without calling the vendor:**
  - the payload the code builds is the one it believes it is sending — fields, types, units, the identifier actually used;
  - the **degraded path** behaves correctly when the vendor returns an error, an unexpected schema, or nothing at all.
- **Not provable by the test suite:** that the vendor still accepts that payload. This requires a real, slow, quota-bound call, which has no place in a suite that gates every validation loop. The skill **declares it out of reach of testing** and refers it to monitoring, instead of proposing a test that would give false assurance — `04-strengthen` when ranking, `01-write` at the gate every new test enters through.

### Cost cap, per boundary

Without a cap, ten integrations produce twenty tests in a skill whose entire purpose is to bound the number. **One external boundary is worth one test by default — the degraded path.**

- The **degraded path** is proposed when a vendor failure can interrupt the journey: blocking script, unhandled rejection, a response whose schema is consumed without a guard. An outbound-only integration whose failure is invisible on the client side gets **no test at all** — it is declared *monitored outside the test suite*, exactly like vendor acceptance.
- The **built payload** earns a second test only when it carries data with a verifiable in-process consequence: an amount, an order identifier, an authorisation status, a consent. A measurement pixel carries none; a Conversions API transmitting a purchase value reconciled later does.
- This is a **ceiling per boundary, not a quota**: an integration may legitimately receive nothing.

### Detection lives in the pivot

`control` carries the criterion; it does not carry the inventory. Which SDKs, tags and outgoing clients exist in a given stack is stack knowledge, and belongs to the `testing` pivot's **Risk signals** field, whose role that already is (see `pivot-contract.md`). Without a pivot, `control` falls back to reading the project's own manifest for dependencies pointing at domains the project does not control, and says the inventory is generic.

## The two reading axes

`control` reads a suite along two axes, and compares their **order**, never their share.

- **Foundations** — model invariants, validation, shared transformations. The structural axis.
- **The project's declared domains** — the functional axis, defined below. When the project has declared none, its code reads in the **out-of-domain** column — a column the matrix already has, read exactly like the other three, never a fallback carrying a substitute inventory of its own.

A third bucket, *recent code*, used to sit here. It is gone: what it described — test what the last commits touched — is the **churn** criterion, which already exists in the risk ranking. The same thing does not need two names and two weightings, and the phase list already refuses "development" as a phase for exactly this reason.

Expected priority order by phase:

| Phase | Expected order |
|---|---|
| `scaffolding` | foundations → domains |
| `hardening` | foundations → domains |
| `production` | domains → foundations |
| `sustaining` | domains → foundations |
| `default` | **none expected** |
| `undetermined` | **none expected** |

Under `default` and `undetermined` there is nothing to compare against, and `05-stats` **says so** rather than emitting an empty comparison — an absent expectation printed as a blank row reads like a perfect match, which is the opposite of the truth.

**No percentage is ever produced.** What this section brings is an expected **ordering**, never a share; `05-stats` compares ranks. The ceiling is a different thing and it exists elsewhere - the matrix cell states it as a count of established proofs (`@decision-matrix.md`), not as a proportion of anything. An ordering is not a ceiling, and neither is a percentage.

Placing an existing test on the **foundations** axis remains an approximation (tier + role of the source file it exercises), and the approximation is **declared** in the output alongside the comparison, so nobody reads it as a measurement. Placing it in a **declared domain** is not an approximation: a file either matches the domain's resolution or it does not, and what matches nothing is reported rather than silently dropped.

## Domains

A domain is a functional part of the product — `auth`, `payment`, `checkout` — resolved in the code by terms: `Login`, `Register`, `SessionGuard`.

Domains depend on the project's core features, and **none of them is universal**: a library, a CLI tool, a game have neither authentication nor payment. This skill therefore proposes no default domain, and the generic level of the precedence cascade is **empty** for them. A project that declares nothing runs in the **out-of-domain** column of the matrix - a column read exactly like the other three, never a fallback carrying a substitute inventory of its own.

### Why no domain is a default

A phase is a universal axis: every project, whatever it does, sits somewhere between a moving model and a settled one, so a generic value (`default`, `undetermined`) can stand in for any project that has not said which yet. A domain is not a universal axis: whether a project has an `auth` domain or a `payment` domain at all is a fact about what it *does*, not about where it stands in its life, and a library, a CLI tool or a game can have neither without that saying anything about their age or health. A default domain would not neutrally wait for an answer the way `default` does for the phase - it would assert a feature the project may not have, which is a false positive of the exact kind this skill spends its whole domain model avoiding. That is why `references/domain-catalogue.md` offers **candidates**, never a default: a candidate is confirmed or dismissed by the project - a default would already have decided.

### Who declares what

| Knowledge | Holder | Why |
|---|---|---|
| **which** domains exist | the project, in its own test strategy document | nobody else can know |
| **how** to spot them in this stack | the language plugin's `testing` pivot, in its **Domain resolution** field | it is stack convention, and it goes stale fast |

Split this way the two cannot contradict each other, so no arbitration rule is needed. The pivot **completes** a domain the project named without resolving; it never overrides a resolution the project wrote explicitly about its own code — the project is talking about the code that exists, the pivot about a convention in general.

This is the same authority split already applied to external boundaries: `control` owns the generic criterion, the pivot owns the inventory.

### A domain prioritises; it never restricts

Same boundary as the phase, for the same reason, and it is the load-bearing rule of the whole mechanism.

What no domain matches **stays in the analysis** — it simply ranks lower — and **it is reported**, together with the term that failed to recognise it. Searching `Login` and `Register` finds `LoginForm.tsx` and misses `SessionController`: a silent false negative would declare a central part of the code out of scope with nobody able to see it. A false positive costs one line of noise; a silent false negative costs the gap the skill exists to prevent.

That trace pays for itself twice — at runtime it hides nothing, and it is what lets `06-align` detect that the declared list has drifted from the code.

## Net balance by phase

`02-audit` and `04-strengthen` answer to a net balance; the phase says which way it is normally expected to lean, and never imposes it.

- `scaffolding`, `hardening` — additions normally outweigh removals: the suite is being built.
- `production` — the balance shifts rather than grows: what the earlier phases justified gives way to what the client journeys demand.
- `sustaining` — a negative balance is expected, never required.
- `default`, `undetermined` — **no expected lean.** Neither weighting deprioritises anything, so neither qualifies a test as obsolete *while it is in force*. What happens on the way out is where the two part company:
  - `default` — **no removal batch, in either direction.** Not because the machinery cannot run, but because a project that has just declared `default` has taken a decision: qualifying tests obsolete on the spot would contradict it. What is exempt is the **outgoing batch alone, never the switch itself**: moving out of `default` into a real phase runs that phase's incoming ranking in full, with an empty outgoing set — nothing was written under a bias that could now be obsolete. Saying the switch does not apply would exempt the incoming half too, and a project leaving `default` would receive no proposal at all (`06-align`, step 10, the `default` bullet, states both halves).
  - `undetermined` — **the removal batch depends on the real phase, once it is known.** Nothing has been decided, so nothing is being contradicted: the moment a phase is declared, the switch applies as it would between any two phases, and the batch is established against the phase declared. Reporting an empty batch here because the previous value was neutral would exempt from re-examination the one suite nobody ever weighted.

**`sustaining` carries the one exception to its own negative balance:** external boundaries remain the only legitimate motive for addition in this phase, and are excluded from any removal batch. It is the phase where nothing internal moves any more while external contracts keep moving — removing their only net at that exact moment would be the worst possible timing.
