---
name: enforce
description: >
  Transforme le contrat figé (release.json et les artefacts qu'il déclare) en gate vérifiable, en HYBRIDE.
  (1) BASELINE : installe lint-core.mjs portable (dérivé du contrat, aucune liste codée en dur),
  câble les 4 gates (import tokens.css · rules de génération · success_condition des plans · hook pre-commit auto-armé).
  Porte le lint instances/DB + boucle corriger→propager→re-lint.
  (2) PIVOT : si un sc-<techno> est présent pour le langage du projet, émet un spec
  d'enforcement agnostique (sc-pivot-contract.md) et relaie la réalisation NATIVE idiomatique
  du linter au sc-<techno>:design-bridge. Dégradation gracieuse si aucun sc-<techno> disponible.
triggers:
  - "installe le linter"
  - "câble les gates"
  - "enforce"
  - "lint les instances"
  - "vérifie la conformité"
  - "arme le pre-commit"
requires:
  - "design/release.json (figé par adjust) — sa racine ; absent, le contrat est en 1.x"
  - "design/tokens.json, design/components.json, design/policies.json (déclarés par release.json)"
  - "design/oracle.json si le contrat en produit un (lu par l'oracle de fidélité, pas par le linter)"
references:
  - ${CLAUDE_PLUGIN_ROOT}/skills/enforce/references/gate-wiring.md
  - ${CLAUDE_PLUGIN_ROOT}/skills/enforce/adapters/lint-core.mjs
  - ${CLAUDE_PLUGIN_ROOT}/skills/enforce/adapters/wordpress.md
  - ${CLAUDE_PLUGIN_ROOT}/references/sc-pivot-contract.md
  - ${CLAUDE_PLUGIN_ROOT}/references/wordpress-pitfalls.md
---

# enforce

## Rôle dans l'entonnoir

```
define → destructure → adjust (figé) → enforce (GATE) → diffuse
```

## Périmètre de `lint-core.mjs`

Le linter portable est un **scanner de chaînes, un fichier de markup à la fois**. Ce qu'il couvre et ce qu'il ne couvre pas, avant toute affirmation de gate :

| Couvert | Hors périmètre par construction |
|---|---|
| Classes littérales `class="…"` / `className="…"` | Liaisons dynamiques (`:class`, `{expr}`), classes assemblées à l'exécution |
| Références `var(--…)` dans le markup scanné | CSS, `theme.json`/presets de plateforme, feuilles de style générées |
| Hex brut dans `style="…"` et `<style>` inline | Contenu stocké en base, sauf extraction explicite (`03-lint-instances`) |
| Namespaces de couleur des classes utilitaires shadées | Adapters, configurations, scripts de build |
| — | Contraste, rôles ARIA, fond réellement appliqué, cohérence inter-fichiers |

Le vocabulaire de classes est **ouvert par défaut** : une classe dont le bloc n'est pas déclaré est ignorée. Il ne se referme que sous `--strict`, en `warning`, sur les seules classes de forme BEM. Les cinq règles, leurs sources et leurs sévérités : `${CLAUDE_PLUGIN_ROOT}/references/contract-schema.md § Dérivation des règles de lint`.

Ce que le gate garantit est donc borné : **le markup passé au linter n'utilise pas de classe ou de token hors contrat — celui que la sortie `CONTRACT` nomme**. Le contrat se passe en `--contract <dossier>` ; deviné, il n'est retenu que s'il est le seul de son arbre, sinon l'outil sort en 2 plutôt que de choisir. Ni la couverture des fichiers, ni la conformité a11y, ni le rendu ne sont établis par ce vert. Le gate de fidélité (§ Deux natures de gate) couvre le rendu ; le reste est un gap déclaré.

## Prérequis

`design/release.json` et les artefacts qu'il déclare doivent exister et être figés (produits par `adjust`). Un artefact déclaré mais absent ou illisible → exit 2.

Les cinq règles dérivent de `tokens.json`, `components.json` et `policies.json` : un `release.json` qui n'en déclare pas les trois n'est pas un contrat plus petit, c'est une règle désactivée, donc **exit 2** plutôt qu'un vert sur rien. `oracle.json` n'est écrit que si le brief produit des cibles de mesure ; aucune règle du linter ne le lit.

Si `release.json` est absent alors que `tokens.json` et `components.json` existent, le contrat est au format 1.x : `lint-core.mjs` sort en 3 — jouer `adjust/03-migrate` d'abord.

## Architecture hybride

```
enforce
  ├── BASELINE (toujours)
  │     lint-core.mjs — dérive ses règles de tokens.json + components.json + policies.json
  │     Sortie : exit 0 (clean) / 1 (errors) / 2 (erreur d'invocation) / 3 (contrat 1.x)
  │
  └── PIVOT (si sc-<techno> présent)
        Émet un spec d'enforcement (sc-pivot-contract.md)
        → sc-<techno>:design-bridge réalise le linter natif idiomatique
        → wiring dans l'outillage natif du projet
```

Le **design garde le QUOI** (contrat = autorité) ; le **sc-<techno> fait le COMMENT** (linter réel, wiring natif). Étendre la couverture au-delà du périmètre ci-dessus passe par le pivot, jamais par une règle ajoutée à `lint-core.mjs`.

## Routage à deux tracks

Le contrat est stack-agnostique, mais la **réalisation** de `03-lint-instances` et `05-fidelity-gate`
diverge selon la stack du projet consommateur. Deux tracks, à identifier avant de dérouler le flux :

| Track | Terrain | Ce qui s'applique |
|-------|---------|---------------------|
| **app-JS-modern** (SPA / from-code) | Vue/React/Tailwind, code source versionné, pas de contenu en DB | 01/02/04 (track-agnostiques) · 03 § Track: app-JS-modern (file-lint) · 05 *seulement si* une maquette de référence externe existe — sinon vocabulaire + bonnes pratiques seules (cf. `05-fidelity-gate.md § Chemin construction-depuis-brief`) |
| **WP/maquette** | WordPress FSE, contenu en DB, réconciliation depuis une maquette | 01/02/04 (track-agnostiques) · 03 § Track: WP-maquette (`wp post get`) · 05 pleine forme (oracle de fidélité) · `agents/copycat.md` |

01, 02 et 04 sont communs aux deux tracks (baseline du linter, câblage des gates, pivot langage).
Seuls 03 et 05 ont un contenu track-spécifique — voir leurs sections `## Track: …` respectives.

## Flux d'exécution

```
01-build-linter → 02-wire-gates → 03-lint-instances → 04-pivot (si applicable) → 05-fidelity-gate (si une maquette de référence existe)
```

1. **01-build-linter** — installe lint-core.mjs dans le projet, configure les chemins, vérifie que la fixture tourne.
2. **02-wire-gates** — câble les 4 points : import `tokens.css` (Gate 0, si pas déjà fait par `adjust`) · rules de génération · success_condition des plans · hook pre-commit.
3. **03-lint-instances** — lint DB/instances (WordPress : `wp post get`) + boucle corriger→propager→re-lint.
4. **04-pivot** — détecte le langage, mappe vers sc-php/sc-js si présents, émet le spec et relaie ; sinon baseline seule.
5. **05-fidelity-gate** — *second gate, nature différente* : mesure la FIDÉLITÉ du rendu à la maquette résolue via l'oracle Python (`getComputedStyle` par breakpoint) + boucle mesurer→corriger→re-mesurer, lit le registre d'écarts. À jouer quand une maquette de référence existe (sinon le lint vocabulaire seul s'applique).

## Les 4 gates

| Gate | Déclenchement | Effet si rouge |
|------|--------------|----------------|
| **Import (`tokens.css`)** | une fois, au figeage du contrat | app garde des `:root` concurrents, dérive silencieuse |
| **Rules** | lors de la génération d'éléments design (diffuse, block patterns) | génération bloquée |
| **success_condition** | dans les plans aidd-dev | plan bloqué tant que gate rouge |
| **pre-commit** | git commit | commit refusé |

Voir `${CLAUDE_PLUGIN_ROOT}/skills/enforce/references/gate-wiring.md` pour le câblage détaillé.

## Deux modes de vocabulaire : `bem` et `utility-first`

`policies.json § mode` détermine sur quoi porte le vocabulaire — noms de classe en `bem`, usage de tokens en `utility-first`. Il est **toujours déclaré** : absent, `lint-core.mjs` sort en 2 au lieu de le déduire. Les deux modes sont de première classe dans la baseline ; aucun n'est un mode dégradé du pivot. Table complète des règles par mode : `${CLAUDE_PLUGIN_ROOT}/references/contract-schema.md § Où porte le vocabulaire, selon mode`.

Une seule règle échappe à la baseline dans les deux modes : une règle de co-occurrence sémantique déclarée en `usage.rules[]` avec `enforcement: "pivot-only"`, qui demande un AST. Sa spec voyage jusqu'au pivot via `references/sc-pivot-contract.md` au lieu d'être réinventée.

## Deux natures de gate : vocabulaire + fidélité

Les 4 gates ci-dessus vérifient tous le **vocabulaire** — import compris : Gate 0 garantit que la source des tokens consommée par l'app est bien celle lintée par les autres. `05-fidelity-gate` ajoute un gate de **nature différente**, contre une référence externe. Les deux doivent être verts ensemble ; aucun ne remplace l'autre.

Ce que chacun établit et n'établit pas : `${CLAUDE_PLUGIN_ROOT}/references/gate-natures.md`.

## Rejouabilité

Si `adjust` re-fige (version bump), re-jouer `/design:enforce` pour re-dériver les règles du linter depuis le nouveau contrat. La boucle corriger→re-lint (03-lint-instances) est l'outil de réconciliation après un re-figeage.

## Références

- `${CLAUDE_PLUGIN_ROOT}/skills/enforce/adapters/lint-core.mjs` — cœur portable du linter (code réel, tourne avec Node.js ≥ 18)
- `${CLAUDE_PLUGIN_ROOT}/skills/enforce/adapters/wordpress.md` — adaptateur WP (lint DB via CLI conteneur)
- `${CLAUDE_PLUGIN_ROOT}/skills/enforce/references/gate-wiring.md` — les 4 points de câblage détaillés
- `${CLAUDE_PLUGIN_ROOT}/references/gate-natures.md` — énoncé canonique de ce que chaque gate établit et n'établit pas
- `${CLAUDE_PLUGIN_ROOT}/references/sc-pivot-contract.md` — interface pivot design ↔ sc-*
- `${CLAUDE_PLUGIN_ROOT}/references/wordpress-pitfalls.md` — pièges WP partagés (classes appariées, eval-file, NFC/NFD…)
- `${CLAUDE_PLUGIN_ROOT}/adapters/measure/` — oracle de fidélité Python (getComputedStyle par breakpoint) ; voir son README — utilisé par `05-fidelity-gate`
- `${CLAUDE_PLUGIN_ROOT}/agents/copycat.md` — agent qui classe les deltas mesurés à la bonne couche (mesure dans le script, jugement dans l'agent)
- `${CLAUDE_PLUGIN_ROOT}/references/deviation-ledger-template.md` — registre des écarts tolérés lu par le gate de fidélité
