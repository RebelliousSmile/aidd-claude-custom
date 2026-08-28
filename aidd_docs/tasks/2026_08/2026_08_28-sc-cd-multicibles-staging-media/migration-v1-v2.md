# Migration du contrat SC-CD v1 vers v2

La v2 est une rupture explicite. Un contrat v1 est diagnostiqué, mais aucune commande distante n'est exécutée tant qu'il n'a pas été migré et validé.

## Correspondance

| v1 | v2 |
| --- | --- |
| une production implicite | `targets[]` avec id, phase, mode et fournisseur |
| commande globale | façade globale plus `target.invocation` explicite |
| source globale souvent mutable | source globale et ref immuable obligatoire en automata |
| opérations code/DB globales | opérations par `code`, `schema`, `data`, `media` et phases autorisées |
| trigger global | trigger par cible, manuel par défaut |
| sauvegarde/récupération globale | préconditions, preuve et récupération par opération et cible |
| synchronisation ou pull | uniquement `deploy:*` depuis local/checkout ; aucun pull ni flux cible-à-cible |

## Procédure

1. Recenser chaque destination réelle et lui donner un id stable.
2. Déclarer sa phase `staging` ou `production`, son mode `server` ou `automata`, son fournisseur et son contexte d'exécution.
3. Conserver une seule façade projet et enregistrer l'invocation exacte de chaque cible.
4. Classer code, migrations, données et médias. En production, `data` et `media` deviennent autoritatifs sur la cible.
5. Déclarer un verrou, une garde distante et une `lifecycleRevision` par cible.
6. Pour un staging miroir, prouver inventaire, empreintes, aperçu, sauvegarde, reprise et vérification finale.
7. Résoudre un ref immuable et un checkout propre pour chaque automata.
8. Valider avec `node tools/sc-cd/validate-project-contract.mjs deploy/contract.json` avant de générer une enveloppe.

## Promotion staging vers production

La promotion sur place exige que les écritures applicatives puissent être suspendues. Sinon, créer une nouvelle cible de production.

1. Acquérir le verrou de la cible et activer la quiescence.
2. Calculer un dernier aperçu stable, vérifier une sauvegarde fraîche et la preuve de santé.
3. Basculer d'abord la garde distante vers `production` avec une révision strictement supérieure. Toute ancienne enveloppe staging échoue alors avant mutation.
4. Mettre à jour le contrat et les autorités : code/schéma locaux, données/médias cibles.
5. Régénérer les enveloppes liées à la nouvelle révision et vérifier le refus des anciennes.
6. Sortir de quiescence, prouver la santé puis libérer le verrou.

## Reprise fail-closed

- Arrêt avant la garde : aucune promotion n'est visible ; reprendre depuis le dernier aperçu sous le même verrou.
- Arrêt entre garde et contrat : la cible est déjà protégée ; reprendre la mise à jour du contrat sans réactiver le miroir.
- Arrêt entre contrat et enveloppes : conserver la révision élevée, régénérer les enveloppes et rejeter toutes les anciennes.
- Ne jamais diminuer `lifecycleRevision`, même lors d'un rollback applicatif.
