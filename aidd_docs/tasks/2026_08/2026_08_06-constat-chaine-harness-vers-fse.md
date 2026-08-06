# Constat — la chaîne « harness rempli → site WordPress FSE », exercée sur un terrain réel

> **Constat, pas plan.** Rien n'est corrigé ici. Toutes les ancres `fichier:ligne` renvoient à la
> **source** (`plugins/…`), jamais au cache installé.
>
> **Terrain** : `arbre-de-jade` (`C:/Users/fxgui/Documents/Pro/Projets/arbre-de-jade/_code`) — thème de
> blocs `arbre-de-jade` + plugin `sc-arbre-de-jade` scaffoldés par `sc-php:setup`, wp-env sur `:8514`,
> WordPress 7.0.2, aucun contrat design. Référence : `aidd_docs/memory/external/maquette-arbre-de-jade.html`,
> harness `design` rempli, 11 pages.
>
> **Portée** : ce document ne juge pas les corrections de `sc-php` 0.11.0 (commit `8eec810`) — il les tient
> pour acquises et regarde ce qui, **après** elles, empêche encore la chaîne d'aboutir. Deux des six points
> portent sur `design`, pas sur `sc-php`.

## Protocole

`design:detail` a été invoqué sur la maquette, routé en `02-route`, et sa sortie confrontée à ce que le
terrain exige réellement pour produire le site. Le décalage entre les deux est l'objet du document. Les
constantes de la maquette (`AGENDA`, `INTERVENANTES_TOUS`) ont servi d'étalon : elles décrivent un modèle de
contenu que la chaîne doit savoir produire.

**Ce qui marche.** Le garde `COMPOSE_PROJECT_NAME` (0.10.4) tient, y compris depuis un répertoire tiers. Le
scaffold est correct et son nouvel énoncé de non-couverture (`02-scaffold-wordpress.md:20`,
`theme-plugin-skeleton.md:191`) dit exactement ce qu'il ne fait pas. `content-model-fse.md` est une bonne
réponse au trou qu'il vise : la table de reconnaissance a classé les 11 pages sans arbitrage humain, et sa
contre-épreuve (retirer `single-<type>.html`, vérifier que le marqueur disparaît) est le seul contrôle qui
distingue un template de type de son repli générique.

---

## 1. `02-route` n'est pas tenu d'émettre les phases du workflow de plateforme — défaut bloquant

C'est le défaut principal : **la correction 0.11.0 est invisible à son unique consommateur.**

`sc-php` 0.11.0 ajoute une phase `off-funnel` « Établir le modèle de contenu » à
`workflow-fse.md:22`, et une règle d'antériorité (`workflow-fse.md:44-49`) qui rend l'énumération du
périmètre de mesure irrecevable avant elle. Le seul mécanisme censé porter cette phase jusqu'à
l'utilisateur est `design:detail/02-route`.

Or `02-route.md:24` définit sa sortie comme :

> L'état de l'extension de plateforme : présente (et par quel pivot), ou absente (et quel `sc-<langage>` installer).

**L'état, pas le contenu.** L'étape 5 du process (`02-route.md:19`) dit « Émettre la séquence : verbes dans
l'ordre, checkpoints humains, gates de sortie, condition d'arrêt » — « la séquence » étant celle que la
classe déclare (`workflow-classes.md:18`, cinq verbes), pas la table `## Phases` du pivot (six lignes).
Rien n'oblige `route` à ouvrir `workflow-fse.md`, et rien ne lui dit quoi en extraire.

**Mesuré.** Exécuté littéralement, `02-route` sur ce terrain rend :

```
mockup-multipage : define → checkpoint → adjust → enforce → diffuse
extension de plateforme : présente, via sc-php:design-bridge
```

La phase « Établir le modèle de contenu » n'y figure pas. Un consommateur qui suit cette sortie lance
`define` en premier — c'est-à-dire exactement le mur que 0.11.0 vient de documenter. Les deux types
(`evenement`, `intervenant`) resteraient non enregistrés, `diffuse` poserait ses patterns dans les trois
templates génériques du scaffold, et le périmètre de mesure rendrait « 3/3 mesurés, tous verts » sur un
thème incomplet.

Je n'ai vu la phase que parce que j'ai lu `workflow-fse.md` directement. Ce n'est pas ce que l'action
prescrit.

**Le plus lourd est ailleurs.** Le *Test* déclaré (`02-route.md:29`) porte sur `contract-drift` et vérifie
qu'après désinstallation du pivot la classe est **la même** et l'extension énoncée **absente**. Il ne
contient aucune assertion sur une phase de plateforme présente dans la sortie. Le circuit de vérification
de l'action ne peut pas distinguer une extension lue d'une extension seulement nommée. Même motif que le
constat du 05/08 § 1 : une sortie verte qui n'atteste rien.

