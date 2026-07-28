# Align

Audit the gap between what a project's test strategy document *says* and what the project *does*, then propose the document's update in two strictly separated blocks: the facts this skill measured, and the strategy the project has to decide.

Mirror image of `05-stats` in direction rather than in kind: `stats` reads the situation and stops, `align` gives its findings somewhere to go. It is the only action of this skill that writes into the target project's own documentation, and it does so under the narrowest terms in the skill - see the transversal rule in `SKILL.md`.

## Inputs

- `project_path` (required) - absolute path to the target project root
- `scope` (optional, default: whole project) - a subdirectory or glob to limit the measurements. **`scope` designates one universe, here as everywhere in this skill: the source code and the tests that match it**, resolved **symmetrically** in either direction - the same perimeter `05-stats` measures. No action has a universe of its own.
- `domain` (optional) - a functional domain declared by the project (`auth`, `payment`). It **orders what the audit reports first; it never bounds what the audit covers** - an alignment run on part of the project and presented as an alignment would put a half-true document in the file. Mutually exclusive with `scope` - given both, stop and ask which was meant (`SKILL.md`, *Parameters*).
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
  | undeclared area   | src/notifications/ | -                    | 14 files under no declared domain and under no fallback |

MEASURED FACTS          (authority: control - proposed as written)
  <the block, in full, exactly as it would be inserted>

PROPOSED STRATEGY       (authority: the project - proposed, never applied by default)
  <the block, in full, exactly as it would be inserted>

PHASE SWITCH            (only when the resolved phase differs from the declared one)
  from -> to  : <declared phase> -> <resolved phase>
  outgoing    : <n> tests, by motive: inherited heuristics <n>, phase-obsolete <n>
  incoming    : <n> gaps the entering phase raises, each routed through 01-write
  net balance : <±n> on a suite of <total> - <the displacement, in one sentence>

REMOVAL BATCH           (only when outgoing > 0 - one consent, or refusal en bloc)
  selection criterion : <one sentence - what every member of this set has in common>
  by rejection motive : <count per motive>
  sample              : <a representative handful, shown on screen>
  exhaustive list     : <path to the file, written before the question is put>
  excluded            : external boundaries <n>, held by consequence <n>, sole net <n>

WRITE PATH
  route       : aidd-context project-memory skill | direct write (fallback)
  consequence : <what this route does, and what it does not do>
