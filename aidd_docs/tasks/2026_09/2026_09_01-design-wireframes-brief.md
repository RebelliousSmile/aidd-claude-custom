# `design:wireframes` — intention consolidée

`design:wireframes` crée ou normalise une planche HTML destinée à vérifier la compréhension d’un brief et à réfléchir à une interface avec un LLM. La planche peut contenir des pages, des fragments d’écran ou des composants. Elle fixe leur disposition, leur hiérarchie et leur usage sans prétendre être une maquette graphique finale ni du code d’intégration.

La planche est faite pour être regardée. Elle montre l’interface et ses états au lieu de les expliquer. Elle intervient avant `design:harness` : `wireframes` permet d’explorer et de valider une direction ; `harness` transforme ensuite les pages retenues en référence autonome, pilotable et mesurable.

## Responsabilités

- Le LLM analyse le brief et les références disponibles, propose les piliers optionnels utiles et produit ou normalise la planche.
- La personne qui demande le wireframe choisit les piliers. Le LLM peut appliquer sa proposition sans question lorsque les entrées rendent ce choix évident ; il demande une décision si deux sélections changeraient matériellement le résultat.
- Cette même personne, ou la personne explicitement désignée comme reviewer, accepte le wireframe avant tout passage au harness. Aucun accord implicite du LLM ne vaut validation.

## Un format commun, indépendant du style

Chaque sortie est un fichier HTML autonome, ouvrable localement sans compilation ni dépendance réseau. Son format commun contient toujours :

1. une planche unique ;
2. un manifeste JSON embarqué et non visible ;
3. une section visible par unité modélisée ;
4. des identifiants stables reliant le manifeste aux unités et à leurs états ;
5. le socle obligatoire et la liste des piliers optionnels activés ;
6. les références utilisées et leur provenance ;
7. zéro erreur du linter avant que la sortie soit déclarée valide.

Une unité déclare un type parmi `page`, `fragment` et `component`. Plusieurs unités peuvent cohabiter dans la planche. Elles sont alors ordonnées selon le parcours utilisateur ou, en l’absence de parcours, selon l’ordre du brief. Elles restent toutes présentes dans le document et accessibles par défilement : une navigation ou une interaction peut faciliter la consultation, mais ne doit jamais être le seul moyen de voir un état essentiel.

Le manifeste porte les décisions nécessaires au contrôle sans les afficher comme de la documentation : identifiant, type, titre court, piliers actifs, contexte ciblé, éléments attendus, action principale éventuelle, états attendus, provenance et, pour une future page de harness, métadonnées de page connues. `primaryAction` contient l’identifiant d’un élément ou `null` lorsqu’une unité purement informative n’a aucune action principale.

## Socle obligatoire

### Disposition et hiérarchie

Une sortie satisfait ce pilier lorsque :

- chaque élément explicitement demandé dans le brief est présent dans le manifeste et dans le rendu correspondant ;
- les regroupements, l’ordre de lecture, les zones et les relations parent-enfant sont perceptibles visuellement ;
- l’action principale se distingue des actions secondaires sans dépendre uniquement de la couleur ;
- aucun élément ne se chevauche, n’est coupé ou ne provoque un défilement horizontal dans le cadre déclaré ;
- les libellés et contenus visibles sont assez représentatifs pour juger l’encombrement réel.

Un élément volontairement omis doit être retiré du périmètre avant la génération. Une note ne peut pas remplacer un élément attendu.

### Usages, interactions et états

Une sortie satisfait ce pilier lorsque :

- le rôle de chaque contrôle se comprend par sa forme, son libellé et son emplacement ;
- chaque interaction déterminante mentionnée dans le brief possède au moins son état initial et son résultat visible ;
- les états nécessaires à une décision de disposition sont juxtaposés dans la section de l’unité ;
- aucune information essentielle ne dépend d’un clic, d’un survol, d’une animation ou d’une annotation ;
- les interactions exécutables éventuelles reproduisent les mêmes états que ceux déjà visibles et ne constituent qu’une aide à l’exploration.

