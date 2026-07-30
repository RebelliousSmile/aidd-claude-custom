# Align

Audit the gap between what a project's test strategy document *says* and what the project *does*, then propose the document's update in three strictly separated blocks: the facts this skill measured, the strategy the project has to decide, and the domain ledger only this action writes.

Mirror image of `05-stats` in direction rather than in kind: `stats` reads the situation and stops, `align` gives its findings somewhere to go. It is the only action of this skill that writes into the target project's own documentation, and it does so under the narrowest terms in the skill - see the transversal rule in `SKILL.md`.

## Inputs

- `project_path` (required) - absolute path to the target project root
- `scope` (optional, default: whole project) - a subdirectory or glob to limit the measurements. **`scope` designates one universe, here as everywhere in this skill: the source code and the tests that match it**, resolved **symmetrically** in either direction - the same perimeter `05-stats` measures. No action has a universe of its own.
- `domain` (optional) - a functional domain, resolved against `<project_path>/aidd_docs/memory/testing-domains.md` when this action has already run once, or against `@../references/domain-catalogue.md` for a first proposal. It **orders what the audit reports first; it never bounds what the audit covers** - an alignment run on part of the project and presented as an alignment would put a half-true document in the file. Mutually exclusive with `scope` - given both, stop and ask which was meant (`SKILL.md`, *Parameters*). **One name, not a list** - given `domain=auth,payment`, stop and ask which was meant too: this action parses no multi-valued `domain`, and neither splitting it nor taking the first is a reading anyone asked for.
- `phase` (optional) - overrides the resolved project phase for this run only

## Outputs

```
PHASE
  <as produced by 05-stats: value, provenance, question, divergence>

GAP AUDIT
  | nature | subject | document says | reality |
  |--------|---------|---------------|---------|
  | missing fact  | e2e runner        | -                       | Playwright, wired in package.json |
  | stale fact    | coverage gate     | "80% global planned"    | thresholds at 47/45/33/45, enforced in CI |
  | missing decision | tier vocabulary | -                     | no line decides what deserves a test |
  | unresolved domain | `auth`           | declared as a domain   | no file matches the term - named `identity` in the code? |
  | undeclared area   | src/notifications/ | -                    | 14 files no declared domain matches - they run out-of-domain |

MEASURED FACTS          (authority: control - proposed as written)
  <the block, in full, exactly as it would be inserted>

PROPOSED STRATEGY       (authority: the project - proposed, never applied by default)
  <the block, in full, exactly as it would be inserted>

DOMAIN LEDGER           (authority: the project - proposed, never applied by default)
  <catalogue x scan candidates, name + level together, and confirmed residue answers>
  double candidacy    : <one line per path proposed under more than one domain: <path> -
                         <domain A> (<level>) + <domain B> (<level>) - both proposed on
                         purpose, the arbitration is yours and no primary owner was picked>
                        | none - no path matched two domains
  <the block, in full, exactly as it would be written to testing-domains.md>

PHASE SWITCH            (only when the resolved phase differs from the declared one)
  from -> to  : <declared phase> -> <resolved phase>
  cell        : <one line per domain-level in force> <phase> x <level> - required proof
                <required proof | none, on a `—` cell>, ceiling <n | none>, before -> after
  outgoing    : <n> tests, by motive: inherited heuristics <n>, phase-obsolete <n>
  incoming    : <n> gaps the entering phase raises, each routed through 01-write
  net balance : <±n> on a suite of <total> - <the displacement, in one sentence>

REMOVAL BATCH           (whenever a switch is reported - one consent, or refusal en bloc)
  selection criterion : <one sentence - what every member of this set has in common>
  by rejection motive : <count per motive>
  sample              : <a representative handful, shown on screen>
  exhaustive list     : <the full list, shown in full in this same turn - not a path standing in
                         for it. Also written to <project_path>/aidd_docs/tasks/<date>-control-
                         removal-batch.md before the question is put, so a refusal or an
                         interruption still leaves a durable record of what was proposed>
  outgoing : 0        : <rendered instead of the four lines above when nothing qualifies -
                         one sentence naming what was examined and which bound emptied the set>
  excluded            : <one line per category, count then the tests and what holds each>
                        external boundaries <n> - <test> : <the boundary it covers>
                        held by consequence <n> - <test> : <the criterion holding it>
                        sole net <n>            - <test> : <the subject it is the sole net on>
                        one motive short <n>    - <test> : <which of the two failed to qualify>

WRITE PATH
  strategy route : aidd-context project-memory skill | direct write (fallback) -> testing.md
  strategy consequence : <what this route does, and what it does not do>
  domain route   : direct write, always - 06-align is testing-domains.md's sole writer
  domain consequence  : no delegate, no fidelity gap to re-check; the idempotence check
                         (frozen entries unchanged, only residue and confirmed additions differ)
                         applies in its place
```

