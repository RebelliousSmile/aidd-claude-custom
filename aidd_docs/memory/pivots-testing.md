# Pivots `testing` — qui fournit, qui ne fournit pas, et pourquoi

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
