# Route

Classe une intention en classe de cas et émet la séquence exécutable. Répond à *quoi lancer*, pas à *ce que c'est* (`01-explain`). Émet et s'arrête — n'invoque aucun verbe.

## Inputs

- L'intention énoncée et la **signature d'entrée** : ce que le consommateur détient (référence visuelle multi-pages, brief écrit, source existante, un élément à faire évoluer, des instances qui divergent, un élément à livrer).
- L'**état du contrat**, observé et non supposé : `release.json` présent ⇒ figé ; artefacts en brouillon sans `release.json` ⇒ brouillon ; aucun ⇒ absent.
- Les **pivots installés** dans la session.
- Quand un pivot est installé et sa stack correspond : la table `## Phases` de son **workflow de plateforme** (`plugins/sc-<langage>/skills/design-bridge/references/workflow-<plateforme>.md`). Lecture obligatoire, pas facultative — c'est le seul chemin par lequel les phases d'un pivot atteignent le consommateur.

## Process

1. Classer en une des six classes (`${DESIGN_PLUGIN_ROOT}/skills/detail/references/workflow-classes.md`), à partir de la signature d'entrée croisée avec l'état du contrat.
2. Si la classe énoncée par le consommateur contredit l'état observé, **signaler l'écart** et re-classer sur l'état réel — jamais corriger en silence.
3. Énoncer la précondition `harness` si la classe l'exige (référence pas encore mesurable).
4. Appliquer la règle de résolution des pivots (`${DESIGN_PLUGIN_ROOT}/references/sc-pivot-contract.md § Règle de résolution`) :
   - pivot installé **et** stack correspondante → la classe **étendue** par le workflow de plateforme du pivot ;
   - pivot absent, ou installé mais stack non correspondante → la classe **seule**, l'absence énoncée + recommandation conditionnelle d'installer `sc-<langage>`.
5. **Extension présente : ouvrir le workflow et fusionner.** Lire sa table `## Phases` — les cinq titres de `sc-pivot-contract.md § Cinq titres requis` sont un jeton d'interface, ils garantissent que cette lecture aboutit sur n'importe quel pivot. Puis dériver la séquence unique, sans interprétation :
   - chaque phase qui instancie un verbe **remplace** ce verbe dans la séquence de la classe, en gardant son libellé natif ;
   - chaque phase `off-funnel` s'insère à sa **position** déclarée (`avant <verbe>`, `après <verbe>`, `fin`) ;
   - une phase dont le verbe ancre est **absent de la séquence de la classe** est omise, l'omission énoncée — jamais rapprochée du verbe le plus proche ;
   - une phase `off-funnel` sans position déclarée est un **défaut du pivot** : la signaler nommément et la placer en fin, jamais la deviner ni la taire.
6. Émettre la séquence : phases et verbes dans l'ordre, checkpoints humains, gates de sortie, condition d'arrêt. Puis s'arrêter.

## Outputs

- L'id de la classe, **la séquence fusionnée**, ses checkpoints humains, ses gates de sortie, sa condition d'arrêt.
- L'état de l'extension de plateforme : présente (et par quel pivot), ou absente (et quel `sc-<langage>` installer).
- Quand l'extension est présente, la séquence émise **compte au moins une ligne absente de `workflow-classes.md`**. Une sortie qui se réduit aux cinq verbes de la classe, extension annoncée présente, est fausse : elle nomme une extension qu'elle n'a pas lue.
- Les **capabilities** du workflow (`## Prerequisites (capabilities)`) qui n'ont aucune cible sur ce terrain, avec les phases qu'elles bloquent. Une séquence dont la dernière phase est inatteignable s'arrête en silence sur un vert ; l'énoncer est ce qui distingue un programme fini d'un programme interrompu.
- Aucun verbe invoqué, aucun artefact écrit.

## Test

Sur un contrat figé dont les instances divergent, `route` rend `contract-drift` avec la boucle corriger→re-linter et les deux gates. Désinstaller le pivot correspondant et rejouer : **même classe**, extension de plateforme énoncée absente, installation de `sc-<langage>` recommandée.

**Second test, sur l'extension elle-même** — le premier ne le couvre pas : il n'atteste que la présence du pivot, jamais la lecture de son workflow. Sur un terrain dont la stack correspond à un pivot installé, la séquence émise doit contenir une phase que `workflow-classes.md` ne déclare pas. Retirer sa ligne de la table `## Phases` du pivot et rejouer : **la phase disparaît de la sortie**. Sans cette bascule, une extension lue et une extension seulement nommée rendent la même chose.
