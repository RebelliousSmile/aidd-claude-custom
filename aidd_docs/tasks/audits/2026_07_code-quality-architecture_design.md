---
name: audit
description: Codebase audit report template
argument-hint: N/A
---

# Codebase Audit: plugin `design` (cohérence & efficacité)

Architecture du contrat saine et bien pensée, mais la documentation normative a dérivé : trois positions contradictoires pour `harness`, un décompte d'artefacts faux jusque dans le manifeste, et une bannière générée documentée à l'opposé de ce que le code émet.

- **Date**: 2026-07-28
- **Scope**: `plugins/design/` — 224 fichiers versionnés, hors fixtures et `.venv`
- **Health**: fair
- **Findings**: 3 critical, 9 warning, 3 minor

Health: `good` = no critical findings; `fair` = critical findings exist but are isolated and addressable; `poor` = systemic or widespread critical findings.

## Findings

One row per issue. Every row MUST cite a concrete `file:line`. Sort by severity (critical first). Read-only: an audit reports, it never edits code.

Severity (shared rubric across every audit pillar, so a full audit ranks consistently):
- 🔴 critical - exploitable security hole, data loss, or broken correctness. Fix now.
- 🟡 warning - real debt or risk that will bite later. Fix soon.
- 🟢 minor - nit or cleanup. Fix when convenient.

Effort: `S` (under 1h), `M` (under 1d), `L` (over 1d).
Category (the audit pillar, one of): `code-quality`, `architecture`, `security`, `dependencies`, `performance`, `tests`, `ui`.