Nothing is written to the project's own files as part of producing this output - no `testing.md`, no `testing-domains.md`, no test file. The one exception is the **removal batch's exhaustive list**, written to `<project_path>/aidd_docs/tasks/<date>-control-removal-batch.md` before the question is put, so that a refusal or an interruption still leaves a durable record of what was proposed. **The condition is that a batch exists, never that it is large**: the list is shown on screen in full whatever its size (step 11), so a file written only past some volume would be a file written exactly where the on-screen list was allowed to be dropped - the case the model does not have. That file records the proposal; it changes nothing in the project, and it is not what the user reads to consent.

## Process

1. Resolve `project_path` and `scope`. Resolve the project **phase** per `@../references/phase-framework.md` - by renvoi, not by re-deriving it.

2. **Run the gap audit on `05-stats`'s production, never on a recomputation.** `05-stats` already establishes the authority in force, the document's readability, the tooling actually wired, what each domain's cell requires against what the suite carries (`exigé`/`trouvé`), the observed order of the reading axes and the resolution of the domains in force. This action consumes those results; it redefines none of them. Two sources of truth for the same measurement will diverge, and the one that diverges silently is the one nobody runs.

3. Classify every gap into exactly one of five natures. The distinction is what keeps the blocks apart later: the first two are facts, the third is a question the project alone can answer through `testing.md`. The last two are **both at once**, and are split accordingly - the measurement (a term matched nothing, an area is under no domain) goes into `MEASURED FACTS`, the response to it goes into `DOMAIN LEDGER`, never into `PROPOSED STRATEGY` - a domain's name and level are `testing-domains.md`'s content, not `testing.md`'s. Splitting them is what stops the skill from writing a decision under its own authority:
   - **Missing fact** - true of the project, absent from the document (an E2E tool in use and never named, an external boundary nobody wrote down).
   - **Stale fact** - stated in the document, no longer true of the project (a runner that was replaced, a threshold that moved, a plan that was carried out or abandoned).
   - **Missing decision** - no line of the document settles something this skill is nonetheless forced to settle at every run: the phase, the tier vocabulary, what the project deliberately refuses to test, the number constraint it holds itself to. This is not a defect in the document; it is the question the document has not been asked yet.
   - **Unresolved domain** - `testing-domains.md` declares a domain that resolves to no file. Two readings, and this action decides neither: the domain is spelled differently in the code than in the ledger, or it does not exist yet. Report the term, both readings, and let the user say which. It is classified apart from a stale fact on purpose - a stale fact is known to be false, this one is only known to be unmatched.
   - **Undeclared area** - a part of the code that no declared domain matches, and that no domain established so far reaches either. It is **not** a defect by itself: a project legitimately declares only the domains it wants prioritised, and the rest runs at neutral weight in the out-of-domain column. It becomes a finding when the area is substantial, and it is reported as a question - is this an area the project chose not to name, or one it forgot? Never as an area to be covered.

     **It is composed from both residue traces, read as one.** Two actions produce a residue and they name **opposite sides** of it: `05-stats` (step 1-quater) reports the **source** files no domain in force matched, `02-audit` reports the **test** files in that same position. Neither half is the area on its own. A directory whose sources go unmatched while a term matches its tests is a naming inconsistency, not an unnamed area - so reading either half alone manufactures a finding where there is none, and misses one where there is. Compose the two before classifying anything here, and when only one half is available, **say which one is missing** rather than presenting it as the whole.

4. **Document absent.** When no `testing.md` (or project-level equivalent) exists, produce the audit anyway - everything is a missing fact - then offer, as an explicit choice, to create the document or to abstain. **Never create it by default.** A project that has never written a test strategy may have decided exactly that, and a file appearing unrequested in `aidd_docs/memory/` is a decision taken on the project's behalf. When the user abstains, the audit stands as the output and the run ends there.