**Correctif proposé.** Faire de la table `## Phases` du pivot une **entrée obligatoire** de `route` quand
l'extension est présente, et de la séquence fusionnée une sortie obligatoire. Le jeton d'interface existe
déjà (`sc-pivot-contract.md:179-183`, cinq titres exacts) et `:186` le déclare « attendu à l'identique par
`design:detail/02-route` » — or `02-route` ne l'utilise nulle part. Le contrat décrit une lecture qui
n'existe pas.

**Test qui l'aurait attrapé.** Sur un terrain FSE avec `sc-php` installé, `route` doit rendre une séquence
contenant une phase absente de `workflow-classes.md`. Retirer la ligne correspondante de `workflow-fse.md`
et rejouer : la phase disparaît de la sortie. Sans cette bascule, le test n'atteste que la présence du
pivot.

## 2. L'ordre d'insertion des phases `off-funnel` n'est spécifié nulle part

Corollaire du 1, et il survivra à sa correction.

`sc-pivot-contract.md:192-194` fige la déclaration d'une phase à trois champs — **input**, **output**,
**verbe**. Aucun champ ne dit *où* la phase s'insère relativement à la séquence de verbes de la classe.
`workflow-classes.md:9` dit seulement que le pivot « ajoute ses phases off-funnel ».

Conséquence : deux lecteurs fusionnant les mêmes deux listes produisent deux ordres différents, tous deux
défendables. J'ai produit une séquence à 8 lignes plaçant le modèle de contenu en position 2 ; rien dans le
contrat ne me disait de le faire, ni où le placer. La contrainte réelle existe pourtant, mais elle est en
prose dans le pivot (`content-model-fse.md:76-84` : « Avant le rendu natif et avant toute énumération du
périmètre de mesure »), là où le consommateur du contrat ne la lit pas.

**Correctif proposé.** Un quatrième champ de position dans la déclaration de phase — `avant: <verbe>` /
`après: <verbe>` — de sorte que la fusion soit dérivable et non interprétée. Le fichier agnostique fige la
forme, le pivot remplit la valeur : la répartition QUOI/COMMENT est préservée.

## 3. L'énumération de `workflow-classes.md:9` est périmée

> « il instancie nativement les phases `enforce` et `diffuse` et **ajoute ses phases `off-funnel`
> (environnement, déploiement, recette)** »

Trois éléments énumérés. `workflow-fse.md` en porte maintenant **quatre** : environnement, modèle de
contenu, import du contenu, déploiement/recette. La parenthèse était exacte à l'écriture ; 0.11.0 l'a
rendue fausse le jour même.

Défaut de nature, pas d'exactitude : un fichier **agnostique** énumère le contenu d'un pivot. Il dérivera
de nouveau à la prochaine phase ajoutée par n'importe quel pivot. La même phrase apparaît en tête de
`workflow-classes.md:9` et en `## Point d'extension` de chacune des six classes.

**Correctif proposé.** Rendre la formulation non énumérative (« ajoute les phases `off-funnel` que son
workflow déclare »). Zéro perte d'information : la liste réelle est dans le pivot, qui est l'autorité.

## 4. L'invariant à trois branches du harness rempli n'a aucun vérificateur

La notice écrite par le générateur dans chaque fichier produit (`harness.py:296-297`) déclare :

> La clé de page doit correspondre à la valeur de l'`<option>` ET au champ `maquette_page` du config measure.

Trois branches à tenir d'accord : les clés du registre `const pages`, les `value` des `<option>`, et le
champ `maquette_page` de la config d'oracle. **Aucune ne vérifie les autres.**

Ce qui existe et ce qui n'existe pas :

- le générateur valide les clés **à la génération** — slug, nom de fonction dérivable, unicité, sortie en 2
  en nommant les clés fautives (`skills/harness/SKILL.md:70`) ;
- rien ne revalide un fichier **rempli**, qui est pourtant celui que `copycat` et l'oracle consomment ;
- `maquette_page` n'apparaît dans tout le plugin `design` qu'à un seul endroit : le **texte de la notice**
  générée, dans `harness.py`. Aucun code ne le lit ;
- `harness-contract.md:51` « Accord measure / oracle » porte sur l'**ensemble fermé de viewports**, pas sur
  les clés de page.

Le mode de défaillance est silencieux dans les deux sens : une page absente du registre ne rend rien, une
page absente de la config d'oracle n'est jamais mesurée — et le bilan de fidélité sort vert sur les pages
restantes. C'est le motif que le contrat de pivot nomme lui-même (`sc-pivot-contract.md:112`) : sans trace,
une règle assignée et une règle oubliée produisent la même absence.

Sur ce terrain les trois branches sont d'accord (11 clés / 11 `<option>` / config d'oracle pas encore
écrite), donc le défaut est **latent, non réalisé**. Je le rapporte parce que la chaîne va précisément
écrire la troisième branche à l'étape suivante.

