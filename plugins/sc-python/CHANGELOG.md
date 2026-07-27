# Changelog — sc-python

> Baseline établie le 2026-05-29 à partir de l'état courant ; transitions récentes reprises de l'historique git. Détail antérieur : `git log -- plugins/sc-python`.

## [0.5.3] — 2026-07-27

### Fixed — discipline de sévérité (l'audit alimente des mutants)

Même correctif transversal que sc-css/sc-rust/sc-php. `legacy/01-scan`, `improve` sont read-only mais `legacy/02-migrate` mute in-place. Correction **inline**, conditionnée à une propriété **mesurée**. Les quatre classes A/B/C/E sont présentes ici.

- **(A) Verdict sur propriété supposée → mesurée.** La modernisation d'annotations (`Optional[X]`→`X | None` 3.10, `List[X]`→`list[X]` 3.9) était étiquetée « low risk, pure annotation change » **sans mesurer le plancher d'interpréteur**. Sur un projet `>=3.8`, l'annotation *évaluée* casse à l'import. Désormais conditionnée au plancher `requires-python` mesuré (ou `from __future__ import annotations`) ; plancher inconnu → ne plus supposer 3.9, marquer `warning` (`legacy/01-scan.md`, `improve/01-analyze.md`, `improve/02-plan.md`, `idioms.md`).
- **(B) Sévérité alimentant la mutation.** `02-migrate` écrit in-place ; la garde « simple identifiers » du `%→f-string` laissait passer `logger.info("%s", x)`. Ajout : les rewrites d'annotations attendent la couverture du plancher (`Skipped (interpreter floor not covered)`), le lazy logging n'est jamais converti (`legacy/02-migrate.md`).
- **(C) « Code mort » indécidable au scan statique.** Le pivot ActivityPub concluait « code mort critique » quand `grep` ne trouvait pas la view inbox dans un `urls.py` — aveugle au routage indirect Django/DRF (`include()`, `as_view()`, routers, dispatch dynamique). Remplacé par « câblage à confirmer manuellement — résoudre l'URL réelle », jamais un verdict (`sniff/references/capabilities/protocol/activitypub-django.md`).
- **(E) Le moteur d'analyse mal-juge les constructions qu'il recommande.** Le regex `print\s+[^(]` flaguait `print ("x")` (appel Py3 valide) → resserré pour exclure l'espace-avant-parenthèse et la réassignation. La conversion f-string était imposée au `logging` %-lazy (interpolation forcée + perte du template structuré) → exclusion des appels `logger.*`/`logging.*` sur toute la chaîne (`legacy/01-scan.md`, `02-migrate.md`, `idioms.md`, `improve/01-analyze.md`).

## [0.5.2] — 2026-05-29

### Fixed
- `references/protocol/activitypub-django.md` §2 Delivery : `acks_late=True` + `soft_time_limit`/`time_limit` sur `deliver_activity` (exemple concret) ; signature des activités sortantes Accept/Reject/Announce (grep de détection inclus)
- `references/protocol/activitypub-django.md` §3 Conformance : `id` absolu obligatoire sur toutes les activités sortantes
- `references/protocol/activitypub-django.md` §4b : nouvelle section cache de clé d'acteur — TTL 24h + invalidation sur `Update(Person)` reçu
- `references/capabilities/ap/ap-protocol-specs.md` : anti-patterns Accept/Reject non signés (ignorés par Mastodon 4+, Misskey) et cache de clé sans TTL/invalidation
- `skills/ap-optimize/SKILL.md` Step 2 : chargement explicite des pivots perf/data supplémentaires après le pivot AP (comportement était implicite)

> Comble un gap de versions : `0.5.0`/`0.5.1`/`0.5.2` avaient été bumpés en plugin.json/marketplace.json sans entrée CHANGELOG correspondante. Reconstruit depuis `git log` (commits `db22060`, `63eb9ce`, `71d0d78`). Le commit `315a499` (2026-05-31, ajout de `references/capabilities/ap/django-activitypub.md`) n'a pas bumpé la version malgré un contenu nouveau — écart à surveiller, non corrigé ici pour ne pas réinventer une version qui n'a jamais été taguée.

## [0.5.1] — 2026-05-29

### Fixed
- `references/capabilities/ap/ap-protocol-specs.md` : anti-patterns livraison avant `transaction.on_commit`, inbox sécurisée non routée (view avec signature ≠ view dans `urls.py`), `coverage.omit` sur chemins AP critiques
- `references/protocol/activitypub-django.md` §0 Pre-flight : commandes de détection de code mort sur l'inbox (cross-check `urls.py` vs fichier contenant `verify_signature`), garde de couverture de test sur `inbox.py`/`signatures.py`/`tasks.py`

## [0.5.0] — 2026-05-29

### Added
- `references/capabilities/perf/httpx.md` — pivot perf httpx : AsyncClient singleton, timeouts, pool, retry `tenacity`, event hooks
- `references/capabilities/perf/drf.md` — pivot perf DRF : N+1 serializers, `select_related`, pagination cursor, JWT auth, throttling
- `references/capabilities/perf/celery.md` — pivot perf Celery : `time_limit`, `acks_late`, retry backoff, idempotence, queue routing, Flower
- `references/capabilities/data/datasets.md` — pivot data HuggingFace datasets : streaming, `map(batched=True)`, `cache_dir`, `select_columns`, `trust_remote_code`
- `references/capabilities/python/spacy.md` — capability pivot spaCy : chargement singleton avec `disable=`, `nlp.pipe()` par batch de langue, `PhraseMatcher`
- `references/capabilities/protocol/activitypub-django.md` — nouvelle catégorie protocol : inbox (signature + idempotence atomique + anti-replay), delivery (`on_commit` + circuit breaker), conformance AS2, SSRF allowlist, observability

