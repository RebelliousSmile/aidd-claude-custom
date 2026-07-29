---
type: quarantaine
statut: ouvert
date: 2026-07-28
lié: 2026_07_plan-integration-retour-terrain-fse.md
---

# Quarantaine — retour de terrain « maquette → site éditable »

## Ce qu'est cette liste

Des observations issues d'**un seul terrain**, qui ne révèlent aujourd'hui aucune faiblesse nommable dans un skill du périmètre. Elles ne sont pas écartées : elles sont mises en attente d'un second constat.

C'est une **mémoire de reconnaissance**, pas un échantillon. Sa seule fonction est qu'un motif revu une seconde fois soit reconnu au lieu d'être redécouvert. Elle ne permet aucune statistique : les skills évoluent pendant que les projets tournent, donc deux retours ne sont jamais produits par le même instrument.

Trois sorties possibles pour une entrée : elle est revue sur un autre terrain et remonte au plan ; elle est infirmée par un contre-exemple et disparaît ; elle reste ici.

---

## Q-01 — Un registre d'erreurs non mesuré est lui-même candidat au registre

**Observation.** Un registre de onze erreurs, chacune adossée à une preuve et à un ticket, s'est réfuté lui-même en vingt-quatre heures sur trois points : un chiffre inventé là où la mesure donnait autre chose, un effectif d'un là où il y en avait huit, deux gates crus contradictoires alors que l'un comparait deux états du même côté.

**Pourquoi en quarantaine.** La tenue d'un journal de projet est hors du périmètre déclaré, et aucun skill du périmètre ne produit ce registre. L'énoncé général — *une affirmation portée dans un artefact de constat doit être mesurée ou marquée non mesurée* — est vrai et non imputable ici.

**Ce qui la ferait remonter.** Un skill du périmètre qui écrit un constat chiffré sans que la mesure soit rejouable depuis l'artefact.

---

## Q-02 — Retirer un composant du contrat est un acte de figeage, pas une suppression

**Observation.** Le retrait d'un composant contracté a été traité comme un nettoyage de code alors qu'il modifie la surface publique du contrat et appelle un incrément de version majeur.

**Pourquoi en quarantaine.** Le geste est probablement déjà couvert par la discipline de version du verbe de figeage ; le vérifier appelle une lecture du flux de figeage que la refonte en cours va réécrire. Le classer maintenant reviendrait à imputer contre un instrument en mouvement.

**Ce qui la ferait remonter.** Un second retrait effectué hors figeage, ou la constatation que le flux de figeage n'oblige à rien sur le retrait.

---

## Q-03 — Un journal en ajout continu pourrit par ses résumés

**Observation.** Le récit chronologique d'un journal est resté exact ; ses sections de synthèse, réécrites au fil de l'eau, ont divergé de lui et sont devenues la version consultée.

**Pourquoi en quarantaine.** C'est une propriété du genre « journal », que le périmètre exclut explicitement. Aucun skill du périmètre ne produit ni ne maintient de journal.

**Ce qui la ferait remonter.** Le même effet constaté sur un artefact qu'un skill du périmètre produit et met à jour — un rapport de gate cumulatif, un registre d'exemptions, un état de maturité.

---

## Q-04 — L'outillage disponible finit par définir le projet

**Observation.** Ce qui pouvait être mesuré est devenu ce qui était exigé ; ce qu'aucun instrument n'atteignait a cessé d'être discuté, sans décision explicite.

**Pourquoi en quarantaine.** L'énoncé est juste et sa conséquence directe est déjà traitée par les items du plan qui obligent à déclarer le champ optique des gates. En tant que dérive de conduite de projet, il n'est imputable à aucun skill.

**Ce qui la ferait remonter.** Un skill dont la sortie encourage à réduire l'exigence au mesurable — par exemple un verdict de complétude qui ne distingue pas « couvert » de « couvert parmi ce qui est mesurable ».

---

## Ce qui a été écarté sans quarantaine

Rappelé ici pour que la question ne soit pas reposée.

| Observation du terrain | Sortie |
|---|---|
| Feuille de style portée sans son markup, comptée comme à moitié faite | **déjà couvert** — le scan inverse de sélecteurs orphelins et la règle de code mort du pivot statique interdisent tous deux le verdict « mort » sans preuve |
| Sélecteur orphelin indiscernable d'un markup non écrit | **déjà couvert** — même origine ; le corpus du scan inverse inclut le contenu stocké |
| Couches et pseudo-classes de spécificité nulle traitées comme des correctifs alors qu'elles aggravent | **déjà couvert** — la stratégie de couche du pivot statique conditionne l'émission à la topologie mesurée |
| Navigation, contenu et configuration de plateforme spécifiques | **projet** — exécution du terrain, hors périmètre |
| Écarts de valeurs entre maquette et implémentation, page par page | **projet** — c'est précisément ce que l'oracle est fait pour ouvrir ; il l'a ouvert |
