---
---

# Testing — governance pivot (PHPUnit)

Structured factual content — an inventory of the stack's test tooling and of the signals the stack makes legible — not code-review patterns, unlike the other files in this directory. That is also why it carries no `paths:`: it does not apply to a family of files, it describes a suite. What this file supplies is stated here; who reads it is not. Applicable as soon as PHP files are present — but the test harness is **never** part of the stack's base toolchain, so unlike some stacks its runner has to be detected, not assumed.

**Section titles** — the contract's field names verbatim, in English. No correspondence list is due: nothing diverges.

**Measurement grounds** — three read-only repositories, because this stack covers two worlds that share almost nothing structurally:

- `kelenaya` — PrestaShop 8 shop, `modules/sc_*`, **nine own modules, each its own git repository**, PHP 8.4.11 / Composer 2.8.2 / PHPUnit 10.5.63. Two suites executed end to end (46 and 29 tests), four more inventoried statically, two with a broken runner.
- `mauceri` — WordPress FSE, **the whole install committed**: 1640 PHP files, 86 of them the project's own, zero PHP test.
- `wp-2026` — WordPress too, but the repository root **is** `wp-content`: 56 PHP files, no `composer.json`, no PHPUnit.

What no ground carried — a coverage driver, Pest, a Laravel or Symfony test harness, `WP_UnitTestCase`, data providers, `#[Test]` attributes, a PHP-side E2E framework — is flagged **unverified** where it appears.

## Test runner(s)

- **Unit / contract**: `vendor/bin/phpunit` (measured: 10.5.63). Where `composer.json` declares one, `composer test` wraps it — measured present on some modules of the ground and *removed* from others, so it is not a reliable entry point.
- **The runner is a project dependency, never a toolchain command.** PHP ships no test runner; PHPUnit arrives through Composer's `require-dev`. Prerequisite, and it is not satisfied by the binary merely existing — see *Known tooling gotchas*, first item:

  ```
  test -x vendor/bin/phpunit && vendor/bin/phpunit --version
  ```

- **Configuration is read from `phpunit.xml` or `phpunit.xml.dist`** at the component root. It carries the test directories, the file suffix and the source roots; none of those is conventional (see *Test file glob*).
- **There is not necessarily one suite per repository, and the root is regularly not where anything runs.** Measured: the PrestaShop ground holds nine modules under `modules/`, each with its own git repository, `composer.json`, `vendor/` and `phpunit.xml.dist`. **No root command runs them.** A measurement launched from the project root returns *zero test* on a project carrying 225 test methods across six components. The unit of measurement is the component, and it is measured N times.
- **E2E**: no standard command — see *Canonical E2E tool*.

## Test file glob

- `tests/**/*Test.php` — PHPUnit's default file suffix is `Test.php`, and it is what selects a test file. **Not** `tests/**/*.php`.
- The directory comes from `phpunit.xml*` › `<testsuite><directory>`, never from convention. Measured divergent on two modules of the same ground: `<directory>tests/Unit</directory>` against `<directory>tests</directory>`.

Source and test are disjoint in this stack: a test class lives in its own file, under a directory the config names. Nothing is due here on that count — stated only so a consumer does not have to infer it from silence.

**Widening the glob to the directory over-counts.** Measured: `tests/Unit/Service/AbstractServiceTestCase.php` is an abstract base class extending `TestCase`, shared by the module's test classes. It matches `tests/**/*.php`, carries no executable test, and PHPUnit ignores it — the suffix, not the location, is what discriminates.

## Test-count command

```
vendor/bin/phpunit --list-tests | grep -c '^ - '
```

Measured **46** and **29** on two independent modules, each equal to the execution footer (`OK (46 tests, 101 assertions)`).

- **No compilation step.** The count is immediate, but the command still loads the autoloader and the declared bootstrap file (measured: `bootstrap="tests/bootstrap.php"` on one module). A bootstrap requiring a database or an undefined constant therefore fails the *count* on a project whose tests are sound. *Not observed here — both bootstraps loaded cleanly.*
- **Static approximation**: `grep -rc 'public function test' tests`. Returned the exact value on both modules. Do not generalise: it **under-counts** methods carrying a `#[DataProvider]` (one method, N cases in `--list-tests`) and methods marked with the `#[Test]` attribute instead of the `test` prefix. *Unverified: zero occurrence of either on the ground, which is why the three numbers agreed.*
- `--list-suites` enumerates the declared suites; `--testsuite <name>` restricts a run to one.
- Any invocation writes a cache directory into the measured repository — see *Known tooling gotchas*.

