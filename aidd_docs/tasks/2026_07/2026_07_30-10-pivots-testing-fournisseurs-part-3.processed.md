---
type: plan
statut: livre
parent: 2026_07_30-10-pivots-testing-fournisseurs-master.md
part: 3
objective: "Ecrire le pivot testing de sc-python, verifie contre un projet Django reel, et rendre atteignables les trois lignes d'eval bloquees par son absence"
success_condition: "test -f plugins/sc-python/skills/sniff/references/capabilities/tools/testing.md && ! rg -q 'aucun pivot Python|no Python pivot' plugins/overcode/skills/control/evals/domains-scenarios.md"
iteration: 0
created_at: 2026-07-30T13:30:51Z
depends_on: [1, 2]
---

# Part 3 — Pivot `sc-python`

## Feature

`sc-python` (0.5.4) porte un arbre `capabilities/` de 5 dossiers et 12 fichiers, et **aucun** `testing.md`. Trois lignes d'eval de `overcode:control` sont N/A en permanence pour cette seule raison :

| Suite | Ligne | Champ non fourni |
|---|---|---|
| `authority-scenarios.md` | S6 | *Risk signals* |
| `matrix-scenarios.md` | M15 | *Anchor boundary* |
| `domains-scenarios.md` | S3 | *Domain resolution* |

C'est le pivot a plus fort rendement : il debloque trois lignes, et il est le seul a disposer d'une fixture reelle deja identifiee.

## Fixture

`C:\Users\fxgui\Documents\Perso\Projects\suddenly\_code\app` — Django, 80 fichiers de test, `aidd_docs/memory/TESTING.md` de 85 lignes, couverture **en mode ligne** (`has_arcs='0'`, donc pas de branches), et un `frontend/package.json`. **Lecture seule, dry-run** : aucune ecriture dans la fixture, aucune commande qui modifie son etat.

Ce projet est aussi le cas polyglotte de la part 1 — d'ou la dependance.

## Projection d'architecture

**Cree**
- `plugins/sc-python/skills/sniff/references/capabilities/tools/testing.md`

**Modifie**
- `plugins/overcode/skills/control/evals/authority-scenarios.md` — cause de N/A de S6
- `plugins/overcode/skills/control/evals/matrix-scenarios.md` — M15
- `plugins/overcode/skills/control/evals/domains-scenarios.md` — S3 (et la note :316 qui annonce que la cause se lira comme fausse)
- `plugins/sc-python/CHANGELOG.md`, `.claude-plugin/marketplace.json` — `sc-python` 0.5.4 → **0.6.0**
- *si A4 = inclus* : `plugins/overcode/skills/control/actions/02-audit.md:26` et `05-stats.md`

**Supprime** — rien.

## Emplacement

`capabilities/tools/testing.md`, aligne sur `sc-js`. Le glob `**/capabilities/**/testing.md` accepte n'importe quel parent, mais un emplacement identique d'un plugin a l'autre evite d'avoir a le redecouvrir. `sc-php` porte deja un `capabilities/testing/bruno.md` : c'est un pivot Bruno, d'une autre nature, il ne bouge pas (part 5).

## Les 10 champs

Redaction en francais si c'est la langue des autres fichiers `capabilities/` de `sc-python` — a verifier avant d'ecrire (contrat §*Language*), et si les titres divergent des noms de champ anglais, le pivot porte sa propre table de correspondance.

