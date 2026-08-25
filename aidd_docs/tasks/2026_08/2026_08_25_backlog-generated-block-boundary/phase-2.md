---
status: done
---

<!-- Fill or omit these sections; never add, rename, or reorder one. -->

# Instruction: Aligner évals et changelog sur la nouvelle borne

## Architecture projection

> Tree of the final files. ✅ create · ✏️ modify · ❌ delete

```txt
.
└── plugins/
    └── overcode/
        ├── CHANGELOG.md                                         ✏️ entrée Unreleased / Fixed
        └── skills/
            └── alias/
                └── evals/
                    ├── backlog-scenarios.md                     ✏️ S1 corrigé + S13 à S16
                    └── fixtures/
                        └── backlog/
                            ├── github-notes-only.md             ✅ repro de l'issue : notes manuelles, aucun titre `##`
                            └── github-manual-section.md         ✅ section `## Backlog` sans aucune ligne générée
```

## Tasks to do

### `1)` Créer les deux fixtures de reproduction

> Les deux cas de destruction ne tiennent pas dans un seul document.

1. Créer `fixtures/backlog/github-notes-only.md` : frontmatter avec `git_repo` GitHub `acme/atlas`, un titre `# ...`, puis des notes manuelles — cases à cocher, lien, commentaire — et aucun titre `##` jusqu'à la fin du fichier.
2. Créer `fixtures/backlog/github-manual-section.md` : même `git_repo`, une section `## Backlog` contenant uniquement du texte manuel et aucune ligne générée, suivie d'une autre section.
3. Inclure dans `github-manual-section.md` une ligne piège de forme générée pointant vers un dépôt tiers, qui doit survivre.
4. Déclarer les deux fixtures dans le bloc « Fixture / preconditions » de la suite.

### `2)` Corriger le scénario S1

> Ses critères de passage encodent le comportement que l'issue supprime.

1. Remplacer « replaces the bytes from `## Backlog` through `### Notes historiques` » par un remplacement borné à la seule ligne générée `- [#4](...)`.
2. Ajouter aux critères : `### Notes historiques` et son texte restent byte-identiques, au même titre que le frontmatter et `## Décisions`.

### `3)` Ajouter les scénarios de préservation

> Un scénario par mode de destruction que l'ancienne borne autorisait.

1. Ajouter les nouveaux scénarios en **S13 et suivants**, sans renuméroter S1 à S12, pour que le log de résultats existant reste lisible.
2. S13 — notes manuelles en fin de fichier : `github-notes-only.md`, insertion puis resynchronisation sur `github_open` ; les notes survivent aux deux passes et les octets sont identiques entre la 2ᵉ et la 3ᵉ passe.
3. S14 — section sans bloc généré : `github-manual-section.md`, bloc inséré en tête de section, texte manuel conservé en dessous dans l'ordre, ligne piège d'un dépôt tiers intacte, rapport `Section: inserted`.
4. S15 — bloc généré suivi d'une sous-section `###` : seul le bloc est remplacé, rapport `Section: replaced`.
5. S16 — contrôle négatif : une implémentation candidate qui étend le remplacement jusqu'à la fin du fichier doit être rejetée par le harnais, la règle violée étant nommée.
6. Laisser intact le log de résultats existant et y ajouter une ligne notant qu'il précède ce changement de borne.

### `4)` Consigner le correctif

> La correction est normative et visible pour l'utilisateur de l'alias.

1. Ajouter sous `## [Unreleased]` → `### Fixed` de `plugins/overcode/CHANGELOG.md` une entrée décrivant la borne par bloc généré, l'ancrage au dépôt résolu et la préservation du contenu manuel de la section.

## Test acceptance criteria

| Task | Acceptance criteria                                                                                                                         |
| ---- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | `github-notes-only.md` reproduit l'issue : un fichier valide où l'ancienne borne s'étendrait jusqu'à la fin du fichier.                        |
| 1    | `github-manual-section.md` contient une ligne de forme générée qu'aucune passe ne doit toucher.                                              |
| 2    | Plus aucun critère de passage de la suite n'exige la suppression de contenu non généré.                                                       |
| 3    | La numérotation S1 à S12 est inchangée et le log de résultats reste interprétable.                                                            |
| 3    | Chaque scénario S13 à S15 échoue si l'action est relue dans sa version d'avant la phase 1, et passe avec la version issue de la phase 1.      |
| 3    | S16 reste rouge par construction et nomme la règle violée.                                                                                    |
| 4    | Le changelog énonce le changement de comportement sans citer de numéro de version.                                                            |
