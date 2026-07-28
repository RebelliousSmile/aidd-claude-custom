# Statut de maturité

Un contrat figé porte un **statut** dans `release.json § status`. Ce statut est **calculé**, jamais écrit à la main : `tools/status.py` est la seule implémentation (`contract-schema.md § Statut de maturité`). Il conditionne ce que l'entonnoir a le droit d'affirmer sur le contrat.

## L'échelle

Quatre barreaux. La première condition non tenue arrête la montée : l'échelle **plafonne**, elle ne saute pas de barreau. Chaque barreau **exige** une condition et **autorise** un usage.

| Statut | Exige | Autorise |
|---|---|---|
| `extracted` | les trois artefacts requis existent et se parsent | la génération des dérivés (`tools/generate.py`) ; rien du côté conformité |
| `normalized` | + charte présente | rien qu'un outil sanctionne : un contrat observé, jamais vérifié. **Un contrat migré entre ici** |
| `validated` | + vérifications enregistrées (`checks` non nul) | l'**invocation de la conformité** par `enforce` et `diffuse` |
| `production-ready` | + contraste vert sur chaque paire **et** états déclaratifs complets sur chaque composant, sans gap plafonnant | atteste en plus que les deux contrôles a11y calculables sont verts — ce que `validated` n'affirme pas |

« Contraste vert sur chaque paire » se lit sur un **nombre de paires non nul** : sur zéro paire la condition serait vraie sans rien affirmer. Un contrat où aucune paire ne peut être construite ne se fige plus (`adjust/references/manifest-schema.md § Invariant 7`) ; s'il l'a été sous dérogation, le gap `contrast-unpaired` le maintient à `normalized`, et un contrat figé avant cette règle porte la même ambiguïté jusqu'à son prochain figeage.

Les deux contrôles a11y calculables au figeage — contraste par thème depuis les valeurs de tokens résolues, présence déclarative des états `disabled`/`error`/`focus` — sont enregistrés dans `checks` et lus par `status.py`. Ce qui n'est pas calculable au figeage (rôles, attributs) reste **assigné à un pivot** et ne pèse pas sur le statut (`enforcement-registry.md`).

## Le seuil

**La conformité ne peut être invoquée qu'à partir de `validated`.** En dessous, `enforce` et `diffuse` ne l'affirment pas : le gate continue de tourner et de bloquer les vraies violations, mais le vocabulaire de conformité est suspendu. `run-gates.py` sort alors en **4** (`master § Exit-code space`) — ni conformité ni silence : les violations restent listées, et le message nomme le chemin pour remonter le contrat.

Ce seuil a **une seule source exécutable** — la constante `THRESHOLD` de `tools/status.py`, que `run-gates.py` importe — et **une seule source humaine** — ce document. Aucun autre fichier ne réécrit le littéral.

### Remonter un contrat

Un contrat sous le seuil se remonte en tenant la condition manquante, puis en re-figeant (`adjust/02-freeze.md`) :

- sous `normalized` : ajouter la charte prose (`design-system.md`).
- sous `validated` : jouer les vérifications au figeage (le contraste et le contrôle d'états s'enregistrent dans `checks`).

## Comment un gap plafonne le statut

Un gap connu ne vit plus comme question ouverte en prose : il est **enregistré** dans `release.json § gaps` et **plafonne** le statut au barreau qu'il nomme. Le même jeu de gaps enregistrés donne toujours le même statut — le plafond est une donnée, pas un jugement.

`status.py` calcule la montée par les conditions, puis applique `min(barreau atteint, plus bas plafond des gaps)`.

| Classe de gap | Enregistrée par | Plafonne à |
|---|---|---|
| charte absente | `gaps[]` de classe `charter-absent` (et `charter.present: false`) | `extracted` |
| contraste jamais calculé | `checks: null` | `normalized` |
| contraste calculé sans aucune paire à comparer, sous dérogation enregistrée | `gaps[]` de classe `contrast-unpaired` | `normalized` |
| une paire de contraste échoue | `gaps[]` de classe `contrast` | `validated` |
| un état déclaratif manquant sur un composant | `gaps[]` de classe `states` | `validated` |

Un gap `contrast` ou `states` empêche d'atteindre `production-ready` sans faire retomber sous `validated` : `min` ne descend jamais en dessous du barreau que les conditions tiennent déjà.
