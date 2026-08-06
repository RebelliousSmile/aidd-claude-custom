# Workflow de plateforme — block theme (FSE)

Instancie les classes de cas agnostiques de `design:detail` sur un thème de blocs WordPress FSE. Squelette figé par `plugins/design/references/sc-pivot-contract.md § Workflow de plateforme`. `design` garde le QUOI ; ce fichier porte le COMMENT propre à la plateforme (dec-002).

## Case classes covered

`mockup-multipage` · `codebase-inherited` · `contract-drift` · `element-evolution` · `element-production` (`workflow-classes.md`). Pour chacune, ce workflow instancie nativement les phases `enforce` et `diffuse` et ajoute les phases `off-funnel` du cycle de vie d'un site à blocs.

## Prerequisites (capabilities)

- **Runtime conteneurisé** portant le CLI de la plateforme et sa base — sans lui, ni mesure ni import (`enforce` sur référence servie, `off-funnel` d'import).
- **Base de données distante** : une part du vocabulaire vit comme contenu stocké, pas dans les sources versionnées.
- **Accès shell distant** vers l'environnement de destination, pour la phase de déploiement.

Écrites comme capabilities : aucun hébergeur ni projet nommé.

## Phases

| Phase | input | output | verbe | position |
|---|---|---|---|---|
| Préparer l'environnement mesurable | contrat figé + runtime conteneurisé ; référence pas encore servie | instance servie, mesurable par l'oracle (précondition `harness`) | `off-funnel` | `avant define` |
| Établir le modèle de contenu | inventaire des pages de la référence + arborescence du thème scaffoldé | types et taxonomies enregistrés dans le plugin + templates de vue correspondants dans le thème (`references/content-model-fse.md`) | `off-funnel` | `avant enforce` |
| Enforcement natif | spec d'enforcement + preuve (markup de blocs, contenu stocké extrait) | linter PHP/WP idiomatique câblé + rapport de pivot | `enforce` | `—` |
| Rendu natif | spec de rendu (composant neutre + variantes) | block pattern + `theme.json` conformes au contrat, **posés** dans une vue ou déclarés non posés | `diffuse` | `—` |
| Importer le contenu | patterns rendus, instances de référence | instances en base | `off-funnel` | `après diffuse` |
| Déployer et recetter | instances vérifiées | cible livrée, recette passée | `off-funnel` | `fin` |

*Établir le modèle de contenu* est posée **avant `enforce`** et non avant `diffuse` : les vues des types
sont ce que le gate vocabulaire linte et ce que le périmètre de mesure énumère (§ Périmètre de mesure —
Antériorité). Placée plus tard, elle laisse les deux gates verts sur un dénominateur amputé.

## Gates

Ce workflow **instancie** les gates du contrat, il n'en crée aucun :

- **Vocabulaire** — lint natif du markup de blocs et du contenu stocké extrait (`references/wordpress-lint-instances.md`).
- **Fidélité** — rendu mesuré par propriété à chaque breakpoint contre la référence servie.
- **Seuil de maturité** — un vert n'affirme la conformité qu'au seuil ; sous le seuil, le runner sort en 4.

Point d'application : le gate vocabulaire après la phase d'enforcement, le gate fidélité après le rendu et l'import.

## Périmètre de mesure — énuméré, jamais implicite

La référence d'une maquette est un ensemble de pages ; la plateforme, elle, rend des **templates**. Les
deux ensembles ne coïncident pas : `single*`, `archive*`, les templates de taxonomie et `404` n'ont
généralement aucun fichier de maquette correspondant.

**Antériorité.** L'énumération n'est recevable qu'après la phase *Établir le modèle de contenu*. Un thème
scaffoldé porte trois templates génériques ; énumérés avant, ils rendent une couverture **complète d'un
thème incomplet** — tous mesurés, tous verts, et les vues des types de contenu absentes du dénominateur.
Le contrôle : chaque type de l'inventaire de contenu doit avoir ses lignes dans l'énumération, `measured`
ou `unmeasured(<raison>)`. Un inventaire sans lignes correspondantes invalide le bilan aussi sûrement
qu'un template sans ligne.

Règle : le périmètre de mesure **énumère tous les templates du thème**, pas les pages de la maquette.
Pour chacun, l'un des deux statuts, écrit :

- `measured` — une config d'oracle existe et tourne ;
- `unmeasured(<raison>)` — **manque déclaré**, avec sa raison. Jamais `extra`, jamais un silence.

Un template sans ligne dans cette énumération invalide le bilan. Le glissement à éviter est nommé :
« N/N pages CLOSED » ne veut jamais dire « la référence est intégrée », et rien dans un bilan ne doit
permettre cette lecture (`wordpress-pitfalls.md`, piège 10).

## Discipline des gates rouges

Un gate rouge est un **bloqueur de programme**, pas un état hérité par l'itération suivante.

- Il se transmet avec son commit d'origine, obtenu par `git log -S"<chaîne>" -- <fichier>`, et un
  propriétaire nommé.
- Les qualificatifs « préexistant », « hors périmètre de cette part », « sans rapport avec ce travail »
  sont interdits comme statut : chacun est vrai relativement à une itération et faux au niveau du
  programme. Un défaut arrivé par un arbre de travail non committé est *inattribué*, pas *préexistant* —
  et l'attribution est une commande, pas une opinion.
- Le vert d'un gate ne compense jamais le rouge d'un autre quand les deux ne mesurent pas la même chose
  (une régression de sérialisation de valeur calculée est invisible à un diff de pixels : les deux
  résultats sont exacts, leur juxtaposition dans un bilan ne l'est pas).
- Aucun bilan ne conclut avec une ligne `OPEN`.

## Reprise des gaps

Tout manque produit par un gate de couverture (`builder-coverage`) sort du workflow en **ticket**, jamais
en ligne de rapport — voir `builder-coverage/actions/01-scan.md § Step 5`. Un manque ne peut pas être
re-déclaré « hors périmètre » plus d'une fois : la seconde occurrence est un arbitrage dû (fermer,
planifier avec échéance, ou refuser explicitement en l'inscrivant au registre des non-réalisés).

## Out of scope

- Le contenu rédigé en base au-delà des instances de référence mesurées — hors de portée du gate, déclaré non réalisé, jamais passé en silence.
- Les liaisons de classe résolues à l'exécution — non lisibles par lint statique, déclarées `unrealized`.
- Les états de données absents de la base : une branche conditionnelle d'un rendu SSR qu'aucune donnée
  n'active n'est jamais capturée, donc jamais comparée. Un oracle par capture ne couvre que les états
  présents — c'est une limite de nature. Les branches se vérifient par lecture croisée référence ↔ SSR
  (`builder-coverage`), pas par mesure.
- Toute garantie que le contrat ne connaît pas : aucun gate local n'est introduit ici.