## Coverage command

```
vendor/bin/phpunit --cache-directory <path outside the repo> --coverage-clover <path>
```

**Prerequisite — a coverage driver, which is a property of the PHP binary, not of the project.** PHP ships none: coverage requires the **Xdebug** extension in `coverage` mode, or **PCOV**. Establishing presence:

```
php -m | grep -iE 'xdebug|pcov'
php -r 'var_dump(extension_loaded("xdebug"), extension_loaded("pcov"));'
```

Both measured absent on the ground. A command failing for want of a driver signals a machine without tooling, **never** a defect of the measured project: the field is absent for that run and its fallback applies (`pivot-contract.md` › *Prerequisites*).

**The failure is silent, and that is where this stack differs most.** Measured with no driver installed: PHPUnit prints `1) No code coverage driver available`, ends on `OK, but there were issues!`, **exits 0**, and **writes no file at all**. A consumer testing the exit code concludes success and then finds no report. The prerequisite has to be established *before*, or the file's existence checked *after* — the exit code carries no information here.

- **`phpdbg -qrr vendor/bin/phpunit --coverage-clover …` is not a substitute.** Widely repeated advice; measured false on PHPUnit 10 — same warning, same exit 0, no file. phpdbg is no longer a driver php-code-coverage 10 accepts.
- With Xdebug installed, `XDEBUG_MODE=coverage` is still required: loaded but in another mode, the extension produces an empty report rather than an error. *Unverified — no ground carried the extension.*
- Other reporters: `--coverage-xml <dir>` (per-file, richer), `--coverage-text` (human-readable only, unusable as a machine format).
- The contract's fallback — a static source-to-test mapping — **does apply here**, source and test being disjoint (see *Test file glob*).

## Source glob & exclusions

Classifiable production code:

- **With a Composer manifest**: the directories the PSR-4 map points at, read from `composer.json` › `autoload.psr-4` (measured: `"ScImportDumps\\": "src/"`), never guessed. `autoload-dev` points at the test tree and is not production code.
- **Without one — the ordinary WordPress case**: the project's own theme and plugin, `wp-content/themes/<theme>/**/*.php` and `wp-content/plugins/<own plugin>/**/*.php`.

Never classifiable:

- **`vendor/`** — third-party code installed by Composer, and frequently committed in a distributed module or plugin, so `.gitignore` does not always exclude it.
- **`node_modules/`** — carries PHP files in some packages.
- **`build/`** — `@wordpress/scripts` output, and it contains **generated PHP**. Measured: `build/<block>/index.asset.php` is a one-line `<?php return array('dependencies' => …, 'version' => …);`, and it is **committed** — the repository's ignore rules do not flag it.
- **WordPress core itself, when the repository is a full install.** Measured on that ground: 1640 `**/*.php`, of which 844 in `wp-includes/`, 240 in `wp-admin/`, 16 at the root and 407 under `wp-content/plugins/` mostly third-party (Akismet, Polylang, Redirection…). The project's own code is 61 theme files + 25 plugin files = **86, i.e. 5.2 %**. A naive `**/*.php` glob is ~95 % noise here.

**The layout is not deducible from the stack.** Two WordPress repositories measured, opposite source universes: one contains the entire install, the other has `wp-content` for its root and no core in tree at all. Discriminant, measured: whether `wp-includes/` sits at the repository root.

**A `composer.json` found is not necessarily the project's.** Measured: the only one in the full WordPress install is `wp-includes/sodium_compat/composer.json` — the manifest of a dependency vendored inside core. Locating a manifest by search, rather than at the component root, resolves the wrong project.

## Risk signals

Structurally high-consequence in this stack:

