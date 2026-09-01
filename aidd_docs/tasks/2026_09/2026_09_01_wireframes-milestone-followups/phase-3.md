---
status: done
---

# Phase 3: Documentation — intake HTML issu d'un Artifact Claude

## Architecture projection

```
plugins/design/
├── references/
│   └── wireframe-artifact-sourcing.md                 ✅ (nouveau)
└── skills/wireframes/
    ├── SKILL.md                                        ✏️ (transversal rules : lien)
    └── actions/02-normalize.md                          ✏️ (Input : lien)
```

## Tasks to do

1. Écrire `references/wireframe-artifact-sourcing.md` : décrire la forme du préambule (le HTML brut d'un Artifact claude.ai publié enveloppe le contenu auteur dans un chrome/JS de visionneuse avant le `<meta charset>`/reset CSS/`</head><body>` propres à l'auteur).
2. Documenter l'heuristique de délimitation : repérer le début du contenu auteur au `<meta charset` (ou au bloc reset-CSS) qui précède `</head><body>`, et conserver tout ce qui suit.
3. Documenter explicitement pourquoi un strip automatique est hors périmètre : le chrome de visionneuse est un balisage tiers non versionné, non contractuel ; un mauvais découpage échouerait silencieusement (chrome conservé ou contenu auteur tronqué).
4. Fournir une recette d'extraction manuelle copier-coller (ex. `sed`/script Python un-liner) à exécuter avant `wireframes-analyze.py`.
5. Lier ce nouveau fichier depuis `02-normalize.md` (Input) et `SKILL.md` (Transversal rules).

## Test acceptance criteria

| Behavior | Expected |
| --- | --- |
| Un lecteur ouvre `wireframe-artifact-sourcing.md` | Trouve la forme du préambule, l'heuristique de délimitation, et la justification explicite du refus de strip automatique |
| Un lecteur suit `02-normalize.md` → Input | Trouve le lien vers `wireframe-artifact-sourcing.md` |
| Un lecteur suit `SKILL.md` → Transversal rules | Trouve le même lien |
