# Contrat de pivot — design ↔ sc-\<langage\>

Interface partagée entre `design:enforce` / `design:diffuse` (émetteurs) et `sc-<langage>:design-bridge` (réceptacles). Fige le format du spec d'enforcement et du spec de rendu, et ce que le réceptacle doit renvoyer.

Réutilise l'idiome de relais existant du dépôt (cf `sc-tiers:setup help` et `sc-*:sniff` → `.claude/rules/07-quality`).

---

## Pourquoi un contrat de pivot

Le design garde le **QUOI** (le contrat : tokens + manifeste = autorité). Les `sc-<langage>` font le **COMMENT** (linter réel idiomatique + wiring natif + rendu). Ce contrat est l'interface qui les découple : `enforce` et `diffuse` n'ont pas besoin de connaître l'outillage de lint natif d'un langage ; `sc-<langage>:design-bridge` n'a pas besoin de savoir comment le manifeste a été produit.

---

## Spec d'enforcement (enforce → design-bridge)

`enforce/04-pivot.md` émet ce spec en contexte (pas dans un fichier) quand un `sc-<langage>` est détecté.

```
## Design enforcement spec

Source: design/tokens.json + design/components.json + design/policies.json
Version: <release.json § designSystem.version>
Themes: [liste plate des thèmes nommés déclarés sous `tokens.json` § `themes`, ex. default, dark, grimoire — vide si aucun `themes` overlay]
Mode: <bem | utility-first> (design/policies.json § mode — toujours déclaré, jamais déduit)

### Valid class sets (mode bem)
Base classes: [liste des .base]
All valid classes: [union de tous .base + .elements.* + .modifiers.*]

### Token paths
All token paths: [liste des chemins de tokens.json aplatis]

### a11y requirements
[Par composant avec .a11y.requires non vide]
- <component>: role=<role>, requires=[<attr>, ...]

### Token-usage rules (mode utility-first — design/policies.json § usage)
Raw hex forbidden: <true|false> (usage.rawHexForbidden)
Colour utility prefixes: [usage.colorUtilityPrefixes, ex. bg, text, border, ring]
Allowed colour namespaces: [clés top-level de tokens.json § color.*, ex. brand, neutral, semantic]
Declared rules:
[Par entrée de usage.rules[] dont l'enforcement désigne ce réceptacle]
- <rule.id> (enforcement: <type du registre>): <rule.description>

### Enforcement target
Language: <langage du réceptacle>
Targets: [globs de fichiers à linter — en mode utility-first, couvrir tous les fichiers de composants, pas seulement le markup statique]

### Report path
<chemin du fichier de rapport attendu — doit figurer dans gates.config.json § pivotReports>

### Request
Réalise un linter natif idiomatique pour <langage> qui vérifie, selon Mode :
1. (bem) Toute classe appartenant au design system utilise un nom déclaré dans valid class sets.
2. Les références de tokens CSS (var(--...)) pointent vers un path existant.
3. (bem) Les composants déclarant .a11y.requires portent les attributs requis.
4. Si Themes n'est pas vide, le linter natif reste theme-agnostique (§ A2 : les thèmes re-déclarent les mêmes noms de `--var` dans leur bloc de sélecteur — aucune règle par thème à générer côté vocabulaire).
5. (utility-first) Toute couleur hexadécimale brute est interdite si Raw hex forbidden = true (le baseline le vérifie déjà dans style="…"/<style> — le pivot peut étendre à d'autres contextes CSS-in-JS idiomatiques au langage, ex. styles co-localisés dans le composant, template literals `css\`...\``).
6. (utility-first) Toute classe utilitaire de couleur (préfixe ∈ Colour utility prefixes) résout son namespace dans Allowed colour namespaces.
7. Pour chaque règle de Declared rules, réalise-la nativement à partir de la preuve que son type d'enforcement nomme (`references/enforcement-registry.md`) — c'est ce que le cœur portable, scanner de chaînes fichier par fichier, ne peut pas couvrir sans faux positif. Ne réinvente pas la règle : reprends l'id et la description tels quels.
8. Écris le rapport à Report path, au format `references/gate-config-schema.md § Rapport de pivot`. Toute règle de Declared rules que tu ne réalises pas y figure en `status: "unrealized"` — c'est une obligation, pas une option (§ Obligation de report).

