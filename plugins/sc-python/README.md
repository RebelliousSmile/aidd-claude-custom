# sc-python

*Knowledge provider pour les stacks Python (Django, FastAPI, Flask, Celery, DRF) : détection de stack, audit, modernisation et enseignement par pivots.*

Détecte la stack du projet depuis ses manifestes Python et charge à la demande les pivots applicables. Les pivots perf/data alimentent `web-optimize` / `data-optimize` (plugin `overcode`).

## Skills

| Skill | Déclencheur | Description |
|---|---|---|
| `sniff` | `/sc-python:sniff` | Détecte la stack depuis `requirements.txt`, `pyproject.toml`, `setup.py`, installe/met à jour uniquement les règles pertinentes |
| `audit` | `/sc-python:audit` | Détecte la stack via sniff puis invoque `aidd-dev:04-audit` (`code-quality`) avec les pivots applicables ; le rapport AIDD reste autoritatif |
| `improve` | `/sc-python:improve` | Analyse le code — écarts d'idiomes pythoniques, opportunités de design patterns, plan d'amélioration |
| `legacy` | `/sc-python:legacy` | Scanne le code pour patterns dépréciés / spécifiques à une version, propose une migration |
| `log-analysis` | `/sc-python:log-analysis` | Analyse les logs d'application Python (local, Docker, prod SSH) — tail, parse-errors, search, summarize |
| `teach` | `/sc-python:teach` | Enseigne les fonctionnalités du langage, idiomes pythoniques, patterns async et idiomes de framework |
| `cd` | `/sc-python:cd local\|server\|automata` | Réconcilie local et production sans convertir le gestionnaire : uv, Poetry ou Pipenv sont conservés ; un projet requirements-only demande un arbitrage. SQL distingue migrations et transfert de données. |

## Pivots disponibles

### Perf pivots — installés par `sniff`, consommés par `/web-optimize`

| Signal de détection | Pivot installé |
|---|---|
| `django` | `perf-pivots-django.md` |
| `djangorestframework` | `perf-pivots-drf.md` |
| `celery` | `perf-pivots-celery.md` |
| `fastapi` | `perf-pivots-fastapi.md` |
| `httpx` | `perf-pivots-httpx.md` |
| `flask` | — gap (pas de pivot dans cette version) |

### Data pivots — installés par `sniff`, consommés par `/data-optimize`

| Signal de détection | Pivot installé |
|---|---|
| `django` (sans sqlalchemy) | `data-pivots-django-orm.md` |
| `sqlalchemy` | `data-pivots-sqlalchemy.md` |
| `datasets` (HuggingFace) | `data-pivots-datasets.md` |

### Capability pivots — chargés à l'audit, non installés sur disque

| Signal de détection | Pivot |
|---|---|
| Tout projet Python | `python/idioms.md` |
| `spacy` | `python/spacy.md` |

### Pivot de gouvernance `testing` — lu par un autre plugin

`skills/sniff/references/capabilities/tools/testing.md` est le seul pivot qui ne sert **ni** à `/sc-python:audit`, **ni** au matching par chemin : il est exposé par glob (`**/capabilities/**/testing.md`) sous la racine du plugin, à qui implémente le contrat de pivot. Il fournit la mécanique Python de gouvernance des tests — runners (`pytest`, `manage.py test`, les orchestrateurs qui n'en sont pas), glob des fichiers de test lu comme valeur de `python_files`, commande de coverage machine-lisible, glob source et exclusions, frontière d'ancrage (`Anchor boundary`), signaux de risque, gotchas d'outillage, résolution de domaine (`Domain resolution` — comment un domaine fonctionnel se lit dans une arborescence d'apps Django et dans les identifiants Python, jamais lesquels existent). Applicable dès que `pytest` est détecté, ou à défaut sur présence d'un `manage.py`.

Ce que ce pivot **ne fait pas** : décider s'il faut écrire un test, ni quel niveau de preuve un cas mérite. Ses commandes et ses chiffres ont été relevés sur un projet Django réel ; ce qui n'a pas pu être mesuré est signalé à l'endroit où il apparaît.

### Résumé

| Type | Où ça vit | Qui le charge | Quand |
|---|---|---|---|
| Capability pivot | Plugin uniquement | Claude Code (automatique, via `paths:`) | À chaque édition de fichier matchant |
| Perf / data pivot | `.claude/rules/07-quality/` | `web-optimize` / `data-optimize` (explicite) | Au lancement du skill |
| Pivot `testing` | Plugin uniquement | Tout consommateur du contrat de pivot (découverte par glob) | À chaque action de gouvernance de tests sur un projet Python |

## CD multi-cibles

`sc-python:cd` conserve uv, Poetry, Pipenv ou l'invocation Python déjà choisie et l'utilise pour des cibles nommées `server` ou `automata`. Les migrations restent séparées des lignes métier et des médias. Chaque production possède sa base et son stockage ; un staging peut être un miroir local seulement lorsque l'inventaire et la reprise sont prouvés.

## Licence

MIT — voir [LICENSE](../../LICENSE).
