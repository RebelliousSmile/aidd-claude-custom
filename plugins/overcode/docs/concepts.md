# Concepts

Ce qu'`overcode` est, et pourquoi il est construit ainsi. Pour savoir **quelle skill lancer quand**, va voir [`workflow.md`](workflow.md). Pour les chaînes d'alias, [`aliases.md`](aliases.md).

## Ce qu'est overcode

Un **socle transversal**, pas une stack. C'est le seul plugin de la marketplace marqué `recommended` : il s'installe globalement et s'applique à tous les projets, quel que soit leur langage.

Il étend le framework [AIDD](https://github.com/ai-driven-dev/aidd-framework) sur quatre axes qu'AIDD ne couvre pas :

| Axe | Question à laquelle il répond |
|---|---|
| **Maintenance** | l'état du projet enregistré correspond-il encore à ce qu'il est ? |
| **Analyse** | qu'est-ce qui va casser, mal vieillir, ou coûter cher plus tard ? |
| **Documentation** | ce qui est écrit dit-il encore la vérité ? |
| **Enchaînement** | comment jouer une séquence de skills sans la retaper à chaque fois ? |

## Le principe : agnostique par défaut, spécialisé par pivot

Aucune skill d'`overcode` ne code en dur la connaissance d'une stack. C'est le point d'architecture central du plugin, et il explique la forme de presque toutes les skills d'audit.

Une skill d'audit fonctionne en deux temps :

1. **Détecter** la stack depuis les manifestes du projet (`package.json`, `composer.json`, `pyproject.toml`, `Cargo.toml`, les lockfiles).
2. **Charger les pivots** — des fichiers de règles installés par les plugins `sc-*` sous `.claude/rules/07-quality/`. Aucun pivot trouvé → un schéma générique s'applique, et l'absence est énoncée.

| Skill | Pivots consommés |
|---|---|
| `web-optimize` | `perf-pivots-*.md` |
| `data-optimize` | `data-pivots-*.md` |
| `ap-optimize` | `ap-pivots-*.md` |

L'inversion de dépendance est délibérée : `overcode` ne connaît pas Laravel ni Nuxt. C'est `sc-php` et `sc-js` qui **déposent** leur savoir dans le projet, et `overcode` qui le ramasse. Ajouter le support d'une stack ne demande donc jamais de toucher `overcode` — c'est ce qui permet aux plugins `sc-*` d'évoluer à leur propre rythme.

Conséquence pratique : `/overcode:web-optimize` sur un projet Laravel sans `sc-php` installé produit un audit générique correct mais moins précis. L'installation du pivot est ce qui fait la différence entre « ton bundle est trop gros » et « ton `@vite` charge le manifest en dev à chaque requête ».

## Le partage de frontière entre skills voisines

Plusieurs skills se ressemblent de loin. Les frontières sont explicites, parce que c'est là qu'un mauvais routage coûte le plus.

**`web-optimize` vs `data-optimize`** — les deux détectent des N+1, mais pas les mêmes. `web-optimize` traite le N+1 *au rendu* (une page qui déclenche N requêtes pendant sa construction) ; `data-optimize` traite le N+1 *de la couche données* (des requêtes répétées sur la même collection ou table, indépendamment du rendu). Un même symptôme, deux couches, deux corrections.

**`behave` vs `control`** — `behave` teste des **prompts** : skills, agents, workflows pilotés par le langage. `control` gouverne les tests de **code** d'un projet. Un scénario `behave` juge un comportement de LLM ; `control` décide si un test unitaire mérite d'exister.

**`taste` vs `foresee`** — `taste` regarde le **présent** : cette affirmation est-elle encore vraie aujourd'hui, cet import pointe-t-il encore quelque part. `foresee` regarde le **moyen terme** : qu'est-ce qui va devenir un problème, sans être détectable par un test ou un linter aujourd'hui.

**`harvest` vs `reconcile-normative`** — `harvest` est un cycle de maintenance large (tracker, décisions, purge de l'éphémère). `reconcile-normative` ne traite qu'une question : le normatif est-il cohérent entre les archives, la mémoire et les règles actives.

## La densité, pas le nombre — le modèle de `control`

`control` mérite un mot à part, parce que son modèle est contre-intuitif.

Il ne borne **pas** le nombre de tests par un plafond. Il raisonne en **densité** : le nombre de cas de test rapporté aux points de branchement, lu contre **la médiane du projet lui-même**. Un module trois fois plus dense que la médiane du projet est suspect ; le même module dans un autre projet ne le serait pas.

La densité n'est pondérée par rien : elle se lit contre la médiane du projet, point. Ce que pondère la **phase**, c'est le classement par risque — quels critères pèsent lourd en ce moment, et dans quel ordre le résultat est restitué.

La phase est déclarée ou demandée, **jamais déduite** :

| Phase | Ce qu'on attend de la suite |
|---|---|
| `scaffolding` | peu de tests, sur les seuls invariants qui tiennent |
| `hardening` | montée en couverture ciblée sur le risque |
| `production` | régression protégée, coût de maintenance assumé |
| `sustaining` | un solde négatif est attendu — jamais exigé |
| `default` | neutralité choisie : aucun biais de classement, aucun lot de suppression |
| `undetermined` | la question a été posée, elle est restée sans réponse |

Le fait que la phase ne soit **jamais déduite** est un choix : un projet en `sustaining` ressemble beaucoup à un projet abandonné, et se tromper coûte soit des tests supprimés à tort, soit une suite qui gonfle sans fin.

Le modèle complet — les trois autorités, les domaines sémantiques, le chaînage des actions — est dans [`control.md`](control.md).

`control` porte `disable-model-invocation: true` — il ne se déclenche jamais tout seul, uniquement sur `/overcode:control`. C'est cohérent avec son pouvoir : une skill qui peut recommander de supprimer des tests ne doit pas s'inviter dans une conversation.

## Ce qu'overcode délègue

Le plugin décide et cadre ; il n'écrit pas le code de production.

- `control` décide du tier d'un test, puis **délègue l'écriture** à `aidd-dev:06-test`.
- Les skills d'audit produisent une **roadmap priorisée**, pas un patch.
- `decompose` produit un **graphe de dépendances** (méthode Mikado, fichiers YAML sous `mikado/<graphName>/`), pas une implémentation.

C'est la même séparation que dans `design` : le plugin garde le *quoi*, l'exécution revient à qui sait faire le *comment*.

## Voir aussi

- [`workflow.md`](workflow.md) — quelle skill pour quelle situation
- [`aliases.md`](aliases.md) — les dix chaînes d'enchaînement
