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

- Chemin nu : le rapport est lu tel qu'il est sur le disque. Rien ne garantit qu'il décrit le code actuel.
- Objet avec `command` : le runner relance le réalisateur natif depuis le répertoire de la configuration, puis lit le rapport. Le code de sortie de la commande est ignoré — « des violations existent » est déjà dans le rapport, et le lire est ce qui décide. Un binaire introuvable sort en 2 en le nommant.

`command` est une liste d'arguments, jamais une ligne de shell : pas de shell, donc pas de règle de quoting à rater.

```json
{
  "realizer": "<nom du linter natif installé>",
  "rules": [
    { "id": "<rule-id>", "status": "pass", "violations": [] }
  ]
}
```

- `id` reprend verbatim le `usage.rules[].id` du contrat — c'est la clé d'appariement. Une entrée sans `id` fait sortir en 2.
- `status` ∈ `pass` · `fail` · `unrealized`.
- `fail` ⇒ chaque entrée de `violations` compte comme une violation du gate ; liste vide ⇒ l'`id` fait office de message.
- `unrealized` ⇒ le réalisateur a reçu la règle et déclare ne pas l'avoir réalisée. Listée non réalisée en nommant qui le déclare ; l'effet dépend de la priorité contractuelle.
- Une règle non couverte par un rapport reste **non réalisée** elle aussi, mais sans auteur : le rapport ne peut pas distinguer « pas encore lancé » de « hors de portée ». C'est ce que `unrealized` supprime (`references/enforcement-registry.md § Marqueur non réalisé`).

La priorité vient du contrat, jamais du rapport : `usage.rules[].priority` vaut `P0`, `P1` ou `P2` et vaut `P1` par défaut. Une règle P0/P1 non réalisée est une preuve manquante bloquante. Une règle P2 en échec ou non réalisée reste un warning.

## Prérequis d'exécution

| Runtime | Rôle | Absent ⇒ |
|---|---|---|
| Python 3.10+ | démarre le runner | le gate ne démarre pas |
| Node.js 18+ | invoque `lint-core.mjs` | exit 2, message nommant Node — jamais 1 |

Le second n'est requis que si `targets` est non vide.