Retourne : le linter installé dans le projet + les instructions de câblage dans l'outillage natif + le rapport écrit.
```

---

## Spec de rendu (diffuse → design-bridge)

`diffuse/04-pivot.md` émet ce spec quand un `sc-<langage>` est détecté.

```
## Design render spec

Source: design/tokens.json + design/components.json
Version: <release.json § designSystem.version>
Themes: [liste plate des thèmes nommés déclarés sous `tokens.json` § `themes`, ex. default, dark, grimoire — vide si aucun `themes` overlay]

### Component to render
Name: <canonical-name>
Base: <.base>
Elements: <map>
Modifiers: <map>
Backgrounds: <liste>
a11y: <.a11y>

### Variants to produce
[Liste des variantes demandées ou "toutes"]

### Render target
Language: <format de composant natif du réceptacle>
Output dir: <chemin souhaité dans le projet>

### Request
Produit le composant en code idiomatique <langage> :
- N'utilise que les classes et tokens du manifeste.
- Consomme design/adapters/tokens.css pour les valeurs.
- Satisfait les attributs .a11y.requires.
- Si Themes n'est pas vide, le composant natif doit rester compatible avec les blocs `.dark`/`[data-theme="…"]` émis par l'adaptateur (aucune valeur en dur qui court-circuiterait la cascade thème).
- Passe le gate enforce : `python design/lint/run-gates.py --config design/lint/gates.config.json` = exit 0.

Retourne : le fichier composant + les instructions d'intégration dans le projet.
```

---

## Obligation de report

Le réceptacle **écrit un rapport pour chaque règle qui lui a été assignée**, réalisée ou non. Format et statuts : `references/gate-config-schema.md § Rapport de pivot` — spécifiés là parce que c'est le fichier d'entrée du runner, et dupliqués nulle part.

Ce que l'obligation ferme : sans rapport, une règle assignée et une règle oubliée produisent la même trace — aucune. Le runner ne peut alors que la déclarer non réalisée « sans nouvelle de son réalisateur », ce qui est vrai des deux cas. Un `status: "unrealized"` nommé par son auteur les sépare : quelqu'un a lu la règle et dit ne pas la couvrir.

| Situation | Ce que le réceptacle écrit | Ce que le rapport du gate affiche |
|---|---|---|
| règle réalisée, aucune violation | `status: "pass"` | `REALIZED <id> (<type>) by <realizer>` |
| règle réalisée, violations trouvées | `status: "fail"` + `violations[]` | `VIOLATION` par entrée, exit 1 |
| règle hors de portée du réceptacle | `status: "unrealized"` | `UNREALIZED <id> (<type>) - <realizer> reports it unrealized` |
| réceptacle non lancé, ou rapport absent | — | `UNREALIZED <id> (<type>) - no report from its realizer` |

Un `unrealized` ne rougit pas le gate. Il n'a jamais à être justifié pour être accepté — seulement pour être écrit.

---

## Ce que le réceptacle doit renvoyer

`sc-<langage>:design-bridge` doit retourner :

| Pour enforcement | Pour rendu |
|-----------------|------------|
| Linter installé dans l'outillage natif du projet | Fichier composant créé à l'Output dir |
| Instructions de câblage dans le workflow existant (pre-commit, CI) | Instructions d'intégration (import, registration, usage) |
| Confirmation que les règles dérivent du spec (pas de listes codées en dur) | Confirmation que le composant passe le gate (exit 0) |
| Le rapport écrit à Report path, couvrant **toutes** les règles assignées | — |

---

## Dégradation gracieuse

Si aucun `sc-<langage>` ne couvre le langage du projet :
- `enforce` reste sur la baseline `lint-core.mjs` et le signale clairement.
- `diffuse` reste sur le rendu HTML+CSS baseline et le signale clairement — ce rendu est une **preview non intégrée**, pas un artefact natif ; le hand-off de promotion vit dans `diffuse/actions/02-render.md § Étape 5` (cf. `diffuse/adapters/html-css.md § Statut de la sortie`).
- Aucune erreur bloquante — le contrat est toujours l'autorité, seule la réalisation idiomatique est absente.

---

## Workflow de plateforme (extension du contrat de pivot)

Un **workflow de plateforme** instancie une classe de cas agnostique (`design:detail`, `skills/detail/references/workflow-classes.md`) sur une plateforme concrète. C'est un artefact **du pivot**, jamais de `design` : le plugin fige sa forme et sa règle de résolution ; il n'en porte jamais le contenu (dec-002 — `design` garde le QUOI, le pivot garde le COMMENT, et un workflow est un COMMENT).

### Chemin canonique

```
plugins/sc-<langage>/skills/design-bridge/references/workflow-<plateforme>.md
```

Le suffixe nomme la **plateforme** que le pivot sert (`fse`, `spa`, `static`…), pas le langage — un même pivot peut en porter plusieurs.

### Cinq titres requis, dans cet ordre

```
## Case classes covered
## Prerequisites (capabilities)
## Phases
## Gates
## Out of scope
```

Ces cinq chaînes sont un **jeton d'interface** : `design:detail/02-route` les attend à l'identique pour lire le workflow d'un pivot. Le corps de chaque section est libre ; les titres ne le sont pas.

### Déclaration de phase

Sous `## Phases`, chaque phase déclare trois champs :

