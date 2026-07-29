---
source: aidd_docs/tasks/2026_07/2026_07_28-control-refonte-phase-domaines.md
generated_at: 2026-07-28
---

# Shadow Areas Report

Source: `aidd_docs/tasks/2026_07/2026_07_28-control-refonte-phase-domaines.md`
Generated: `2026-07-28`

Total gaps: 16 | Blocker: 7 | Major: 7 | Minor: 2

---

## Warnings

- Les probes sont rédigées en français, la langue de la source. Les formes de question verrouillées de `references/locked-sets.json` sont anglaises ; la conformité est structurelle (question directe, une seule cible, terminaison `?`), pas littérale.
- La source déclare elle-même 4 questions bloquantes ouvertes (§6). **Aucune des 7 `blocker` ci-dessous n'en est un doublon** — Q1 à Q4 portent sur des arbitrages de forme, les blockers ci-dessous sur des mécanismes absents. Les deux listes se cumulent.
- Le rapport analyse un document rédigé par le même agent que celui qui le produit. Traiter les `minor` comme un plancher, pas comme une mesure.

---

## Gaps by Category

### unstated assumption

**[blocker]** Comment un domaine fonctionnel se détecte-t-il dans une base de code qui n'en porte aucune signature structurelle (monolithe procédural, thème WordPress, scripts) ?
> §3.3 — « catalogue de référence × scan du code »

L'hypothèse centrale de la refonte — un domaine laisse une trace grep-able — n'est ni énoncée ni discutée. Elle tient sur une stack à conventions fortes (`pages/<domain>/`, `<Domain>Controller`) et s'effondre sans elles. `05-stats:88` documente déjà le mode de défaillance silencieux : *« searching `Login` and `Register` finds `LoginForm.tsx` and misses `SessionController`, and the missed zone does not surface as excluded - it surfaces as a zone with no gap »*. La refonte fait reposer **tout l'arbitrage** sur cette détection, ce qui transforme un défaut de précision en défaut de fondation.

**[minor]** Que signifie « quasi-statiques » appliqué aux domaines — une garantie de stabilité ou une simple observation empirique ?
> §3.3 — « Quasi-statiques : ils n'évoluent qu'à l'occasion de gros changements applicatifs »

