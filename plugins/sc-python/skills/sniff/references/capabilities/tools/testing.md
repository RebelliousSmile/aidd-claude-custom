---
---

# Testing — pivot de gouvernance (pytest + coverage.py)

Contenu factuel structuré — inventaire de l'outillage de test et des signaux que la stack rend lisibles — et non des patterns de revue de code, contrairement aux autres fichiers de ce dossier. C'est aussi pourquoi il ne porte pas de `paths:` : il ne s'applique pas à une famille de fichiers, il décrit une suite. Ce que ce fichier fournit est décrit ici ; qui le lit ne l'est pas. Applicable quand `pytest` est détecté (`pyproject.toml`, `requirements*.txt`, `setup.cfg`, `tox.ini`), ou à défaut quand un `manage.py` Django est présent.

Les commandes et les sorties citées ont été **vérifiées sur un projet Django réel** (Django 5.0, pytest 9.1.1, pytest-django, pytest-cov, coverage.py 7.15 — 80 fichiers de test, 1028 tests collectés). Ce qui n'a pas pu être mesuré est signalé comme tel à l'endroit où il apparaît.

## Test runner(s)

- **pytest** — `pytest`. C'est le runner de fait dès que `pytest` figure dans les dépendances de dev, y compris sur un projet Django : `pytest-django` fournit `DJANGO_SETTINGS_MODULE`, la base de test et les fixtures (`db`, `client`, `settings`, `live_server`).
- **unittest / `manage.py test`** — runner historique de Django, et **le seul disponible sans pytest**. Sa découverte est celle d'`unittest` : elle ne collecte que des méthodes de classes dérivant de `unittest.TestCase`.
- **`tox` / `nox`** — orchestrateurs multi-environnements, jamais des runners : ils invoquent l'un des deux ci-dessus. Le runner réel se lit dans la section `commands` de `tox.ini` / dans le corps des sessions `noxfile.py`.

**Les deux runners ne collectent pas le même ensemble, et l'un peut n'en collecter aucun.** `manage.py test` ignore les fonctions de test au niveau module et les classes `Test*` qui ne dérivent pas de `TestCase` — c'est-à-dire la totalité du style pytest. Mesuré sur la fixture : 280 fonctions `def test_*` au niveau module, 218 classes `Test*` nues, **0** classe dérivant de `TestCase` ; `manage.py test` y collecterait zéro test sur 1028. Ce que le projet déclare dans sa documentation ne tranche pas : ce qui tranche est le style effectif des tests, et il se compte.

Sur un projet Django où les deux sont installés, lancer `manage.py test` sur une suite écrite pour pytest ne produit pas d'erreur — il produit un run vide et vert.

## Test file glob

**Le glob n'est pas une convention, c'est une valeur de configuration.** `python_files` (section `[tool.pytest.ini_options]`, `pytest.ini` ou `setup.cfg`) **remplace** le défaut de pytest, il ne s'y ajoute pas. Le lire est la première opération ; le supposer est une erreur mesurée.

- Défaut pytest, quand `python_files` est absent : `test_*.py` **et** `*_test.py`.
- Valeur relevée sur la fixture : `["tests.py", "test_*.py", "*_tests.py"]` — donc `*_test.py`, pourtant l'un des deux défauts, n'y est **pas** collecté, et `tests.py` / `*_tests.py` le sont.
- `manage.py test` (unittest) : `test*.py`, motif non configurable par ce fichier — il se change par `--pattern`.