**Correctif proposé.** Un mode de vérification sur fichier rempli — le selftest exécute déjà le fichier
généré, il peut lire `Object.keys(pages)` et les `<option>` du DOM et les comparer, plus la config d'oracle
quand elle est fournie.

## 5. `index.json` ne porte ni version ni description

`index.json` est décrit par les règles du dépôt comme « index racine (versions + descriptions) ». Son
contenu réel est onze entrées de la forme `{ "id": "sc-php", "name": "sc-php" }` — ni version, ni
description. Les versions ne vivent que dans `.claude-plugin/marketplace.json` et dans chaque
`plugin.json`.

Ce n'est pas cosmétique : **rien ne détecte l'écart entre la source et le cache installé.** Mesuré
aujourd'hui — source à `sc-php` 0.11.0, `~/.claude/plugins/cache/my-marketplace/sc-php/` plafonnant à
**0.10.4**. Une invocation runtime de `design:detail` aurait donc routé la séquence d'avant, sans la phase
modèle de contenu, sans qu'aucun signal ne le dise. Le retest a dû être conduit sur la source, ce qui n'est
pas ce que l'utilisateur exécute.

**Correctif proposé.** Soit `index.json` porte les versions et devient comparable au cache, soit la règle
qui le décrit est corrigée pour cesser de promettre ce qu'il ne contient pas.

## 6. Deux citations relatives non résolvables — mineur

`skills/harness/SKILL.md:91` et `:179` citent `` `references/harness-contract.md` `` en relatif. Résolu
depuis le répertoire de la skill, le chemin n'existe pas : le fichier est à
`plugins/design/references/harness-contract.md`, au niveau plugin. La ligne 17 du même fichier utilise la
forme correcte `${CLAUDE_PLUGIN_ROOT}/references/harness-contract.md` — un lecteur qui l'a vue s'en sort.
Signalé pour cohérence, pas comme un blocage.

---

## Question ouverte, pas un défaut : aucun état terminal local

`workflow-fse.md:9-13` déclare trois capabilities requises. Deux — **base de données distante** et **accès
shell distant** — n'ont aucune cible sur ce projet, et la dernière ligne de la table des phases est
« Déployer et recetter ». Le workflow n'offre donc aucun point d'arrêt légitime à un projet qui n'a pas
encore d'hébergement : les phases 1 à 7 aboutissent, la 8 est structurellement bloquée, et la condition
d'arrêt de la classe (« les deux gates verts au seuil, éléments diffusés ») est atteinte sans que le
workflow le reconnaisse.

Je ne le classe pas en défaut parce que je ne sais pas si c'est voulu — un workflow de plateforme dont la
finalité est un site en ligne peut légitimement refuser de déclarer un état terminal local. Mais le cas
« maquette → site FSE local, mise en ligne plus tard » est exactement celui de ce projet, et il n'a pas de
nom dans le workflow.

---

## Non-défauts vérifiés — à ne pas chercher

- **Le hand-off scaffold → modèle de contenu existe déjà.** Ajouté par 0.11.0 en
  `02-scaffold-wordpress.md:20` (étape 8) et `theme-plugin-skeleton.md:191`. J'allais le rapporter
  manquant ; il ne l'est pas.
- **Faux positif que j'ai produit et qui vaut avertissement.** J'ai d'abord rapporté un défaut du harness
  rempli : une fonction `pageHome()` orpheline, déclarée deux fois, absente du registre. **Faux.** Les deux
  occurrences sont aux lignes 1543 et 1545 de la maquette, à l'intérieur du bloc de commentaire HTML
  `1530 → 1583` — c'est-à-dire dans la notice « COMMENT LE REMPLIR » que le générateur écrit lui-même, dont
  l'exemple type est `function pageHome() { return placeholder('home', 'Accueil'); }`. En colonne 0, le
  fichier porte exactement 11 déclarations, pour 11 `<option>` et 11 clés de registre.
  Un audit par `grep` tolérant l'indentation (`^\s*function page…`) mord dans la notice du générateur et
  compte une douzième page qui n'existe pas. Tout contrôle automatique de l'invariant du § 4 doit ignorer
  les commentaires — sinon il naîtra rouge sur tout fichier conforme.

---

## Ordre de traitement suggéré

1. **§ 1** — bloquant, et il annule la valeur de la correction 0.11.0 tant qu'il tient.
2. **§ 2** puis **§ 3** — même chantier que le 1, tant que le contrat de pivot est ouvert.
3. **§ 5** — bon marché, et il conditionne la testabilité de tout le reste au runtime.
4. **§ 4** — latent ici, réalisé dès que la config d'oracle sera écrite.
5. **§ 6** — au fil de l'eau.