| Sev | Category     | Location | Issue | Suggested fix | Effort |
| --- | ------------ | -------- | ----- | ------------- | ------ |
| 🔴  | architecture | `skills/harness/SKILL.md:24-30` | Trois positions contradictoires pour `harness` dans l'entonnoir : ici **en aval d'`enforce`** (`enforce → diffuse ↓ harness`), dans `docs/workflow.md:24-28` **en précondition avant `define`**, dans `docs/concepts.md:25` « hors entonnoir ». Un agent qui route une intention n'a pas de réponse. | Un seul énoncé dans `skills/detail/references/funnel-map.md` (déjà source unique lue par `01-explain`) ; les deux autres pointent au lieu de redire. | M |
| 🔴  | code-quality | `references/token-schema.md:212,234` | La bannière documentée est `Regenerate via /design:define.` ; `tools/generate.py:143-146` émet `Regenerate via tools/generate.py.` (et un tiret simple, pas un cadratin). Or `references/write-system-procedure.md:59 § Test` **exige** qu'aucun fichier ne soit écrit sous `design/adapters/` par `define`. La doc oriente vers le verbe qui a interdiction de produire le fichier. | Aligner les trois blocs d'exemple sur la sortie réelle de `generate.py:143-146`, tiret compris. | S |
| 🔴  | architecture | `.claude-plugin/plugin.json:5` | Le manifeste annonce un « **4-artifact contract** rooted by release.json » et n'énumère que `components.json, policies.json, oracle.json and release.json` — `tokens.json` et `deviations.json` manquent. `docs/concepts.md:29` et `references/contract-schema.md:1` en comptent **cinq**. C'est la première chose que lit un installateur. | Corriger en « 5-artifact contract » et citer les cinq artefacts. | S |
| 🟡  | architecture | `references/design-system-contract.md:5,7` | Le fichier se déclare source unique de **quels fichiers** composent le design system, titre `## Les 4 artefacts et leur racine` puis « quatre artefacts adressables », mais son tableau en liste cinq et **`deviations.json` est absent du tableau comme du `## Project layout` (l.31)** — alors qu'il apparaît dans 20 autres fichiers du plugin. | Passer à cinq, ajouter la ligne `deviations.json` au tableau et au layout. | S |
| 🟡  | code-quality | `skills/enforce/SKILL.md:49` et `:120` | La règle « vocabulaire ouvert par défaut » est réénoncée **8 fois dans 6 fichiers** (`docs/concepts.md:49`, `references/design-system-contract.md:62,71`, `references/write-system-procedure.md:19`, `skills/adjust/references/manifest-schema.md:50`, `skills/adjust/SKILL.md:40`, et deux fois dans ce fichier). Aucune n'est désignée canonique. Violation de la règle cardinale du plugin appliquée à sa propre doc. | Désigner `manifest-schema.md:50 § Invariant 1` « Énoncé canonique » (patron déjà utilisé en `references/gate-natures.md:3`) ; les sept autres pointent en une ligne. | M |
| 🟡  | architecture | `references/token-schema.md:259` | Violation **auto-déclarée non résolue** : les sections Tailwind v3/v4 nomment une plateforme dans un fichier de contrat, contre `references/enforcement-registry.md:3` « Aucune valeur ne nomme une plateforme ». Le texte reconnaît la faute et dit sa relocalisation « assigned », sans destinataire ni échéance. | Déplacer les deux sections vers `sc-js:design-bridge` ; ne laisser ici que le rôle abstrait (`stylesheet source`, `build configuration`). | M |
| 🟡  | architecture | `references/design-system-contract.md:46` | Répertoire mort `wireframes/` dans le **layout normatif**, et `skills/enforce/actions/01-build-linter.md:55` propose `"targets": ["../wireframes/**/*.html"]` comme config d'exemple. Le verbe `wireframe` a été absorbé par `diffuse` (`skills/diffuse/SKILL.md:10`). Un utilisateur qui suit le layout crée un dossier que rien ne produit. | Retirer `wireframes/` du layout ; remplacer la cible d'exemple par le glob dérivé du mode. | S |
| 🟡  | architecture | `references/write-system-procedure.md:23` | Délègue à un verbe supprimé : « list them in the inventory; `component` writes the specs on demand ». Aucun verbe `component` n'existe dans les 7 skills. L'instruction renvoie dans le vide. | Remplacer par `diffuse/01-define-element` (le repreneur réel) ou supprimer la délégation. | S |
| 🟡  | architecture | `skills/define/SKILL.md:1-5` | Schéma de frontmatter divergent entre les 7 SKILL.md : `define` et `destructure` n'ont que `name`/`model`/`description` (ni `triggers`, ni `requires`, ni `references`) ; `adjust` n'a pas de `requires` ; seuls `detail`, `enforce`, `diffuse`, `harness` sont complets. Les 5 verbes du pipeline ne se déclarent pas de la même façon. | Fixer un schéma minimal commun aux 7 et le vérifier dans les évals. | M |
| 🟡  | architecture | `skills/harness/SKILL.md:1-12` | `references:` liste des chemins **relatifs** (`adapters/harness/harness.py`, `references/harness-contract.md`) là où les six autres skills utilisent `${CLAUDE_PLUGIN_ROOT}/…`. Un chemin relatif ne résout pas depuis `~/.claude/plugins/cache/…` selon le cwd de l'agent. | Préfixer par `${CLAUDE_PLUGIN_ROOT}/` comme partout ailleurs. | S |
| 🟡  | code-quality | `tools/run-gates.py:90-256` | `run()` = 166 lignes, sur 5 fonctions au total dans le fichier — elle porte le lint, la lecture du statut, l'agrégation et le rendu du rapport. Toute règle nouvelle s'y empile. | Extraire trois fonctions (`_run_lint`, `_read_status`, `_render_report`) ; `run()` devient l'orchestrateur. | M |
| 🟡  | code-quality | `references/token-schema.md:3` | « how the **two adapters** are generated » — vestige d'un modèle à 2 adapters, alors que l'énoncé canonique `write-system-procedure.md:33-38` définit **quatre** rôles de consommateur. La phrase d'ouverture du plus gros fichier de référence est fausse. | « how adapters are generated », et pointer § Adapter emission rule pour le décompte. | S |
| 🟢  | code-quality | `references/design-system-contract.md:5,31,66` | Langue hybride dans un même fichier : titres en anglais (`## Project layout`, `## Consumption rules`), corps en français. `token-schema.md` et `write-system-procedure.md` sont intégralement anglais, `contract-schema.md`/`gate-natures.md`/`enforcement-registry.md` intégralement français. | Choisir une langue par corpus (les `references/` sont normatives, donc une seule) et harmoniser. | L |
| 🟢  | code-quality | `CHANGELOG.md:1` | 544 lignes / 108,5 Ko — **le plus gros fichier du plugin**, devant `adapters/measure/measure.py` (40 Ko). Il est lu intégralement par toute action qui veut vérifier une date de suppression de verbe. | Archiver les majeures closes dans `CHANGELOG-1.x.md`, ne garder que la 2.x courante. | S |
| 🟢  | architecture | `audits/2026_07_design-cycle-critique.md:1` | Artefact de travail (audit expérientiel daté du 2026-07-05) versionné **à l'intérieur d'un plugin distribué** : il part dans le cache de chaque installation. Ses findings #1, #2, #3 et #5 sont pourtant vérifiés corrigés ou adressés dans l'état courant. | Déplacer vers `aidd_docs/tasks/audits/` du marketplace, ou marquer les entrées résolues et clore le fichier. | S |

