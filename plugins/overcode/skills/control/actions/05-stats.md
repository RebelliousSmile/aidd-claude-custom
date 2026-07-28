# Stats

Read-only snapshot of a project's test situation in one screen: how many tests exist, of which kind, and **which test strategy is actually in force** - the project's own, or this skill's generic default.

Writes nothing, proposes nothing, deletes nothing. It is the **entry point** of the skill: the action a user runs before deciding whether they need `audit`, `strengthen`, `configure` or `align` (`SKILL.md`, *Action chaining*).

## Inputs

- `project_path` (required) - absolute path to the target project root
- `scope` (optional, default: whole project) - a subdirectory or glob to limit the counts. **`scope` designates one universe, here as everywhere in this skill: the source code and the tests that match it**, resolved **symmetrically** in either direction. No action has a universe of its own.
- `domain` (optional) - a functional domain declared by the project (`auth`, `payment`). It **orders the reading; it never bounds the counts** - a snapshot whose figures silently excluded part of the project would be the one thing this action must never produce. Mutually exclusive with `scope` - given both, stop and ask which was meant (`SKILL.md`, *Parameters*).
- `phase` (optional) - overrides the resolved project phase for this run only

## Outputs

```
PHASE
  value       : scaffolding | hardening | production | sustaining | default | undetermined
  provenance  : argument | declared <path> | answered <this run only> | unanswered
  question    : <the question put to the user, and the observations offered with it>
                (present whenever provenance is `answered` or `unanswered`; absent otherwise)
  divergence  : <argument vs declared, when both exist and differ> | none
  excluded    : <every file the phase set aside, each with the phase motive that
                 set it aside - the phase may narrow the universe, never in silence>
              | none - this phase narrows nothing
  axes        : expected <order for this phase> / observed <order measured>
              | none expected under `default` - neutrality was declared, so no order is
                predicted; the observed one is reported alone
              | none expected under `undetermined` - the phase is unknown, so nothing
                predicts an order; the observed one is reported alone
                (classification is approximate: tier + role of the source file exercised + churn)
  domains     : <declared domains, and for each: resolved to <n> files | term matched nothing>
                (absent when the project declares none - the generic `critical journeys`
                 fallback applies and is named as such)
  unmatched   : <n> source files matched by no domain in force - still in the analysis,
                 ranked last <one line each: <path> - nearest term that failed to
                 recognise it> | none - every source file was matched
                (absent only when no domain is in force at all - neither declared
                 by the project nor given as an argument: there is then no term to fail)

STRATEGY
  authority   : project doc <path> | generic default (references/decision-framework.md)
  readability : actionable | empty-template | filled-but-undeciding | absent
                (the last three fall back to the default tier mapping - name which one,
                 they call for opposite corrections)
  tiers       : <tiers named by the authority in force, and the mapping applied if any>
  budget      : <explicit test-count limit from the project doc> | null (the constraint in force is the density below)
  density     : median <ratio> over <n> files carrying a matched case (<n> unmatched, excluded)
              | insufficient population (<n> files carry a test - no median is defensible)
              | not measurable - no coverage report, so no denominator (-> 03-configure)
              | not measurable - report present but in line mode, no branch data
                (-> 03-configure: one runner flag, not coverage from scratch)
  outliers    : <n> past 3x the median | none
              <one line each: <path> <ratio> - refactoring signal (top decile of branch points) | low-value tests (-> 02-audit)>
  matching    : <how test cases were mapped to source files> - <n> unmatched
  declared    : <any coverage percentage the doc states, verbatim - reported, never used as a target>
  mechanics   : <language plugin> testing pivot | none (stack-agnostic run)

VOLUME
  contract    : <n> files / <n> cases
  e2e         : <n> files / <n> cases
  ratio       : <n> test files for <n> source files
  counting    : cases (pivot test-count command) | files only (no count command available)

TOOLING
  runner      : <command actually wired in the project>
  coverage    : gate configured and invoked in <CI/hook> | configured but never invoked | none
  e2e tool    : <established tool - never a replacement candidate>

FLAGS
  - <one line per divergence or gap, each naming the action that addresses it>
```

## Process

1. Resolve `project_path` and `scope`.
1-bis. **Phase provenance** - resolve the project phase per `@../references/phase-framework.md`, which **never deduces it**, and report the four possible provenances distinctly: **argument** (given explicitly for this run), **declared** (cite the document path), **answered** (the user was asked before anything was ranked, and answered - good for this run only, recorded nowhere), **unanswered** (the question was asked and left unanswered).

   **`value` and `provenance` are two different lines and never collapse into one.** The value says *which phase*, the provenance says *where that came from*, and only one pairing is forced: provenance `unanswered` always carries value `undetermined`, and vice versa. Every other combination is free - `default` can arrive by argument, by declaration or by an answer, exactly like `production`. The provenance axis is deliberately worded as the `answered` / `unanswered` pair, so that the axis names itself rather than borrowing the name of a phase value it happens to imply once.

   When an argument and a declaration both exist and differ, report the divergence - the argument wins for this run, the declaration stays in the file. An answer given in conversation is never written down by this action, and never reported as if the project had declared it: `06-align` is what turns it into a declaration.
