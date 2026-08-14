# Contribuer

Marketplace personnelle de plugins Claude Code et Codex. Ce guide décrit comment ajouter ou modifier un plugin portable en respectant les conventions du dépôt. Tutoiement par convention.

## Structure du dépôt

```
.claude-plugin/marketplace.json   # registre du marketplace (source de vérité installable)
.agents/plugins/marketplace.json  # catalogue Codex natif (politique + catégorie)
index.json                        # registre des plugins (id, nom) — ni version ni description
plugins/<nom>/
  .claude-plugin/plugin.json      # manifeste du plugin
  .codex-plugin/plugin.json       # manifeste Codex natif
  README.md                       # doc du plugin
  CHANGELOG.md                    # journal du plugin
  references/                     # docs partagées + contrat host-portability
  skills/<skill>/
    SKILL.md                      # routeur du skill (frontmatter + actions + flow)
    actions/NN-<nom>.md           # une étape par fichier
    references/                   # docs/templates propres au skill
    evals/scenarios.json          # cas de routage (prompt → expect_action)
memory/                           # guidelines d'authoring (README, CLAUDE.md)
aidd_docs/internal/decisions/     # ADR (décisions d'architecture, ex. DEC-001)
```

Les tests sont **versionnés** : `tools/eval/` (gardes et fixtures), `package.json` (scripts, dont `pnpm test`) et `.github/workflows/test.yml`. Ils tournent en local comme en CI — une garde ajoutée profite aux deux sans démarche.

## Anatomie d'un skill

Un `SKILL.md` est un **routeur**, pas une procédure. Frontmatter :

```yaml
---
name: <skill>
description: >-          # déclencheurs + périmètre + "Do NOT use ... use X instead"
  ...
---
```

Le frontmatter portable ne porte que `name` et `description`. Pour une skill explicit-only dans Codex, ajouter `agents/openai.yaml` avec une `interface` valide et `policy.allow_implicit_invocation: false`; ne pas remettre `model`, `triggers` ou `disable-model-invocation` dans `SKILL.md`.

Corps attendu :

- **Available actions** — tableau `# · Action · Role · Input`.
- **Default flow** — linéaire (`01 → 02`) ou routeur, avec un mapping *trigger → action*.
- **Transversal rules** — invariants valables pour toutes les actions.
- **References / Evals** — pointeurs.

Chaque `actions/NN-<nom>.md` suit : `Inputs` → `Process` → `Outputs` → `Test`. Le `Test` doit être vérifiable (une condition observable, pas « ça marche »).

**Le numéro vit dans le nom du fichier et dans la table, jamais dans le titre** : `# Bump plugin`, pas `# Action 03 — bump-plugin`. Un numéro écrit à trois endroits se corrige à un seul le jour d'un renommage — c'est ainsi qu'`alias` a fini avec six actions sur dix mal numérotées et deux « Action 06 ». Le numéro **identifie**, il n'ordonne pas : un doublon est une erreur, un trou est toléré (l'interdire rendrait bloquante la cascade de renommages qui suit chaque suppression d'action).

**Convention `evals/scenarios.json`** : liste de `{ "prompt", "expect_action" }`. `expect_action` vaut **soit l'id exact d'une action** de la table (préféré — la couverture est alors traçable), **soit `null`** (le prompt ne doit pas déclencher ce skill). Les **labels sémantiques** non-id (ex. `build+wire` pour un flux composite) sont tolérés mais non traçables automatiquement — à éviter pour les nouveaux skills. Idéalement, exposer le mapping *trigger → action* en prose (`"phrase" → \`action\``) plutôt qu'en seul frontmatter `triggers:`.

Pour partager une procédure entre skills (DRY), la placer dans `plugins/<nom>/references/` et la référencer via la racine portable définie par `references/host-portability.md` (`${<PLUGIN>_PLUGIN_ROOT}`). Cette racine se dérive du `SKILL.md` chargé ; `CLAUDE_PLUGIN_ROOT` n'est qu'un hint optionnel — **référencer, ne pas redupliquer**.

## Règles installées dans un projet