Points a etablir **par mesure sur la fixture**, pas par connaissance generale :
- *Test runner(s)* — `pytest` et/ou `manage.py test` ; la fixture tranche laquelle est reellement utilisee. E2E separement.
- *Test file glob* — `test_*.py` **et** `*_test.py` ; les 80 fichiers de la fixture disent lequel domine, et si `tests/` est un package.
- *Test-count command* — `pytest --collect-only -q` compte des **tests**, un glob compte des **fichiers** : nommer lequel est rendu.
- *Coverage command* — reporter machine-lisible explicite (`--cov-report=xml:...` / `json`), et le champ doit produire son rapport **independamment de toute gate** (`--cov-fail-under` ne doit pas conditionner l'ecriture). Signaler que la fixture est en mode ligne : `has_arcs='0'` → pas de branches, `--cov-branch` requis pour en avoir.
- *Source glob & exclusions* — jamais classifiables : `migrations/`, `settings/`, `manage.py`, `venv/`, `static/`, code genere.
- *Anchor boundary* — ou tombe la frontiere en Python web : le test client Django (`self.client`) **n'ancre pas** (in-process, court-circuite le serveur) ; ce que seule la frontiere reelle etablit. Le champ **positionne la frontiere, il ne dit jamais quelle preuve un cas merite** (contrat:24).
- *Risk signals* — a consequence structurelle : paiement, auth, ORM/persistance, suppressions, `settings` transverses, taches asynchrones. Non structurel : passe-plat de framework, serializers generes. Frontieres externes typiques et leur detection dans `requirements.txt` / `pyproject.toml`.
- *Known tooling gotchas* — sous forme (probleme, detection, correctif).
- *Domain resolution* — arbres d'apps Django (`<app>/` avec `models.py`/`views.py`), `apps/<domaine>/`, prefixes de classes. Meme interdits qu'en part 2 : aucune liste de domaines.
- *Canonical E2E tool* — informatif seulement.

## Phases

### Phase 1 — Mesure sur la fixture
- [x] Executer, en lecture seule, chaque commande candidate et enregistrer la sortie reelle
- [x] Relever la convention de nommage effective des 80 fichiers de test
- [x] Verifier que la commande de couverture ecrit bien son rapport sans gate
- **Critere d'acceptation** : aucun champ du pivot n'est ecrit sans une sortie de commande observee

> **Ce que la mesure a rendu que la connaissance generale aurait manque.** (1) `python_files` **remplace** le defaut de pytest au lieu de s'y ajouter : la fixture declare `["tests.py","test_*.py","*_tests.py"]`, donc `*_test.py` — un defaut pytest — n'est jamais collecte. (2) `--collect-only -q` rend **1027** et non 1028, parce que `addopts` ajoute silencieusement `-m 'not e2e and not e2e_federation'` ; `-o addopts=''` rend 1028. (3) La gate de couverture ne conditionne pas l'ecriture du rapport, mais elle conditionne le **code de sortie** : memes tests verts, exit **1** avec `--cov-fail-under=50`, exit **0** avec `=0`. Le premier sondage lisait le statut de `tail`, pas celui de pytest — refait avec `> /dev/null 2>&1; echo $?` sur chaque invocation. (4) `manage.py test` collecterait **zero** test ici : 0 sous-classe de `TestCase` contre 280 `def test_` de module et 218 classes `Test*` nues — un run vide et vert. (5) L'univers du rapport ment deux fois : `--cov=suddenly` laisse `config/` entierement dehors, et `omit` retire deux fichiers de vues de 21 ko cumules pendant que leurs voisins `*_views.py` restent.

### Phase 2 — Redaction
- [x] Ecrire les 10 sections, une par champ, titre enoncant le champ
- [x] DEC-001 : detection framework + wrapper, pas de duplication de ce que les autres `capabilities/` de `sc-python` disent deja, frontmatter `paths:` minimal
- [x] Controle : aucun consommateur nomme, aucun champ infere d'un voisin
- **Critere d'acceptation** : chaque question du contrat est repondable en lisant le seul pivot

> Frontmatter **vide** (`---` / `---`), comme `sc-js`, et le motif est ecrit dans le fichier : ce pivot ne s'applique pas a une famille de fichiers, il decrit une suite — un `paths:` l'attacherait a un declencheur qui n'a pas de sens ici.

### Phase 3 — Reprise des suites
- [x] Reecrire les causes de N/A de S6, M15, S3 : elles ne peuvent plus dire « pas de pivot Python »
- [x] Corriger la note `domains-scenarios.md:316`
- **Critere d'acceptation** : aucune cause de N/A ne survit a la lecture qu'un pivot existe desormais

> **Les trois lignes ne bougent pas de la meme facon, et le plan supposait qu'elles le feraient.** **M15** et **S6** deviennent scorables ; **S3 reste N/A**, sur une cause qui etait deja la et que le pivot ne pouvait pas lever — aucune des deux fixtures ne **declare** de domaine qu'un pivot pourrait laisser debout. Le plan comptait « trois lignes debloquees » ; la mesure en rend deux.
>
> **Et S6 se debloque autrement que prevu.** Sa cause « pas de pivot Python » avait deja ete levee en run 8 par un deplacement vers la fixture JS `choix-narratifs`, ou une **seconde** cause l'avait remplacee : sans *Coverage command*, `04-strengthen.md:63` rebase la population sur les modules sans aucune reference de test, et il ne restait plus de ligne classee qu'un signal puisse deplacer. La ligne revient sur `app`, ou les **deux** causes tombent — `pyproject.toml` y soude `--cov` et `--cov-fail-under=50` dans `addopts`, donc la population classee existe. Le run 8 concluait qu'il faudrait « une fixture avec des donnees de branches **et** un pivot » : c'etait trop exigeant, le rebase se declenche sur la **commande**, pas sur les branches. La variante `choix-narratifs` est conservee, barree et non scoree, avec sa cause. Les huit fichiers sources cites dans la nouvelle situation ont ete verifies sur disque (4 migrations `RunPython`, 2 `tasks.py` Celery, `activitypub/inbox.py`, 2 `services.py` a ecriture destructrice).
>
> **Trois constats hors des trois lignes, trouves en tirant le fil.** (1) `pivot-contract.md:3` et `SKILL.md:103` affirmaient tous deux *« Only `sc-js` ships one today »* — devenu faux par cette livraison meme, dans la **cible**. Corriges, avec la precision que les deux pivots livres ne sont pas un gabarit a recopier champ par champ. (2) `chaining-scenarios.md:266` consignait que **les deux fixtures etant sans pivot, toute la moitie raffinee par pivot de la cible n'etait jamais exercee par cette suite** — c'est le gain le plus large de la part, et il n'etait pas dans le plan. Annote comme clos, avec la consigne de re-verifier dans l'autre sens. (3) `measurement-scenarios.md:182` demandait une regle reconciliant le `omit` de couverture avec le glob source : le pivot la porte (*le glob definit l'univers, `omit` ne l'ampute pas, un fichier du glob absent du rapport est non couvert*), et la friction citait `celery.py` que le pivot ne nommait pas — ajoute.
>
> **Rien n'a ete reecrit dans les enregistrements de runs dates.** Les quatre corrections ci-dessus sont des annotations datees en fin de constat ; les clauses vivantes qui les contredisent portent la mention explicite qu'elles **priment** sur les runs plus anciens, parce qu'un en-tete declarant une ligne N/A prime sur la ligne elle-meme dans la lecture d'un juge.

### Phase 4 — Rejeu `behave`
- [ ] **Ne rien editer pendant le run** — correctifs apres retour de tous les verdicts (memoire `behave-eval-method`)
- [ ] Rejouer les 3 suites touchees
- [ ] Rapporter le Δ a **trois colonnes** : PASS, FAIL, **et le mouvement de N/A** — un « 0 FAIL » ne dit rien de la couverture
- [ ] Ne pas additionner les tallies inter-suites (denominateurs non commensurables : certaines comptent des cellules)
- [ ] Noter, sans le corriger, que le registre vivant dans le fichier de suite empeche le jugement a froid
- **Critere d'acceptation** : les 3 lignes ne sont plus N/A **par absence de pivot** ; si elles restent N/A pour une autre raison, la raison est nommee

### Phase 5 — Version
- [ ] `CHANGELOG.md` sc-python + `marketplace.json` 0.6.0, meme commit
- **Critere d'acceptation** : arbre propre

## ~~Si A4 est inclus — repli generique sans pivot~~ — **A4 refute, section sans objet**

Le master a **refute** A4 sur disque plutot que de le trancher : le defaut decrit n'existe pas. `02-audit.md:37-39` **nomme** `**/*.{test,spec}.*` comme *« the defect this states in place of »* et impose deja un repli sur la convention observee du projet ; `:26` porte le slot `unmatched`, pas un glob ; `05-stats.md:108` rend `enumerated: pivot test file glob | project convention <pattern>, approximate`. Le constat d'eval qui portait A4 (`authority-scenarios.md:233`, finding 1) est **perime** — ecrit avant le correctif, jamais rouvert. Rien a faire ici.

*(Un defaut voisin **subsiste** et n'est pas celui-la : `05-stats.md:152` n'enonce pas que l'absence de pivot n'est pas en soi une raison que les preuves ne puissent etre lues. Consigne ouvert a `measurement-scenarios.md:364`, hors perimetre de cette part.)*

## Risques

| Risque | Mitigation |
|---|---|
| Ecrire une commande « connue » plutot que mesuree | Phase 1 bloquante : pas de champ sans sortie observee |
| Modifier la fixture par une commande de test | Lecture seule, dry-run, aucune ecriture |
| Juger a chaud (registre dans le fichier de suite) | Defaut de harnais connu et ouvert ; le noter, ne pas le corriger ici |
| « 0 FAIL » lu comme succes | Δ a trois colonnes obligatoire |
| Le pivot Python masque le defaut de repli generique | A4 |

## Log

| Date | Evenement |
|---|---|
| 2026-07-30 | Cree |
| 2026-07-30 | Livre. Pivot ecrit (181 l., 10 champs, mesure sur un projet Django reel). Trois lignes reecrites et rejouees : matrix 17/18 -> 18/18 (0 N/A), authority 12/17 -> 13/17 (N/A 4 -> 3), domains 14/17 inchange, S3 N/A sur la moitie declaration seule. sc-python 0.5.4 -> 0.6.0, marketplace 3.7.0 -> 3.8.0. Jugement a chaud, divulgue dans les trois entrees. |
