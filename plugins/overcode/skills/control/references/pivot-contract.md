# Testing pivot contract

A language plugin (e.g. `sc-js`, `sc-php`, `sc-python`, `sc-rust`) MAY provide a `testing` capability pivot, nested under its own `sniff`-equivalent skill tree alongside its existing capability categories - e.g. in `sc-js` this lives at `skills/sniff/references/capabilities/tools/testing.md`, next to `tools/vitest.md` and `tools/playwright.md`. Only `sc-js` ships one today; other language plugins could provide one following the same shape, but none is an established example yet. The pivot is consumed when the target project's active language plugin ships one; its generic, stack-agnostic checks run unrefined when none is available.

## Detecting the active language plugin

Use the same detection convention the language plugin's own `sniff`-equivalent action uses for the target project (e.g. inspecting its package manifest or build files) - stack detection is not reimplemented here; whichever language plugin is already installed and applicable is reused.

## Locating the testing pivot

Canonical filename: `testing.md`. Discovery glob: `**/capabilities/**/testing.md`, run under the active language plugin's own root directory - never project-wide. The parent directory right above `testing.md` is each language plugin's own choice (`tools/`, a dedicated `testing/`, or directly under `capabilities/`); the glob's `**` accepts all of them, so no further convention is needed there.

The active language plugin's root directory is resolved the same way as its detection in the section above: the root of whichever installation is actually loaded in the current session - `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/` in normal execution, or the plugin's source root (`plugins/<plugin>/`) when this runs directly against a marketplace repo (e.g. while developing the skill itself). Neither path is hardcoded; the root is located the same way it is already located to detect the plugin.

## Expected shape

A `testing` pivot is a markdown file answering the following questions, one section per field, the section's title stating the field it answers. Every question below must be answerable by reading the pivot alone - none requires opening a consumer to make sense of.

- **Test runner(s)** - What command runs unit/contract tests in this stack? What command, separately, runs E2E tests?
- **Test file glob** - What pattern(s) identify test files in this stack (e.g. `**/*.spec.js`, `**/*_test.py`)?
- **Test-count command** - What command or query returns the current number of tests (or test files) in this stack?
- **Coverage command** (optional) - What command produces a machine-readable, **per-file** branch/line coverage report for this stack, and at what path does it write it? It must be a command runnable as-is: a stack's default reporters are frequently human-readable only, so this names the reporter to request explicitly. It must also produce its report **independently of any coverage gate**: a project enforcing thresholds exits non-zero when they are missed, and reading a report is not the same act as passing a gate. When absent, the fallback is a static source-to-test mapping, stated as such.
- **Source glob & exclusions** (optional) - What pattern(s) identify the stack's *classifiable production code*, and what is never classifiable in it (build artifacts, generated code, config files, vendored code)? A file matching this glob but absent from the coverage report is **uncovered**, never nonexistent - the source glob defines the universe, the coverage report only enriches it. When absent, the fallback is the project's own directory convention, with the universe stated as approximate.
- **Anchor boundary** (optional) - Where, in this stack, does the boundary fall between an **anchored proof** (crossing the product's real public boundary) and an **internal proof** (staying in process)? Name what does not anchor despite looking like it should (an emulator, a local double of an external service) and what only the real boundary establishes (a rendering default only a real browser applies, a hydration mismatch only a real DOM catches). **This field refines the position of the boundary, in this stack's own concrete terms; it never refines what proof a case is due** - that stays decided elsewhere, unaffected by anything this field says. When absent, the generic anchor table applies unrefined.
- **Risk signals** (optional) - What is structurally high-consequence in this stack (money, auth, persistence, deletion, cross-cutting state), and what structurally is not (framework pass-through, generated glue)? What are this stack's typical **external boundaries** - the SDKs, tag containers, third-party scripts and outgoing API clients a project of this stack commonly depends on - and how are they detected in a manifest? This field supplies stack knowledge only; the criteria that use it are generic and stated elsewhere, so no field here needs to repeat them. When absent, the fallback is reading the project's manifest for dependencies pointing at domains outside its control, with the inventory stated as generic.
- **Known tooling gotchas** - What config bugs are specific to this stack's test tooling (e.g. a coverage-threshold config key that silently disables the gate on an invalid schema)? State each as (issue, detection, fix), as structured keys or as tagged prose - either is acceptable, since this pivot is read as an agent, not as a parser.
- **Domain resolution** (optional) - How does this stack's convention express a **functional domain** in the filesystem and in identifiers: the directory shapes, filename patterns and identifier prefixes a domain typically lands on (e.g. a `pages/<domain>/` tree, a `<Domain>Controller` class, a `*.guard.ts` suffix)? This field carries **no list of domains** - which domains a product has, and at what level, is established elsewhere, by catalogue and confirmation, and would be meaningless to restate per stack. This field answers *how to find them here*, never *which ones exist*, and it only **completes** a domain already named - it never overrides a resolution stated explicitly about the project's own code.

  This is a separate field rather than an extension of **Source glob & exclusions** on purpose: that field is structural (what is classifiable production code at all), this one is semantic (what part of the product a file belongs to). Merging them would put two different natures behind one name.

- **Canonical E2E tool** - What E2E framework does this stack standardize on, if any? Informational only - nothing reads this field as licence to propose replacing it.

## Field names versus section titles

The field names above are this contract's vocabulary, in English. A pivot's actual section titles are written in its own plugin's language (see *Language* below), so they will often not match verbatim - a French-language pivot may carry `Signaux de risque` for **Risk signals**, or `Glob source et exclusions` for **Source glob & exclusions**.

**No shipped pivot is cited here as the example, and that is deliberate.** The only `testing` pivot the marketplace currently ships writes these field names in English verbatim, so it diverges from nothing; naming it as the illustration is how this section acquired a claim that stopped being true the day that pivot was rewritten. The two rules below hold whether or not any pivot currently diverges - a rule that only applies once an example exists is a rule the first divergent pivot has to discover for itself.

Two rules keep discovery from depending on an improvised translation:

- **One section per field, and its title states the field.** A pivot must not scatter a field across sections, nor merge two fields under one title. Reading the pivot as an agent makes a faithful translation of the field name enough - but a title that renames the concept (`Priorités`, `Ce qui compte`) is not: it makes the field undiscoverable.
- **The pivot declares its own mapping when the titles diverge.** A pivot whose titles are not literal translations carries a short correspondence list, so the binding is stated in the pivot rather than guessed by the reader.

A field that cannot be located is treated as **absent**, and its documented fallback applies - never as an error, and never as an invitation to infer the field from a neighbouring section.

## No field names its consumer

Every field above states what it supplies and, where relevant, its fallback when absent. None states who reads it. A pivot is a contract about a stack, not a map of the skill that happens to consume it - naming a consumer here would tie the pivot's shelf life to that consumer's internal structure, which is exactly the coupling this contract exists to avoid.

## Absence

No pivot existing for the detected language plugin is not an error. Generic, stack-agnostic checks run, and the output states that stack-specific refinement was unavailable for that run.

## Language

A pivot is written in whichever language its own language plugin already uses for its other capability files - a single language is not imposed across plugins, only consistency within each plugin's own tree.