Un skill `setup`/`sniff` route les instructions selon l'hôte : section bornée de `AGENTS.md` et références sous `.agents/rules/` sur Codex, fichiers sous `.claude/rules/` sur Claude Code. Codex ne charge pas automatiquement `.agents/rules/` : `AGENTS.md` doit dire quand lire chaque référence. Sur Claude Code, chaque règle porte un frontmatter `paths:` et s'auto-charge quand un fichier touché correspond.

- `paths:` d'une **règle de codage** → globs de fichiers source pertinents (`**/*.vue`, `**/*.css`…).
- `paths:` d'un **pivot perf** (consommé par `web-optimize`) → uniquement les fichiers de **config** (`vite.config.ts`…), pas les globs source — voir DEC-001.
- Bullets impératifs et courts (`Always X` / `Never Y`), un `## Why` quand utile.

## Ajouter un plugin

1. Créer les deux manifests : `plugins/<nom>/.claude-plugin/plugin.json` et `plugins/<nom>/.codex-plugin/plugin.json` (`name`, `version`, `description`, `author`, `skills`, métadonnées d'interface Codex).
2. Ajouter les skills sous `skills/`.
3. **Enregistrer le plugin à trois endroits** :
   - `.claude-plugin/marketplace.json` (bloc `plugins[]` : `name`, `version`, `source`, `description`, `recommended`).
   - `.agents/plugins/marketplace.json` (bloc `plugins[]` : source locale, politiques `installation`/`authentication`, catégorie ; aucune version ni description dupliquée).
   - `index.json` (bloc `plugins[]` : `id`, `name` — **rien d'autre**, voir *Versionnement*).
4. Documenter dans le `README.md` racine (tableau des plugins + section dédiée + tableau « par type de projet » si pertinent) et créer `plugins/<nom>/README.md`.
5. Créer `plugins/<nom>/CHANGELOG.md`.

Garder les deux manifests, les deux catalogues et les README cohérents à chaque changement.

## Versionnement

- SemVer par plugin dans les deux manifests ; le manifest Claude porte la version sémantique de référence et le manifest Codex partage cette version, avec au plus un suffixe de cachebuster `+codex.*`. Le catalogue Claude duplique la version ; le catalogue Codex ne la duplique pas.
- `index.json` ne porte **ni version ni description**. Il les a portées, et elles ont dérivé sur six plugins sans qu'aucun lecteur ne s'en aperçoive — parce qu'aucun lecteur ne s'en sert. Une copie que personne ne lit ne se maintient pas : elle se supprime. Les y remettre ferait revenir la dérive.
- **Mineur** : ajout rétro-compatible (skill, action, règle).
- **Majeur** : suppression/renommage cassant un usage existant.
- Consigner chaque bump dans le `CHANGELOG.md` du plugin ; les changements de composition du marketplace (ajout/retrait de plugin) vont dans le `CHANGELOG.md` racine.

## Commits

Convention *Conventional Commits* :

```
feat(<plugin>): ...
fix(<plugin>/<skill>): ...
docs(<plugin>): ...
chore(<plugin>): bump x.y.z → x.y.(z+1)
```

Messages factuels, impératifs. Pas d'emoji dans les artefacts versionnés.

## Développement local

Sur la machine de dev, enregistrer le marketplace Claude avec `"source": "directory"`. Pour Codex, enregistrer la marketplace locale contenant `.agents/plugins/marketplace.json` avec le CLI ou le navigateur de plugins.

Après modification d'un plugin déjà installé, utiliser le flux de cachebuster/réinstallation propre à l'hôte puis ouvrir une nouvelle session.

## Avant de pousser

- JSON valides (les deux marketplaces, `index.json`, les deux manifests, chaque `evals/scenarios.json`).
- Chaque plugin passe `validate_plugin.py` et chaque skill passe `quick_validate.py`.
- Chaque action a un `Test` vérifiable.
- Les tests passent : `pnpm test`.
- Les références croisées (`${<PLUGIN>_PLUGIN_ROOT}/...`) pointent vers des fichiers existants. `M4` couvre les racines portables et la compatibilité historique, mais une référence hors table déclarative reste à vérifier à la main.
- README racine + README plugin + CHANGELOG cohérents avec la version.