- **input** — ce que la phase consomme ;
- **output** — ce qu'elle produit ;
- **verbe** — le verbe design qu'elle instancie (`define`, `destructure`, `adjust`, `enforce`, `diffuse`), ou **`off-funnel`** quand elle n'en instancie aucun (préparation d'environnement, déploiement, recette de production).

### Règle des capabilities

Sous `## Prerequisites (capabilities)`, un prérequis s'écrit comme une **capability** — runtime conteneurisé, accès shell distant, base de données distante, hébergement statique — **jamais** comme un fournisseur, un hébergeur ou un nom de projet. La plateforme est nommée ; le vendor ne l'est pas.

### Règle d'instanciation des gates

Sous `## Gates`, un workflow **instancie** les gates que le contrat connaît déjà (vocabulaire, fidélité, seuil de maturité) : il en nomme le point d'application dans sa séquence. Il n'en **redéfinit aucun** et n'en **introduit aucun** que le contrat ignore. Un gate créé hors du contrat ferait croire à une conformité locale qui n'en est pas une.

### Règle de résolution (par `02-route`)

| État du terrain | Ce que `route` émet |
|---|---|
| pivot installé **et** stack correspondante | la classe agnostique **étendue** par le workflow de plateforme |
| pivot absent | la classe agnostique **seule**, l'absence énoncée explicitement + recommandation conditionnelle d'installer `sc-<langage>` |
| pivot installé mais stack non correspondante | la classe agnostique **seule**, la non-correspondance énoncée (le workflow présent ne couvre pas cette plateforme) |

---

## Stack mapping

Le réceptacle se déduit du **langage de la preuve** que la règle doit lire, pas de la plateforme du projet. Le langage des feuilles de style et celui du runtime peuvent différer, et désignent alors deux réceptacles distincts pour un même projet (`references/enforcement-registry.md`).

| Langage de la preuve | sc-* à appeler |
|----------------------|---------------|
| Feuilles de style | `sc-css:design-bridge` |
| JavaScript / TypeScript | `sc-js:design-bridge` |
| PHP | `sc-php:design-bridge` |
| Python | `sc-python:design-bridge` (non encore implémenté) |
| Rust | `sc-rust:design-bridge` (non encore implémenté) |
| Aucun réceptacle installé | Cœur portable seul + règles assignées listées non réalisées |