```

Nothing is written as part of producing this output.

## Process

1. Resolve `project_path` and `scope`. Resolve the project **phase** per `@../references/phase-framework.md` - by renvoi, not by re-deriving it.

2. **Run the gap audit on `05-stats`'s production, never on a recomputation.** `05-stats` already establishes the authority in force, the document's readability, the tooling actually wired, the volume by tier, the observed order of the reading axes and the resolution of the declared domains. This action consumes those results; it redefines none of them. Two sources of truth for the same measurement will diverge, and the one that diverges silently is the one nobody runs.

3. Classify every gap into exactly one of five natures. The distinction is what keeps the two blocks apart later: the first two are facts, the third is a question the project alone can answer. The last two are **both at once**, and are split accordingly - the measurement (a term matched nothing, an area is under no domain) goes into `MEASURED FACTS`, the response to it goes into `PROPOSED STRATEGY`. Splitting them is what stops the skill from writing a decision under its own authority:
   - **Missing fact** - true of the project, absent from the document (an E2E tool in use and never named, an external boundary nobody wrote down).
   - **Stale fact** - stated in the document, no longer true of the project (a runner that was replaced, a threshold that moved, a plan that was carried out or abandoned).
   - **Missing decision** - no line of the document settles something this skill is nonetheless forced to settle at every run: the phase, the tier vocabulary, what the project deliberately refuses to test, the number constraint it holds itself to, the domains it recognises. This is not a defect in the document; it is the question the document has not been asked yet.
   - **Unresolved domain** - the document declares a domain that resolves to no file. Two readings, and this action decides neither: the domain is spelled differently in the code than in the document, or it does not exist yet. Report the term, both readings, and let the user say which. It is classified apart from a stale fact on purpose - a stale fact is known to be false, this one is only known to be unmatched.
   - **Undeclared area** - a part of the code that no declared domain matches and that the generic fallback does not reach either. It is **not** a defect by itself: a project legitimately declares only the domains it wants prioritised, and the rest is analysed at neutral weight. It becomes a finding when the area is substantial, and it is reported as a question - is this an area the project chose not to name, or one it forgot? Never as an area to be covered.

4. **Document absent.** When no `testing.md` (or project-level equivalent) exists, produce the audit anyway - everything is a missing fact - then offer, as an explicit choice, to create the document or to abstain. **Never create it by default.** A project that has never written a test strategy may have decided exactly that, and a file appearing unrequested in `aidd_docs/memory/` is a decision taken on the project's behalf. When the user abstains, the audit stands as the output and the run ends there.

5. **Build the `MEASURED FACTS` block.** It carries only what this skill is itself the source of:
   - the test runner actually wired, and the established E2E tool;
   - whether a coverage gate is configured **and invoked**, or configured and inert;
   - volume by tier, and the observed order of the reading axes, with the approximation declared as `05-stats` declares it - and, under `default` or `undetermined`, with no expected order to compare it against, said in words rather than left blank;
   - the **resolution of each declared domain**: how many files it matched, and which terms matched nothing;
   - the **inventory of external boundaries** - third-party integrations found in the manifest and in the source, and for each one whether any test references it or not.

   That inventory is the most perishable fact in the block, and it is what makes a second run of this action worthwhile on a project whose own code has not moved: a third-party SDK major can shift, or an integration can be added by a dependency bump alone, and no internal signal fires. Nothing enters this block that the skill cannot measure - a fact it merely believes is a strategy in disguise.

6. **Build the `PROPOSED STRATEGY` block.** It carries what the project has to decide and the skill only drafts: the declared phase, the tier vocabulary, what the project refuses to test, the number constraint, and **the list of domains**.

   The domain list belongs here and nowhere else, because it is the one thing in the whole model no measurement can produce: which functional parts a product has is a statement about the product, not about its repository. The skill may *propose* candidates from what it observed - recurring directory names, identifier families - and it proposes them as candidates, explicitly, never as an inventory it discovered. The project keeps the last word on each, including the word "no". **Declaring no domain is a valid answer**, and it is recorded as such: the generic `critical journeys` fallback then applies, and the question stops being re-asked.

   Include here the response to every *unresolved domain* and *undeclared area* found at step 3 - rename the term, add the domain, or record that the area is deliberately unnamed. Recording the deliberate choice matters as much as the other two: it is what stops the next run from re-raising it.

   `default` is proposed here on the same footing as any other phase value. When a project keeps being asked its phase run after run and does not want to answer, the answer available to it is not silence - it is `default`, written down, which declares neutrality as a choice rather than leaving it as an omission. Say that plainly whenever the provenance is `unanswered`; the point of the value is lost if nobody is told it exists. And it is the provenance that triggers this, not the value - a `default` that arrived by an answer rather than by a declaration needs exactly the same offer, since nothing was written down either.

   On that last one, propose a **density rather than an absolute cap** (`@../references/test-density.md`), and propose it as the project's own measured median - a number the project can recognise, not one this skill invented. A cap is a number a project outgrows without noticing, and the day it does, the only options it leaves are raising it or ignoring it. A density stays meaningful as the codebase grows because it grows with it. The project may still choose a cap - it is the project's decision, and a declared cap wins - but it should choose it against the alternative, so state both.

   The density's **known blind spot belongs in this block too**, when the audit found one: a file whose cases are data-driven (a regex, a table, a schema) reads as an outlier while its tests genuinely discriminate. Writing that down here is what stops the next run from re-flagging it, and it is the one place the project can record it as its own judgement rather than as a measurement error. It is proposed as **complete prose, in the document's own language**, so the user validates a text rather than an intention - and it is validated **line by line**. Nothing here is applied by default, and a block the user leaves unanswered counts as refused.

7. **Approve each block independently.** Refusing the strategy does not withdraw the facts; refusing the facts does not withdraw the strategy. An all-or-nothing gate would make the action unusable in the exact case it exists for - a project that accepts being described and is not ready to commit to a doctrine.

8. **Write path.** When `aidd-context`'s project-memory skill is installed, **delegate to it**: it owns `memory/`, it carries its own approval gate, and it does one thing a direct write does not - it resynchronises the AI-context files that embed the project memory. In the version installed at the time of writing (`1.0.1`) that skill is `aidd-context:05-learn`, chaining `01-scope` (analyse, categorise, **user approval**) → `02-write` (create or update the `memory/` files) → `03-sync` (refresh the AI-context block). Resolve it by that role, never by that number - the naming has changed across `aidd-context` majors, and a pinned action is how this action silently stops delegating. Enter through its scoping step so its own gate applies, and make sure its sync step runs. **A silent sync is not a successful sync.** That step legitimately has nothing to do when the AI-context files already list the document, and it then exits with no output at all - indistinguishable from a failure that swallowed its own error. So do not take a clean exit as proof: open the AI-context file and check the memory block actually names the document. Report which of the two it was - resynchronised, or already up to date. When it is absent, fall back to a **direct write**. Either way, **announce the route taken in the output, and say what the route does not do**: a fallback that silently skips resynchronisation leaves the AI-context files stating the old strategy, which is worse than not writing at all.

9. **Fidelity rule - the delegate is not a scribe.** The project-memory skill analyses, categorises and reformulates what it retains before writing; nothing in its contract promises it inscribes a supplied text **verbatim**. The "validated line by line" guarantee would therefore break in silence. So: hand the approved text over as **literal content to be inscribed verbatim**, not as material to analyse; then **re-read the written file** and compare it, line for line, to the approved text. Any divergence - a reformulation, a section moved, a line absorbed into another - is **reported to the user, and never corrected on the spot**. It is another plugin's document; silently rewriting it would recreate the very problem delegation avoids.

10. **Phase switch - detect it, never assume it.** A switch exists when the resolved phase **differs from the one declared in the document**, or when the user explicitly overrides it. Comparison, not supposition: a project whose document declares nothing is not switching, it is declaring for the first time, and that is step 6's business - **with one exception, which the third bullet below states in full: a prior `undetermined` switches like any other phase.** A document that declares nothing and a project that has been running on `undetermined` are the same repository seen twice; what separates them is that the question has already been put and left unanswered, and an answer given now is a switch, not a first declaration.

    **`default` and `undetermined` are not the same case here, and treating them alike is the error to avoid.** Both weight the ranking neutrally, but only one of them has decided anything.

    - **`default` stays out of the switch machinery - by consent, not by mechanics.** A project declaring `default` has just taken a decision; following it with a batch of tests to qualify obsolete would contradict that choice at the instant it is made. So: moving **to** `default` is reported as a declaration - net balance zero, no removal batch at all. Moving **from** `default` to a real phase gets the entering phase's incoming ranking through `04-strengthen` and **an empty outgoing set**: nothing was written under a bias that could now be obsolete.
    - **`undetermined` has decided nothing at all, and switches like any other phase as soon as one is declared.** It is not a neutrality the project chose, it is a question left unanswered - and the answer, when it comes, is a first real phase taking effect. The outgoing batch is then established **against the phase actually declared, once it is known**, on the two motives below, exactly as between two real phases. Reporting a zero balance here because "the previous value was neutral" is the mistake: it would let a suite written under no declared bias escape the only pass that would ever re-examine it.

    When there is one, report the movement **as one thing**, because a suite's centre of gravity moving is a single event and not two unrelated lists.

    - **Outgoing** rests on **two distinct motives**, and needs both. The heuristics of `02-audit` alone would produce an empty batch by construction: a model-shape test written in `scaffolding` is not a duplicate, not trivial, not a getter, and no existing heuristic would ever qualify it.
      - *Inherited motive* - `02-audit`'s value heuristics (duplicate, trivial, getter/setter), simply moved up the ranking by the entering phase. Taken as they are, redefined nowhere.
      - *Motive proper to the switch - **phase-obsolete***: a test whose **only** justification is a criterion the outgoing phase raised and the entering phase lowers. It qualifies only when **no other criterion holds it**: not consequence (money, authorisation, persistence, deletion), not a dependency on an external contract, not being the sole net on its subject. A test held by any one of those three stays, whatever the switch. This is the single removal motive this action adds, and those three exclusions are its bounds. The phase still decides nothing about **tier**: it qualifies a removal, never a classification.
    - **Incoming** is obtained by re-running `04-strengthen`'s ranking with the new phase in force - never by reimplementing it here. Each confirmed gap goes back through `01-write`, **one at a time**, with the number constraint re-evaluated between each, exactly as `04-strengthen` already routes them.
    - **Net balance** is a **finding, never a target.** No phase requires a negative balance - `sustaining` expects one, it does not demand it. A suite that comes out of a switch larger is not a failure.
    - **`sustaining` carries the exception to its own negative balance:** external boundaries are excluded from every removal batch and remain the one legitimate motive for addition. It is the phase where nothing internal moves any more while external contracts keep moving; stripping their only net at that exact moment would be the worst possible timing.

11. **The removal batch - consent bears on a rule, not on a scroll.** At the scale where a batch earns its keep, several hundred lines are no more readable than a counter. So a batch is composed of four things, all four required:
    - its **selection criterion**, spelled out in one sentence - what every member of the set has in common;
    - the **count per rejection motive**;
    - a **representative sample**, shown on screen;
    - the path to a file holding the **exhaustive list**, written **before** the question is put and offered for reading explicitly.

    **Refusal is en bloc, unconditional, and triggers no fallback** - in particular no per-item confirmation, which would walk around the refusal one test at a time.

    Excluded from any batch, whatever the switch: tests covering an external boundary, tests some consequence criterion holds by other means, tests that are the sole net on their subject, and every test **neither of the two motives qualifies**. Sitting on a reading axis the phase lowers is not, by itself, a reason to delete anything - and neither is sitting outside every declared domain, which weights a ranking and qualifies no removal. When nothing qualifies, say so - an empty batch is a legitimate result and is reported as one, never dressed up as a hollow one.

12. **Never overwrite in silence.** Adding is the default behaviour. An existing section is replaced only after its difference has been shown and that specific replacement explicitly validated - a hand-written paragraph is the most valuable content in the file, precisely because no tool produced it.

13. Report the result: what was written, by which route, what was removed or left in place, and what remains open.

## Constraints

- A document not yet aligned keeps being classified as settling no tier by `05-stats` - `empty-template` or `filled-but-undeciding`. That is not a detection failure: it is the state this action exists to change, and it must stay visible until it does. **Carry the shape through, do not collapse it to "template-shaped"** - step 2 consumes `05-stats`'s classification rather than recomputing it, so whichever of the two it named is the only one this action can report.
- **Outside a phase switch, this action proposes no test, ranks no gap and deletes nothing.** When a plain alignment reveals the suite itself needs work, name `02-audit` or `04-strengthen` and stop. A switch is the one occasion where it does more than describe - and even then it originates nothing: the outgoing motives come from `02-audit`, the incoming ranking from `04-strengthen`, and every addition goes back through `01-write`. It reports the movement; it does not invent either of its halves.
- The phase is written into the document as a **declaration by the project**, in the strategy block - never as a fact in the measured block. This skill never deduces it and therefore never has one of its own to write: what reaches the file is the user's answer, presented back for validation as the decision it is. A phase written down as a measured fact would be read by every later run as authority, and nobody would ever be asked again.
- This is the action that ends the questioning. A phase resolved by asking is worth one run; once it is declared in the document, every action reads it from there. When the user declines to declare it, say plainly that the question will be put again at the next run - that is the cost of not writing it down, and it is theirs to accept.

## Test

Covered by `../evals/align-write-scenarios.md` (S4, S6, S7, S8, S9, S10, S11, S17).
Run: `overcode:behave 02-run <suite> <fixture>`.
