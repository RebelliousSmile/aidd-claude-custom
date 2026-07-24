# Contract schema — quatre artefacts, une racine

Le contrat est un répertoire de cinq fichiers : quatre **artefacts** adressables et une **racine** qui les identifie.

| Fichier | Rôle | Écrit par | Lu par |
|---|---|---|---|
| `release.json` | Racine — identité, versions par artefact, hash de source, provenance, statut de maturité | `adjust/02-freeze.md`, `tools/migrate-contract.py` | `lint-core.mjs` (présence + les trois artefacts dont il dérive ses règles), `tools/status.py` |
| `tokens.json` | Valeurs (couleurs, espacements, typographie, breakpoints…) au format W3C DTCG | `adjust/02-freeze.md` | `lint-core.mjs` Règles 2/4, `config-gen.py`, générateurs d'adapters |
| `components.json` | Anatomie des composants — nomenclature déclarée, rien d'autre | `adjust/02-freeze.md` | `lint-core.mjs` Règles 1/5, `config-gen.py` |
| `policies.json` | Politiques transverses — mode, usage des tokens, préfixes utilitaires, table des adapters | `adjust/02-freeze.md` | `lint-core.mjs` Règles 1/3/4, pivots `sc-*` |
| `oracle.json` | Cibles de mesure — hints par composant | `adjust/02-freeze.md` | `config-gen.py` |

`design-system.md` (charte prose) n'est **pas** un artefact du contrat : c'est une **entrée** dont `release.json § charter` enregistre la présence et la version. Aucun outil ne la lit ; `status.py` observe seulement qu'elle existe ou non.

**Règle fondamentale : une donnée vit dans un seul artefact.** Une valeur vit dans `tokens.json`, une nomenclature dans `components.json`, une politique dans `policies.json`, un hint de mesure dans `oracle.json`, une version dans `release.json`. Aucun champ n'est dupliqué d'un artefact à l'autre.

**L'absence de `release.json` identifie un contrat 1.x.** `lint-core.mjs` sort alors en 3 et nomme la commande de migration. Aucun chemin de lecture 1.x ne subsiste.

## Étiquetage des champs

Chaque champ est **exécutable** — un consommateur nommé le lit et en tire un effet vérifiable — ou **informationnel** — il documente une intention qu'aucun outil ne vérifie. Un champ dont le seul consommateur est un lot à venir est informationnel à cette version, et le lot est nommé.

## `release.json`

```json
{
  "$schema": "design/references/contract-schema#release",
  "$format": "2.0",
  "designSystem": { "version": "1.2.0" },
  "artifacts": {
    "tokens.json":     { "version": "1.2.0", "sourceHash": "sha256:…" },
    "components.json": { "version": "1.2.0", "sourceHash": "sha256:…" },
    "policies.json":   { "version": "1.2.0", "sourceHash": "sha256:…" },
    "oracle.json":     { "version": "1.2.0", "sourceHash": "sha256:…" }
  },
  "charter": { "present": true, "path": "design-system.md", "version": "1.2.0" },
  "provenance": { "producedBy": "migrate-contract.py", "producedAt": "<ISO-8601>", "from": "contrat 1.x" },
  "checks": null,
  "status": "normalized"
}
```

