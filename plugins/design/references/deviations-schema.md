# deviations.json — la source structurée des écarts sanctionnés

Un écart toléré est une **donnée** avant d'être une prose. Tant qu'il vivait dans un Markdown, aucun outil ne pouvait décider s'il était encore valide : c'est l'opérateur qui affirmait « celui-ci est sanctionné ». `deviations.json` porte l'écart sous une forme que l'oracle lit, valide et fait expirer sans jugement humain.

`release.json` le racine comme les quatre autres artefacts. **Fichier optionnel** : un contrat qui ne tolère aucun écart ne l'écrit pas.

## Ce qu'un écart sanctionne

Le gate de fidélité mesure un rendu contre une référence, propriété par propriété. Un delta non nul est une **dérive** — à corriger — *sauf* s'il est couvert par une entrée active de ce fichier. La couverture n'est jamais présumée : une entrée déclare l'`id`, la cible oracle, la propriété et la **valeur attendue** (ce qui ship à la place de la maquette). Sans valeur attendue, l'entrée ne sanctionne rien — l'oracle sort `OPEN`.

Le config de mesure et les `ack` de collection **référencent** un `id` ; ce fichier est l'**autorité** qui dit si l'`id` existe, est actif, n'a pas expiré et porte une valeur attendue.

## Forme

```json
{
  "$schema": "design/references/contract-schema#deviations",
  "active": [
    {
      "id": "DEV-001",
      "status": "active",
      "target": "Hero · lede",
      "prop": "fontSize",
      "expected": "17px",
      "date": "2026-06-15",
      "expires": "2026-12-31",
      "reason": "adopte le token fluide de corps unique ; +1px à 375 sous le seuil perceptif"
    }
  ],
  "historical": [
    {
      "id": "DEV-000",
      "status": "superseded",
      "target": "Hero · title",
      "prop": "letterSpacing",
      "expected": "-0.02em",
      "date": "2026-05-02",
      "decidedAt": "2026-06-10",
      "reason": "remplacé par DEV-004 après refonte de l'échelle typographique"
    }
  ]
}
```

## Champs

| Champ | Requis | Statut · consommateur | Description |
|---|---|---|---|
| `$schema` | oui | informationnel | Toujours `"design/references/contract-schema#deviations"` |
| `active` | oui | exécutable · `adapters/measure/measure.py` | Entrées qui **peuvent** sanctionner un delta. Une entrée absente d'ici ne sanctionne jamais, même présente dans `historical` |
| `historical` | non | informationnel | Décisions révolues — conservées pour l'audit, jamais lues par l'oracle. Séparer les deux empêche qu'un écart révoqué continue de passer |
| `active[].id` | oui | exécutable · `measure.py` (validation d'une exception) | Identifiant stable, forme `DEV-<NNN>`. Référencé par le config de mesure et par `components.json § deviation_refs` |
| `active[].status` | oui | exécutable · `measure.py` | `"active"` pour une entrée de `active`. Toute autre valeur y est une incohérence, signalée et traitée comme non sanctionnante |
| `active[].target` | oui | exécutable · `measure.py` | Nom de la cible oracle à laquelle l'écart s'applique — le `name` d'un target du config de mesure |
| `active[].prop` | oui | exécutable · `measure.py` | Propriété CSS mesurée dont le delta est toléré |
| `active[].expected` | oui | exécutable · `measure.py` | Valeur qui ship à la place de la maquette. **Absente ⇒ l'entrée ne sanctionne rien, verdict `OPEN`** |
| `active[].date` | oui | informationnel | Date de décision, ISO-8601 |
| `active[].expires` | non | exécutable · `measure.py` (comparée à l'horloge du run) | Date ISO-8601 après laquelle l'entrée ne sanctionne plus. Absente ⇒ pas d'expiration. Une entrée expirée produit un verdict `OPEN` — l'expiration n'est jamais une tolérance silencieuse |
| `active[].reason` | oui | informationnel | Justification concrète de ce que l'écart achète (DRY/SOLID/token unique), pas « plus propre » |
| `historical[].decidedAt` | oui | informationnel | Date où l'entrée est passée en historique |
| `historical[].status` | oui | informationnel | Pourquoi elle n'est plus active — `superseded`, `revoked`, `expired`, `fixed` |

Les autres champs d'une entrée `historical` reprennent la forme d'une entrée `active`, `expires` en moins.

## Ce qui rend un verdict `OPEN`

L'oracle valide chaque `id` référencé par une exception du config. L'exception échoue — donc le delta redevient une dérive et le verdict passe `OPEN` — dans l'un de ces cas :

| Situation | Diagnostic |
|---|---|
| `id` absent de `active` | Exception qui référence un écart inexistant ou révolu |
| entrée `active` sans `expected` | Rien à sanctionner : la valeur qui ship n'est pas déclarée |
| entrée `active` avec `expires` < horloge du run | Écart expiré ; l'expiration s'évalue à l'exécution |

Aucun de ces cas n'est un crash ni un exit de commande : ce sont des raisons ajoutées à `summary.reasons`, le verdict devient `OPEN`, la mesure continue.

## Migration depuis le registre Markdown

Le registre 1.x (`deviation-ledger-template.md`) est du Markdown en prose. `tools/migrate-contract.py --ledger` le parse en `deviations.json`, une entrée par bloc `### DEV-NNN`, en mappant :

| Ligne Markdown | Champ `deviations.json` |
|---|---|
| `### DEV-NNN — <titre>` | `id` (le titre est reporté en `reason` s'il n'y a pas de `justification`) |
| `date:` | `date` |
| `contract value: <prop> = <valeur>` | `prop` et `expected` |
| `component:` / `selector(s):` | `target`, au mieux — signalé en anomalie si la cible oracle n'est pas dérivable |
| `justification:` | `reason` |
| `expires:` (si présent) | `expires` |

Une entrée qui ne fournit ni `prop` ni `contract value` ne peut pas sanctionner : elle est **reportée en anomalie, jamais silencieusement ignorée**. La passe est idempotente — rejouée, elle réécrit un fichier identique.

## Vue Markdown générée

`deviations.json` est la source ; `tools/generate.py` en dérive une vue Markdown lisible (`deviation-ledger-template.md` en est le gabarit de sortie). La vue est un artefact généré : une retouche à la main y est une dérive, `generate.py --check` la signale. On édite `deviations.json`, jamais la vue.