- **Money** — cart, order, price, discount, tax, payment. On an e-commerce stack this sits in the domain core, not at its edge.
- **Hand-built SQL.** Measured: the ground concatenates `LIKE` and `DELETE` statements directly. Once outside an ORM, escaping is an application responsibility with no compiler behind it.
- **Deletion and filesystem writes** — `unlink`, `rmdir`, upload handling, dump import.
- **Cross-cutting state** — `Configuration::set` (PrestaShop), `update_option` / `add_filter` (WordPress): action at a distance over the whole application.
- **Authentication and capabilities** — `current_user_can`, `check_ajax_referer`, `wp_verify_nonce`, admin controller access checks.
- **Superglobals read without sanitising** — `$_GET`, `$_POST`, `$_REQUEST`, `$_FILES`.

Structurally not high-consequence:

- **Framework pass-through** — PrestaShop `hookDisplay*` methods, presentation-only WordPress hooks.
- **Pure markup files.** Measured: `themes/<theme>/patterns/*.php` is a comment header followed by markup — PHP as far as any glob is concerned, carrying no logic.
- **Generated glue** — `build/**/index.asset.php`.

**External boundaries, read from the manifest** — Composer `require`: `guzzlehttp/guzzle`, `symfony/http-client` (outgoing clients); `doctrine/dbal`, `doctrine/orm`, `illuminate/database` (external persistence — measured `doctrine/dbal ^3.0`); `stripe/stripe-php`, `aws/aws-sdk-php`, `sentry/sentry`, `monolog/monolog` (SaaS and telemetry).

**WordPress ordinarily has no manifest at all.** Measured: the ground's own plugin carries no `composer.json`, so no dependency list exists to read. The boundaries are then read from the code: `wp_remote_get` / `wp_remote_post` — measured, two files (`includes/brevo-subscribe.php`, `includes/brevo-contact.php`) identify the Brevo API as the product's only outgoing boundary. Also worth grepping: `curl_init`, `file_get_contents('http`.

**A `composer.json` without `require-dev` does not signal a component without tests.** Measured: one module whose `autoload-dev`, `require-dev` and `scripts.test` were stripped from the working copy for packaging carries 93 test methods, a `tests/` tree and a `phpunit.xml.dist`. The manifest describes what is shipped, not what exists.

## Anchor boundary

Positions the boundary in this stack's own terms. **It never says what proof a case is due** — that is decided elsewhere, and nothing here modifies it.

**Anchors** — crosses the product's real public boundary:

- **A real HTTP request served by a real server against a real database** — a PrestaShop front controller, a rendered WordPress page. PHP tears down and re-initialises on every request: the full request cycle *is* the boundary the product exposes, and almost nothing of it is exercised in a test process.
- **The real database schema.** Applicative PHP is overwhelmingly written against a RDBMS; a query that a real schema rejects is the stack's most common escape.
- **A real CLI invocation** — `bin/console <cmd>`, `wp <cmd>` — with its arguments, environment and exit code.
- **A real outgoing call** to the third-party service, where that is the boundary the product exposes.

**Does not anchor, despite appearances**:

- **A `TestCase` with a doubled connection.** Measured on the ground: `Connection&MockObject` injected in place of the DBAL connection — the SQL is built and never executed by anything that could reject it.
- **A bootstrap that redeclares the framework's own classes.** Measured, and it is the stack's sharpest case: one module's `tests/bootstrap.php` declares its own `Configuration` class so the code under test can run *outside* PrestaShop. The suite never loads the framework; it proves the module's logic, and says nothing about its integration. Such a suite can be large, green and entirely internal.
- **`WP_UnitTestCase`** — boots WordPress in-process against a transactional database. Heavy and real, but **no request is served**: real and anchored are not synonyms. *Unverified — absent from every ground.*
- **A built-in server (`php -S`) started by the test** — anchors only if the product is actually served by it; a server standing in for a fake client is a double. *Unverified — no ground carried one.*

## Known tooling gotchas

