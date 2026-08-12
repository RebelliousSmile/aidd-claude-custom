# Schéma de configuration du gate

Fichier lu par `tools/run-gates.py`. **Tous les chemins qu'il porte sont relatifs à lui-même** — le gate se déplace avec le fichier, jamais avec le répertoire d'appel.

```json
{
  "$schema": "design/references/gate-config-schema",
  "contract": "<répertoire du contrat>",
  "linter": "<chemin de lint-core.mjs>",
  "targets": ["<fichier ou glob>"],
  "strict": false,
  "pivotReports": ["<fichier ou glob>"],
  "workflowChecks": [{"id": "pre-commit", "status": "pass|fail", "message": "<detail>"}]
}
```

| Champ | Requis | Description |
|---|---|---|
| `contract` | oui | Répertoire contenant `release.json` et les artefacts qu'il déclare. Sans `release.json` ⇒ exit 3 |
| `linter` | si `targets` non vide | Chemin de `skills/enforce/adapters/lint-core.mjs` installé dans le projet |
| `targets` | non | Fichiers de markup, littéraux ou globs. Un littéral absent est signalé par son nom ; un glob sans correspondance ne l'est pas |
| `strict` | non | Passé à `--strict`. Ne change aucun code de sortie : la Règle 1 stricte produit des `warning` |
| `pivotReports` | non | Rapports écrits par les réalisateurs natifs (`references/sc-pivot-contract.md`). Chaque entrée est un chemin — littéral ou glob — ou un objet `{ "path": …, "command": [ … ] }` |
| `workflowChecks` | non | Contrôles P2 d'intégration (`rules`, `success_condition`, pre-commit, import automatique). Un `fail` est imprimé comme warning et ne change jamais seul le code de sortie |

Un `targets` vide est une configuration valide : un contrat dont aucune règle n'est de type `markup` n'a rien à faire linter, et son gate ne tient que par les rapports de pivot.

## Rapport de pivot

Deux formes d'entrée, un seul effet sur le gate :

```json
"pivotReports": [
  "reports/design-native.json",
  { "path": "reports/design-style.json", "command": ["<binaire>", "<argument>"] }
]
```

- Chemin nu : le rapport est lu tel qu'il est sur le disque. S'il est absent, il est simplement
  omis : les règles assignées restent `UNREALIZED` (P0/P1 bloquent, P2 avertit). Rien ne garantit
  qu'un rapport nu décrit le code actuel.
- Objet avec `command` : le runner retire d'abord tout ancien rapport, puis relance le réalisateur
  natif depuis le répertoire de la configuration. Les exits 0 et 1 sont admis — les violations
  vivent dans le rapport — mais l'invocation doit **créer** un nouveau rapport valide. Un autre
  exit, un binaire introuvable ou l'absence de nouveau rapport sort en 2. L'ancien contenu est
  restauré uniquement pour diagnostic après échec et n'est jamais consommé comme preuve. Cette
  règle repose sur la création, pas sur la granularité incertaine d'un timestamp.

`command` est une liste non vide d'arguments non vides, jamais une ligne de shell : pas de shell,
donc pas de règle de quoting à rater. Une clé `command: []` est invalide et sort en 2 ; elle ne
transforme jamais silencieusement l'objet en chemin nu.

```json
{
  "realizer": "<nom du linter natif installé>",
  "rules": [
    { "id": "<rule-id>", "status": "pass", "violations": [] }
  ]
}
```

Pour compatibilité avec les premiers rapports 2.x, `realizer` peut être absent (le chemin du
rapport sert alors de nom) et `rules` peut être absent (aucune preuve apportée). Dès qu'ils sont
présents, `realizer` doit être une chaîne non vide et `rules` un tableau. Les nouveaux pivots
écrivent toujours les deux champs.

- `id` reprend verbatim le `usage.rules[].id` du contrat — c'est la clé d'appariement. Une entrée absente, inconnue ou dupliquée fait sortir en 2.
- `status` ∈ `pass` · `fail` · `unrealized`.
- Toute autre valeur de `status` sort en 2 ; elle n'est jamais assimilée à `pass`.
- `fail` ⇒ chaque entrée de `violations` compte comme une violation du gate ; liste vide ⇒ l'`id` fait office de message.
- `unrealized` ⇒ le réalisateur a reçu la règle et déclare ne pas l'avoir réalisée. Listée non réalisée en nommant qui le déclare ; l'effet dépend de la priorité contractuelle.
- Une règle non couverte par un rapport reste **non réalisée** elle aussi, mais sans auteur : le rapport ne peut pas distinguer « pas encore lancé » de « hors de portée ». C'est ce que `unrealized` supprime (`references/enforcement-registry.md § Marqueur non réalisé`).

La priorité vient du contrat, jamais du rapport : `usage.rules[].priority` vaut `P0`, `P1` ou `P2` et vaut `P1` par défaut. Les identifiants `usage.rules[].id` sont uniques ; un doublon invalide le contrat et sort en 2. Une règle P0/P1 non réalisée est une preuve manquante bloquante. Une règle P2 en échec ou non réalisée reste un warning.

Le protocole du linter portable est lui aussi fermé : exits 0/1 avec un objet JSON contenant des
tableaux de chaînes `realized` et `errors`, ou exits publics 2/3 déjà diagnostiqués. JSON malformé,
racine non objet, tableaux mal typés et tout autre exit sortent en 2, jamais par traceback.

## Prérequis d'exécution

| Runtime | Rôle | Absent ⇒ |
|---|---|---|
| Python 3.10+ | démarre le runner | le gate ne démarre pas |
| Node.js 18+ | invoque `lint-core.mjs` | exit 2, message nommant Node — jamais 1 |

Le second n'est requis que si `targets` est non vide.
