---
status: done
---

# Phase 2: wireframes-analyze.py — signaux d'inventaire enrichis

## Architecture projection

```
plugins/design/
├── tools/
│   ├── wireframes-analyze.py                        ✏️ (InventoryParser : groupement structurel + risque annotation)
│   └── wireframes-selftest.sh                        ✏️ (nouvelles assertions)
├── adapters/wireframes/fixtures/
│   ├── normalize-tabbed.html                          ✅ (nouveau, sections togglées structurellement similaires)
│   └── normalize-annotation-heavy.html                ✏️ (étendu : annotation citant hash/chemin de fichier)
└── references/
    └── wireframe-normalization.md                     ✏️ (note : signaux avancés, non autoritaires)
```

## Tasks to do

1. Dans `InventoryParser`, détecter les groupes de frères structurellement similaires (même balise, token de classe non générique partagé — exclure une liste d'arrêt type `container`/`wrapper`/`row`/`col`) au sein d'un même parent ; quand ≥2 frères partagent une signature et qu'un gestionnaire `classList.toggle/add/remove` ou `style.display` référence une classe/id du groupe, peupler `inventory.unitCandidates` avec une empreinte structurelle en plus des candidats déjà déclarés par attribut.
2. Extraire les paires `(trigger, target)` des gestionnaires de bascule détectés quand les deux sélecteurs sont inférables du script inline ; ajouter `inventory.transitionCandidates: [{trigger, target}]`. Documenter en commentaire que ce sont des candidats à revoir, jamais autoritaires (`wireframe-normalization.md` garde la main).
3. Pour chaque nœud `data-wireframe-annotation`, évaluer la longueur (>60) et un pattern hash commit (`\b[0-9a-f]{7,40}\b`), chemin de fichier (`[\w./-]+\.\w+` avec `/`), référence ticket/commit (`#\d+`, `\b[A-Z]+-\d+\b`) ; en cas de match, ajouter `"annotation-contract-risk"` à `decisions` et l'index/raison à `inventory.annotationRisks[]`.
4. Étendre `wireframes-selftest.sh` : fixture avec ≥3 sections togglées structurellement similaires → assert `unitCandidates` et `transitionCandidates` non vides ; fixture avec annotation citant un hash/chemin → assert `annotation-contract-risk` dans `decisions` et entrée dans `annotationRisks`.
5. Ajouter une ligne dans `wireframe-normalization.md` : les signaux structurels/de risque d'annotation de l'inventaire sont des candidats à revue, jamais autoritaires ; les règles d'arrêt de `normalize` s'appliquent malgré leur présence.

## Test acceptance criteria

| Behavior | Expected |
| --- | --- |
| `wireframes-analyze.py` sur une fixture à 3+ sections togglées structurellement similaires | `unitCandidates` non vide, `transitionCandidates` contient au moins une entrée |
| `wireframes-analyze.py` sur une fixture avec annotation citant un hash de commit ou un chemin de fichier | `decisions` contient `"annotation-contract-risk"`, `annotationRisks` nomme l'annotation |
| `wireframes-selftest.sh` | Passe intégralement (aucun `FAIL`) avec les nouvelles assertions |
| Fixtures existantes (`normalize-document.html`, `normalize-fragment.html`, `normalize-states.html`, `normalize-ambiguous.html`) | Classification et code de sortie inchangés |
| `wireframes-analyze.py` sur une fixture avec des sections partageant seulement une classe générique de layout (`container`/`wrapper`/`row`/`col`), sans token spécifique commun | Ces sections ne rejoignent pas `unitCandidates` par le seul effet du groupement structurel |