4-bis. **Domain ledger absent.** When no `testing-domains.md` exists, the project's entire code is in the **out-of-domain** column - not a special case, the column the matrix already has. Produce the gap audit and the domain candidates anyway (step 6-bis), and offer the same explicit choice: write the ledger, or abstain. Abstaining leaves the project in the out-of-domain regime, correctly - it is not this action's business to force a domain into existence.

5. **Build the `MEASURED FACTS` block.** It carries only what this skill is itself the source of:
   - the test runner actually wired, and the established E2E tool;
   - whether a coverage gate is configured **and invoked**, or configured and inert;
   - per domain in force, what its cell requires and what the suite carries against it (`exigé`/`trouvé`, `05-stats`'s two columns, and never a third that subtracts them), and the observed order of the reading axes, with the approximation declared as `05-stats` declares it - and, under `default` or `undetermined`, with no expected order to compare it against, said in words rather than left blank;
   - the **resolution of each domain already frozen in `testing-domains.md`**: how many files each of its terms matched, and which matched nothing;
   - the **inventory of external boundaries** - third-party integrations found in the manifest and in the source, and for each one whether any test references it or not.

   That inventory is the most perishable fact in the block, and it is what makes a second run of this action worthwhile on a project whose own code has not moved: a third-party SDK major can shift, or an integration can be added by a dependency bump alone, and no internal signal fires. Nothing enters this block that the skill cannot measure - a fact it merely believes is a strategy in disguise.

6. **Build the `PROPOSED STRATEGY` block.** It carries what the project has to decide and the skill only drafts: the declared phase, the tier vocabulary, what the project refuses to test, and the number constraint. **No domain content enters this block** - a domain's name and level are `testing-domains.md`'s content, built at step 6-bis, never `testing.md`'s.

   `default` is proposed here on the same footing as any other phase value. When a project keeps being asked its phase run after run and does not want to answer, the answer available to it is not silence - it is `default`, written down, which declares neutrality as a choice rather than leaving it as an omission. Say that plainly whenever the provenance is `unanswered`; the point of the value is lost if nobody is told it exists. And it is the provenance that triggers this, not the value - a `default` that arrived by an answer rather than by a declaration needs exactly the same offer, since nothing was written down either.

   On that last one, propose a **density rather than an absolute cap** (`@../references/test-density.md`), and propose it as the project's own measured median - a number the project can recognise, not one this skill invented. **The density is not a cap and is never named as one**: it observes a population and says whether the cases sit in the right place, it refuses nothing (`SKILL.md`, *Transversal rules*). What refuses is the `phase x domain-level` cell's **ceiling** (`@../references/decision-matrix.md`), which is in force whatever this block proposes, and the project's own declared test-count cap where it declares one. The three are read together at `01-write` and never merged into one number here. A cap is a number a project outgrows without noticing, and the day it does, the only options it leaves are raising it or ignoring it. A density stays meaningful as the codebase grows because it grows with it. The project may still declare a cap - it is the project's decision, and a declared cap wins over the proposal - but it should choose against the alternative, so state both. **A cap is proposed as a number, never as a multiple of the median**: a multiple would make the refusal move with the very population it is meant to bound. When the coverage report the median would be computed from carries no branch data - runs in line mode, branch tracking never switched on - there is no denominator and no median to propose (`@../references/test-density.md`, *Degenerate cases*): say so, name `03-configure` as what changes it, and propose nothing invented in its place.

   The density's **known blind spot belongs in this block too**, when the audit found one: a file whose cases are data-driven (a regex, a table, a schema) reads as an outlier while its tests genuinely discriminate. Writing that down here is what stops the next run from re-flagging it, and it is the one place the project can record it as its own judgement rather than as a measurement error. It is proposed as **complete prose, in the document's own language**, so the user validates a text rather than an intention - and it is validated **line by line**. Nothing here is applied by default, and a block the user leaves unanswered counts as refused.

6-bis. **Build the `DOMAIN LEDGER` block.** It is the one thing in the whole model no measurement can produce: which functional parts a product has is a statement about the product, not about its repository. This action establishes it by **catalogue (`@../references/domain-catalogue.md`) x code scan**, and **assigns the level together with the name** - a domain named without a level designates no matrix column and requires nothing, which is the same as not declaring it.

   The catalogue is a **floor of detection, never the inventory**: it guarantees a `payment` or an `auth` present in the code is not missed, it forbids no domain proper to the project from existing, and its level is a default starting point, never an imposition. **The code scan itself is stack-refined when a pivot is loaded**: each applicable language plugin's `testing` pivot, if present, states in its **Domain resolution** field how that stack's own convention expresses a functional domain in directory shapes, filenames and identifier prefixes, and the scan reads each file's candidates through the convention of **its own** stack (`@../references/pivot-contract.md` › *The pivot follows the file*). Reading a Python tree through a JavaScript convention finds nothing and reports an unnamed area. For a stack with no pivot, or no such field on it, the scan falls back to generic recurring directory names and identifier families alone, and says the detection is unrefined **for that stack**. Either way the skill *proposes* candidates - from the catalogue's matches and from what the scan (refined or generic) independently observed - explicitly as candidates, never as an inventory it discovered. **A domain exists only once the user confirms it**, name and level together. **Declaring no domain is a valid answer**, and it is recorded as such: the project's code then runs in the **out-of-domain** column - not a fallback, the column the matrix already has - and the question stops being re-asked once "no domain" is the recorded answer.

   **A domain passed as an argument is already the user's declaration - the argument is the confirmation, asking again would confirm the same thing twice.** What remains open is only its **level**: present in the catalogue, it takes that level without a question; absent from the catalogue, this step asks - never guesses, since guessing would pick a ceiling in the project's place.

   Include here the response to every *unresolved domain* and *undeclared area* found at step 3 - rename the term, add the domain, or record that the area is deliberately unnamed (a confirmed, frozen `out-of-domain` answer for that path, distinct from unmatched residue still pending a scan). Recording the deliberate choice matters as much as the other two: it is what stops the next run from re-raising it.

   **Resolution terms are literal substrings, matched case-insensitively, plus paths - no regex, no stemming.** The file is hand-edited by the project; a regex becomes unreadable, then wrong, and a wrong match fails in silence.

   **Idempotence by materialized judgment: this action judges once and freezes the judgment in literal terms.** A run does not re-resolve what a prior run already froze - it **applies** the frozen entries as they stand, and only the **residue** (what no frozen term matches) is scanned anew. A file may belong to several domains at once - forcing exclusivity would decide a real case by an arbitrary rule. Renaming a domain is an explicit choice made here, never the side effect of a scan noticing a pattern. Drift (a growing residue, a term that stopped matching anything) is `05-stats`'s to report, never this action's to apply on its own - it re-judges only once the user, informed by that report, asks it to.

7. **Approve each block independently.** Refusing the strategy does not withdraw the facts; refusing the facts does not withdraw the strategy; refusing the domain ledger withdraws neither, and leaves the project in the out-of-domain regime for anything the ledger would have named. An all-or-nothing gate would make the action unusable in the exact case it exists for - a project that accepts being described and is not ready to commit to a doctrine.

8. **Write path for `MEASURED FACTS` and `PROPOSED STRATEGY`.** When `aidd-context`'s project-memory skill is installed, **delegate to it**: it owns `memory/`, it carries its own approval gate, and it does one thing a direct write does not - it resynchronises the AI-context files that embed the project memory. **Resolve that skill by its role, never by a name or a number written here** - both have already moved across `aidd-context` versions, and a pinned action is how this action silently stops delegating. The role is a three-step chain and it is the chain that identifies it: a scoping step that analyses, categorises and **puts its own approval gate to the user**; a writing step that creates or updates the `memory/` files; a sync step that refreshes the AI-context block. Read the installed plugin's own manifest to find the skill filling that role. Enter through its scoping step so its own gate applies, and make sure its sync step runs. **A silent sync is not a successful sync.** That step legitimately has nothing to do when the AI-context files already list the document, and it then exits with no output at all - indistinguishable from a failure that swallowed its own error. So do not take a clean exit as proof: open the AI-context file and check the memory block actually names the document. Report which of the two it was - resynchronised, or already up to date. When it is absent, fall back to a **direct write**. Either way, **announce the route taken in the output, and say what the route does not do**: a fallback that silently skips resynchronisation leaves the AI-context files stating the old strategy, which is worse than not writing at all.

8-bis. **Write path for `DOMAIN LEDGER` - always direct, never delegated.** `<project_path>/aidd_docs/memory/testing-domains.md` is a **separate artifact from `testing.md`**, and `06-align` is its **sole writer** - not through `aidd-context`'s project-memory skill, which owns `testing.md` and nothing outside it. One file, one writer: routing this write through a delegate that reformulates on the way in would put two writers on the same file with neither aware of the other. Write the approved ledger verbatim - name, level, resolution terms, paths - and never rename or drop a frozen entry the current run did not itself confirm changing.

    **A "no domain" answer is written to that file too, as an explicit empty ledger.** Step 6-bis calls declaring no domain a valid answer and says the question stops being re-asked once it is *recorded*; two flags in `05-stats` - the out-of-domain statement's conditional referral, and the drift flag's prior condition - both turn on that record existing. With no file, nothing is recorded: the answer is lost the moment the run ends, and the next run asks again. `control` keeps no state between runs, so this file is the only place an answer can survive, and an answer nobody can find was not an answer. So write it - the ledger's header, zero entries, and one line stating that the project declared no domain and runs out-of-domain by its own decision. **An empty ledger and an absent file are opposite statements**, exactly as `unknown` and `0` are everywhere else in this model.

9. **Fidelity rule - the delegate is not a scribe.** The project-memory skill analyses, categorises and reformulates what it retains before writing; nothing in its contract promises it inscribes a supplied text **verbatim**. The "validated line by line" guarantee would therefore break in silence. So, for the `testing.md` route only: hand the approved text over as **literal content to be inscribed verbatim**, not as material to analyse; then **re-read the written file** and compare it, line for line, to the approved text. Any divergence - a reformulation, a section moved, a line absorbed into another - is **reported to the user, and never corrected on the spot**. It is another plugin's document; silently rewriting it would recreate the very problem delegation avoids. **This step does not apply to `testing-domains.md`** - there is no delegate on that route to diverge from it; what is re-read there is whether the frozen entries survived unchanged (step 6-bis, idempotence).

10. **Phase switch - detect it, never assume it.** A switch exists when the resolved phase **differs from the one declared in the document**, or when the user explicitly overrides it. Comparison, not supposition: a project whose document declares nothing is not switching, it is declaring for the first time, and that is step 6's business - **with one exception, which the third bullet below states in full: a prior `undetermined` switches like any other phase.** A document that declares nothing and a project that has been running on `undetermined` are the same repository seen twice; what separates them is that the question has already been put and left unanswered, and an answer given now is a switch, not a first declaration.

    **What decides between the two is a record in the document, and nothing else.** `control` keeps no state between runs (step 10's own *Net balance* bullet, and `05-stats`'s centre-of-gravity flag, both rest on it), so "has been running on `undetermined`" is not something a repository shows. Three readings of the document, and they exhaust the case:

    - **The document records a phase value** - any of the six, `default` and `undetermined` included. Resolved value differs -> **switch**. Same value -> nothing to report.
    - **The document records nothing about the phase** -> **first declaration**, step 6's business, no switch machinery, no removal batch. This is the default reading, and it is the one an absence gets.
    - **The user explicitly overrides a value the document records** -> switch, against that value.

    **The three readings are disjoint as well as exhaustive, and the bound on the third is what makes them so.** A declaration made where the document records nothing is the **second** bullet, whatever word the user uses for it - there is no recorded value, so there is nothing to override and no switch to run. Without that bound the two overlap on the most common case there is, a first explicit declaration on a phase-silent document, since "recording nothing" is something a document does; the reading would then be settled by which bullet the run happened to read first.

    **A `provenance` of `unanswered` in the current run is not a record.** It is this run's own unanswered question, asked minutes ago; answering it in the same turn is a first declaration and produces no outgoing batch. What the third bullet of the pair below is about is a document in which `undetermined` was **written down** - the project recorded that the question was put and left open - which is a record like any other and switches like any other. Reading a live `unanswered` as a prior `undetermined` would qualify a batch of removals against a phase the project never ran under, on the strength of a question this run itself asked.

    **`default` and `undetermined` are not the same case here, and treating them alike is the error to avoid.** Both weight the ranking neutrally, but only one of them has decided anything.

    - **`default` stays out of the switch machinery - by consent, not by mechanics.** A project declaring `default` has just taken a decision; following it with a batch of tests to qualify obsolete would contradict that choice at the instant it is made. So: moving **to** `default` is reported as a declaration - net balance zero, no removal batch at all. Moving **from** `default` to a real phase gets the entering phase's incoming ranking through `04-strengthen` and **an empty outgoing set**: nothing was written under a bias that could now be obsolete.
    - **`undetermined` has decided nothing at all, and switches like any other phase as soon as one is declared.** It is not a neutrality the project chose, it is a question left unanswered - and the answer, when it comes, is a first real phase taking effect. The outgoing batch is then established **against the phase actually declared, once it is known**, on the two motives below, exactly as between two real phases. Reporting a zero balance here because "the previous value was neutral" is the mistake: it would let a suite written under no declared bias escape the only pass that would ever re-examine it.

    When there is one, report the movement **as one thing**, because a suite's centre of gravity moving is a single event and not two unrelated lists.

    **State what the switch changed in the matrix, per domain-level in force - the `cell` line, and it is not optional.** A phase switch is a change of classifying authority (`@../references/decision-matrix.md`): the required proof and the ceiling both move, per level, and those two numbers are what makes the outgoing and incoming counts readable rather than asserted. Report each level's cell **before and after**, `—` included - a level that was requiring nothing and now requires an anchored proof is the whole reason a gap became incoming, and a report giving the count without the cell asks the user to consent to an arithmetic whose premise is off-screen.

    - **Outgoing** rests on **two distinct motives**, and needs both. The heuristics of `02-audit` alone never read phase at all: run on their own, they would flag the same duplicates and getters on any phase, contributing nothing specific to *this* switch. A model-shape test written in `scaffolding` - neither a duplicate, nor trivial, nor a getter - marks the edge of what heuristics alone reach, which is why `phase-obsolete` had to be named as a second, distinct motive rather than folded into the first: without it, nothing phase-specific would ever leave through this batch, heuristics alone being blind to why a test stopped earning its place.
      - *Inherited motive* - `02-audit`'s value heuristics (duplicate, trivial, getter/setter), simply moved up the ranking by the entering phase. Taken as they are, redefined nowhere.
      - *Motive proper to the switch - **phase-obsolete***: a test whose **only** justification is a criterion the outgoing phase raised and the entering phase lowers. It qualifies only when **no other criterion holds it**: not consequence (money, authorisation, persistence, deletion), not a dependency on an external contract, not being the sole net on its subject. A test held by any one of those three stays, whatever the switch. This is the single removal motive this action adds, and those three exclusions are its bounds. The phase still decides nothing about **tier**: it qualifies a removal, never a classification.
    - **Incoming** is obtained by re-running `04-strengthen`'s ranking with the new phase in force - never by reimplementing it here. Each confirmed gap goes back through `01-write`, **one at a time**, with the number constraint re-evaluated between each, exactly as `04-strengthen` already routes them.
    - **Net balance** is a **finding, never a target.** No phase requires a negative balance - `sustaining` expects one, it does not demand it. A suite that comes out of a switch larger is not a failure.
    - **`sustaining` carries the exception to its own negative balance:** external boundaries are excluded from every removal batch and remain the one legitimate motive for addition. It is the phase where nothing internal moves any more while external contracts keep moving; stripping their only net at that exact moment would be the worst possible timing.

11. **The removal batch - consent bears on a rule, and the rule is read in full.** A batch is composed of four things, all four required:
    - its **selection criterion**, spelled out in one sentence - what every member of the set has in common;
    - the **count per rejection motive**;
    - a **representative sample**, shown on screen;
    - the **exhaustive list**, shown **in full, in the same turn** - the same standard `MEASURED FACTS` and `PROPOSED STRATEGY` hold, shown as blocks in full rather than referenced by path. It is also written to `<project_path>/aidd_docs/tasks/<date>-control-removal-batch.md` **before** the question is put, so a refusal or an interruption still leaves a durable record of what was proposed - but that file is not what the user reads to consent, the list shown on screen is.

    **`excluded` is rendered per category, and a bare count is not a rendering.** Each category states its count *and* what it holds: the test, and the ground on which it was held out. A line reading `sole net 3` tells the user how many tests were spared and nothing about whether the sparing was right - and this is the block whose whole purpose is that the user can contest the criterion before consenting to it. Four categories, never three: the three substantive exclusions of the paragraph below, plus the tests **one of the two motives failed to qualify**, which are held out on a different ground entirely and would otherwise disappear into a total nobody can decompose.

    **Refusal is en bloc, unconditional, and triggers no fallback** - in particular no per-item confirmation, which would walk around the refusal one test at a time.

    Excluded from any batch, whatever the switch: tests covering an external boundary, tests some consequence criterion holds by other means, tests that are the sole net on their subject, and every test **one of the two motives fails to qualify** - inclusion needs both to hold at once, never either alone; a test the inherited heuristics do not flag is excluded on that fact alone, whatever `phase-obsolete` would otherwise say of it. Sitting on a reading axis the phase lowers is not, by itself, a reason to delete anything - and neither is a cell requiring no proof at all, whether because its `phase x domain-level` cell is a `—` on `@../references/decision-matrix.md` or because the test sits outside every domain established so far (out-of-domain): **a cell without requirement qualifies no removal, it only ever weighs a ranking.** When nothing qualifies, say so **in the block itself**: `REMOVAL BATCH` is rendered whenever a switch is reported, with `outgoing : 0` and one sentence naming what was examined and which bound emptied the set. Suppressing the block in the empty case is the failure this sentence exists to prevent - an absent block and a block nobody produced read identically, and only one of the two is a result. An empty batch is a legitimate outcome and is reported as one, never dressed up as a hollow one.

12. **Never overwrite in silence.** Adding is the default behaviour. An existing section is replaced only after its difference has been shown and that specific replacement explicitly validated - a hand-written paragraph is the most valuable content in the file, precisely because no tool produced it.

13. Report the result: what was written, by which route, what was removed or left in place, and what remains open.

## Constraints

- A document not yet aligned keeps being classified as settling no tier by `05-stats` - `empty-template` or `filled-but-undeciding`. That is not a detection failure: it is the state this action exists to change, and it must stay visible until it does. **Carry the shape through, do not collapse it to "template-shaped"** - step 2 consumes `05-stats`'s classification rather than recomputing it, so whichever of the two it named is the only one this action can report.
- **Outside a phase switch, this action proposes no test, ranks no gap and deletes nothing.** When a plain alignment reveals the suite itself needs work, name `02-audit` or `04-strengthen` and stop. A switch is the one occasion where it does more than describe - and even then it originates nothing: the outgoing motives come from `02-audit`, the incoming ranking from `04-strengthen`, and every addition goes back through `01-write`. It reports the movement; it does not invent either of its halves.
- The phase is written into the document as a **declaration by the project**, in the strategy block - never as a fact in the measured block. This skill never deduces it and therefore never has one of its own to write: what reaches the file is the user's answer, presented back for validation as the decision it is. A phase written down as a measured fact would be read by every later run as authority, and nobody would ever be asked again.
- This is the action that ends the questioning. A phase resolved by asking is worth one run; once it is declared in the document, every action reads it from there. When the user declines to declare it, say plainly that the question will be put again at the next run - that is the cost of not writing it down, and it is theirs to accept.

## Test

**Referred by file, never by row number.** A row list goes stale on the next renumbering of a suite, and a stale list is worse than none - it points a reader at a scenario that now tests something else. Each suite below declares the actions it targets in its own opening paragraph; that declaration is the authority for this list, and it is the thing to re-read when a suite is added or re-scoped.

Covered by `../evals/align-write-scenarios.md`, `../evals/domains-scenarios.md`, `../evals/confirmations-scenarios.md`, `../evals/phase-scenarios.md` and `../evals/chaining-scenarios.md`.

`align-write-scenarios.md` is the anchor suite - this is the only action in the skill that touches disk, and that suite exists for its write paths. `domains-scenarios.md` owns the ledger's content, `confirmations-scenarios.md` the block-by-block gate, `phase-scenarios.md` the phase-switch batch, `chaining-scenarios.md` the graph position.

Run: `overcode:behave 02-run <suite> <fixture>`.
