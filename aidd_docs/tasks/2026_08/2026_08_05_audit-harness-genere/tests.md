# Codebase Audit: design:harness — le HTML généré (pilier tests)

Vingt-deux assertions `grep` sur un fichier dont la valeur est du JavaScript : un harness dont tous les scripts sont morts passe ALL GREEN, exit 0.

- **Date**: 2026_08_05
- **Scope**: `plugins/design/tools/harness-selftest.sh`, `tools/eval/design-harness.mjs`, `plugins/design/skills/harness/evals/scenarios.json`
- **Health**: fair
- **Findings**: 1 critical, 2 warning, 1 minor

Health: `good` = no critical findings; `fair` = critical findings exist but are isolated and addressable; `poor` = systemic or widespread critical findings.

## Findings

| Sev | Category | Location | Issue | Suggested fix | Effort |
| --- | -------- | -------- | ----- | ------------- | ------ |
| 🔴 | tests | `plugins/design/tools/harness-selftest.sh:66-169` | Les 22 assertions sont des `grep` sur le texte du fichier ; **rien n'exécute jamais le JavaScript généré**. Or le fichier n'est vendu que pour ça : `window.setPage(key)` / `window.setViewport(mode)` (docstring `harness.py:5-7`, `harness-contract.md`). Contre-épreuve : une copie du générateur avec une accolade non fermée injectée dans `setViewport` → `bash tools/harness-selftest.sh` rend **ALL GREEN, exit 0**, et le `dead.html` produit donne au navigateur `typeof setPage === "undefined"`, `typeof setViewport === "undefined"`, `#page-container.innerHTML.length === 0`. Le fichier mort au vert que la passe de durcissement du 05/08 déclare avoir supprimé est toujours atteignable — la garde ajoutée porte sur les sentinelles et le code de sortie, pas sur l'exécutabilité. | Une assertion de chargement après génération : soit `node --check` sur les corps de script extraits (bon marché, attrape la syntaxe, rien d'autre), soit — mieux — un chargement headless assertant `typeof window.setPage === "function"`, `setViewport('mobile')` pose la classe sur `#preview-frame`, et `#page-container` non vide. La seconde forme fermerait aussi le 🔴 de `ui.md` (largeur de contenu du cadre) et le 🟡 de `security.md` (clé `#constructor`). | M |
| 🟡 | tests | `plugins/design/adapters/harness/harness.py:245` ↔ `plugins/design/adapters/measure/measure.py:195` | L'accord documenté en `references/harness-contract.md:53` — l'oracle attend 400 ms parce que le cadre transite `max-width` en `.4s` — n'est asserté **nulle part**. Porter la CSS à `1s` laisse tout au vert et fait lire à chaque mesure device une largeur en cours de transition : des écarts de fidélité aléatoires, imputés à l'implémentation. Deux constantes couplées par un commentaire, dans deux fichiers, dans deux langages. | Asserter la chaîne `.4s` dans la CSS générée côté selftest, et faire dériver l'attente de `measure.py` de la valeur lue (ou asserter l'égalité des deux). | S |
| 🟡 | tests | `plugins/design/skills/harness/evals/scenarios.json` | 12 scénarios, tous sur le routage `--contract` / scaffold. **Zéro** sur `--pages`, `--pages-json`, ou un jeu de pages invalide — alors que ce sont les six branches exit-2 que le selftest couvre au niveau programme et le mode d'emploi principal de la skill. Rien ne vérifie que « fais-moi une maquette 3 pages accueil/à-propos/contact » route vers `--pages` avec les bonnes clés. La couverture est inversée : l'option opt-in est testée, le chemin par défaut ne l'est pas. | Ajouter 4-5 scénarios d'intention : pages nommées → `--pages` ; liste longue ou groupée → `--pages-json` ; clé en chemin d'URL (`/contact/`) → refus attendu ; doublon de clé → refus attendu. | S |
| 🟢 | tests | `tools/eval/design-harness.mjs:47` | `resolveBash()` retombe sur `'bash'` : sous Windows sans Git for Windows, c'est le bash WSL, qui rend 127 sans avoir lu le script. Le message affiché devient `harness-selftest.sh exit 127`, qui impute au selftest ce qui est un interpréteur absent — l'inverse de l'en-tête du fichier. Seul `r.error` (ENOENT) est traité à part. Reporté de `review.md` du 05/08, toujours ouvert. | Traiter `r.status === 127` comme `r.error` : nommer le bash résolu et rappeler `HARNESS_SELFTEST_BASH`. | S |

## Top actions

1. **Exécuter le fichier généré au moins une fois par run** (🔴). C'est le trou de couverture qui rend les trois autres piliers difficiles à garder corrigés : ni le bezel, ni la barre inatteignable, ni la clé `#constructor` ne peuvent être assertés tant qu'aucun test ne charge le document. Une fois le chargement en place, chaque *finding* de `ui.md` et `security.md` devient une assertion d'une ligne. Handoff : `test`.
2. **Lier les deux constantes de transition** (🟡 400 ms). Petit, mais c'est le seul couplage inter-fichiers du contrat d'oracle qui ne repose que sur un commentaire.
3. **Équilibrer les évals d'intention** (🟡 scenarios.json). Indépendant des deux premiers, se fait en parallèle.

## Coverage

- **Scanned**: tests — `harness-selftest.sh` intégralement (22 assertions relues une à une, plus la contre-épreuve du générateur régressé), la couverture des six branches exit-2 du chemin pages, `tools/eval/design-harness.mjs` (résolution de bash, propagation du code), `skills/harness/evals/scenarios.json` (12 scénarios, axes couverts).
- **Skipped**: aucun sous-domaine. Réserve : aucun outil de couverture (le selftest est du shell, il n'y a pas de métrique de couverture à produire) — le jugement porte sur ce que les assertions atteignent, pas sur un pourcentage. Les piliers `architecture`, `dependencies` et `performance` sont hors périmètre de ce run (4 piliers retenus sur 7), pas « skipped ».
