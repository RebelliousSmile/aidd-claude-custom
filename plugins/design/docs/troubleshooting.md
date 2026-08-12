# Diagnostic

Les outils du plugin communiquent par **codes de sortie**, pas par messages à interpréter. Cette page dit ce que chaque code signifie et quelle est la correction attendue.

## Table des codes

Un même code a le même sens dans tous les outils du plugin.

| Code | Sens | Correction |
|---|---|---|
| `0` | conforme | — |
| `1` | violations réelles, ou dérive d'un artefact généré | corriger le markup, ou régénérer depuis la source |
| `2` | invocation invalide, ou artefact déclaré mais absent/illisible | corriger l'appel ou le contrat — ce n'est pas un verdict sur le code |
| `3` | contrat au format 1.x | migrer : invoquer `design:adjust`, action `03-migrate` |
| `4` | contrat sous le seuil de maturité | remonter le statut (voir plus bas) |

Répartition par outil :

| Outil | Codes possibles |
|---|---|
| `lint-core.mjs` | 0 · 1 · 2 · 3 |
| `tools/run-gates.py` | 0 · 1 · 2 · 3 · 4 |
| `tools/generate.py` | 0 · 1 · 2 · 3 |
| `adapters/harness/harness.py` | 0 · 2 · 3 — **jamais 1, jamais 4** |

`run-gates.py` est le **seul point d'appel du gate**, aux trois sites : local, pre-commit, CI. C'est lui qui ajoute le 4 par-dessus le verdict du linter.

---

## Exit 4 — « conformité non affirmée »

Le symptôme qui surprend le plus : **aucune violation listée, et le gate sort quand même en rouge**.

Ce n'est pas un bug. Le contrat n'a pas atteint le seuil `validated`, donc le runner refuse d'affirmer une conformité qu'il ne peut pas établir. Les violations, s'il y en a, restent listées — le 4 s'ajoute au verdict, il ne le masque pas.

**Que faire** : lire le statut courant et ce qui le plafonne.

```bash
python design/lint/status.py --contract design/
```

Quatre causes, par ordre de fréquence :

| Statut bloqué à | Cause | Correction |
|---|---|---|
| `extracted` | `design-system.md` absent | écrire la charte, la déclarer dans `release.json` |
| `normalized` | aucune vérification enregistrée dans `checks` | jouer les vérifications, les enregistrer |
| `normalized` | contraste jamais calculé | `adapters/a11y/contrast.py` au figeage |
| `normalized` | contraste calculé sur **zéro paire**, figé sous dérogation (gap `contrast-unpaired`) | déclarer les `.foregrounds` des composants qui portent du texte, puis re-figer |

La dernière mérite d'être lue deux fois : `checks.contrast.allPass` peut y valoir `true` sans qu'aucune couleur n'ait été comparée. C'est pourquoi `status.py` lit `allPass` **avec** `pairs`, et pourquoi un contrat dans cet état ne se fige plus qu'en enregistrant explicitement la dérogation.

Un **gap** enregistré dans `release.json § gaps[]` plafonne le statut délibérément. Si le statut ne monte pas alors que les conditions semblent remplies, c'est un gap actif — il est là pour être vu, pas pour être contourné.

**Cas particulier du contrat migré** : une migration 1.x → 2.0 fait entrer le contrat à `normalized`, donc sous le seuil. C'est intentionnel — aucun droit acquis n'est hérité de l'ancien format. Il faut enregistrer les vérifications pour franchir le seuil.

---

## Exit 3 — contrat 1.x

`design/tokens.json` et `design/components.json` existent, mais pas `design/release.json`. Le linter ne tente pas de deviner : il sort en 3 et nomme la migration.

```bash
python ${DESIGN_PLUGIN_ROOT}/tools/migrate-contract.py --contract design/
```

Ou, guidé : invoquer `design:adjust` puis l'action `03-migrate`. Elle vérifie en plus la
**non-régression du verdict** — le contrat migré doit rendre le même jugement que l'ancien sur le
même markup.

Un re-figeage ordinaire **ne fait pas** la conversion au passage : il faut migrer d'abord.

---

## Exit 2 — ce n'est pas un verdict sur ton code

Le 2 dit « je ne peux pas juger », jamais « c'est faux ». Causes réelles :

**Un artefact déclaré par `release.json` est absent ou illisible.** Le contrat se contredit lui-même.

**Les trois artefacts requis ne sont pas tous déclarés.** Un `release.json` qui ne déclare pas `tokens.json`, `components.json` *et* `policies.json` n'est pas un contrat plus petit : c'est une règle désactivée. Le linter préfère sortir en 2 plutôt que rendre un vert sur rien.

