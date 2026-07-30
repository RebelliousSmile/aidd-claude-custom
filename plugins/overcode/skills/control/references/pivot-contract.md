# Testing pivot contract

A language plugin (e.g. `sc-js`, `sc-php`, `sc-python`, `sc-rust`) MAY provide a `testing` capability pivot, nested under its own `sniff`-equivalent skill tree alongside its existing capability categories - e.g. in `sc-js` this lives at `skills/sniff/references/capabilities/tools/testing.md`, next to `tools/vitest.md` and `tools/playwright.md`. Any language plugin may provide one, following the same shape; which ones currently do is read from the tree, never from this document. **A pivot already shipped is not a template to copy field by field**: each writes what its own stack makes legible, in its own language, and they diverge wherever the stacks do - a pivot that reads like its neighbour on a stack that does not work like its neighbour's is the failure this warns against. A pivot is consumed when a language plugin applicable to the target project ships one; the generic, stack-agnostic checks run unrefined for whichever of the project's stacks has none.

## Detecting the applicable language plugins

Use the same detection convention each language plugin's own `sniff`-equivalent action uses for the target project (e.g. inspecting its package manifest or build files) - stack detection is not reimplemented here; whichever language plugins are already installed and applicable are reused.

**More than one may be applicable, and that is the ordinary case.** A Python backend carrying a `frontend/` package manifest, a TypeScript application whose engine is a Rust crate in the same repository, a PHP codebase with a Node lint pipeline - each is applicable to two. Detection therefore returns a **set**, never a winner.

### The pivot follows the file

There is no dominant stack and no election. **Every applicable plugin contributes its own pivot, and a field is resolved by the pivot of the plugin whose stack the file under consideration belongs to.** Electing a single plugin would answer every field of the project out of a stack most of its files are not written in - and the stack that wins a manifest-level election is regularly not the one carrying the code.

Four consequences, stated here so no consumer needs a rule of its own:

- **Enumerations are unions, and they say what they are made of.** The test population is the union of each contributed **Test file glob**; the source universe, the union of each **Source glob & exclusions**. A run names the globs it combined. A file matched by none is not *no test* - it is a file outside the enumerated stacks, and it is reported as such rather than being silently absent, since an under-enumeration reads exactly like a clean population.
- **Nothing is summed across stacks.** Any count, density or coverage figure a consumer renders is rendered per stack, with the stack named. One number over two populations counted by two conventions states a quantity nothing measured.
- **Absence is per stack, and so is the fallback.** A stack whose plugin ships no pivot falls back to that field's documented fallback, and the run states the fallback **for that stack**. *No pivot available* said of a whole polyglot project is false as soon as one of its stacks has one.
- **The same field answered differently by two pivots is not a conflict.** They answer about different files. A consumer needing one answer for the whole project is asking something the project does not have; it renders both, attributed.

Applicability is re-read at the run's `scope`, not fixed once at the project: a plugin applicable to the repository but to no file under `scope` contributes nothing to that run.

## Locating the testing pivot

Canonical filename: `testing.md`. Discovery glob: `**/capabilities/**/testing.md`, run under each applicable language plugin's own root directory - never project-wide, and once per applicable plugin. The parent directory right above `testing.md` is each language plugin's own choice (`tools/`, a dedicated `testing/`, or directly under `capabilities/`); the glob's `**` accepts all of them, so no further convention is needed there.

A language plugin's root directory is resolved the same way as its detection in the section above: the root of whichever installation is actually loaded in the current session - `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/` in normal execution, or the plugin's source root (`plugins/<plugin>/`) when this runs directly against a marketplace repo (e.g. while developing the skill itself). Neither path is hardcoded; the root is located the same way it is already located to detect the plugin.

## Expected shape

A `testing` pivot is a markdown file answering the following questions, one section per field, the section's title stating the field it answers. Every question below must be answerable by reading the pivot alone - none requires opening a consumer to make sense of.

