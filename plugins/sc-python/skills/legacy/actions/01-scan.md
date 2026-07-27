# Action 01 — scan

Detect version-specific and deprecated patterns in the Python codebase. Emit a structured manifest for `02-migrate`.

## Inputs

- `path` (optional, default: project root) — directory to scan
- `target` (optional) — target Python version (e.g. `3.12`) or `"modernize"` (latest stable)
- `direction` (optional) — `upgrade` | `downgrade` (inferred from context if omitted)

## Process

### Step 1 — Load version references

@../references/python-versions.md
@../references/framework-migrations.md

### Step 2 — Detect current Python version

1. Read `.python-version` (pyenv)
2. Read `pyproject.toml` → `[tool.poetry] python` or `[project] requires-python`
3. Read `setup.py` → `python_requires`
4. Read `tox.ini` → `[tox] envlist`
5. If still unknown: check Dockerfile `FROM python:X.X`. **Si aucune source ne donne le plancher, ne pas supposer 3.9** : marquer la version `unknown` et rétrograder toute modernisation dépendante de la version en `warning` (« plancher d'interpréteur non mesuré — la cible du rewrite peut ne pas être disponible à l'exécution »). Une version supposée qui sur-estime le plancher produit du code qui casse au runtime, pas à l'analyse.

### Step 3 — Determine direction and target

- If user said "upgrade" or "modernize" or target > current: `direction = upgrade`, `target = 3.12` (or user value)
- If user said "downgrade" or "compat" or target < current: `direction = downgrade`, ask for target if not provided
- If direction still unknown: ask the user before scanning

### Step 4 — Scan deprecated and version-specific patterns

Grep the source files (`.py`) under `path`. Exclude `.venv/`, `venv/`, `__pycache__/`, migration files (`migrations/`, `alembic/versions/`).

#### Python 2 remnants (upgrade direction)

| Pattern | Signal | Replacement |
|---|---|---|
| `print` statement | `^\s*print\s+[^(=]` — **exclure `print (…)`** (espace avant parenthèse = appel Py3 valide) et `print =` (réassignation) | `print()` function. Le signal nu `print\s+[^(]` flague `print ("x")`, qui est déjà un appel correct. |
| `xrange()` | `\bxrange\(` | `range()` |
| `dict.iteritems()` | `\.iteritems\(\)` | `dict.items()` |
| `dict.iterkeys()` | `\.iterkeys\(\)` | `dict.keys()` |
| `dict.itervalues()` | `\.itervalues\(\)` | `dict.values()` |
| `dict.has_key()` | `\.has_key\(` | `in` operator |
| `unicode()` | `\bunicode\(` | `str()` |
| `basestring` | `\bbasestring\b` | `str` |
| Old `raise` syntax | `raise\s+\w+,\s*` | `raise Exception("msg")` |
| Old `except` syntax | `except\s+\w+,\s*\w+:` | `except Exception as e:` |
| `execfile()` | `\bexecfile\(` | `exec(open(file).read())` |
| Long integers `123L` | `\d+L\b` | plain `int` |

#### Type annotation modernization (upgrade, Python 3.9+/3.10+)

**Condition de plancher, pas de présomption.** Chaque rewrite ci-dessous n'est applicable que si le plancher `requires-python` **mesuré** (Step 2) est ≥ la colonne `Since`. Sur un projet qui déclare `>=3.8`, réécrire `Optional[X]` en `X | None` (3.10) ou `List[X]` en `list[X]` en annotation *évaluée* (hors `from __future__ import annotations`) **casse à l'import**. Ce n'est donc pas un « pure annotation change, low risk » inconditionnel : c'est `low risk` **seulement** si le plancher couvre la cible. Plancher inconnu → `warning`, jamais auto-appliqué.

| Pattern | Signal | Replacement | Since |
|---|---|---|---|
| `Optional[X]` | `Optional\[` | `X \| None` | 3.10 |
| `Union[X, Y]` | `Union\[` | `X \| Y` | 3.10 |
| `List[X]` | `List\[` | `list[X]` | 3.9 |
| `Dict[X, Y]` | `Dict\[` | `dict[X, Y]` | 3.9 |
| `Tuple[X, ...]` | `Tuple\[` | `tuple[X, ...]` | 3.9 |
| `Set[X]` | `Set\[` | `set[X]` | 3.9 |
| `Type[X]` | `Type\[` | `type[X]` | 3.9 |
| Missing function type hints | Functions without annotations | Add hints | 3.5+ |

#### String formatting modernization (upgrade, Python 3.6+)

| Pattern | Signal | Replacement |
|---|---|---|
| `%` formatting | `%\s*(\(|[sdif])` | f-string — **sauf `logging`**. `logger.info("%s", x)` est du *lazy % formatting* voulu : l'interpolation n'a lieu que si le niveau est actif. Le convertir en f-string force l'évaluation à chaque appel (coût + perte du champ structuré). Exclure les arguments de `logger.*`/`logging.*` → ne pas flaguer. |
| `.format()` | `\.format\(` | f-string (if variables are simple) — même exclusion `logging`. |

#### Downgrade targets

| Feature | Signal | Target |
|---|---|---|
| Walrus operator `:=` | `:=` | < 3.8 |
| Positional-only params `/` | `def fn(..., /, ...)` | < 3.8 |
| `X \| Y` type union in annotations | `\bint\s*\|\s*str\b` | < 3.10 |
| `match`/`case` structural pattern matching | `^\s*match\s` | < 3.10 |
| `tomllib` stdlib | `import tomllib` | < 3.11 |
| `Self` type | `\bSelf\b` | < 3.11 |
| `TypeVarTuple`, `Unpack` | | < 3.11 |
| PEP 695 `type X =` | `^type\s+\w+\s*=` | < 3.12 |

### Step 5 — Detect framework version gaps (if detected)

If Django detected: check installed version and note patterns removed between detected and target major.
If FastAPI detected: check for deprecated `@app.on_event` → `lifespan` context manager pattern.

### Step 6 — Output manifest

```
📊 sc-python legacy — scan results

Current Python: 3.9 (from .python-version)
Target: 3.12 (upgrade)

Python 2 remnants:
  (none)

Type annotation updates:
  MEDIUM  Optional[X] → X|None — 14 occurrences in 6 files
  MEDIUM  List[X] → list[X] — 8 occurrences in 4 files
  MEDIUM  Dict[X, Y] → dict[X, Y] — 5 occurrences in 3 files

String formatting:
  LOW     % formatting — 3 occurrences → f-string candidates
  LOW     .format() — 11 occurrences → f-string candidates (simple vars only)

Missing type hints:
  LOW     12 public functions without annotations (src/services/)

→ migrate will modify 9 files.
```

Then proceed to `02-migrate`.

## Test — non-régression (faux positifs corrigés)

Sur un fichier de test couvrant chaque cas, rejouer `scan` et vérifier :

- `print ("x")` (espace avant parenthèse) et `print = something` **ne sont pas** flagués comme `print` statement Python 2 — seul `print "x"` l'est.
- `logger.info("%s", x)` **n'est pas** listé comme candidat f-string.
- Sans plancher `requires-python` détectable, la version est marquée `unknown` et les modernisations d'annotations sortent en `warning`, **pas** supposées 3.9 ni auto-appliquées.
