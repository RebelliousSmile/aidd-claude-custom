# Codebase Audit: `design:harness` — tests

La seule preuve exécutable du harness n'est branchée sur rien, et elle ne regarde que le chemin `--contract` : aucun des huit défauts trouvés par ailleurs dans cette exécution ne pouvait être vu par la suite existante.

- **Date**: 2026-08-05
- **Scope**: `plugins/design/tools/harness-selftest.sh`, `plugins/design/skills/harness/evals/scenarios.json`, `package.json § scripts.test`, `tools/eval/*`
- **Health**: poor
- **Findings**: 2 critical, 2 warning, 1 minor

## Findings

| Sev | Category | Location                                                | Issue                                                                                                                                                                                                                                        | Suggested fix                                                                                                                                              | Effort |
| --- | -------- | ------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ |
| 🔴  | tests    | `package.json:7`                                        | `pnpm test` enchaîne cinq scripts `tools/eval/*` ; **aucun n'appelle `tools/harness-selftest.sh`**. Grep sur tout le dépôt : les seules mentions sont dans le plan de juillet, le CHANGELOG et une mémoire — jamais dans un runner. La preuve a été écrite le 2026-07-25, elle n'a plus jamais été rejouée automatiquement | Ajouter un maillon au `test` du marketplace (ou un `tools/eval/design-harness.mjs` qui shell out sur le `.sh`), pour que la régression du générateur casse le vert | S      |
| 🔴  | tests    | `plugins/design/tools/harness-selftest.sh:40-56`        | Le selftest n'asserte **rien sur le HTML produit** hors deux chaînes : la bannière `GENERATED from tokens.json` et l'absence de `@media`. Ni `h1`, ni nom accessible, ni unicité des fonctions, ni échappement, ni fonctionnement de `setPage`/`setViewport` — c'est-à-dire aucun des huit défauts relevés dans `ui.md` et `code-quality.md` | Un contrôle de la sortie générée : compter les `h1`, asserter l'unicité des `function page…`, asserter qu'aucune valeur d'entrée ne ressort non échappée         | M      |
| 🟡  | tests    | `plugins/design/tools/harness-selftest.sh:17-37`        | La fonction `check` asserte que le code obtenu **égale** le code attendu, mais rien n'asserte que **1 ne sort jamais**, alors que c'est l'interdit explicite de `references/harness-contract.md:26`. Le défaut 🔴 de `code-quality.md` (`--pages-json` → exit 1) passe précisément par ce trou : le selftest ne teste que des invocations valides ou volontairement cassées **côté contrat**, jamais côté `--pages*` | Ajouter les cas d'entrée malformée (`--pages-json` illisible, mal formé, `--pages` vide) et un garde générique « aucun run ne rend 1 »                          | S      |
| 🟡  | tests    | `plugins/design/skills/harness/evals/scenarios.json:2-10` | Les 9 scénarios couvrent le routage d'intention (`scaffold`, `contract-inline`, `exit-3-migrate`, `exit-2-generate`, `scaffold-warn`) — donc l'axe `--contract` seul. **Zéro scénario** sur `--pages` / `--pages-json`, qui est pourtant l'entrée nominale du scaffold, ni sur `--out` (chemin non inscriptible, écrasement) | Trois scénarios de plus : pages passées en JSON, jeu de pages invalide, remplissage d'un harness existant                                                       | S      |
| 🟢  | tests    | `plugins/design/adapters/harness/harness.py:151` ↔ `plugins/design/adapters/measure/measure.py:195` | Couplage temporel non déclaré : le cadre a `transition: max-width .4s` et l'oracle attend exactement `wait_for_timeout(400)`. `references/harness-contract.md` documente l'accord sur les **viewports** (`:34`) mais pas celui-ci. Mesuré : à t=400 ms la largeur mobile est déjà stabilisée à 390 px — pas de défaut observé, mais marge nulle et personne ne saurait qu'allonger la transition casse l'oracle | Déclarer le couplage dans `harness-contract.md` à côté de celui des viewports ; ou faire attendre `transitionend` plutôt qu'une constante                        | S      |

### Reproduction

```bash
# 🔴 le selftest n'est branché nulle part
grep -rn "harness-selftest" --include="*.mjs" --include="*.json" --include="*.yml" .
#   (aucun résultat hors aidd_docs/ et CHANGELOG.md)
cat package.json | grep '"test"'
#   "test": "node tools/eval/consistency.mjs && node tools/eval/harness.mjs
#            && node tools/eval/coverage.mjs && node tools/eval/pivot-map.mjs
#            && node tools/eval/selftest.mjs"
#   ⚠ tools/eval/harness.mjs est le harness d'évaluation du marketplace,
#     homonyme et sans rapport avec design:harness.

# 🟡 le trou par lequel passe l'exit 1
cd plugins/design && bash tools/harness-selftest.sh   # → ALL GREEN
echo 'x' > /tmp/bad.json
python adapters/harness/harness.py --out o.html --pages-json /tmp/bad.json ; echo $?   # → 1
```

**L'homonymie mérite d'être notée** : `tools/eval/harness.mjs` (racine du marketplace) et `design:harness` n'ont rien en commun. Lire la ligne `test` du `package.json` donne l'impression que le harness est couvert. Il ne l'est pas.

## Top actions

1. **Brancher `harness-selftest.sh` sur `pnpm test`** (résout le 🔴 de branchement). C'est le geste le moins cher du lot et il conditionne tous les autres : sans lui, chaque assertion ajoutée reste dormante. Handoff : `aidd-dev:03-act`.
2. **Étendre le selftest à la sortie générée et à l'espace des codes** (résout le 🔴 de portée et le 🟡 de contrôle négatif). Une passe sur le HTML — `grep -c '<h1'`, unicité des `function page…`, absence de `<b>` hors contenu — plus un garde « jamais 1 » sur toutes les branches, y compris les entrées `--pages*` malformées. C'est le motif du chantier #14 : ici le vert n'atteste que le chemin contractuel.
3. **Compléter `scenarios.json` sur l'axe pages** (résout le 🟡 d'évaluation), pour que le routage d'intention couvre l'entrée nominale du scaffold et pas seulement l'option `--contract`.

## Coverage

- **Scanned**: ui, code-quality, tests
- **Skipped**:
  - **architecture** — le périmètre est un générateur stdlib de 460 lignes, sans dépendance interne ni couche : il n'y a ni ADR ni frontière à opposer. Un audit d'architecture n'aurait produit que des observations déjà couvertes par `code-quality`.
  - **security** — la sortie est un fichier HTML local ouvert par son propre auteur, dont toutes les entrées viennent de la ligne de commande du même auteur. Les défauts d'échappement relevés dans `code-quality.md` sont des défauts de **correction**, pas des vecteurs : il n'existe ni entrée non fiable ni surface réseau. Les qualifier de sécurité serait un faux positif.
  - **dependencies** — `harness.py` est stdlib Python uniquement (`argparse`, `json`, `sys`, `pathlib`), et le HTML produit ne charge aucun script. Aucune surface de CVE, de licence ni de chaîne d'approvisionnement. Seule exception notée, et traitée sous `ui` : deux `preconnect` vers Google Fonts que rien n'utilise.
  - **performance** — la génération est une substitution de chaînes sur un template constant, le rendu est un fichier statique de 11 666 octets (scaffold à 2 pages) sans requête. Le seul point mesurable est le couplage `transition .4s` ↔ `wait 400 ms`, reporté ci-dessus sous `tests` parce que ce qui est en cause est la fiabilité de la mesure, pas la vitesse.