Les deux lectures conduisent au même comportement (re-scan du résidu, jamais d'écrasement). Sans effet sur l'implémentation.

### ambiguous term

**[major]** Un « terme de résolution grep-able » est-il un littéral, une regex, ou un préfixe d'identifiant, et la casse est-elle significative ?
> §3.3 — « `align` écrit le nom du domaine + ses termes de résolution grep-ables + les chemins »

C'est le format de l'artefact que produit `align` et que toutes les autres actions consomment. Deux interprétations raisonnables donnent deux implémentations incompatibles, et le choix décide directement du taux de faux négatifs décrit dans le gap précédent.

**[minor]** Quels sont précisément « les six critères de risque » que §3.2 conserve comme classement intra-domaine ?
> §3.2 — « les six critères de risque survivent comme classement intra-domaine »

Inférable de `04-strengthen:51`, mais `01-plan` s'exécute en contexte forké et n'aura que ce document. Un renvoi de fichier:ligne suffit.

### missing edge case

**[blocker]** Quelle preuve la matrice exige-t-elle pour du code source n'appartenant à aucun domaine ?
> §3.4 — « le résidu (fichiers sans aucune correspondance) est scanné à neuf »

La matrice est indexée `phase × domaine`. Le résidu n'a donc **aucune cellule**, alors qu'il constitue en pratique la majorité des fichiers d'un projet réel. Le document traite le résidu uniquement comme un signal de dérive à rapporter, jamais comme une population à régir. Sans réponse, `01-write` sur un comportement hors domaine n'a pas de règle applicable — la refonte laisserait le cas le plus fréquent sans autorité, ce qui est le défaut qu'elle existe pour supprimer.

**[major]** Que produit la matrice sur un projet où le scan ne détecte aucun domaine ?
> §3.3 — production par « catalogue de référence × scan du code »

État normal d'un projet en `scaffolding`. Cas limite du précédent, mais distinct : ici la matrice entière est vide, pas seulement une population résiduelle.

**[major]** Quelle preuve la matrice exige-t-elle sur une stack dépourvue de runner E2E — bibliothèque, CLI, service sans interface ?
> §2.1 — « Un e2e traverse l'interface réelle »

Le raisonnement fondateur suppose une interface à traverser. §7 signale déjà que `sc-rust` casse trois hypothèses du contrat ; celle-ci en est une quatrième et elle touche la matrice, pas le pivot. Une exigence de preuve impossible à satisfaire dans la stack se solde soit par un blocage, soit par un contournement silencieux.

### missing actor

**[blocker]** Qui possède la section « domaines » de `aidd_docs/memory/testing.md` du projet cible — `aidd-context` ou `overcode:control#06-align` ?
> §3.3 — « Les domaines sont établis et écrits par `06-align` »

`aidd_docs/memory/testing.md` est déclaré propriété de `aidd-context`. La refonte y fait écrire une autre skill d'un autre plugin, sans nommer le mécanisme de coexistence. Deux écrivains sur un fichier sans protocole produisent une perte d'écriture à la première collision, et l'artefact perdu est celui dont dépend tout l'arbitrage.

**[major]** Qui déclenche un re-jugement des domaines lorsque les capteurs de dérive signalent un résidu croissant ?
> §3.4 — « capteurs de dérive : rapportés, jamais appliqués »

La règle « rapporté, jamais appliqué » est correcte et protège l'idempotence, mais elle laisse la boucle ouverte : le rapport n'a pas de destinataire désigné ni de seuil déclenchant. Un signal sans acteur est un signal que personne ne lit.

### missing failure mode

**[major]** Que devient un projet dont le `testing.md` est écrit dans l'ancien vocabulaire de tiers lorsque la refonte est livrée ?
> §4 — « `decision-framework.md` / table des tiers comme autorité » disparaît

La stratégie documentée d'un projet fait autorité (`05-stats:42`). Les documents existants sont rédigés en `contract` / `e2e` / `skip`. Aucune règle de lecture rétrograde n'est prévue, et Q3 envisage en plus de changer ce vocabulaire.

**[major]** Que se passe-t-il pour le pivot `sc-js/tools/testing.md` au moment où le champ *Tier thresholds* est supprimé du contrat ?
> §4 — suppression du champ *Tier thresholds* ; §5.2 — DEC-004 §5 déclare le contrat « interface publique »

Le seul pivot existant est susceptible de déclarer ce champ. Le document reconnaît la rupture d'interface au niveau de l'ADR, mais ne dit pas si le pivot est corrigé dans le même commit, ni ce que fait `control` en rencontrant un champ retiré — l'ignorer silencieusement ou le signaler.

### missing acceptance criterion

**[blocker]** Quelles valeurs contient la matrice phase × domaine pour au moins une ligne complète ?
> §3.2 — « Une matrice phase × domaine → preuve exigée + plafond »

La matrice est le cœur de la refonte et remplace quatre dispositifs à elle seule, mais le document n'en donne pas une seule cellule. 6 phases × N domaines, et zéro valeur. Sans une ligne exemplaire — disons `production` × `payment` — rien ne permet de vérifier que la matrice est exprimable, ni de la reviewer, ni d'en dériver un plan. C'est le gap dont dépendent tous les autres arbitrages de forme (Q1, Q2).

**[blocker]** Que se passe-t-il concrètement lorsqu'un domaine dépasse son plafond ?
> §3.1 — « Elle gagne le droit de fixer un plafond par domaine »

Trois régimes possibles et incompatibles : refus d'ajout, avertissement franchissable, ou proposition de retrait. Le document justifie longuement pourquoi un plafond est légitime là où un plancher ne l'est pas, sans jamais dire ce qu'il fait. Or `test-density.md:65` pose que **la densité ne refuse jamais** : si le plafond ne refuse pas davantage, il n'est pas un plafond mais un second signal, et §3.1 s'effondre. Q1 ne couvre pas ce point — elle porte sur l'unité de mesure, pas sur l'opposabilité.

**[blocker]** Quel artefact contient le catalogue de référence des domaines, et quels domaines y figurent ?
> §3.3 — « catalogue de référence × scan du code, où le catalogue est un plancher de détection »

Le catalogue est une dépendance de production de tout l'arbitrage et n'existe pas. Ni son emplacement, ni son format, ni son contenu initial ne sont énoncés. La question non bloquante de §6 traite sa **ligne de partage** avec le pivot, ce qui présuppose résolu ce qui ne l'est pas : son existence.

**[major]** Quel critère atteste que la refonte est terminée ?
> §5.1 — « page → suites `behave` rouges → skill »

L'ordre de travail est posé, le critère d'arrêt non. Le passage au vert de quelles suites, et quel sort pour les scénarios que la refonte rend caducs (S2, S11, S6, partiellement hors périmètre) ? Sans réponse, la fin de chantier se décidera à vue.

### missing dependency

**[blocker]** Que font `01-write`, `02-audit`, `04-strengthen` et `05-stats` sur un projet où `06-align` n'a jamais été exécuté ?
> §3.2 — « les domaines d'abord, la phase ensuite » ; §3.3 — les domaines sont écrits par `06-align`

La refonte fait des domaines une entrée obligatoire de l'arbitrage et confie leur production à une seule action, sans prévoir de repli. C'est le cas d'un premier contact avec un projet — donc le cas le plus fréquent, et précisément celui que `05-stats` existe pour servir en tant que porte d'entrée. Soit un repli dégradé et annoncé est défini (dans l'esprit de DEC-004 §2), soit `align` devient un prérequis dur de la skill entière, ce qui est une décision d'architecture à assumer explicitement.