1-ter. **Reading-axis order** - compare the expected ordering of the axes for the resolved phase (`foundations` and the project's declared domains, or the generic `critical journeys` fallback, per `phase-framework.md`) against the observed one. Report **orders, never shares**: no percentage is produced here, and the classification of an existing test onto an axis is an approximation, declared as such next to the comparison.

   **Under `default` and `undetermined` there is no expected order, and the line says so in words.** Neither phase predicts one - `default` because neutrality was chosen, `undetermined` because nothing is known - so the observed order is reported alone. An empty expected side of a comparison reads as a measurement that failed, which is the opposite of what is true here.

1-quater. **Domain resolution** - resolve every domain **in force** to code per `phase-framework.md` and report, per domain, how many files it matched. A domain is in force when the project declares it *or* when it arrives as the `domain` argument: **provenance changes what the run may write down, never how the term resolves.** An argument orders this run and is recorded nowhere - only `06-align` turns it into a declaration - but while it is in force it resolves, reports and leaves a residue exactly like a declared one. Suspending the resolution because the project never wrote the term down would make the argument silently inert, which is the one outcome a caller cannot detect. **A term that matched nothing is reported as such**, never omitted: an unresolved domain and a domain with nothing to report look identical in a snapshot, and only one of the two is good news.

   And the symmetric half, which is the one that bites: **report the residue - every source file no declared domain matched.** A domain prioritises, it never restricts, so that residue stays in the analysis and is only ranked last; it is never excluded, and never silently dropped. Name, for each, the nearest term that failed to recognise it. The reason is the failure mode of term matching: searching `Login` and `Register` finds `LoginForm.tsx` and misses `SessionController`, and the missed zone does not surface as excluded - it surfaces as a zone with no gap, which is the exact opposite of the truth. A phase excludes by rule and a rule can be re-read; a term match fails silently, so only the trace makes it visible. That trace has a second use: it feeds `06-align`'s drift detection, where a domain vocabulary that stopped matching the code is what drift looks like.
2. **Strategy provenance** - the point of this action. Look for the project's documented strategy at `<project_path>/aidd_docs/memory/testing.md` (AIDD memory convention, generated by `aidd-context`'s project-memory skill - refer to the document, not to a pinned action name, since those change across `aidd-context` majors) or an equivalent project-level document naming its own tiers. Report which one is in force, by path, and never merge the two silently: if the project has no document, say the generic default is in force, and say so as a finding, not as a neutral state - it means `budget` is structurally `null` and no tier vocabulary is owned by the project.
3. **Strategy readability** - a `testing.md` existing is not the same as a `testing.md` this skill can act on. The canonical AIDD template does not speak this skill's tier vocabulary, and its shape varies by `aidd-context` major (older ones list test types and a "desired coverage percentage"; newer ones use Strategy / Tools / Conventions / Run with unfilled placeholders). Classify the document as:
   - **actionable** - it names tiers, or states what must be tested versus not, in terms this skill can map to `contract` / `e2e` / `skip`;
   - **empty-template** - untouched placeholders, the generic template as `aidd-context` generated it. Nothing was filled;
   - **filled-but-undeciding** - richly written, no placeholder left, and settling no tier all the same: it lists test *types*, tools and conventions without ever saying what deserves a test. This is the shape that misleads, because it reads as a strategy in force and governs nothing;

   The last two both fall back to the same mapping - unit and integration -> `contract`, end-to-end -> `e2e` - and the tier decision is flagged as still generic in both. **Report which of the three shapes was met, never the fallback alone** (`SKILL.md`, *Transversal rules*): the correction differs, and reporting the third as "template-shaped" sends the project to fill placeholders it already filled. This classification is what `06-align` consumes at its step 2 rather than recomputing, so a shape collapsed here is a shape that action can never recover.
   - **budget** - populate it only from an explicit test-count limit. A coverage percentage is **not** a budget and never becomes one - report it verbatim as declared, outside the `budget` line.

3-bis. **The universe comes from the source glob, never from the coverage report.** Establish the set of files this snapshot reasons over from the pivot's **Source glob & exclusions** (`@../references/pivot-contract.md`), or from the project's own directory convention when no pivot is available - the same universe `04-strengthen` ranks. The coverage report then **adds detail to that universe; it never defines it.** Reports routinely omit files no test ever imports, so a universe read off the report is a universe with its own gaps already deleted from it - and a snapshot whose figures silently excluded the untested part of the project is the one thing this action must never produce. Report the two counts side by side whenever they differ: files in the universe, and files the report knows about.

