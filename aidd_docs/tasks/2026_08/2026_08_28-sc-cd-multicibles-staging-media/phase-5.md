---
status: pending
---

# Instruction: Adapter JavaScript au contrat v2

## Architecture projection

> Tree of the final files. ✅ create · ✏️ modify · ❌ delete

```txt
plugins
├── sc-js/skills/cd
│   ├── SKILL.md                                      ✏️ multi-cibles et phases
│   ├── actions/{02-server,03-automata}.md            ✏️ façade et délégation v2
│   ├── references/{command-facade,data-layers}.md    ✏️ surfaces SQL et médias
│   └── evals/{scenarios.json,delivery-scenarios.md,delivery-safety-scenarios.md} ✏️ preuves v2
└── tools/eval/fixtures-sc-cd/behave-park/fixture.yaml ✏️ variantes JavaScript
❌ aucun fichier supprimé
```

## User Journey

```mermaid
flowchart TD
  A[Stack JavaScript détectée] --> B[Choisir cible nommée]
  B --> C[Construire artefact]
  C --> D[Appliquer migrations déclaratives]
  D --> E[Respecter autorité des données]
  E --> F[Appeler la même façade en server ou automata]
```

## Test Scope

```mermaid
---
title: Test scope
---
journey
  section Setup
    Préparer fixtures Node et Nuxt avec SQL et médias => cibles staging et production déclarées: 5: cli
  section Happy path
    Configurer deux cibles JavaScript => artefact et migrations utilisent une façade unique: 5: cli
  section Edge case - donnée mutable
    Demander une copie locale en production => aucune donnée ou média distant n'est muté: 1: cli
  section Edge case - cible absente
    Omettre l'identifiant => aucune cible par défaut n'est choisie quand plusieurs existent: 1: cli
```

## Tasks to do

### `1)` Adapter JavaScript

> Distinguer migrations, données serveur, IndexedDB et médias persistants.

1. Sélectionner la cible dans la façade du gestionnaire déjà détecté.
2. Garder SQL schema local, contenu SQL distant en production et migrations IndexedDB dans la release de code.
3. Autoriser un miroir staging des données ou médias seulement lorsqu'une stratégie export/import ou inventaire existe.
4. Étendre les scénarios Nuxt, Node et statiques sans inventer un stockage.

## Test acceptance criteria

| Task | Acceptance criteria |
| ---- | ------------------- |
| 1 | Une application JavaScript multi-cibles distingue code, schéma, données serveur et données navigateur sans inventer de copie de production. |