- **Test runner(s)** - What command runs unit/contract tests in this stack? What command, separately, runs E2E tests?
- **Test file glob** - What pattern(s) identify test files in this stack (e.g. `**/*.spec.js`, `**/*_test.py`)? **This population is not guaranteed disjoint from Source glob & exclusions.** Some stacks host tests inside the production file itself, so a same file is both, and the file stops being the unit that separates them. A pivot whose stack is in that case **says so here, and names the real unit** (the in-file construct a test actually lives in). Nothing is required of a pivot whose stack does separate them - the declaration is due only when the disjunction does not hold.
- **Test-count command** - What command or query returns the current number of tests (or test files) in this stack?
- **Coverage command** (optional) - What command produces a machine-readable, **per-file** branch/line coverage report for this stack, and at what path does it write it? It must be a command runnable as-is: a stack's default reporters are frequently human-readable only, so this names the reporter to request explicitly. It must also produce its report **independently of any coverage gate**: a project enforcing thresholds exits non-zero when they are missed, and reading a report is not the same act as passing a gate. Where the command depends on tooling the stack's base toolchain does not ship, name that prerequisite and how to establish its presence (see *Prerequisites* below). When absent, the fallback is a static source-to-test mapping, stated as such - and where **Test file glob** declares source and test non-disjoint, that mapping no longer discriminates in this stack, which the run states instead of ranking on it.
- **Source glob & exclusions** (optional) - What pattern(s) identify the stack's *classifiable production code*, and what is never classifiable in it (build artifacts, generated code, config files, vendored code)? A file matching this glob but absent from the coverage report is **uncovered**, never nonexistent - the source glob defines the universe, the coverage report only enriches it. When absent, the fallback is the project's own directory convention, with the universe stated as approximate.
- **Anchor boundary** (optional) - Where, in this stack, does the boundary fall between an **anchored proof** (crossing the product's real public boundary) and an **internal proof** (staying in process)? Name what does not anchor despite looking like it should (an emulator, a local double of an external service) and what only the real boundary establishes (a rendering default only a real browser applies, a hydration mismatch only a real DOM catches). **This field refines the position of the boundary, in this stack's own concrete terms; it never refines what proof a case is due** - that stays decided elsewhere, unaffected by anything this field says. When absent, the generic anchor table applies unrefined.
- **Risk signals** (optional) - What is structurally high-consequence in this stack (money, auth, persistence, deletion, cross-cutting state), and what structurally is not (framework pass-through, generated glue)? What are this stack's typical **external boundaries** - the SDKs, tag containers, third-party scripts and outgoing API clients a project of this stack commonly depends on - and how are they detected in a manifest? This field supplies stack knowledge only; the criteria that use it are generic and stated elsewhere, so no field here needs to repeat them. When absent, the fallback is reading the project's manifest for dependencies pointing at domains outside its control, with the inventory stated as generic.
- **Known tooling gotchas** - What config bugs are specific to this stack's test tooling (e.g. a coverage-threshold config key that silently disables the gate on an invalid schema)? State each as (issue, detection, fix), as structured keys or as tagged prose - either is acceptable, since this pivot is read as an agent, not as a parser.
- **Domain resolution** (optional) - How does this stack's convention express a **functional domain** in the filesystem and in identifiers: the directory shapes, filename patterns and identifier prefixes a domain typically lands on (e.g. a `pages/<domain>/` tree, a `<Domain>Controller` class, a `*.guard.ts` suffix)? This field carries **no list of domains** - which domains a product has, and at what level, is established elsewhere, by catalogue and confirmation, and would be meaningless to restate per stack. This field answers *how to find them here*, never *which ones exist*, and it only **completes** a domain already named - it never overrides a resolution stated explicitly about the project's own code.

  This is a separate field rather than an extension of **Source glob & exclusions** on purpose: that field is structural (what is classifiable production code at all), this one is semantic (what part of the product a file belongs to). Merging them would put two different natures behind one name.

- **Canonical E2E tool** - What E2E framework does this stack standardize on, if any? Informational only - nothing reads this field as licence to propose replacing it.

## Field names versus section titles

The field names above are this contract's vocabulary, in English. A pivot's actual section titles are written in its own plugin's language (see *Language* below), so they will often not match verbatim - a French-language pivot may carry `Signaux de risque` for **Risk signals**, or `Glob source et exclusions` for **Source glob & exclusions**.

**No shipped pivot is cited here as the example, and that is deliberate.** Naming one is how this section twice acquired a claim about how many pivots exist and what language they are written in - a claim that stops being true the day the next pivot ships, and that nothing in a run ever re-reads. The two rules below hold whether or not any pivot currently diverges: a rule that only applies once an example exists is a rule the first divergent pivot has to discover for itself.

Two rules keep discovery from depending on an improvised translation:

- **One section per field, and its title states the field.** A pivot must not scatter a field across sections, nor merge two fields under one title. Reading the pivot as an agent makes a faithful translation of the field name enough - but a title that renames the concept (`Priorités`, `Ce qui compte`) is not: it makes the field undiscoverable.
- **The pivot declares its own mapping when the titles diverge.** A pivot whose titles are not literal translations carries a short correspondence list, so the binding is stated in the pivot rather than guessed by the reader.

A field that cannot be located is treated as **absent**, and its documented fallback applies - never as an error, and never as an invitation to infer the field from a neighbouring section.

## No field names its consumer

Every field above states what it supplies and, where relevant, its fallback when absent. None states who reads it. A pivot is a contract about a stack, not a map of the skill that happens to consume it - naming a consumer here would tie the pivot's shelf life to that consumer's internal structure, which is exactly the coupling this contract exists to avoid.

## Prerequisites

A field answered by a **command** carries a dependency the pivot cannot resolve: whether that command's tooling is installed is a property of the machine the run happens on, not of the stack. Several stacks ship no coverage reporter with their test runner at all, and even where one exists it is an opt-in package a project may not carry.

The pivot supplies the half it knows: **when a field's command depends on tooling the stack's base toolchain does not ship, the pivot names that prerequisite and the command that establishes its presence.** Knowing what a field depends on is stack knowledge; knowing whether it is installed is not.

The consumer applies the other half: **a prerequisite established as absent means the field is absent for that run** - the field's documented fallback applies, stated as such. A command failing for want of tooling is never rendered as a defect of the measured project; a missing tool and a missing measurement call for opposite corrections, and a run that conflates them sends the reader to fix the wrong thing.

This holds for any field whose answer is a command, not only the coverage one.

## Absence

No pivot existing for a detected language plugin is not an error. Generic, stack-agnostic checks run for that plugin's stack, and the output states which stack went unrefined - never that the run was unrefined, when another of the project's stacks contributed a pivot.

## Language

A pivot is written in whichever language its own language plugin already uses for its other capability files - a single language is not imposed across plugins, only consistency within each plugin's own tree.
