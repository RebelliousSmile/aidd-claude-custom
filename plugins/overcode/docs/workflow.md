# Quelle skill, quand

Cette page route une situation vers une skill. Le **pourquoi** des frontières est dans [`concepts.md`](concepts.md) ; le détail d'exécution vit dans chaque `SKILL.md`.

Les skills s'invoquent sous la forme `/overcode:<skill>`.

## Table de routage

| Ta situation | Skill |
|---|---|
| « où en est le projet ? » | [`status`](#santé-projet--status) action `report`, ou l'alias `previously` |
| « ce document dit-il encore la vérité ? » | [`taste`](#obsolescence--taste) |
| « qu'est-ce qui va nous coûter cher dans six mois ? » | [`foresee`](#prospective--foresee) |
| « le site est lent » | [`web-optimize`](#audits-de-performance) |
| « le backend / la base est lente » | [`data-optimize`](#audits-de-performance) |
| « on n'est pas visibles sur Google » | [`seo-optimize`](#audit-seo--geo) |
| « la fédération ActivityPub déconne » | [`ap-optimize`](#activitypub) |
| « faut-il écrire ce test ? » | [`control`](#gouvernance-des-tests--control) |
| « cette skill se comporte-t-elle correctement ? » | [`behave`](#tests-comportementaux--behave) |
| « la mémoire projet est en vrac » | [`harvest`](#maintenance) puis [`reconcile-normative`](#maintenance) |
| « il faut un README / un CHANGELOG » | [`readme`](#documentation) · [`changelog`](#documentation) |
| « ce chantier est trop gros » | [`decompose`](#planification--decompose) |
| « cette feature marche-t-elle de bout en bout ? » | [`journey`](#recette--journey) |
| « je ne comprends rien à ce sujet » | [`baby`](#vulgarisation--baby) |
| « je veux enchaîner plusieurs skills » | [`alias`](aliases.md) |

---

## Santé projet — `status`

Trois actions indépendantes, à ne pas confondre :

| Action | Ce qu'elle rend |
|---|---|
| `memory` | synthétise la mémoire projet et exporte les décisions |
| `report` | rapport complet — audit, sécurité, plan à 7 jours |
| `audit` | qualité, fraîcheur et contradictions **des fichiers de mémoire eux-mêmes** |

`audit` est le méta-niveau : il ne juge pas le projet, il juge ce qu'on a écrit sur le projet.

Pour une reprise de contexte rapide en début de session, l'alias `previously` est plus direct : snapshot git + tests + lint, avec le contexte de statut.

## Obsolescence — `taste`

Deux actions selon la cible :

- **`assess-doc`** — extrait les affirmations d'un `.md` et les vérifie contre le codebase, liens Markdown relatifs compris. Sans argument, `/overcode:taste` passe en **mode scan** : il groupe les trouvailles par cause racine et produit un plan de correction ordonné.
- **`assess-code`** — imports dépréciés, imports relatifs cassés, appels à des symboles supprimés, violations de règles, TODO/FIXME périmés. Chemin requis.

C'est la skill à lancer avant de faire confiance à une doc qu'on n'a pas relue depuis longtemps.

## Prospective — `foresee`

Analyse à moyen terme de documents, de code ou de dépendances. Elle cherche ce qu'aucun test ni linter ne signale : un couplage qui va coincer, une dépendance qui va devenir un problème, un plan dont une hypothèse ne tiendra pas.

Trois flags, valables pour toutes les actions :

| Flag | Effet |
|---|---|
| *(aucun)* | sortie inline uniquement |
| `--discuss` | présente chaque trouvaille et attend une réponse — **n'écrit aucun fichier** |
| `--plan` | après la sortie inline, crée un plan de correction dans `aidd_docs/tasks/` |

Sur un répertoire, l'analyse de code borne délibérément sa largeur : elle sélectionne les fichiers les plus déterminants (`--depth`, 10 par défaut) et les analyse en profondeur. Ce n'est pas un scanner exhaustif — la profondeur est la valeur.

## Audits de performance

Même forme pour les deux : détection de stack → chargement des pivots `sc-*` → checklist → roadmap priorisée. Un argument optionnel borne le périmètre à une route ou une action.

**`web-optimize`** — LCP, CLS, INP, TBT, TTFB, taille de bundle, ressources bloquantes, N+1 **au rendu**.

**`data-optimize`** — N+1 **de la couche données**, nombre de requêtes, pagination, listeners temps réel, taille de payload, stratégie de cache, quota et coût, indexation, règles de sécurité, observabilité.

Les deux détectent un monorepo et **s'arrêtent pour demander** quel package auditer plutôt que d'auditer la racine. Les deux capturent une baseline chiffrée avant de recommander quoi que ce soit — sans mesure de départ, une roadmap de perf est une opinion.

## Audit SEO / GEO

`seo-optimize` couvre le référencement classique **et** l'optimisation pour les moteurs génératifs : indexabilité, title/meta/H1, données structurées, extractabilité par les IA, SEO local et Google Business Profile, E-E-A-T, Core Web Vitals comme signal de classement.

Il détecte le type de site (`local-business`, `saas`, `blog/content`, `e-commerce`, `docs`) — c'est ce qui pilote la section de pivot chargée. Il capture une baseline falsifiable (positions GSC, score GBP, grille de citations IA) avant recommandation.

Sortie : roadmap priorisée **plus le copy prêt à coller**.

## ActivityPub

`ap-optimize` audite une implémentation de fédération : idempotence de l'inbox, vérification des signatures HTTP, fan-out de delivery, cache actor/clés, conformité de pagination de l'outbox, rate limiting, circuit breaker, conformité AS2, sécurité, observabilité.

## Gouvernance des tests — `control`

Six actions, à choisir selon le moment :

| Action | Moment |
|---|---|
| `stats` | l'état des lieux d'un coup d'œil — **le point d'entrée**, il route vers les quatre autres |
| `write` | **avant** d'écrire un test — décide du tier, puis délègue l'écriture à `aidd-dev:06-test` |
| `audit` | traque les tests sans valeur |
| `strengthen` | classe par risque les tests manquants |
| `align` | réaligne le document de stratégie de test sur ce que le projet fait réellement |
| `configure` | détecte l'outillage mal configuré (couverture qui ne fait pas échouer le build, par exemple) |

Quand on ne sait pas par où commencer, on commence par `stats`. Tout nouveau test, quelle que soit l'action qui l'a fait remonter, passe par `write` — aucune action n'en écrit en contournant ce passage.

`align` gère aussi le solde net d'une bascule de phase : passer en `sustaining` produit un lot de suppression **caractérisé par son critère**, pas une liste arbitraire.

`configure` est à part : elle vérifie le câblage de l'outillage, ce qui est vrai ou faux indépendamment de la phase du projet. Elle ne prend ni phase ni périmètre.

Cette skill ne se déclenche jamais d'elle-même — uniquement sur `/overcode:control`. Son modèle complet est dans [`control.md`](control.md).

## Tests comportementaux — `behave`

Harness pour tester des **prompts** : skills, agents, workflows pilotés par le langage.

| Action | Rôle |
|---|---|
| `scaffold` | écrit une suite de scénarios (Situation → Comportement attendu → Critères de passage) |
| `run` | joue la suite en dry-run jugé, contre une fixture peuplée, **sans muter de données réelles** |
| `regress` | rejoue une suite pour la non-régression |
| `review` | audite une suite existante — couverture comportementale + qualité par scénario (grille à 7 axes) |

Pour les tests unitaires et d'intégration du code, c'est `control` puis le runner du projet — pas `behave`.

## Maintenance

**`harvest`** — cycle large : réconcilie le tracker avec les plans traités, extrait les décisions non évidentes vers la mémoire et les règles, purge les fichiers de tâche éphémères, puis passe méthodiquement en revue ce qui reste.

**`reconcile-normative`** — une seule question, traitée à fond : le normatif est-il cohérent entre les archives (`decisions/`), la mémoire (`memory/`) et les règles actives (`.claude/rules/`) ? Il détecte redondances, contradictions, patterns non codifiés et règles périmées.

L'ordre naturel est `harvest` d'abord (il alimente la mémoire), `reconcile-normative` ensuite (il la met en cohérence).

## Documentation

**`readme`** — `write` depuis zéro (complet, draft ou fragment), `update` sur un README existant, globalement ou section par section. Il suit la guideline d'authoring du dépôt.

**`changelog`** — `generate` depuis l'historique git au format Keep a Changelog, commit et tag annoté signé. L'action `curate` comble les versions non documentées et condense les cycles majeurs antérieurs en résumés bornés (≤ 20 items).

Ni l'un ni l'autre ne touche aux numéros de version dans `package.json` ou `Cargo.toml` — c'est l'alias `bump-plugin` pour les plugins de cette marketplace.

## Planification — `decompose`

Méthode Mikado : décompose un objectif en graphe de dépendances par questions-réponses itératives, puis génère des fichiers YAML sous `mikado/<graphName>/`.

À utiliser quand un chantier est trop gros pour être attaqué de front et qu'on cherche l'ordre des étapes sûres, pas l'implémentation.

## Recette — `journey`

Exécute un parcours utilisateur depuis une issue GitHub ou GitLab, journalise les résultats Playwright étape par étape dans un rapport `<plan>.journey.md`, et poste le résumé et la conclusion sur l'issue.

Prérequis : une issue existante **et** un fichier de plan correspondant.

## Vulgarisation — `baby`

Explique, réécrit ou compare un sujet en langage progressif et concret, sans jargon non défini. Utile pour un transfert de contexte vers un non-spécialiste, ou pour présenter un arbitrage technique et ses compromis à qui doit trancher sans être du métier.

## Voir aussi

- [`concepts.md`](concepts.md) — le modèle des pivots et les frontières entre skills voisines
- [`aliases.md`](aliases.md) — enchaîner plusieurs skills en une commande