| Champ | Requis | Statut · consommateur | Description |
|---|---|---|---|
| `$schema` | oui | informationnel | Toujours `"design/references/contract-schema#release"` |
| `$format` | oui | informationnel | Version du format de contrat. C'est la **présence du fichier**, pas sa valeur, qui distingue 2.x de 1.x |
| `designSystem.version` | oui | informationnel | Semver du design system pris comme un tout |
| `artifacts` | oui | exécutable · `lint-core.mjs` (doit déclarer `tokens.json`, `components.json` et `policies.json` ; chaque artefact déclaré doit exister et se parser ; sinon exit 2) | Clés = noms de fichier des artefacts. `oracle.json` n'est déclaré que si le contrat en produit un |
| `artifacts.<file>.version` | oui | informationnel | Version **déclarée** de cet artefact. Des versions divergentes sont une donnée, pas une violation (§ Disparition de l'invariant 5) |
| `artifacts.<file>.sourceHash` | oui | informationnel · le gate de dérive du Lot 3 le lira | `sha256:<hex>` de la source dont l'artefact dérive |
| `charter.present` | oui | exécutable · `tools/status.py` | Charte prose présente ou absente dans le répertoire du contrat |
| `charter.path` | oui | exécutable · `tools/status.py` | Chemin relatif de la charte |
| `charter.version` | non | informationnel | Version déclarée par la charte ; `null` si absente ou non déclarée |
| `provenance.producedBy` | oui | informationnel | Outil ou action qui a écrit ce contrat |
| `provenance.producedAt` | oui | informationnel | Horodatage ISO-8601 |
| `provenance.from` | oui | informationnel | Origine — contrat 1.x migré, ou figeage direct |
| `checks` | oui | exécutable · `tools/status.py` | Enregistrement des vérifications passées. `null` = jamais jouées |
| `status` | oui | informationnel · le gate de conformité du Lot 5 le rendra opposable | Statut de maturité, écrit par `tools/status.py` et par lui seul (§ Statut de maturité) |

### Statut de maturité

Une échelle : la première condition non tenue arrête la montée. `tools/status.py` est la seule implémentation ; aucun autre code ne calcule un statut.

| Statut | Condition atteinte |
|---|---|
| `extracted` | Les artefacts existent |
| `normalized` | + charte présente |
| `validated` | + vérifications jouées (`checks` non nul) |
| `production-ready` | + entrées de contraste et d'états — ajoutées par le Lot 5, jamais atteintes à cette version |

Charte absente ⇒ plafond à `extracted`, quelles que soient les vérifications : l'échelle plafonne, elle ne saute pas de barreau.

### Disparition de l'invariant 5

En 1.x, `components.json § $version` devait rester en phase avec `design-system.md § version:` — un invariant qu'aucun consommateur ne vérifiait. `release.json` déclare une version par artefact et une version de charte. Un écart est **enregistré**, pas sanctionné.

## `tokens.json`

Inchangé — schéma complet dans `token-schema.md`. Aucun champ ne quitte ni ne rejoint cet artefact au passage en 2.0.

## `components.json`

Anatomie seule. `mode`, `$utilityPrefixes` et `usage` sont partis en `policies.json` ; `oracle` en `oracle.json` ; `$version` en `release.json`.

```json
{
  "$schema": "design/references/contract-schema#components",
  "components": {
    "<canonical-name>": {
      "base": "<BEM-block>",
      "elements":  { "<element-label>": "<BEM-element>" },
      "modifiers": { "<variant-label>": "<BEM-modifier>" },
      "backgrounds": ["<token.path>"],
      "a11y": { "role": "<ARIA-role>", "requires": ["<attribute>"] }
    }
  }
}
```

Champ par champ, invariants et exemples : `adjust/references/manifest-schema.md`.

## `policies.json`

```json
{
  "$schema": "design/references/contract-schema#policies",
  "mode": "bem",
  "$utilityPrefixes": ["<utility-prefix>"],
  "usage": {
    "rawHexForbidden": true,
    "colorUtilityPrefixes": ["<utility-prefix>"],
    "rules": [
      { "id": "<rule-id>", "description": "<prose>", "enforcement": "baseline" }
    ]
  },
  "adapters": [
    { "artifact": "adapters/tokens.css", "consumer": "stylesheet" }
  ]
}
```

| Champ | Requis | Statut · consommateur | Description |
|---|---|---|---|
| `$schema` | oui | informationnel | Toujours `"design/references/contract-schema#policies"` |
| `mode` | oui | exécutable · `lint-core.mjs` (sélection des règles) · `tools/migrate-contract.py` (refuse de le deviner) | `"bem"` ou `"utility-first"`. Aucune auto-détection : absent, le contrat est inutilisable et le linter sort en 2 |
| `$utilityPrefixes` | non | exécutable · `lint-core.mjs` Règle 1 (`--strict`) | Préfixes de classes utilitaires à ne jamais signaler |
| `usage.rawHexForbidden` | non | exécutable · `lint-core.mjs` Règle 3 | `true` ⇒ toute couleur hexadécimale brute dans un `style="…"` ou un `<style>` inline est une `error`. Hors de ces deux contextes, aucune détection |
| `usage.colorUtilityPrefixes` | non | exécutable · `lint-core.mjs` Règle 4 | Préfixes de classe utilitaire porteurs de couleur. Pour `<prefix>-<nom>-<NN\|NNN>`, `<nom>` doit être une clé top-level de `tokens.json § color.*`. Mode `utility-first` uniquement |
| `usage.rules[].id` | — | exécutable · pivot `sc-*` | Identifiant de la règle déclarée |
| `usage.rules[].description` | — | exécutable · pivot `sc-*` | Énoncé lu par le pivot qui la réalise |
| `usage.rules[].enforcement` | — | exécutable · pivot `sc-*` | `"baseline"` = portée par les Règles 3/4 · `"pivot-only"` = hors de portée d'un scanner de chaînes, réalisée par le pivot (`references/sc-pivot-contract.md`) |
| `adapters[].artifact` | non | informationnel · le gate de dérive du Lot 3 le lira | Chemin relatif de l'adapter généré |
| `adapters[].consumer` | non | informationnel · le gate de dérive du Lot 3 le lira | Rôle qui consomme cet artefact. Jamais un nom de plateforme ni de projet |

### Table de correspondance des adapters

Une entrée par adapter **réellement présent** sous `<contrat>/adapters/`, jamais par adapter que le plugin sait écrire. `tools/migrate-contract.py` la dérive de l'extension du fichier :

| Extension | `consumer` |
|---|---|
| `.css` | `stylesheet` |
| `.scss` · `.sass` · `.less` | `stylesheet source` |
| `.json` | `platform token file` |
| `.js` · `.mjs` · `.cjs` · `.ts` | `build configuration` |
| autre | `unknown` — remonté comme anomalie du rapport, à compléter à la main |

Règle d'émission d'un adapter : `write-system-procedure.md § Adapter emission rule`.

## `oracle.json`

Inerte pour le lint. Seul `config-gen.py` le lit. **Fichier optionnel** : un contrat sans cible de mesure ne l'écrit pas et ne le déclare pas dans `release.json § artifacts`.

```json
{
  "$schema": "design/references/contract-schema#oracle",
  "components": {
    "<canonical-name>": {
      "elements": {
        "<element-label>": { "check_text": true, "props": ["fontSize", "color"] }
      },
      "collections": [
        { "name": "<label>", "item_selector": "<BEM-element>", "ack": { "id": "DEV-xxx", "reason": "<prose>" } }
      ]
    }
  }
}
```

| Champ | Requis | Statut · consommateur | Description |
|---|---|---|---|
| `$schema` | oui | informationnel | Toujours `"design/references/contract-schema#oracle"` |
| `components.<name>.elements.<label>.check_text` | non | exécutable · `config-gen.py` | `true` sur les éléments dont le texte doit correspondre à la référence. Interdit sur les cibles en prose |
| `components.<name>.elements.<label>.props` | non | exécutable · `config-gen.py` | Surcharge la liste de props token-dérivées pour cet élément |
| `components.<name>.collections[].name` | — | exécutable · `config-gen.py` | Libellé de la structure répétée |
| `components.<name>.collections[].item_selector` | — | exécutable · `config-gen.py` | Classe de l'item répété |
| `components.<name>.collections[].ack` | non | exécutable · `adapters/measure/measure.py` | Pré-sanction d'une divergence attendue : `{ "id": "…", "reason": "…" }` |
| `contract` | non | informationnel | Hints de mesure de portée contrat, hérités d'un `components.json § oracle` 1.x. Aucun consommateur ne les lit — seule la forme par composant en a un. Conservés pour ne rien perdre à la migration, à reventiler à la main |

Les clés de `oracle.json § components` sont les noms canoniques de `components.json § components` ; les libellés d'élément sont ceux de `components.<name>.elements`. Un composant sans hint n'a pas d'entrée — `config-gen.py` génère quand même une cible par élément, sans `check_text` et avec les props par défaut.

## Dérivation des règles de lint

`lint-core.mjs` lit `tokens.json`, `components.json` et `policies.json`, sur **un fichier de markup à la fois**, et n'en dérive que les cinq règles ci-dessous. Aucun autre champ du contrat n'a d'effet sur le lint.

| Règle | Mode | Dérivée de | Sévérité |
|---|---|---|---|
| 1 — vocabulaire de classes | `bem` | `components.json § .base + .elements.* + .modifiers.*` ; `policies.json § $utilityPrefixes` | `error` (bloc déclaré) · `warning` sous `--strict` (forme BEM, bloc non déclaré, hors `$utilityPrefixes`) |
| 2 — références `var(--…)` | les deux | chemins de `tokens.json` aplatis en `--chemin-avec-tirets` | `error` |
| 3 — raw-hex | les deux (inerte sans `usage`) | `policies.json § usage.rawHexForbidden` | `error` |
| 4 — namespaces de couleur | `utility-first` | `policies.json § usage.colorUtilityPrefixes` × clés top-level de `tokens.json § color.*` | `error` |
| 5 — `--report-unused` | `bem` | entrées de `components.json` absentes du fichier scanné | rapport seul, jamais bloquant |

Champs **inertes pour le lint** : `.backgrounds` et `.a11y` de `components.json`, `policies.json § adapters[]`, `usage.rules[]` en `enforcement: "pivot-only"`, et `oracle.json` entier.

### Où porte le vocabulaire, selon `mode`

Sur une stack qui compose des classes utilitaires au lieu de classes BEM, `components` ne décrit rien de ce que le code écrit : la Règle 1 tourne à vide et ressort verte sans avoir rien vérifié. `mode` déplace donc la cible.

| | `bem` | `utility-first` |
|---|---|---|
| Le vocabulaire porte sur | les noms de classe | l'usage des tokens |
| `components.json § components` | requis | optionnel — absent, vide ou partiel |
| `policies.json § usage` | généralement absent | requis pour que le linter vérifie quoi que ce soit |
| Règle 1 | s'exécute | jamais |
| Règles 3/4 | inertes sans `usage` | s'exécutent |

Les deux modes sont de première classe ; aucun n'est un mode dégradé de l'autre. Les namespaces de couleur autorisés se dérivent à l'exécution des clés top-level de `tokens.json § color.*` : ajouter `color.accent` au contrat l'autorise immédiatement, sans toucher `policies.json`.

## Redistribution depuis un contrat 1.x

Exhaustive. Rien n'est inventé, rien n'est perdu. `tools/migrate-contract.py` applique exactement cette table.

| Source 1.x | Cible 2.0 |
|---|---|
| `tokens.json` (entier) | `tokens.json`, inchangé |
| `components.json § $schema` | `components.json § $schema`, réécrit vers ce document |
| `components.json § $version` | `release.json § designSystem.version` et `§ artifacts.*.version` |
| `components.json § mode` (ou `--mode`) | `policies.json § mode` |
| `components.json § $utilityPrefixes` | `policies.json § $utilityPrefixes` |
| `components.json § usage.*` | `policies.json § usage.*` |
| `components.json § components.<n>.{base, elements, modifiers, backgrounds, a11y}` | `components.json § components.<n>.*` |
| `components.json § components.<n>.oracle.{elements, collections}` | `oracle.json § components.<n>.*` |
| `components.json § oracle` (portée contrat) | `oracle.json § contract` — sans lecteur, signalé en anomalie |
| `components.json § <clé top-level non listée ci-dessus>` | `policies.json § <clé>`, verbatim — signalé en anomalie |
| `components.json § components.<n>.<clé non listée ci-dessus>` | `components.json § components.<n>.<clé>`, verbatim — signalé en anomalie |
| `design-system.md` — présence et `version:` | `release.json § charter` |
| adapters présents sous `adapters/` | `policies.json § adapters[]` |
| — (nouveau) | `release.json § artifacts.*.sourceHash`, `§ provenance`, `§ checks`, `§ status` |

Le registre d'écarts en Markdown reste hors contrat à cette version ; sa forme structurée appartient au Lot 4.

## Contrat incomplet

| Situation | Diagnostic |
|---|---|
| `release.json` absent | Contrat 1.x — `lint-core.mjs` sort en 3 et imprime la commande de migration |
| `release.json` présent, un artefact déclaré absent ou illisible | Contrat inutilisable — exit 2, l'artefact est nommé |
| `policies.json § mode` absent | Décision que l'outil refuse de deviner — exit 2 |