## Top actions (ranked by impact)

Highest impact first. Each action names the finding rows it resolves and, when a fix is wanted, the act-skill to hand off to (refactor, test, impeccable - the audit itself never edits code).

1. **Trancher la place de `harness` et n'en garder qu'un énoncé** (rows 1). C'est le seul défaut qui casse le routage : trois documents autoritaires donnent trois réponses. `funnel-map.md` est déjà déclaré source unique — l'appliquer. → `aidd-dev:07-refactor`
2. **Aligner la bannière documentée sur la sortie de `generate.py`** (row 2). Falsifiable en un `grep`, corrigible en 5 minutes, et actuellement la doc contredit une règle testée (`§ Test` de `write-system-procedure.md`). → `aidd-dev:07-refactor`
3. **Passer tout le corpus à cinq artefacts et réintégrer `deviations.json`** (rows 3, 4). Le manifeste installé et la référence « source unique du quoi » énoncent tous deux quatre. → `aidd-dev:07-refactor`
4. **Canoniser la règle du vocabulaire ouvert** (row 5). Huit copies dérivent tôt ou tard ; le patron « Énoncé canonique » existe déjà dans trois fichiers, il suffit de l'étendre. Gain de contexte immédiat pour tout agent chargeant `enforce`. → `aidd-dev:07-refactor`
5. **Purger les vestiges de verbes supprimés** (rows 7, 8, 12) : `wireframes/`, le verbe `component`, les « two adapters ». Trois éditions ponctuelles, aucun risque. → `aidd-dev:07-refactor`
6. **Uniformiser les frontmatters et les chemins `${CLAUDE_PLUGIN_ROOT}`** (rows 9, 10). Le chemin relatif de `harness` est un bug latent d'installation, pas seulement une incohérence de style. → `aidd-dev:07-refactor`
7. **Découper `run()` et sortir Tailwind du contrat** (rows 6, 11). Dette structurelle, à traiter quand la 2.8 s'ouvre. → `aidd-dev:07-refactor`

## Coverage

Proves each pillar was examined. A pillar with no findings is still scanned and listed here. A pillar that could not be examined (missing tool or runtime) is listed under Skipped with the reason - never silently dropped.

- **Scanned**: `code-quality` (7 SKILL.md, 19 actions, 15 références racine, 4 outils Python, `lint-core.mjs`, docs, CHANGELOG) ; `architecture` (conformité à l'entonnoir documenté, couplage inter-skills, taille de surface partagée, cohérence du contrat d'artefacts)
- **Skipped**:
  - `security` — non demandé ; aucune surface réseau, aucun secret, aucune entrée non fiable dans le périmètre.
  - `dependencies` — non demandé ; le plugin revendique zéro dépendance Node (`lint-core.mjs:10-11`) et n'expose pas de lockfile auditables hors `adapters/measure/`.
  - `performance` — non demandé ; pas de chemin chaud, pas de profileur applicable à un corpus de skills.
  - `tests` — non demandé. Constat non chiffré retenu au passage : 7 fichiers `evals/scenarios.json` couvrant 100 scénarios de routage, plus des fixtures `enforce/fixtures/` par cas de gate.
  - `ui` — non demandé et sans objet : le plugin ne rend aucune interface.

### Vérification des findings de l'audit préexistant

`plugins/design/audits/2026_07_design-cycle-critique.md` (2026-07-05, 9 findings) a été recoupé contre l'état courant :

| # | Sujet | État vérifié |
| --- | --- | --- |
| 1 | Bug `cssVarToTokenPath` (`.replace(/-/g,'.')`) | **corrigé** — plus aucune occurrence dans `lint-core.mjs` ; la résolution passe par `flattenTokenPaths` (l.346-368) |
| 2 | Utility-first non traité en première classe | **adressé** — fixtures `enforce/fixtures/utility/` + `policies.json § mode` |
| 3 | Modèle thème/mode absent | **adressé** — `token-schema.md:78-108 § Modes / themes` + fixtures `themed/` |
| 5 | Dérive documentaire | **partiellement corrigé** — `write-system-procedure.md:3,55` rectifiés ; résidus confirmés et reportés ci-dessus (rows 2, 7, 8, 12) |
| 4, 6, 7, 8, 9 | — | non revérifiés dans ce passage ; hors des deux piliers demandés |
