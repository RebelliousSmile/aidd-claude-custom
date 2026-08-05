# Review: design-harness-durcissement

- **Verdict**: approve
- **Diff**: `0ebb248...18678d5`
- **Axes run**: code
- **Date**: 2026_08_05
- **Findings**: 0 critical, 3 warning (corrigés en 2.9.1), 4 minor

## Phases

Not run — axe fonctionnel non demandé.

## Findings

| Sev | Kind | Phase | Location | Issue | Fix |
| --- | ---- | ----- | -------- | ----- | --- |
| 🟡 | code | 2 | `plugins/design/adapters/harness/harness.py:438` | Le `try` ajouté dans `init()` commence **après** l'appel qui jette. `decodeURIComponent` (l. 435) lève `URIError` sur un fragment mal formé (`#%E0%A4%A`) : l'IIFE avorte, `setViewport('desktop')` et `render()` ne tournent jamais, et `#page-container` (l. 341) est vide dans le template → page blanche sans bloc d'erreur. Exactement l'état que la phase 2 supprime ailleurs. `window.setPage` étant assigné l. 426 avant `init()`, l'oracle s'en tire ; un humain qui ouvre le lien, non. | **Corrigé (2.9.1)** — décodage déplacé dans le `try` (`harness.py:441`). Mesuré au navigateur sur `#%E0%A4%A` : avant `innerHTML.length: 0` et `preview-frame` sans classe, après `152` / `h1 = "Page 1"` / `preview-frame mobile`. Assertion selftest sur la ligne qui précède le décodage, contre-épreuve faite. |
| 🟡 | code | 1 | `plugins/design/adapters/harness/harness.py:536-551` | `substitute()` laisse littérale toute sentinelle absente de `values` (`if name not in values: return match.group(0)`). La protection visée — une valeur utilisateur contenant `%%PAGE_OPTIONS%%` n'est pas re-balayée — n'exige pas ce silence côté **template** : une clé oubliée ou mal orthographiée expédie `%%FOO%%` dans le HTML à exit 0. Même classe que le défaut que la phase 1 corrige (« ce qui a laissé un fichier mort passer au vert »). Latent aujourd'hui : les 10 sentinelles du template sont couvertes, rien ne le garde. | **Corrigé (2.9.1)** — `missing_sentinels()` (`harness.py:536`) comparé aux clés avant écriture, `_fail` → 2. Mesuré sur une copie où `PAGE_REGISTRY` est mal orthographiée : exit 2, message nommant `%%PAGE_REGISTRY%%`, aucun fichier écrit. `grep -q "%%"` sur les sorties scaffold et couplée au selftest. |
| 🟡 | code | 3 | `plugins/design/tools/harness-selftest.sh:22` | `python` en dur, sur une ligne réécrite par la phase 3 et désormais dans le chemin de `pnpm test`. Ubuntu 22+ n'expose que `python3` : le selftest y rend 127 sur chaque `check`, rapporté comme « exit 127, expected 0 » — un défaut d'interpréteur déguisé en échec d'assertion. Le script s'astreint par ailleurs au POSIX sh strict, et `design-harness.mjs` rend `'bash'` hors Windows : le support non-Windows est revendiqué. | **Corrigé (2.9.1)** — résolution `HARNESS_SELFTEST_PYTHON` → `python3` → `python` (`harness-selftest.sh:20-31`), override vérifié utilisable, 10 appels passés en `"$PY"`. Mesuré avec `HARNESS_SELFTEST_PYTHON=/nope/python` : arrêt immédiat, message nommant l'interpréteur, exit 1, au lieu de quatorze faux échecs. |
| 🟢 | code | 3 | `tools/eval/design-harness.mjs:47` | `resolveBash()` retombe sur `'bash'` : sous Windows sans Git for Windows, c'est le bash WSL, qui rend 127 sans avoir lu le script. Le message affiché est alors `harness-selftest.sh exit 127`, qui impute au selftest ce qui est un interpréteur absent — l'inverse de l'en-tête du fichier (« bash introuvable est un ÉCHEC, jamais un skip silencieux »). Seul `r.error` (ENOENT) est traité à part. | Traiter `r.status === 127` comme `r.error` : nommer le bash résolu et rappeler `HARNESS_SELFTEST_BASH`. |
| 🟢 | code | 2 | `plugins/design/adapters/harness/harness.py:379-382` | `keyToFn` en JS duplique `key_to_fn` en Python (l. 65-68) sans qu'aucune assertion ne les lie. Le nom cité dans le bloc d'erreur (l. 386) et celui réellement déclaré par `build_functions` viennent de deux implémentations : une divergence n'échoue pas, elle désigne une fonction inexistante à qui doit la corriger. | Assertion selftest : générer une page à clé composée, vérifier que le nom cité par `errorBlock` est celui déclaré — ou dériver le JS depuis Python à la génération. |
| 🟢 | code | 1 | `plugins/design/adapters/harness/harness.py:151-153` | La docstring de `js_literal` annonce « quotes, backslashes and newlines all covered » ; `json.dumps` ne neutralise ni `</script>` ni U+2028/U+2029. Non atteignable aujourd'hui (les clés sont validées identifiants, les libellés passent par `html.escape` l. 185) — c'est la promesse qui est fausse, pas le comportement. | `.replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")`, ou une docstring qui énonce la précondition d'échappement amont. |
| 🟢 | code | 1 | `plugins/design/adapters/harness/harness.py:154` | Une seule ligne vide entre `js_literal` et `build_options` ; le reste du fichier sépare ses définitions de premier niveau par deux (PEP 8). | Ajouter la ligne vide. |

## Verification

Not run — axe fonctionnel non demandé.
