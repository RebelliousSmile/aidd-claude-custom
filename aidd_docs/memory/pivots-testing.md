# Pivots — qui fournit, qui ne fournit pas, et pourquoi

> Deux campagnes sur le même objet. La première (#10) porte sur le champ `testing` du contrat de pivot, consommé par `overcode:control` — c'est tout ce qui suit jusqu'à la section *Le piège de mesure*. La seconde (#11, 2026-08-03) porte sur les pivots installés sous `.claude/rules/07-quality/` et sur ce que leurs consommateurs en disent — dernière section.

Le champ `testing` est consommé par `overcode:control`, découvert par glob `**/capabilities/**/testing.md` sous la racine du plugin de langage actif. Contrat : `plugins/overcode/skills/control/references/pivot-contract.md`.

## État des fournisseurs — 4 sur 6, et c'est un état stable

| Plugin | Pivot | Motif |
|---|---|---|
| `sc-js` | ✅ | premier livré, complété de *Domain resolution* |
| `sc-python` | ✅ | mesuré sur un projet Django réel |
| `sc-rust` | ✅ | mesuré sur un crate binaire Win32 |
| `sc-php` | ✅ | mesuré sur **trois** terrains — PrestaShop modulaire + WordPress |
| `sc-css` | ❌ **décision, pas oubli** | décompte 2026-07-30 : 1 champ sur 10, **0 des 5 requis**. Aucun outil n'exécute du CSS ; la régression visuelle est un test de *page*, outillée par la stack JS. Les 2 champs qui semblaient répondre sont déjà fournis, plus finement, par `sc-css:audit#01-audit.md` et `sniff#01-scan.md`. **Ne pas rouvrir sans nouvel outillage CSS réel.** |
| `sc-godot` | ❌ | squelette, et surtout **aucun projet Godot mesurable** sur le poste |

## La règle qui a coûté le plus cher à établir

**Un pivot est un fournisseur de savoir de stack, jamais un décideur** — aucun champ ne nomme son consommateur, ni ne raffine l'exigence de preuve, seulement sa position (DEC-007).

**Le pivot suit le fichier** (DEC-008) : sur un dépôt polyglotte, la détection rend un *ensemble* de plugins, les énumérations sont des **unions**, rien n'est sommé entre stacks, et l'absence se déclare par stack. Corollaire opérationnel : livrer un pivot pour une stack sans population de tests fait entrer ses fichiers dans l'univers source d'un run dont la contribution de tests est vide — le run rend un zéro qui n'est le défaut de personne. **L'absence déclarée vaut mieux qu'un pivot creux.**

**Deux suppositions tacites rendues explicites** (DEC-009) : source et test **ne sont pas garanties disjointes** (Rust met ses tests dans le fichier source) ; et **un prérequis constaté absent vaut champ absent pour ce run**, pour tout champ dont la réponse est une commande.

## Méthode de rédaction, éprouvée sur quatre pivots

- **Mesurer, jamais déduire.** Chaque commande du pivot est exécutée sur un projet réel, en **lecture seule** : caches redirigés hors dépôt (`CARGO_TARGET_DIR`, `--cache-directory`), `git status --porcelain` comparé octet pour octet avant/après. Sur une fixture non propre à HEAD, on **compare** au lieu d'exiger le vide.
- **Un terrain ne suffit pas toujours.** `sc-php` a demandé trois terrains parce que la stack couvre deux mondes sans intersection. Le terrain nommé par le plan peut être disqualifié à l'ouverture — celui de `sc-php` n'avait aucune infrastructure de test PHP.
- **Écrire ce que la mesure contredit.** Les constats de valeur sont ceux qui démentent le conseil courant : couverture PHP sans driver qui **sort 0 sans écrire de fichier**, `phpdbg -qrr` mort en PHPUnit 10, `vendor/bin/phpunit` présent mais inexécutable.
- **Langue du plugin, titres verbatim du contrat, frontmatter vide** — un `paths:` ferait charger le pivot à chaque édition de fichier de la stack, or il ne décrit pas une famille de fichiers mais une suite.
- Les 4 pivots sont **strictement homogènes** : même chemin, mêmes 10 titres, même ordre. Le contrat n'impose pas d'ordre ; l'homogénéité est une convention à tenir à la main.

## Le piège de mesure qui s'est répété

**La stack PHP n'a pas de point d'entrée unique** : neuf modules, neuf dépôts, neuf `vendor/`, aucune commande racine. Une mesure lancée à la racine rend *zéro test* sur un projet qui en porte 225. Avant de conclure « pas de tests », vérifier quelle est l'**unité de mesure** de la stack — dépôt, composant, ou espace de travail.

---

# Pivots `07-quality` — la quittance (#11, 2026-08-03)

Objet : les fichiers `<famille>-pivots-<stack>.md` que les `sc-*` déposent dans `.claude/rules/07-quality/`, et ce que les quatre `*-optimize` d'`overcode` disent de leur chargement. ADR : `aidd_docs/internal/decisions/010-pivot-consumer-receipt.md`.

## La quittance : rendre compte de ce qu'on n'a pas chargé

**Un repli n'est pas un défaut ; un repli silencieux en est un.** Une skill qui charge un pivot quand il est là et son schéma générique sinon rend deux rapports indiscernables pour deux situations opposées. La règle générale, valable au-delà de ces skills : **toute skill à chargement conditionnel rend une quittance** — d'où vient ce qu'elle a chargé, et pourquoi le reste ne l'a pas été.

**Quatre états, pas deux.** `installed` · `not installed` (un plugin le fournit, ce projet ne l'a pas) · `no provider` (aucun plugin de la marketplace n'écrit ce nom) · `empty receptacle` (la famille est une interface publique que personne ne remplit). Les trois derniers appellent trois suites incompatibles — installer ici, générer, n'attendre personne. Un binaire présent/absent les confond et fabrique une recommandation qui ne mène nulle part.

**Deux lectures qui ne se déduisent pas.** La quittance se lit **par stack**, jamais par dépôt (DEC-008 s'applique tel quel). Et « vide » se lit **sur les règles**, pas sur les fichiers : un réceptacle contenant un `.gitkeep` est vide.

**`no provider` exige une table statique.** Une skill qui tourne dans un projet ne voit pas les autres plugins de la marketplace : elle ne peut rien dériver à l'exécution. `plugins/overcode/references/pivot-providers.md` porte `<stack> → <plugin>, <commande>`, citée par les quatre skills, recopiée par aucune. **La commande est portée par plugin, jamais par famille** — `sc-tiers` s'installe par `setup`, les quatre `sc-<langage>` par `sniff` ; un gabarit uniforme remplace un remède faux par un autre.

## Une déclaration d'installeur est une affirmation vérifiable

Neuf cibles `.claude/rules/` étaient déclarées sans aucun fichier source derrière — trois chez `sc-tiers`, six chez `sc-css` — depuis des mois. Ce qui manquait n'était pas la vigilance mais **la garde**. Deux ont été ajoutées à `tools/eval/consistency.mjs` :

- **M4** — toute ligne d'action citant une cible `.claude/rules/` voit **toutes** ses sources résoudre sur disque. Trois choix de conception qui se paient si on les rate : ancrage sur la **forme** de la ligne et jamais sur l'intitulé de colonne (il varie d'un plugin à l'autre) · **deux** bases de résolution (`${CLAUDE_PLUGIN_ROOT}/x` → racine du plugin ; relatif → racine du skill) · formulée **par ligne**, parce qu'une action de `sc-python` met source et cible dans la même cellule.
- **M5** — chaque ligne de `pivot-providers.md` joint une paire (plugin, cible) que M4 a validée. Formulée ainsi, elle est **indépendante de l'ordre des parts** ; la formulation abandonnée (« désigne un fichier réellement produit ») rendait son verdict dépendant de ce qui avait déjà été corrigé.

**Le remède au fantôme est le retrait de la déclaration, pas l'écriture du contenu.** Écrire les neuf pivots manquants est une décision produit ; retirer la promesse corrige l'écart sans rien fabriquer. Corollaire pour un consommateur : la stack bascule de `not installed` à `no provider`, ce qui est vrai.

**Un doublon de source pour une même cible se tranche en lisant les corps.** Deux fichiers de `sc-python` visaient `ap-pivots-django-activitypub.md`. Un grep lexical plaidait pour l'un ; la lecture a montré que l'autre couvrait deux sections entières que le premier n'a pas. Le delta du perdant se **verse** dans le gagnant avant retrait — sinon le doublon se résout par une perte.

## Ce que le rejeu behave a appris (à ajouter à [`behave-eval-method`](behave-eval-method.md))

**Une suite tout-verte a changé de fonction.** Run 1 : 1 PASS / 16 FAIL / 1 N/A sur les deux suites. Run 2 sur le code corrigé : plus aucun rouge dans une famille de défauts entière — donc plus de **contrôle négatif**. Le contrôle positif seul n'établit plus qu'un cas fautif serait détecté. La suite est devenue une suite de **non-régression** là où elle était une suite de **reproduction** ; c'est structurel, pas réparable en éditant une ligne.

**Une colonne qui annonce ses verdicts périme à la correction.** *Instruction pinned* était biaisante au run 1 ; elle est **activement trompeuse** au run 2 — un juge qui la recopie rend six FAIL faux. Une suite qui écrit ses attentes doit prévoir où elles vont quand elles cessent d'être vraies.

**Une précondition peut mourir sans que son critère meure.** Une ligne décrivant « quatre pivots déclarés, trois absents » ne décrit plus rien après le retrait — mais son critère (« le compte n'est pas figé ») reste jugeable. Distinguer *situation* et *critère* est ce qui permet de rejouer.

**Un `FAIL → N/A` peut être l'issue nominale**, à condition d'être écrit d'avance : la ligne dont la cible est supprimée par la correction atteste la suppression. Écrit après coup, il est indiscernable d'une dette.
