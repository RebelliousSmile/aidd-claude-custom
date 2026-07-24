# Decision: Éclatement du contrat design en quatre artefacts racinés par `release.json`

| Field   | Value |
|---------|-------|
| ID      | DEC-005 |
| Date    | 2026-07-24 |
| Feature | `design` 2.0.0 — contrat 1.x monolithique → quatre artefacts + racine |
| Status  | Accepted |

## Context

Jusqu'en 1.17.0, `components.json` portait quatre natures de données à la fois : l'anatomie des composants, les politiques transverses (`mode`, `$utilityPrefixes`, `usage`), les hints de mesure (`oracle`) et l'identité de version (`$version`). Trois conséquences observées :

- **Le mode se devinait.** `lint-core.mjs` inférait `utility-first` d'un jeu de composants vide. Un contrat non écrit rendait donc un run vert : un verdict sur rien.
- **La parité de versions était un invariant tenu à la main.** `$version` devait égaler le `version:` de la charte, sans qu'aucun outil ne le revérifie — un invariant que rien ne portait.
- **Un consommateur ne pouvait pas déclarer ce qu'il lit.** `config-gen.py` lisait `components.*.oracle`, `lint-core.mjs` lisait `components.*.base` ; aucune frontière ne disait qui dépend de quoi, donc toute écriture dans le manifeste risquait de casser l'autre lecteur.

## Decision

### 1 — Une donnée vit dans un seul artefact

| Artefact | Contenu | Lecteur nommé |
|---|---|---|
| `tokens.json` | valeurs (inchangé) | `lint-core.mjs`, adapters |
| `components.json` | anatomie seule | `lint-core.mjs` |
| `policies.json` | `mode`, `$utilityPrefixes`, `usage`, table des adapters | `lint-core.mjs` |
| `oracle.json` | cibles de mesure | `config-gen.py` |
| `release.json` | versions, empreintes, provenance, statut | racine du contrat |

`design-system.md` reste une **entrée** du contrat, pas un artefact : la charte est écrite par un humain, sa présence et sa version sont constatées dans `release.json`.

### 2 — `release.json` est la racine, et son absence est la signature d'un contrat 1.x

Il n'y a pas de double chemin de lecture. Un contrat sans `release.json` n'est pas parsé : il est diagnostiqué (exit 3, avec la commande de migration). Un format, un chemin, un diagnostic.

### 3 — L'invariant de parité de versions disparaît

`release.json` déclare une version par artefact et la version de la charte. Un écart devient une **donnée constatée**, plus une violation. Rien à tenir à la main, donc rien à oublier.

### 4 — Le mode est déclaré, jamais déduit

`policies.json § mode` est obligatoire. `lint-core.mjs` sort en 2 s'il est absent ; `migrate-contract.py` refuse de migrer sans lui et exige `--mode`. Un mode faux laisse les règles de vocabulaire inertes — c'est précisément la classe de bug que 1.x rendait silencieuse.

### 5 — Une seule implémentation du statut de maturité

`tools/status.py` détient l'échelle `extracted → normalized → validated → production-ready` et les quatre littéraux n'apparaissent nulle part ailleurs. `migrate-contract.py` et `02-freeze` l'appellent et recopient ce qu'il rend. Le statut est écrit dans `release.json` mais n'est opposable à rien à ce lot.

### 6 — La rupture est assumée et outillée

Le bump est **majeur** et le passage n'est pas rétrocompatible. La contrepartie est un outil : `tools/migrate-contract.py`, `--dry-run` par défaut dans la procédure, sauvegarde du contrat 1.x avant écriture, seconde exécution no-op, et un contrôle de non-régression — le linter 2.0 doit rendre le même verdict, fichier par fichier, qu'avant migration. Aucun champ n'est perdu : une clé hors table de redistribution est transportée telle quelle et signalée comme anomalie.

## Consequences

- Les contrats déjà figés doivent être migrés une fois ; sans migration, le gate ne tourne plus mais nomme le remède au lieu de casser.
- Écrire un contrat coûte trois fichiers au lieu d'un ; en échange chaque lecteur déclare son artefact et une écriture ne peut plus casser un lecteur voisin par accident.
- `config-gen.py` accepte `--oracle` et retombe sur le frère `oracle.json` de `--components` : les invocations existantes continuent de fonctionner une fois le contrat migré.

## Relation à DEC-002

La frontière WHAT/HOW de `002-design-funnel-hybrid-pivot.md` est **inchangée**. L'éclatement redistribue des données à l'intérieur du WHAT ; il ne déplace aucune décision vers le HOW, n'ajoute aucun pivot `sc-*` et ne modifie aucune règle de délégation. Les artefacts restent agnostiques de la stack ; la table des adapters nomme des rôles de consommateur, jamais des plateformes.

## Alternatives rejetées

- **Garder le monolithe et ajouter un `release.json` à côté.** Le mode aurait continué d'être deviné et la parité de versions serait restée un invariant tenu à la main. La racine seule ne réglait aucun des trois problèmes.
- **Double chemin de lecture 1.x + 2.0 dans le linter.** Deux chemins veulent dire deux comportements à maintenir et une migration jamais faite. Le refus outillé force la conversion une fois, puis n'a plus de coût.
- **Migration implicite au premier lint.** Une écriture silencieuse d'un contrat figé, déclenchée par une commande de lecture, est exactement ce qu'un gate ne doit pas faire.