3-ter. **Density** per `@../references/test-density.md`. A `null` budget is not an absence of constraint, and this is the line that makes that true: compute the project's own distribution from its coverage report, report the median, and list every file past **3× that median** with **which of the two readings applies** - top decile of branch points means the code branches too much (a refactoring signal, and this skill proposes no refactoring), otherwise it means tests with no detection power (which is `02-audit`'s subject, named as such and judged no further here).

   Two things are reported and not glossed over. **The matching rule**, with how many test files it failed to map to a source - a ratio built on a naming convention carries that convention's error rate, and an undeclared approximation is how a number acquires authority it did not earn. And **`insufficient population`** when too few files carry a matched case: emit no median and no outlier rather than a median over three points. That is the ordinary state of a small or young project and is reported as a fact about the measurement, never as a finding about the suite.

3-quater. **Coverage is read as `covered`/`total`, never as a percentage alone.** Whenever a figure comes out of the coverage report - to feed the density denominator, or to be reported at all - carry both terms. A percentage alone loses the population it was computed over, and that loss is not cosmetic: **a file with no branch point reports 100 % branch coverage while being entirely untested**, because the ratio is `0/0` rounded up by the tool. Read that way, the most dangerous file in the snapshot reads as the safest. Report `covered`/`total` per file whenever a per-file figure is emitted, and flag any `0/0` explicitly as *no branch to cover - says nothing about whether the file is tested*. This bound holds regardless of the resolved phase.
4. **Mechanics provenance** - detect the active language plugin and whether it ships a `testing` pivot (`@../references/pivot-contract.md`). Report found/absent; absent is not an error, it only means the counts and tooling lines are stack-agnostic.
5. **Volume** - count with the pivot's test-count command when available, which gives test **cases**; otherwise count test **files** matching the glob, and say explicitly that the count is file-level. Split contract vs e2e by the pivot's respective globs, else by the project's own directory convention. Add the source-file ratio using the pivot's source glob when it provides one.
6. **Tooling** - report the runner command actually wired in the project (not the one the docs claim), whether a coverage gate exists **and is invoked** by something that runs, and the established E2E tool. Never evaluate the E2E tool choice.
7. **Flags** - one line per divergence found, each naming the action that handles it. Report only what the snapshot itself proves:
   - no documented strategy -> the generic default is in force, and no **cap** is declared; the number constraint still applies, as the density (see `write`);
   - density outliers reported -> name the action each one routes to, and route nothing here: refactoring signals are stated and left with the user, low-value readings go to `02-audit`;
   - `testing.md` present but settling no tier -> it exists without governing anything; the fix is to fill it in the project's own terms, through whichever `aidd-context` project-memory action owns that document in the installed version - this skill never writes it. **Name the shape** (`empty-template` or `filled-but-undeciding`): the first needs the placeholders filled, the second needs a decision the document never took, and offering the first to a project that already wrote three pages reads as a run that did not open the file;
   - documented strategy naming a tool the project does not actually have installed, or vice versa -> stale document;
   - coverage gate declared but invoked by nothing -> `03-configure`;
   - e2e count comparable to or above contract count -> inverted pyramid, the most expensive tier is carrying the suite (see `02-audit`);
   - source-to-test ratio with large untested areas -> `04-strengthen`;
   - observed axis order matching an earlier phase's expected order better than the resolved phase's -> **centre of gravity left on the previous phase**: the suite still protects what the product used to be. Deduced from comparing orders, never from a stored history - `control` keeps no state between runs. Not raisable under `default` or `undetermined`, which predict no order to compare against;
   - a declared domain resolving to no file -> either the domain is named differently in the code than in the document, or it does not exist yet. Report the term and both readings; decide neither -> `06-align`;
   - source files matched by no domain in force -> the vocabulary no longer covers the code. Report the residue with the term that failed on each; the same trace is what `06-align` reads as drift. Not a finding about the suite, and never an exclusion -> `06-align`;
   - a per-file coverage figure of `0/0` reported as 100 % -> a file with no branch point, which the tool scores as fully covered while nothing exercises it. Report both terms and say so -> `04-strengthen`;
   - provenance `unanswered` (so value `undetermined`), or **any** value whose provenance is `answered` -> the project's document does not say what phase it is in, and every run will keep asking until it does -> `06-align`. **What silences this flag is the provenance, not the value.** A `default` whose provenance is `declared` raises nothing - the question has been settled, and re-routing it would ask the project to decide what it has already decided. A `default` whose provenance is `answered` raises the flag exactly like any other answered value: it was said out loud and written nowhere, so the next run will ask again. Reading this flag off the value alone is the mistake the two-axis split exists to prevent.
8. Print the snapshot. Stop. Suggesting an action is allowed; running one is not - the user chooses.

## Constraints

- No number in this snapshot is a target. Coverage and counts are reported as **situation**, never as a goal to move; proposing to raise a figure is the job of `04-strengthen`, and only on risk grounds.
- Never infer a strategy the project has not written down. An undocumented project is reported as undocumented, not as "implicitly following the default well".

## Test

Covered by `../evals/measurement-scenarios.md` (S16) and `../evals/align-write-scenarios.md` (S4, S5).
Run: `overcode:behave 02-run <suite> <fixture>`.
