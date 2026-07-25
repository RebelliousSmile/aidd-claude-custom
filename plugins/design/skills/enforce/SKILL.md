---
name: enforce
description: >
  Transforme le contrat figé (release.json et les artefacts qu'il déclare) en gate vérifiable, en HYBRIDE.
  (1) BASELINE : installe lint-core.mjs portable (dérivé du contrat, aucune liste codée en dur),
  câble les 4 gates (import tokens.css · rules de génération · success_condition des plans · hook pre-commit auto-armé).
  Porte le lint des instances déjà stockées + boucle corriger→propager→re-lint.
  (2) PIVOT : si un sc-<langage> est installé pour le langage de la preuve, émet un spec
  d'enforcement agnostique (sc-pivot-contract.md) et relaie la réalisation NATIVE idiomatique
  du linter au sc-<langage>:design-bridge. Règles non réalisées déclarées si aucun n'est installé.
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
  - ${CLAUDE_PLUGIN_ROOT}/references/enforcement-registry.md
  - ${CLAUDE_PLUGIN_ROOT}/references/sc-pivot-contract.md
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
| Références `var(--…)` dans le markup scanné | Feuilles de style, fichiers de configuration de plateforme, styles générés |
| Hex brut dans `style="…"` et `<style>` inline | Contenu stocké hors des fichiers source, sauf extraction explicite (`03-lint-instances`) |
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
  └── PIVOT (si un sc-<langage> est installé)
        Émet un spec d'enforcement (sc-pivot-contract.md)
        → sc-<langage>:design-bridge réalise le linter natif idiomatique
        → wiring dans l'outillage natif du projet
```

Le **design garde le QUOI** (contrat = autorité) ; le **sc-<langage> fait le COMMENT** (linter réel, wiring natif). Étendre la couverture au-delà du périmètre ci-dessus passe par le pivot, jamais par une règle ajoutée à `lint-core.mjs`.

## Routage des actions

01, 02 et 04 s'appliquent toujours : baseline du linter, câblage des gates, pivot par langage.
03 et 05 se déroulent différemment selon **deux propriétés du terrain**, indépendantes l'une de l'autre — jamais selon le nom de la plateforme, qui n'en décide aucune :

| Question à trancher | Réponse | Effet |
|---|---|---|
| Tout le markup vit-il dans des fichiers versionnés ? | oui | 03 § Track: fichiers source — lint direct |
| | non, une part vit dans un magasin de contenu | 03 § Track: contenu stocké — extraire, linter, corriger, réécrire |
| Une référence visuelle externe existe-t-elle ? | oui | 05 pleine forme (oracle de fidélité) · `agents/copycat.md` |
| | non (construction depuis un brief) | 05 sans objet — vocabulaire + bonnes pratiques seules (`05-fidelity-gate.md § Chemin construction-depuis-brief`) |

Les deux se combinent : un projet peut avoir du contenu stocké sans maquette, ou l'inverse.

## Flux d'exécution

```
01-build-linter → 02-wire-gates → 03-lint-instances → 04-pivot (si applicable) → 05-fidelity-gate (si une maquette de référence existe)
```

1. **01-build-linter** — installe lint-core.mjs dans le projet, configure les chemins, vérifie que la fixture tourne.
2. **02-wire-gates** — câble les 4 points : import `tokens.css` (Gate 0, si pas déjà fait par `adjust`) · rules de génération · success_condition des plans · hook pre-commit.
3. **03-lint-instances** — lint des instances existantes, fichiers ou contenu stocké, + boucle corriger→propager→re-lint.
4. **04-pivot** — route chaque règle vers le réceptacle nommé par son type d'enforcement, émet le spec et relaie ; les règles sans réceptacle installé sont déclarées non réalisées.
5. **05-fidelity-gate** — *second gate, nature différente* : mesure la FIDÉLITÉ du rendu à la maquette résolue via l'oracle Python (`getComputedStyle` par breakpoint) + boucle mesurer→corriger→re-mesurer, lit le registre d'écarts. À jouer quand une maquette de référence existe (sinon le lint vocabulaire seul s'applique).

## Les 4 gates

| Gate | Déclenchement | Effet si rouge |
|------|--------------|----------------|
| **Import (`tokens.css`)** | une fois, au figeage du contrat | app garde des `:root` concurrents, dérive silencieuse |
| **Rules** | lors de la génération d'éléments design (`diffuse`) | génération bloquée |
| **success_condition** | dans les plans aidd-dev | plan bloqué tant que gate rouge |
| **pre-commit** | git commit | commit refusé |

Voir `${CLAUDE_PLUGIN_ROOT}/skills/enforce/references/gate-wiring.md` pour le câblage détaillé.

## Deux modes de vocabulaire : `bem` et `utility-first`

`policies.json § mode` détermine sur quoi porte le vocabulaire — noms de classe en `bem`, usage de tokens en `utility-first`. Il est **toujours déclaré** : absent, `lint-core.mjs` sort en 2 au lieu de le déduire. Les deux modes sont de première classe dans la baseline ; aucun n'est un mode dégradé du pivot. Table complète des règles par mode : `${CLAUDE_PLUGIN_ROOT}/references/contract-schema.md § Où porte le vocabulaire, selon mode`.

## Portée de la baseline

`lint-core.mjs` lit **un fichier de markup à la fois, en texte**. Cinq règles, toutes dérivées du contrat à l'exécution, aucune valeur codée en dur, aucun état entre deux runs. Le vocabulaire est **ouvert par défaut** : une classe dont le bloc n'est pas déclaré passe comme utilitaire ; `--strict` la signale en `warning`, jamais en `error`.

Hors de portée par construction, donc jamais couvert par un run vert : feuilles de style, liaisons de classe dynamiques, contenu stocké hors des fichiers source, fichiers de configuration de plateforme, contrastes, rôles ARIA, toute cohérence entre deux fichiers.

Ce qui sort de cette portée n'est pas perdu : c'est déclaré en `usage.rules[]` avec un `enforcement` qui nomme son réalisateur, ou marqué non réalisé. Espace fermé des types et obligation de rapport : `${CLAUDE_PLUGIN_ROOT}/references/enforcement-registry.md`. L'agrégation des deux côtés est `tools/run-gates.py`.

## Seuil de maturité — la conformité n'est opposable qu'au-dessus

Un gate vert n'affirme la conformité que si le contrat a atteint le seuil de maturité. `tools/run-gates.py` relève le statut du contrat après avoir linté : **sous le seuil, il sort en 4** — les violations restent listées, mais la conformité n'est pas affirmée, et le rapport nomme le chemin qui remonte le statut. Un contrat migré depuis 1.x entre à `normalized`, donc sous le seuil : le gate bloque toujours les vraies violations, mais ne certifie rien tant que les vérifications ne sont pas enregistrées et le statut relevé.

Ce document ne réénonce pas la valeur du seuil : elle a **une seule source humaine**, `${CLAUDE_PLUGIN_ROOT}/references/maturity-status.md`, et **une seule source exécutable**, la constante `THRESHOLD` de `tools/status.py` que `run-gates.py` importe.

## Deux natures de gate : vocabulaire + fidélité

Les 4 gates ci-dessus vérifient tous le **vocabulaire** — import compris : Gate 0 garantit que la source des tokens consommée par l'app est bien celle lintée par les autres. `05-fidelity-gate` ajoute un gate de **nature différente**, contre une référence externe. Les deux doivent être verts ensemble ; aucun ne remplace l'autre.

Ce que chacun établit et n'établit pas : `${CLAUDE_PLUGIN_ROOT}/references/gate-natures.md`.

## Rejouabilité

Si `adjust` re-fige (version bump), re-jouer `/design:enforce` pour re-dériver les règles du linter depuis le nouveau contrat. La boucle corriger→re-lint (03-lint-instances) est l'outil de réconciliation après un re-figeage.

## Références

- `${CLAUDE_PLUGIN_ROOT}/skills/enforce/adapters/lint-core.mjs` — cœur portable du linter (code réel, tourne avec Node.js ≥ 18)
- `${CLAUDE_PLUGIN_ROOT}/skills/enforce/references/gate-wiring.md` — les 4 points de câblage détaillés
- `${CLAUDE_PLUGIN_ROOT}/references/gate-natures.md` — énoncé canonique de ce que chaque gate établit et n'établit pas
- `${CLAUDE_PLUGIN_ROOT}/references/enforcement-registry.md` — espace fermé des types d'enforcement, réalisateur de chacun, marqueur non réalisé
- `${CLAUDE_PLUGIN_ROOT}/references/sc-pivot-contract.md` — interface pivot design ↔ sc-*
- `${CLAUDE_PLUGIN_ROOT}/adapters/measure/` — oracle de fidélité Python (getComputedStyle par breakpoint) ; voir son README — utilisé par `05-fidelity-gate`
- `${CLAUDE_PLUGIN_ROOT}/agents/copycat.md` — agent qui classe les deltas mesurés à la bonne couche (mesure dans le script, jugement dans l'agent)
- `${CLAUDE_PLUGIN_ROOT}/references/deviation-ledger-template.md` — registre des écarts tolérés lu par le gate de fidélité
