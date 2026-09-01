---
status: done
---

# Phase 1: Documentation — environnement de rendu, règle harness, routing plan

## Architecture projection

```
plugins/design/
├── skills/wireframes/
│   ├── SKILL.md                                    ✏️ (transversal rules + routing)
│   └── actions/
│       ├── 02-normalize.md                         ✏️ (step 4 : règle prefill harness)
│       └── 03-lint.md                               ✏️ (Input : lien setup rendu)
└── references/
    ├── wireframe-render-setup.md                    ✅ (nouveau)
    └── wireframe-manifest-schema.md                 ✏️ (note Harness metadata)
```

## Tasks to do

1. Écrire `references/wireframe-render-setup.md` : install standard (`pip install -r plugins/design/adapters/measure/requirements.txt` puis `python -m playwright install chromium`, hors `--target /tmp`), export `WIREFRAMES_CHROMIUM` vers l'exécutable installé, note que `render-check.py` et `wireframes-browser-selftest.sh` lisent tous deux cette variable, symptôme si absente ("WIREFRAMES_CHROMIUM must name an executable Chromium").
2. Lier ce nouveau fichier depuis `SKILL.md` (Transversal rules, aux côtés de `wireframe-normalization.md`/`wireframe-harness-handoff.md`) et depuis `03-lint.md` (Input, à côté de la ligne Playwright/Chromium).
3. Ajouter à `02-normalize.md` step 4 une règle explicite : pour une unité `page`, ne remplir `harness.key`/`label`/`group` que si la source nomme sans ambiguïté une route/écran ; sinon laisser le bloc `harness` absent. Préciser que dans ce dernier cas, `promote` refuse toute métadonnée harness manquante (`04-promote.md`) : un humain doit compléter `harness` manuellement avant promotion, `normalize` ne le fait pas à sa place.
4. Ajouter dans `wireframe-manifest-schema.md`, section Harness metadata, une ligne renvoyant vers cette règle de `02-normalize.md`.
5. Ajouter à `SKILL.md` Routing une ligne référençant l'étape `03-wireframe` de `aidd-dev:01-plan` : après un croquis ASCII basse-fidélité issu du plan, produire le board validé/rendu correspondant → `scaffold`.

## Test acceptance criteria

| Behavior | Expected |
| --- | --- |
| Un lecteur suit `SKILL.md` → lien setup rendu | Arrive sur `wireframe-render-setup.md`, qui nomme l'install standard et `WIREFRAMES_CHROMIUM` |
| Un lecteur suit `03-lint.md` → Input | Trouve le même lien vers `wireframe-render-setup.md` |
| Un lecteur applique `02-normalize.md` step 4 sur une source sans route nommée | Comprend qu'il doit laisser `harness` absent, pas en inventer une |
| Un lecteur consulte `wireframe-manifest-schema.md` section Harness metadata | Trouve le renvoi vers la règle de prefill de `02-normalize.md` |
| Un lecteur vient de l'étape wireframe de `aidd-dev:01-plan` avec un croquis ASCII validé | Trouve dans `SKILL.md` Routing la ligne qui l'oriente vers `scaffold` |
