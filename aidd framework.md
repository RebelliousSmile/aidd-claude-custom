

# framework

## gestion de la mémoire

#### Deux racines, deux rôles                                                                                                                                                                         
  - `aidd_docs/internal/` → **décisions** (ADRs). Source : skill `/learn`. Index dans `ADR.md`.                                                                                                    
  - `aidd_docs/memory/` → **mémoire de contexte projet**, auto-chargée dans CLAUDE.md via `<aidd_project_memory>`.
  
  Pas de chevauchement : une ADR documente *une décision datée*, une mémoire documente *un état courant transverse*.

### Sous-arborescence de `memory/`

| Dossier                | Chargement       | Source                                   | Templates                                   |
| ---------------------- | ---------------- | ---------------------------------------- | ------------------------------------------- |
| `memory/*.md` (racine) | auto (CLAUDE.md) | `/init`, `/learn`, `reconcile-normative` | `aidd_docs/templates/aidd/memory/`          |
| `memory/internal/*.md` | on-demand        | `/init`, `reconcile-normative`           | `aidd_docs/templates/aidd/memory/internal/` |
| `memory/external/*.md` | on-demand        | **manuel uniquement**                    | aucun (par design)                          |

  `update_memory.js` ne scanne que la racine — les sous-dossiers ne sont pas auto-injectés.

#### Qui écrit où

  - `/init` : crée/MAJ tout l'arbre depuis les templates (idempotent, rejouable en milieu de projet)
  - `/learn` : ADR dans `internal/decisions/` + maj `ADR.md` + sync `update_memory.js`
  - `reconcile-normative` : phase C classe une nouvelle entrée mémoire via le tableau Topic → file
  - `external/` : édition humaine uniquement (pas de skill ne doit y écrire)

#### Critère rule vs memory

  - **Rule** (`.claude/rules/`) si convention path-scopable (glob étroit) ET vérifiable à l'écriture
  - **Memory** si transverse, conceptuel, ou explicatif (le « why »)
  - Ambigu et testable + scopable → rule. Sinon memory.

### Tableau Topic → file (skill `reconcile-normative`)

  Étendu aujourd'hui : ajout de `agents_coordination.md`, `custom-main-workflow.md`, et 7 sujets transverses (auth, real-time, caching, feature flags, i18n, RGPD, notifications). Fallback réécrit
   en scan-first / create-only-if-no-fit.

#### Garde-fous

  - Un nouveau fichier mémoire doit s'aligner sur un template existant — sinon justifier le nouveau template
  - Suppression d'un fichier mémoire → confirmation utilisateur obligatoire
  - Pas de duplication rule ↔ memory (DRY normatif)## Deux racines, deux rôles                                                                                                                                                                         
  - `aidd_docs/internal/` → **décisions** (ADRs). Source : skill `/learn`. Index dans `ADR.md`.                                                                                                    
  - `aidd_docs/memory/` → **mémoire de contexte projet**, auto-chargée dans CLAUDE.md via `<aidd_project_memory>`.
  
  Pas de chevauchement : une ADR documente *une décision datée*, une mémoire documente *un état courant transverse*.

### Sous-arborescence de `memory/`

| Dossier                | Chargement       | Source                                   | Templates                                   |
| ---------------------- | ---------------- | ---------------------------------------- | ------------------------------------------- |
| `memory/*.md` (racine) | auto (CLAUDE.md) | `/init`, `/learn`, `reconcile-normative` | `aidd_docs/templates/aidd/memory/`          |
| `memory/internal/*.md` | on-demand        | `/init`, `reconcile-normative`           | `aidd_docs/templates/aidd/memory/internal/` |
| `memory/external/*.md` | on-demand        | **manuel uniquement**                    | aucun (par design)                          |

  `update_memory.js` ne scanne que la racine — les sous-dossiers ne sont pas auto-injectés.

#### Qui écrit où

  - `/init` : crée/MAJ tout l'arbre depuis les templates (idempotent, rejouable en milieu de projet)
  - `/learn` : ADR dans `internal/decisions/` + maj `ADR.md` + sync `update_memory.js`
  - `reconcile-normative` : phase C classe une nouvelle entrée mémoire via le tableau Topic → file
  - `external/` : édition humaine uniquement (pas de skill ne doit y écrire)

#### Critère rule vs memory

  - **Rule** (`.claude/rules/`) si convention path-scopable (glob étroit) ET vérifiable à l'écriture
  - **Memory** si transverse, conceptuel, ou explicatif (le « why »)
  - Ambigu et testable + scopable → rule. Sinon memory.

#### Tableau Topic → file (skill `reconcile-normative`)

  Étendu aujourd'hui : ajout de `agents_coordination.md`, `custom-main-workflow.md`, et 7 sujets transverses (auth, real-time, caching, feature flags, i18n, RGPD, notifications). Fallback réécrit
   en scan-first / create-only-if-no-fit.

#### Garde-fous

  - Un nouveau fichier mémoire doit s'aligner sur un template existant — sinon justifier le nouveau template
  - Suppression d'un fichier mémoire → confirmation utilisateur obligatoire
  - Pas de duplication rule ↔ memory (DRY normatif)

## aidd-claude-custom

### existant

### à faire

- command + template pour faire un audit sur un fichier
- debrief pour export dans obsidian + planification


nouveaux fichiers à réintégrer

- Skills nouvelles : web-optimize/SKILL.md, web-optimize/tests.md,
  web-optimize/references/framework-mapping.md, reconcile-normative/SKILL.md
  - Skill réécrite : harvest/SKILL.md
  - Rules nouvelles : 01-standards/1-normative-vs-archive.md,
  01-standards/1-file-language-and-style.md, 09-other/9-harvest-trigger.md (déplacée depuis    
  custom/)
   - templates/dev/perf_checklist_nuxt.md ⚠️ template nouveau — j'avais répondu à tort « aucun  
  template » plus tôt, parce que mon filtre LastWriteTime n'a pas remonté ce fichier
  (probablement écrit avant (Get-Date).AddDays(-1) à cause d'un fuseau ou de la précision). Mes
   excuses pour l'erreur.