### Changed
- `01-scan.md` : refonte de la spec sniff — optional-dependencies et groupes Poetry couverts, output template déplacé avant Process, tables markdown/ASCII interdites, readiness lines par sous-section, gap buckets A/B, détection ActivityPub (Step 3), nouvelle catégorie `protocol/` (Step 4), companions étendus (DRF, Celery, httpx, datasets, spaCy, AP)

## [0.4.9] — 2026-05-29

- Bump de synchronisation — marketplace aidd-overlay alignée sur 0.4.9 ; aucun changement fonctionnel.

## [0.4.8] — 2026-05-29

### Added
- `references/capabilities/perf/drf.md` — pivot perf DRF : N+1 dans les serializers, pagination cursor, `select_related` dans `get_queryset`, JWT vs SessionAuth, throttling, `cache_page` sur ViewSet
- `references/capabilities/perf/celery.md` — pivot perf Celery : `soft_time_limit`/`time_limit`, `acks_late`, retry backoff exponentiel, idempotence, queue routing par priorité, Flower

### Changed
- `01-scan.md` : détection `djangorestframework` → `perf-pivots-drf.md`, `celery` → `perf-pivots-celery.md`
- `01-scan.md` : companions DRF (`drf-spectacular`, `drf-extensions`, `djangorestframework-simplejwt`) et Celery (`django-celery-beat`, `kombu`, `celery[redis]`) ajoutés à la liste de filtrage
- `01-scan.md` : `Pillow` ajouté aux exemples de Bucket A
- `02-install-pivots.md` : entrées DRF et Celery ajoutées

## [0.4.7] — 2026-05-29

- Bump post-session (exécution de `sc-python:improve` sur un projet consommateur).

## [0.4.6] — 2026-05-29

### Added
- `references/capabilities/perf/httpx.md` — pivot perf httpx : AsyncClient singleton, `Limits`/`Timeout`, retry via `tenacity`, `asyncio.gather`, event hooks de logging
- `references/capabilities/data/datasets.md` — pivot data HuggingFace datasets : `streaming=True`, `.map(batched=True)`, `cache_dir`, `select_columns`, `trust_remote_code`
- `references/capabilities/python/spacy.md` — capability pivot spaCy : chargement singleton avec `disable=`, `nlp.pipe()` par batch de langue, `PhraseMatcher`, `EntityRuler`, extensions `Doc.set_extension`

### Changed
- `01-scan.md` : détection `httpx`, `datasets`, `spacy` ajoutée dans Step 4 ; companions mis à jour (`respx`, `huggingface_hub`, `tokenizers`, spaCy language models) ; Bucket A — `spacy`/`datasets` retirés (couverts), `transformers`/`playwright`/`Pillow` ajoutés
- `02-install-pivots.md` : entrées httpx et datasets ajoutées

## [0.4.5] — 2026-05-29

### Changed
- `01-scan.md` : Output template déplacé **avant** le Process (ancrage avant tout traitement)
- `01-scan.md` : `ALL TABLES ARE FORBIDDEN` — interdiction explicite des tables markdown (`| col |`) ET ASCII box-drawing (`┌───┐`)
- `01-scan.md` : noms de sections fixés — interdiction d'inventer des noms alternatifs ; deuxième exemple mis à jour (FastAPI + spaCy + datasets + httpx)

## [0.4.4] — 2026-05-29

### Changed
- `01-scan.md` : bloc DEPRECATED enrichi — nomme explicitement `Skills support:`, `Gaps (no plugin pivot):` et le format plat des pivots comme structures à ne pas reproduire

## [0.4.3] — 2026-05-29

### Changed
- `01-scan.md` Step 1 : ajout de `[project.optional-dependencies.*]` et `[tool.poetry.group.*.dependencies]` — détection via optional-deps spécifiée (plus d'improvisation modèle)
- `01-scan.md` : enforcement header output format (tables markdown interdites, sections obligatoires)
- `01-scan.md` : readiness lines par sous-section (`→ /skill : PRÊT`) remplacent la section `Skills support:` autonome
- `01-scan.md` : closing summary constraint ajouté
- `01-scan.md` : gap buckets A (capability candidates) et B (tooling/infra) avec filtrage des companion packages
- `01-scan.md` : exemple Flask gap ajouté dans le second template

## [0.4.2] — 2026-05-29 (baseline)

Knowledge provider Python (Django, FastAPI, Flask). Skills : `sniff`, `audit`, `improve`, `legacy`, `log-analysis`, `teach`.

### Added
- `improve` : Step 1.5 — chargement des capability pivots pour les anti-patterns spécifiques à la stack.

## [0.4.1]
- `legacy` : ajout de `references/` (patterns dépréciés / spécifiques à une version).

## [0.4.0]
- Alignement sur le modèle sc-php v0.4.0 : sniff à deux niveaux (pivot model), skill `audit` déléguant la revue, evals. Bump 0.3.0 → 0.4.0.

## Antérieur
- Voir `git log -- plugins/sc-python` pour l'historique complet.