Emplacements des fichiers, par ordre de fréquence : un arbre `tests/` à la racine (package, avec `__init__.py`), un `tests/` par app Django, ou `<module>/tests.py` (convention Django d'origine). Les trois coexistent ; le glob ne dit pas où chercher, il dit quoi retenir de ce qui est trouvé.

E2E : pas de motif de nom dédié en Python. Les tests navigateur (`pytest-playwright`, Selenium) se distinguent par un **marker** (`@pytest.mark.e2e`) ou par un répertoire, pas par une extension. Voir `Known tooling gotchas` : un marker déclaré ne prouve pas qu'il classe quoi que ce soit.

## Test-count command

- **Nombre de tests** : `pytest --collect-only -q` — la dernière ligne rend `N tests collected`, ou `N/M tests collected (K deselected)` quand un filtre est actif.
- **Nombre de fichiers** : énumération du glob applicable. pytest n'expose pas de compteur de fichiers.

**Les deux nombres ne sont pas interchangeables, et l'écart est d'un ordre de grandeur** : 80 fichiers pour 1028 tests sur la fixture, soit ×12,8. Nommer lequel est rendu.

**Le comptage par défaut est déjà filtré.** `addopts` s'ajoute silencieusement à toute invocation, y compris `--collect-only`. Sur la fixture, `addopts` porte `-m 'not e2e and not e2e_federation'` : la commande nue rend 1027, pas 1028. Pour compter l'univers complet : `pytest --collect-only -q -o addopts=''`. Pour compter ce que le projet exécute réellement, garder `addopts` — mais alors dire que le nombre est filtré, et par quoi.

Deux flags à ajouter dans les deux cas, pour ne rien écrire dans le dépôt mesuré : `-p no:cacheprovider` (n'écrit pas `.pytest_cache/`) et `--no-cov` (n'écrit pas `.coverage`, et évite le coût d'instrumentation).

## Coverage command

`pytest-cov` (enveloppe de coverage.py). Reporter machine-lisible à demander explicitement — les reporters par défaut écrivent un tableau de terminal, pas un fichier exploitable.

```
pytest --cov=<package> --cov-config=pyproject.toml --cov-branch \
       --cov-report=xml:<chemin> --cov-fail-under=0 -p no:cacheprovider
```

- **`--cov-fail-under=0` neutralise la gate du projet.** Vérifié : sur les mêmes tests tous verts, avec `--cov-fail-under=50` pytest sort en **1**, avec `--cov-fail-under=0` il sort en **0**. Le rapport, lui, est écrit dans les deux cas — la ligne `Coverage XML written to file …` précède le `FAIL Required test coverage …`. Ce qui est fourni ici est un rapport à lire, pas un gate à faire passer ; laisser la gate active fait lire un échec de couverture comme un échec de tests.
- **`--cov-branch` n'est pas optionnel si les branches doivent être lues.** Sans lui, coverage.py enregistre des lignes seulement : le `.coverage` porte `has_arcs = '0'` et le XML `branches-valid="0" branch-rate="0"`. Un classement au taux de branches sur un rapport en mode ligne classe tout à zéro branche, sans que rien ne l'indique.
- **`COVERAGE_FILE=<chemin>`** déplace le fichier de données hors du dépôt mesuré, quand celui-ci doit rester intact.
- Alternative sans pytest : `coverage run -m pytest …` puis `coverage xml -o <chemin>` — même données, deux étapes. `coverage json` produit la même chose en JSON.

**Univers du rapport, et les deux façons dont il ment.**

- **`--cov=<package>` définit l'univers, et il est plus étroit que le code de production.** Sur la fixture, `--cov=suddenly` laisse `config/` — settings, `urls.py`, ASGI — entièrement hors du dénominateur. Ce code n'est ni couvert ni non couvert : il est absent.
- **`[tool.coverage.run] omit` retire aussi du code applicatif réel.** Sur la fixture, `omit` retire deux fichiers de vues de 21 ko cumulés, présents sur disque et non triviaux, tandis que les autres `*_views.py` des mêmes packages restent au rapport. Un `omit` n'est pas une liste d'exclusions structurelle : c'est une liste que quelqu'un a écrite, et elle peut porter sur du code qu'il faut classer. C'est le `Source glob & exclusions` ci-dessous qui définit l'univers à classer ; le rapport ne fait que l'enrichir, et un fichier du glob absent du rapport est **non couvert**, pas inexistant.

**Les chemins du rapport sont relatifs au package couvert.** Le XML porte `filename="characters/models.py"`, pas `suddenly/characters/models.py` : le préfixe passé à `--cov=` est retiré. Croiser le rapport avec un glob de dépôt exige de le remettre. `line-rate` est une **fraction** (`0.1509`), pas un pourcentage.

## Source glob & exclusions

Code de production classable, par convention de la stack :

- Django : `<projet>/<app>/*.py` — `models.py`, `views.py` et tout `*_views.py`, `services.py`, `serializers.py`, `forms.py`, `tasks.py`, `signals.py`, `managers.py`, `permissions.py`, `templatetags/*.py`, `management/commands/*.py`
- Package plat : `src/<package>/**/*.py`, `<package>/**/*.py`
- FastAPI / Flask : `app/**/*.py`, `api/**/*.py`, `routers/**/*.py`, `schemas/**/*.py`

Jamais classable — ces chemins ne portent aucun comportement propre à cette stack :

- Environnements et caches : `venv/`, `.venv/`, `env/`, `site-packages/`, `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `.tox/`, `htmlcov/`, `build/`, `dist/`, `*.egg-info/`
- Migrations : `*/migrations/*.py` — code généré par `makemigrations`. **Exception à examiner, jamais à exclure d'office** : une migration portant un `RunPython` contient de la logique écrite à la main, qui transforme des données de production et ne s'exécute qu'une fois.
- Configuration et points d'entrée : `manage.py`, `wsgi.py`, `asgi.py`, `settings.py` ou `settings/*.py`, `celery.py` (l'instanciation `Celery(...)` du projet, à distinguer des `tasks.py` qui portent du comportement), `conftest.py`, `noxfile.py`, `setup.py`
- Déclaratif sans logique : `apps.py`, `admin.py` sans méthode surchargée, `urls.py` de pur routage, `__init__.py` de réexport, `*.pyi`
- Code généré : sorties de `protoc`, clients OpenAPI générés, `*_pb2.py`
- Les fichiers de test eux-mêmes, `tests/factories.py`, les fixtures et doubles

**Un répertoire n'est pas un package.** Un dossier ne contenant que `__pycache__/`, sans aucun `.py` source, est le résidu d'un package supprimé — constaté sur la fixture. Il ne porte rien à classer, et il apparaît pourtant dans toute énumération faite au niveau du système de fichiers.

## Risk signals

**Ne classent jamais un tier** : un signal peut faire remonter un gap en tête de table, jamais changer la preuve exigée pour lui.

À forte conséquence dans cette stack :

- **Écriture destructrice via l'ORM** — `.delete()` sur un queryset, `.update()` en masse, `bulk_create`/`bulk_update`, `on_delete=CASCADE` sur une relation, `raw()`/`extra()`. L'erreur n'y est pas rattrapable par un rechargement, et le queryset porte la portée aussi discrètement qu'un filtre absent.
- **Migrations de données** — tout `RunPython` : écrit du code écrit à la main, sur des données réelles, exactement une fois, et sans annulation garantie (`reverse_code` est facultatif).
- **Autorisation** — `permission_classes` DRF, décorateurs `@login_required`/`@permission_required`, `has_perm`, `get_queryset` filtrant par propriétaire, adaptateurs allauth, tout `request.user` comparé à un objet.
- **Argent** — calcul de montant, remise, taxe, appel à une passerelle de paiement, tout ce qui produit une somme affichée ou débitée.
- **Signaux et hooks implicites** — `post_save`, `pre_delete`, `m2m_changed`, `save()` surchargé : l'effet est déclenché à distance du code qui le provoque, et n'apparaît dans aucune pile d'appel lue à l'œil.
- **Tâches asynchrones** — `@shared_task` / `@app.task` Celery, tâches périodiques `django-celery-beat` : elles s'exécutent hors du cycle requête, souvent sans utilisateur, et leurs échecs ne remontent à aucune réponse HTTP.
- **Entrées externes non maîtrisées** — handlers de webhook, `inbox` ActivityPub, désérialisation de payload tiers, `pickle`/`yaml.load` sur données stockées : le code y reçoit ce qu'il n'a pas produit.
- **Configuration transverse** — `settings/*.py`, `INSTALLED_APPS`, middlewares, `AUTH_USER_MODEL` : une valeur y rayonne sur tout le projet, et le code qui la lit est rarement celui qui casse.

### Frontières externes de la stack

Dépendances à un contrat qu'on ne maîtrise pas : elles cassent sans qu'aucune ligne du dépôt ne bouge, donc aucun signal interne (churn, branches, blast radius, commits de fix) ne les remonte jamais. Détection par le manifeste (`pyproject.toml`, `requirements*.txt`), par les variables d'environnement attendues (`.env.example`), et par tout client HTTP visant un domaine que le projet ne possède pas.

- **Paiement** — `stripe`, SDK PayPal/Mollie/Adyen : SDK versionné **et** contrat d'API distant, les deux pouvant bouger séparément.
- **Identité déléguée** — `django-allauth` et ses providers, clients OIDC/OAuth : le contrat est celui du fournisseur, pas celui du dépôt.
- **Stockage et infrastructure objet** — `django-storages[s3]`, `boto3`, clients S3-compatibles : signatures, permissions et URLs présignées relèvent du fournisseur.
- **Clients d'API sortants** — `httpx`, `requests`, `aiohttp` vers un domaine tiers ; fédération ActivityPub, webhooks émis.
- **Courtier et cache** — Celery sur Redis/RabbitMQ, cache Redis : le protocole est stable, la disponibilité ne l'est pas, et le chemin dégradé est rarement exercé.
- **Envoi d'e-mail** — backend SMTP ou API transactionnelle : silencieusement remplacé par `locmem` en test, donc jamais exercé par la suite.

Ce qu'un test peut y prouver **sans appeler le fournisseur** : que la charge utile construite est bien celle qu'on croit envoyer, et que le **chemin dégradé** tient quand le fournisseur échoue, renvoie un schéma inattendu ou ne renvoie rien. Ce qu'il ne peut pas prouver : que le fournisseur accepte encore cette charge utile — cela relève de la surveillance, pas de la suite. Ce fichier n'arbitre pas : il constate ce que la stack rend prouvable, sans nommer de tier ici non plus (la ligne d'ouverture de ce champ vaut pour tout ce qui suit). Le plafond de coût et l'arbitrage appartiennent au consommateur, quel qu'il soit.

Structurellement sans comportement propre à prouver dans cette stack :

- `apps.py`, `urls.py` de pur routage, `admin.py` sans méthode surchargée.
- Sérialiseurs DRF déclaratifs sans `validate_*` ni `create`/`update` surchargés ; formulaires sans `clean_*`.
- `__str__`, `__repr__`, `Meta`, propriétés d'accès sans logique, constantes de module.
- Réexports de `__init__.py`, code généré par un compilateur de schéma.

## Anchor boundary

**Ne nomme aucun tier, et n'en dérive aucun.** Ce champ situe où tombe, dans cette stack, la frontière entre une preuve **ancrée** (elle traverse la frontière publique réelle du produit) et une preuve **interne** (elle reste en process). Quelle preuve un cas donné est dû se décide ailleurs, et rien de ce qui suit ne l'infléchit : une même position de frontière peut être due ancrée ou non selon ce que le consommateur exige, et un fichier de stack qui trancherait cela se substituerait à lui.

### Générique Python

- Fonction pure, méthode de service, validateur, calcul → **en process**, sans discussion.
- Accès disque ou base via une couche du projet → reste **en process** : traverser une frontière d'I/O locale n'est pas traverser la frontière du produit.
- Un double (`unittest.mock`, `pytest-mock`, `responses`, transport `httpx` simulé) posé sur la chose même qui est sous test **n'établit rien, à aucune position de frontière** : ce n'est pas une frontière déplacée, c'est l'objet du test remplacé.

### Django (si `manage.py` / `django` détecté)

- **Le test client Django n'ancre pas.** `django.test.Client`, la fixture `client` de pytest-django et `rest_framework.test.APIClient` construisent une requête en mémoire et appellent le handler WSGI directement : aucun socket, aucun serveur, aucune sérialisation réseau. L'observation reste **interne**, quel que soit le réalisme apparent de l'URL et du code de statut. C'est le cas que ce champ existe pour nommer dans cette stack.
- `live_server` (pytest-django) / `LiveServerTestCase` démarrent un vrai serveur WSGI sur un port : la requête traverse une frontière réseau réelle. Mais sans navigateur, cela reste un double local du produit — le rendu, le JavaScript et le parcours n'y sont pas. Position intermédiaire, à nommer comme telle et non à ranger d'office d'un côté.
- Un parcours utilisateur complet observé par un navigateur réel (`pytest-playwright` ou Selenium contre `live_server`) → **seule la frontière réelle l'établit**.
- **Celery en mode `ALWAYS_EAGER` n'ancre pas la chaîne asynchrone.** La tâche s'exécute en ligne, dans le process appelant : ce qui est prouvé est le corps de la tâche, jamais le trajet par le courtier, la sérialisation de ses arguments, ni le comportement au réessai.
- **Les migrations ne sont établies que par leur application réelle.** Une suite lancée avec `--no-migrations` (ou `--nomigrations`) construit le schéma directement depuis les modèles : elle passe alors même que les migrations sont cassées ou divergentes du modèle.
- Le backend e-mail est remplacé par `locmem` sous `DJANGO_SETTINGS_MODULE` de test : `mail.outbox` prouve qu'un message a été **construit**, jamais qu'il a été **envoyé**.

## Known tooling gotchas

- **`addopts` s'applique à tout, y compris à ce qu'on croit être une mesure neutre** — la valeur de `addopts` (pyproject / pytest.ini) est concaténée à chaque invocation, `--collect-only` compris. Un comptage « brut » peut donc être déjà filtré par un `-m 'not …'`, et une commande de couverture ad hoc peut hériter d'une gate qu'on n'a pas demandée. Détection : lire `addopts` avant toute mesure ; comparer `pytest --collect-only -q` et `pytest --collect-only -q -o addopts=''`. Fix : `-o addopts=''` pour mesurer l'univers, `addopts` intact pour mesurer ce que le projet exécute — et dire lequel des deux est rendu.
- **Code de sortie pollué par la gate de couverture** — `--cov-fail-under` fait sortir pytest en 1 alors que tous les tests passent. Vérifié : mêmes tests, exit 1 avec `--cov-fail-under=50`, exit 0 avec `--cov-fail-under=0`. Un consommateur qui lit le code de sortie conclut « suite rouge » sur une suite verte. Détection : la sortie porte `FAIL Required test coverage of N% not reached` et aucun `failed` dans le résumé. Fix : `--cov-fail-under=0` pour toute mesure, et lire le résumé, jamais le seul code de sortie.
- **Rapport en mode ligne pris pour un rapport avec branches** — sans `--cov-branch`, coverage.py n'enregistre pas d'arcs. Le fichier `.coverage` porte alors `has_arcs = '0'` (lisible : `sqlite3 .coverage "select key,value from meta"`) et le XML `branches-valid="0"`. Rien dans le rapport ne signale que la mesure n'a pas été demandée. Détection : `branches-valid="0"` alors que le code comporte manifestement des conditions. Fix : ajouter `--cov-branch` et remesurer ; ne jamais lire une couverture de branches à 0 % comme un résultat.
- **`python_files` redéfini, fichiers invisibles** — `python_files` remplace le défaut. Un projet qui déclare `["tests.py", "test_*.py", "*_tests.py"]` ne collecte pas `*_test.py`, pourtant un défaut de pytest : le fichier existe, contient des tests, et n'est jamais exécuté. Détection : comparer l'énumération du système de fichiers (`test_*.py` **et** `*_test.py`) au `--collect-only`. Fix : lire `python_files` avant d'écrire un glob ; signaler tout fichier de test présent hors du motif configuré.
- **Marker déclaré, jamais appliqué** — un marker inscrit dans `markers` et filtré par `addopts` peut n'être porté par aucun test : le filtre s'applique alors à l'ensemble vide. Mesuré : `e2e_federation` déclaré et exclu du run par défaut, **zéro** test le portant, et un fichier nommé `test_federation_e2e.py` dont le docstring affirme qu'il en est exclu alors que ses tests tournent tous dans le run par défaut. Détection : `pytest --collect-only -q -m '<marker>'` — s'il rend 0, le filtre ne filtre rien. Fix : ne jamais déduire la composition d'une suite de ses markers déclarés ni de sa documentation ; la déduire de `--collect-only`.
- **Ce que le projet dit de sa suite diverge de ce que sa suite fait** — sur la même fixture, la note de test interne annonce un seuil de couverture de 80 % là où la configuration en impose 50, et le docstring d'un fichier décrit une exclusion inexistante. Deux documents, deux affirmations fausses, aucune ne produisant d'erreur. Détection : recouper systématiquement toute affirmation de doc contre `pyproject.toml` et contre `--collect-only`. Fix : la configuration et la collecte font foi ; citer la doc comme un écart à signaler, jamais comme une source.
- **Deux environnements virtuels, deux versions du runner** — `venv/` et `.venv/` coexistants dans le même dépôt, portant ici pytest 9.0.2 et 9.1.1. Selon celui qui est activé, la collecte et les avertissements diffèrent. Détection : `ls -d venv .venv` ; `<env>/Scripts/python.exe -m pytest --version` (`<env>/bin/python` hors Windows). Fix : invoquer explicitement l'interpréteur de l'environnement mesuré, ne jamais compter sur un `pytest` de `PATH`.
- **`manage.py test` sur une suite pytest : un run vide et vert** — voir `Test runner(s)`. Aucun message ne signale que rien n'a été collecté au-delà du `Ran 0 tests`. Détection : compter les classes dérivant de `TestCase` ; zéro sur un projet à plusieurs centaines de tests signe une suite pytest. Fix : ne jamais substituer un runner à l'autre pour mesurer.
- **Base de test partagée entre runs concurrents** — le nom de la base de test dérive de celui de la base de développement (`test_<nom>`) et est donc identique pour tous les processus pytest de la machine. Deux runs simultanés se détruisent mutuellement le schéma, avec des erreurs qui ressemblent exactement à des régressions (`relation "…" does not exist`). Détection : erreurs de schéma non reproductibles, sur des tests sans rapport entre eux. Fix : isoler par `DATABASE_URL` distinct, ou par `--create-db` sur une base dédiée ; ne jamais chercher dans le code la cause d'un échec de cette forme.
- **Une mesure qui écrit dans le dépôt mesuré** — pytest écrit `.pytest_cache/`, `--cov` écrit `.coverage`, tous deux dans le répertoire courant. Sur un dépôt à ne pas modifier, c'est une écriture non intentionnelle. Fix : `-p no:cacheprovider`, `--no-cov` quand la couverture n'est pas demandée, et `COVERAGE_FILE=<chemin hors dépôt>` quand elle l'est.

## Domain resolution

**Comment retrouver ici un domaine déjà nommé, jamais lesquels existent.** Quels domaines un produit possède, et à quel niveau, s'établit ailleurs. Ce champ **complète** une résolution ; il ne prime jamais sur ce qui est énoncé explicitement à propos du code du projet. Champ sémantique : il ne retire ni n'ajoute rien à ce que `Source glob & exclusions` déclare classable.

### Par les répertoires

- **App Django** — `<projet>/<domaine>/` portant `models.py`, `apps.py`, `views.py`. C'est la découpe par domaine la plus courante de la stack.
- **`INSTALLED_APPS` est plus fiable que l'arbre.** Il énumère les apps réellement chargées, distingue celles du projet de celles des dépendances, et exclut d'office les répertoires morts. Le `label` d'une `AppConfig` peut différer du nom du dossier ; c'est le `label` qui circule dans le reste du framework.
- **Package plat** — `src/<package>/<domaine>/`, `<package>/<domaine>/`, `apps/<domaine>/`.
- **FastAPI / Flask** — `routers/<domaine>.py`, `api/v1/endpoints/<domaine>.py`, blueprints `<domaine>/`. Le préfixe d'`APIRouter`/`Blueprint` (`prefix="/<domaine>"`) est plus fiable que le nom de fichier.
- **Monorepo Python** — `packages/<domaine>/`, chacun avec son `pyproject.toml`. Le champ `[project] name` est plus fiable que le nom du dossier, qui est libre.

**La découpe par couche ne porte pas le domaine.** `models.py`, `views.py`, `serializers.py`, `forms.py`, `services.py`, `tasks.py`, `signals.py`, `admin.py`, `urls.py`, `migrations/`, `management/commands/`, `templatetags/` sont des couches, à l'intérieur d'un domaine. Sur un arbre organisé par couche au premier niveau (`models/`, `views/`, `services/`), aucun répertoire n'expose de domaine — il se lit alors dans les identifiants.

### Par les identifiants

- **Noms de fichier** — `<domaine>_views.py`, `<domaine>_service.py`, `<domaine>_tasks.py`, `<domaine>_forms.py`, et sous une couche `models/<domaine>.py`.
- **Symboles exportés** — `<Domaine>Serializer`, `<Domaine>ViewSet`, `<Domaine>Service`, `<Domaine>Manager`, `<Domaine>Form`, `<Domaine>Config` (AppConfig), `<Domaine>QuerySet`.
- **Routes** — dans un `urlpatterns`, le premier segment du préfixe (`path("<domaine>/", include(…))`) ; sous FastAPI, le `prefix` de l'`APIRouter`. Ce qui suit est la ressource ou le verbe.
- **Tâches Celery** — le nom qualifié d'une tâche (`<package>.<domaine>.tasks.<verbe>`) porte le domaine à l'avant-dernier segment.

### Prudences

- Un même domaine se graphie de plusieurs façons dans le même dépôt (`billing`, `Billing`, `BILLING_`, `billing_service`). Apparier sans casse et sans séparateur.
- Un répertoire de premier niveau peut nommer une **technique** et non un domaine : `core/`, `common/`, `shared/`, `utils/`, `helpers/`, `api/`, `config/`, `lib/`.
- Un répertoire sans aucun `.py` source n'est pas un package : le résidu d'une app supprimée reste visible dans l'arbre et porte encore son ancien nom de domaine.
- **Un arbre `tests/` peut rejouer la découpe par domaine sans en faire autorité.** Un fichier de test se rattache au domaine du code qu'il exerce, pas à son propre emplacement — la fixture mesurée a un `tests/<domaine>/` en miroir des apps, et sept fichiers de test à sa racine qui n'appartiennent à aucun.

## Canonical E2E tool

`pytest-playwright`, quand détecté. À défaut, Selenium (`selenium`, `pytest-selenium`) sur les projets plus anciens. Informationnel uniquement : un outil établi se documente, il ne se remplace pas.