Les états techniques génériques — chargement, vide, erreur, succès ou désactivation — ne sont exigés que s’ils sont mentionnés par le brief ou s’ils modifient la disposition. Le manifeste énumère les états retenus ; le linter vérifie que chacun possède un rendu.

## Piliers optionnels

### Responsive

Ce pilier est binaire. Lorsqu’il est actif, chaque unité possède exactement deux cadres : `desktop` à 1440 px et `mobile` à 390 px. Il n’existe ni tablette ni troisième largeur implicite. Les deux cadres montrent les mêmes capacités, sauf différence volontaire déclarée dans le manifeste, et passent les contrôles d’absence de chevauchement, de coupure et de défilement horizontal.

Lorsqu’il est inactif, le demandeur choisit un seul contexte parmi `desktop`, `mobile` ou `intrinsic`. `intrinsic` est réservé aux fragments et composants dont la largeur dépend du conteneur parent ; le manifeste déclare alors la largeur numérique du conteneur utilisée pour contrôler le rendu.

### Contenu représentatif

Ce pilier interdit le lorem ipsum, les répétitions artificielles et les libellés génériques tels que « Titre » ou « Texte ». Le manifeste nomme au moins un scénario de contenu. Le rendu utilise des valeurs crédibles et des longueurs suffisamment variées pour révéler les problèmes de disposition attendus dans ce scénario.

### Insertion dans l’existant

Ce pilier évalue la place d’un nouvel élément dans une interface déjà existante. Au moins un rendu montre l’élément nouveau avec les éléments voisins nécessaires pour juger sa taille, son alignement, sa hiérarchie et son effet sur le parcours. Il ne requiert ni couleur de marque ni reproduction graphique fidèle.

### Identité visuelle

Ce pilier reprend uniquement les couleurs, typographies, formes, logos ou composants de marque attestés par une référence. Il n’est jamais activé par défaut et reste indépendant de l’insertion dans l’existant. Le linter refuse toute valeur présentée comme appartenant à la marque si sa provenance n’est pas déclarée ; les choix purement neutres du chrome de la planche restent autorisés.

## Références et arbitrage

Pour l’insertion dans l’existant ou l’identité visuelle, chaque référence doit être lisible au moment de produire la sortie et être enregistrée dans le manifeste. L’autorité suit cet ordre :

1. la référence explicitement désignée par le demandeur pour ce wireframe ;
2. un contrat de design figé applicable à l’écran ;
3. le rendu actuel de l’application ;
4. ses sources locales ou captures datées.

Le LLM ne mélange pas deux références contradictoires. Si leur priorité ne permet pas de trancher, il s’arrête avant d’écrire et demande laquelle fait foi. Si une référence requise est absente ou illisible, le pilier concerné ne peut pas passer silencieusement en mode neutre : le LLM demande la référence ou l’accord explicite pour désactiver ce pilier.

Sans pilier contextuel actif, la planche utilise un vocabulaire visuel neutre et n’invente aucune identité de marque.

## Annotations

La valeur par défaut est zéro annotation. Une annotation n’est permise que pour une contrainte essentielle qui ne peut être rendue par la disposition, le contenu ou un état visible.

Chaque unité accepte au maximum deux annotations, chacune limitée à 60 caractères. Elles sont marquées `data-wireframe-annotation`, ne contiennent ni paragraphe ni liste et ne sont jamais regroupées dans un panneau explicatif. Les titres d’unité, noms d’état, libellés d’interface et valeurs de contenu ne sont pas des annotations.

Une sortie échoue si une annotation décrit ce que le rendu aurait pu montrer, si elle contient une instruction d’implémentation ou si sa suppression empêche de comprendre l’usage principal. Dans ce dernier cas, le rendu doit être retravaillé.

## Compréhension immédiate

La compréhension « d’un coup d’œil » s’évalue unité par unité, et non sur la hauteur totale d’une planche multipage. Sans exécuter d’interaction et sans lire les annotations, un reviewer doit pouvoir identifier dans chaque section :