**`policies.json § mode` est absent.** Le mode (`bem` ou `utility-first`) détermine sur quoi porte le vocabulaire. Il est toujours déclaré explicitement — le linter ne le déduit pas.

**Le contrat n'a pas pu être résolu.** Passe-le explicitement :

```bash
node design/lint/lint-core.mjs --contract design/ <fichiers>
```

Deviné, le contrat n'est retenu que s'il est le seul de son arbre. S'il y en a plusieurs, l'outil sort en 2 plutôt que d'en choisir un au hasard.

---

## Exit 1 sur `generate.py --check` — dérive

Un artefact dérivé ne correspond plus à l'empreinte gravée dans `release.json § generated`. Deux causes, même code :

- **une retouche manuelle** d'un fichier généré ;
- **une source modifiée** sans régénération.

```bash
python ${DESIGN_PLUGIN_ROOT}/tools/generate.py --contract design/
```

**Aucun drapeau ne neutralise cet échec.** C'est délibéré : la correction est toujours la source, jamais l'artefact. Si le fichier généré ne te convient pas, ce qui doit changer est l'entrée de `policies.json § adapters[]` ou le token en amont.

`diffuse` refuse de rendre tant que `--check` ne sort pas en 0 — un rendu bâti sur des dérivés périmés produirait du markup conforme à un contrat qui n'existe plus.

---

## Le lint est vert mais le rendu est faux

C'est le cas normal, pas une anomalie — et c'est la raison d'être du second gate.

`lint-core.mjs` vérifie le **vocabulaire** : le markup scanné n'utilise ni classe ni token hors contrat. Il ne mesure rien du rendu. Un fichier peut n'employer que des tokens légitimes et ne ressembler en rien à la maquette.

La fidélité relève de `enforce/05-fidelity-gate` et de l'oracle `measure.py`, qui mesure les styles calculés par breakpoint contre `oracle.json`.

Hors périmètre du gate vocabulaire **par construction** — donc jamais couvert par son vert :

- les feuilles de style, les configurations de plateforme, les scripts de build ;
- les liaisons de classe dynamiques (`:class`, `{expr}`, classes assemblées à l'exécution) ;
- le contenu stocké hors fichiers source, sauf extraction explicite par `03-lint-instances` ;
- les rôles ARIA, le fond réellement appliqué, le contraste **du rendu** (le contraste des paires déclarées, lui, est mesuré bien plus tôt — au figeage, par `adapters/a11y/contrast.py`) ;
- toute cohérence entre deux fichiers.

Énoncé complet de ce que chaque gate établit : [`../references/gate-natures.md`](../references/gate-natures.md).

---

## Une règle apparaît « non réalisée »

Le rapport du gate liste une règle sans verdict. C'est attendu quand aucun pivot `sc-<langage>` n'est installé pour le langage concerné.

Une règle non réalisée **n'est ni une violation ni une conformité** — le code de sortie est inchangé. Le rapport la nomme plutôt que de laisser croire qu'elle a été vérifiée.

Pour la réaliser : installer le `sc-<langage>` correspondant, qui porte la skill `design-bridge`. Le routage se fait sur le type d'enforcement de la règle ([`../references/enforcement-registry.md`](../references/enforcement-registry.md)), jamais sur le nom de la plateforme.

---

## `diffuse` refuse de livrer

Trois refus distincts, dans cet ordre :

1. **`generate.py --check` ≠ 0** — dérive d'un artefact dérivé. Régénérer.
2. **`lint-core.mjs` = 1** — le rendu produit des violations. `02-render` corrige et re-linte avant de livrer ; le gate n'est pas négociable.
3. **Aucun pivot détecté** — ce n'est pas un refus : le rendu baseline HTML/CSS est produit, mais c'est une **preview non intégrée**. Le lint valide son vocabulaire, il ne prouve pas qu'elle est branchée dans l'application. Le hand-off vers l'intégration est une obligation de livraison additionnelle, pas un relâchement du gate.

---

## Après un re-figeage, tout est rouge

Attendu. `adjust` a bumpé la version, donc les règles du linter dérivées de l'ancien contrat sont périmées.

Invoquer `design:enforce` dans l'hôte courant.

Re-jouer `enforce` re-dérive les règles depuis le nouveau contrat. La boucle *corriger → propager → re-linter* de `03-lint-instances` est l'outil de réconciliation prévu pour ça — c'est la classe de cas [`contract-drift`](workflow.md#contract-drift--les-instances-ont-divergé).

---

## Voir aussi

- [`concepts.md`](concepts.md) — pourquoi les gates sont bornés comme ils le sont
- [`workflow.md`](workflow.md) — la séquence adaptée à ta situation
- [`../references/maturity-status.md`](../references/maturity-status.md) — la table complète des statuts et du seuil