- **A present `vendor/bin/phpunit` can be dead.** *Detection*: the binary exists and exits on `PHP Fatal error: Uncaught Error: Class "PHPUnit\TextUI\Application" not found` — measured on two modules. *Cause*: the autoloader was regenerated without dev dependencies while `vendor/phpunit/` stayed on disk. *Reliable check*: `grep -c '"phpunit/phpunit"' vendor/composer/installed.json` returns **0** although the directory is there (measured, along with zero PHPUnit entry in `autoload_psr4.php` and `autoload_static.php`). *Fix*: `composer install` with dev dependencies. This is a machine/checkout state, never a defect of the measured suite.
- **PHPUnit writes into the measured repository.** *Detection*: `.phpunit.cache/` appears at the component root — and measured, one module **tracks** it (`.phpunit.cache/test-results` under version control), so it is not even covered by an ignore rule. *Fix*: `--cache-directory <path outside the repository>`, applied to every measurement behind this pivot; `git status --porcelain` was identical before and after on each module touched.
- **Coverage fails silently with exit code 0** and writes nothing (see *Coverage command*). *Detection*: the `No code coverage driver available` warning in the output, or the absence of the expected file. *Fix*: establish the driver beforehand; never read the exit code as proof a report exists.
- **`phpdbg` is no longer a coverage driver.** *Detection*: `phpdbg -qrr vendor/bin/phpunit --coverage-clover …` produces the same warning and no file (measured, PHPUnit 10). *Fix*: install Xdebug or PCOV; the advice predates php-code-coverage 10.
- **The test directory is not conventional.** *Detection*: two modules of the same ground declare `tests/Unit` and `tests` respectively. *Fix*: read `phpunit.xml` / `phpunit.xml.dist`; never presume `tests/`.
- **`failOnWarning="true"` / `failOnRisky="true"` turn a warning into a red run.** *Detection*: those attributes on the `<phpunit>` element — measured present across the ground's configs. *Fix*: none needed; read the output, since a red run here does not imply a failed assertion.
- **A directory glob over-counts test files** (see *Test file glob*). *Detection*: files under the test tree not ending in the configured suffix. *Fix*: follow the suffix, not the directory.
- **One repository can hold N independent suites.** *Detection*: several `composer.json` / `phpunit.xml.dist` pairs below the root, each with its own `vendor/` (measured: nine). *Fix*: measure per component and name each; a single root invocation reports zero.

## Domain resolution

**How to find a domain already named here, never which ones exist.** This field completes a resolution; it never overrides what is stated about the project's own code.

### Composer projects

- **`composer.json` › `autoload.psr-4` maps namespace to directory** (measured: `"ScImportDumps\\": "src/"`). The root namespace names the *component*, not a domain.
- **`src/<Layer>/` is a layer, not a domain.** Measured: `src/Controller/Admin/`, `src/Service/`, `src/Traits/` — layers throughout, no domain at the first level. A tree whose first level is entirely layers exposes no domain in the filesystem; it is then read from identifiers.
- **Identifier suffixes** — `<Domain>Controller`, `<Domain>Service`, `<Domain>Repository`, `<Domain>Entity`, `<Domain>Type`. These are the reliable carriers when the tree is layered.
- **PrestaShop**: `modules/<module>/` is the distribution unit. A module may hold one domain or several; the directory name says which product it extends, not which domain it implements.

### WordPress

- **No PSR-4 to read** — measured: the ground's own plugin has no manifest. A domain lands on a filename instead: `includes/<domain>.php`, measured as `brevo-subscribe.php`, `brevo-contact.php`, `brevo-settings.php` (three files, one domain), alongside `custom-post-types.php` and `clean-urls.php`.
- **Block names carry domains** — `blocks/<name>/` with `block.json` › `"name": "<plugin>/<name>"`. Measured: `posts-listing`, `services-list`, `offres-list`, `faq-accordion`, `testimonials-carousel`, `kpi-stats`, `brevo-form`.
- **Registration slugs** — the first argument of `register_post_type`, `register_taxonomy`, `register_block_type`, and option prefixes (`<plugin>_<domain>_…`).
- **Layers, not domains**: `functions.php`, `inc/`, `patterns/`, `templates/`, `parts/`, `build/`.

## Canonical E2E tool

**None.** PHP standardises on no E2E framework, and both web grounds measured run their E2E **outside PHP**: Playwright driven from `package.json` (measured: `"playwright": "^1.60.0"`, harness under `tools/qa/`). That a PHP project's E2E is ordinarily a Node harness is a property of this stack, not an oddity of the ground — and it means the E2E command is regularly not a PHP command at all.

PHP-side frameworks that do exist, *none observed on any ground*: Behat, Codeception, Symfony Panther, Laravel Dusk.

Informational: nothing reads this field as licence to propose a replacement.