- le sujet de l’unité ;
- son ordre de lecture ;
- l’action principale, lorsqu’elle existe ;
- les états qui changent sa disposition ou son usage.

Le linter contrôle les indices objectifs — présence des états, ordre DOM, unicité de l’action principale déclarée, visibilité sans interaction et limites d’annotation. L’acceptation humaine confirme que ces indices produisent effectivement une interface comprise. L’automatisation ne prétend pas remplacer ce jugement.

## Normalisation d’un wireframe existant

La normalisation ne modifie jamais la source et exige un chemin de sortie distinct. Elle préserve, dans cet ordre :

1. le contenu et les contrôles explicitement reliés au brief ;
2. l’ordre et les regroupements porteurs de sens ;
3. les états et interactions utiles ;
4. les éléments d’identité couverts par un pilier actif.

Elle peut remplacer le document englobant, le chrome de présentation, les annotations excessives, les styles sans provenance et les interactions qui cachent des états essentiels. Si une transformation nécessaire changerait le sens, l’ordre du parcours ou un contenu métier, le LLM s’arrête et demande une décision. La réponse finale inventorie les éléments préservés, transformés et omis ; cet inventaire n’est pas injecté dans la planche.

## Comportement du linter

Le linter charge le manifeste, contrôle le format commun, applique le socle puis uniquement les piliers activés.

- Une violation du format commun, du socle ou d’un pilier actif est une erreur et rend la sortie invalide.
- Une recommandation qui ne change pas la conformité est un avertissement.
- Le mode par défaut analyse et rapporte sans modifier le fichier.
- Un correctif opt-in peut réparer seulement les défauts mécaniques sans ambiguïté, comme un identifiant manquant ou un attribut de liaison incohérent.
- Le correctif ne modifie jamais la disposition, le contenu, les états, le choix des piliers ou les références.
- Après correction, le linter rejoue tous les contrôles. Une sortie n’est valide qu’avec zéro erreur ; les avertissements restants sont nommés.

Le contrôle combine des règles déterministes sur le HTML et le manifeste avec la validation visuelle humaine. Les règles déterministes ne déclarent jamais seules que le brief a été correctement interprété.

## Passage vers `design:harness`

Une unité est prête à être proposée au harness lorsque le linter ne remonte aucune erreur et que le reviewer l’a explicitement acceptée.

Seules les unités `page` passent directement. Leur manifeste fournit une clé slug unique et, lorsqu’ils sont connus, `label`, `group`, `route`, `source` et `theme`, compatibles avec les métadonnées de pages du harness. Une unité `fragment` ou `component` doit d’abord être associée à une page et à une zone de cette page ; aucune page englobante n’est inventée.

Le passage utilise la normalisation officielle du harness vers un nouveau fichier. Le HTML wireframe reste une source auteur : il n’imite pas le chrome, le registre ou les scripts du harness. Le harness ajoute son propre échantillon tablette ; l’absence de tablette dans le wireframe est déclarée comme une décision encore à prendre et ne doit pas être interpolée silencieusement.

Le passage n’est complet que lorsque le harness possède son format canonique, un runtime valide, une migration sans élément non résolu et une comparaison visuelle acceptée selon son propre contrat. La validation du wireframe ne vaut ni conformité au contrat de design ni preuve de fidélité du harness.

## Cas de refus explicites

La skill s’arrête sans écrire de sortie lorsque :

- aucun brief ou contenu à normaliser ne permet d’identifier une unité ;
- les éléments indispensables du brief se contredisent ;
- un pilier contextuel actif dépend d’une référence absente ou illisible ;
- deux références d’autorité égale se contredisent ;
- la normalisation exige une transformation qui changerait le sens sans arbitrage ;
- aucune sélection de piliers ne peut être inférée sans changer matériellement le résultat.

Elle produit une sortie invalide, accompagnée d’erreurs actionnables, lorsque le HTML peut être écrit mais échoue aux règles du format, du socle ou d’un pilier actif. Elle ne masque jamais un refus ou une erreur par une annotation supplémentaire.
