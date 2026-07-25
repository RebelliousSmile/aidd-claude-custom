# 02-route

Classe une intention en classe de cas et émet la séquence exécutable. Répond à *quoi lancer*, pas à *ce que c'est* (`01-explain`). Émet et s'arrête — n'invoque aucun verbe.

## Inputs

- L'intention énoncée et la **signature d'entrée** : ce que le consommateur détient (référence visuelle multi-pages, brief écrit, source existante, un élément à faire évoluer, des instances qui divergent, un élément à livrer).
- L'**état du contrat**, observé et non supposé : `release.json` présent ⇒ figé ; artefacts en brouillon sans `release.json` ⇒ brouillon ; aucun ⇒ absent.
- Les **pivots installés** dans la session.

## Process

1. Classer en une des six classes (`${CLAUDE_PLUGIN_ROOT}/skills/detail/references/workflow-classes.md`), à partir de la signature d'entrée croisée avec l'état du contrat.
2. Si la classe énoncée par le consommateur contredit l'état observé, **signaler l'écart** et re-classer sur l'état réel — jamais corriger en silence.
3. Énoncer la précondition `harness` si la classe l'exige (référence pas encore mesurable).
4. Appliquer la règle de résolution des pivots (`${CLAUDE_PLUGIN_ROOT}/references/sc-pivot-contract.md § Règle de résolution`) :
   - pivot installé **et** stack correspondante → la classe **étendue** par le workflow de plateforme du pivot ;
   - pivot absent, ou installé mais stack non correspondante → la classe **seule**, l'absence énoncée + recommandation conditionnelle d'installer `sc-<langage>`.
5. Émettre la séquence : verbes dans l'ordre, checkpoints humains, gates de sortie, condition d'arrêt. Puis s'arrêter.

## Outputs

- L'id de la classe, sa séquence, ses checkpoints humains, ses gates de sortie, sa condition d'arrêt.
- L'état de l'extension de plateforme : présente (et par quel pivot), ou absente (et quel `sc-<langage>` installer).
- Aucun verbe invoqué, aucun artefact écrit.

## Test

Sur un contrat figé dont les instances divergent, `route` rend `contract-drift` avec la boucle corriger→re-linter et les deux gates. Désinstaller le pivot correspondant et rejouer : **même classe**, extension de plateforme énoncée absente, installation de `sc-<langage>` recommandée.
