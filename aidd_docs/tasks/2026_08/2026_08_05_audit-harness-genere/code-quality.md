# Codebase Audit: design:harness — le HTML généré (pilier code-quality)

Deux des trois langages du générateur vivent dans une chaîne Python qu'aucun outil ne lit, et les largeurs d'échantillon device sont redéclarées à huit endroits — toutes fausses aujourd'hui.

- **Date**: 2026_08_05
- **Scope**: `plugins/design/adapters/harness/harness.py` (643 lignes) et ses déclarations miroir dans la doc et l'oracle
- **Health**: good
- **Findings**: 0 critical, 2 warning, 3 minor

Health: `good` = no critical findings; `fair` = critical findings exist but are isolated and addressable; `poor` = systemic or widespread critical findings.

## Findings

| Sev | Category | Location | Issue | Suggested fix | Effort |
| --- | -------- | -------- | ----- | ------------- | ------ |
| 🟡 | code-quality | `plugins/design/adapters/harness/harness.py:247-248` | Les largeurs d'échantillon device sont redéclarées **huit fois**, sans qu'aucune assertion ne les lie : la CSS (l. 247-248, seule faisant autorité), trois commentaires (l. 249, 264, 307), la carte de fenêtres de l'oracle (`adapters/measure/config-gen.py:63-64`), la skill (`skills/harness/SKILL.md:46` et `:145`) et la référence (`references/harness-contract.md:49`). Le 🔴 de `ui.md` en est la démonstration : la boîte de contenu vaut 814 / 374, donc **les huit déclarations sont fausses en même temps**, et aucune ne peut le dire. | Une constante unique côté Python injectée dans la CSS générée, une assertion selftest qui compare la valeur trouvée dans la sortie à cette constante (et, idéalement, à la largeur de contenu mesurée), la doc citant la constante au lieu de la recopier. | M |
| 🟡 | code-quality | `plugins/design/adapters/harness/harness.py:201-450` | `TEMPLATE` est une chaîne brute de 250 lignes contenant du HTML, ~60 lignes de CSS et ~80 lignes de JavaScript. Aucun linter, formateur ou parseur ne voit les deux derniers : ni coloration, ni `node --check`, ni parseur CSS, ni règle de style. La conséquence est mesurée dans `tests.md` (🔴) — un JS syntaxiquement mort traverse toute la chaîne au vert. C'est aussi ce qui rend le duplicat `keyToFn` ci-dessous indétectable. | Extraire le JS (et la CSS) en fichiers voisins lus à la génération — `adapters/harness/template/{chrome.css,control.js}` — inlinés dans le document produit. Le fichier gagne un parseur pour chaque langage sans changer la sortie d'un octet, ce qui rend le refactor vérifiable par comparaison binaire. | M |
| 🟢 | code-quality | `plugins/design/adapters/harness/harness.py:379-382` | `keyToFn` (JS) duplique `key_to_fn` (Python, l. 65-68) sans qu'aucune assertion ne les lie. Le nom cité dans le bloc d'erreur (l. 386) vient de la copie JS, celui réellement déclaré vient de la copie Python : une divergence n'échoue pas, elle désigne une fonction inexistante à qui doit la corriger. Reporté de `review.md` du 05/08, toujours ouvert. | Assertion selftest sur une clé composée : le nom cité par `errorBlock` doit être celui déclaré. Ou dériver le JS depuis Python à la génération. | S |
| 🟢 | code-quality | `plugins/design/adapters/harness/harness.py:151-153` | La docstring de `js_literal` annonce « quotes, backslashes and newlines all covered » ; `json.dumps` ne neutralise ni `</script>` ni U+2028/U+2029. Reporté de `review.md`, et **désormais atteignable** : `security.md` 🟢 mesure une clé de page portant un U+2028 brut jusque dans le littéral JS émis. C'est la promesse qui est fausse. | Neutraliser dans la fonction, ou énoncer la précondition d'échappement amont dans la docstring. | S |
| 🟢 | code-quality | `plugins/design/adapters/harness/harness.py:154` | Une seule ligne vide entre `js_literal` et `build_options` ; le reste du fichier sépare ses définitions de premier niveau par deux (PEP 8). Reporté de `review.md`, toujours ouvert. | Ajouter la ligne vide. | S |

## Top actions

1. **Une seule source pour les largeurs device** (🟡). C'est la condition pour que le correctif du bezel (`ui.md` 🔴) reste vrai : sans constante unique ni assertion, la prochaine modification du cadre redivergera en silence, exactement comme aujourd'hui.
2. **Sortir le JS et la CSS de la chaîne Python** (🟡). Habilitant, pas cosmétique : c'est ce qui rend possible l'assertion de `tests.md` 🔴 sans machinerie d'extraction ad hoc. Refactor à sortie identique — se vérifie par diff binaire du fichier généré avant/après.
3. **Solder les trois 🟢 reportés de `review.md`** (`keyToFn`, docstring `js_literal`, PEP 8). Un seul passage, effort S cumulé ; le second cesse d'être théorique depuis la mesure U+2028.

## Coverage

- **Scanned**: code-quality — lisibilité et nommage, duplication (Python ↔ JS, et les huit déclarations de largeur), taille de fichier et de fonctions (643 lignes dont 250 de template ; aucune fonction au-delà de ~50 lignes, `resolve_tokens_style` étant la plus longue à 60 et restant linéaire), gestion d'erreur (l'espace 0/2/3 est tenu, chaque chemin de lecture nomme le fichier et la cause), code mort (aucun), complexité (aucune branche imbriquée au-delà de 3).
- **Skipped**: aucun sous-domaine. Réserve : aucun linter Python configuré dans le dépôt (pas de ruff/flake8) — la revue est manuelle, donc les nits de style relevés ne prétendent pas être exhaustifs. Les piliers `architecture`, `dependencies` et `performance` sont hors périmètre de ce run (4 piliers retenus sur 7), pas « skipped ».
