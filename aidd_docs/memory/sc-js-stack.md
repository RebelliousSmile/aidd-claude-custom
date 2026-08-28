# sc-js — état de la stack

| Champ | Valeur |
|---|---|
| Version courante | 0.17.1 |
| Dernière release | 2026-08-28 |

## Frameworks détectés

Nuxt, SvelteKit, Svelte SPA, Vue SPA, Vite hybrid, Alpine.js, Astro, 11ty

## Pivots capability disponibles

| Catégorie | Pivots |
|---|---|
| State | pinia, alpine-store, svelte-stores |
| Code splitting | dynamic-import, defineAsyncComponent |
| SSR | storage-guards |
| Server | nitro-imports |
| TypeScript | typescript |
| Icons | lucide-vue, svg-inline |
| Images | web-optimization |
| Networking | preconnect |
| Styling | css-transitions |
| Tools | biome, testing |

## Pivots perf installés (web-optimize)

nuxt, vue-spa, vite, alpine, static, sveltekit

## Pivots data installés (data-optimize)

prisma, drizzle, typeorm, mongoose, graphql, trpc

## Pivot consommé par un autre plugin

`tools/testing.md` (v0.9.0+) — seul pivot de `sc-js` qui n'est lu par aucune skill de `sc-js`. Il est découvert **par glob** (`**/capabilities/**/testing.md`) et consommé par `overcode:control`, dont `references/pivot-contract.md` fait foi sur les champs attendus. Voir `DEC-004`, et [pivots-testing.md](pivots-testing.md) depuis que trois autres plugins en fournissent un.

## Réceptacles pivot design

`design-bridge` (v0.7.0+) — réceptacle pour `design:enforce` + `design:diffuse` :
- `01-realize-lint` → génère `design/lint/eslint-design-rule.mjs` (règle ESLint + Biome fallback)
- `02-render` → composant Vue 3 SFC ou React TypeScript + CSS module

## Livraison continue JavaScript

`sc-js:cd` possède une façade applicative unique pour plusieurs cibles `server` ou `automata`, dans le cadre SC-CD v2. Son adaptateur traite les permissions visibles sur DrvFs comme des données synthétiques : un chemin `/mnt/<lettre>` est un signal à corroborer, jamais une preuve suffisante ni l'assurance d'un mode `777`. Vers Linux, un artefact DrvFs doit désactiver la préservation des permissions, owner et group puis appliquer des modes destination explicites ; l'autre voie sûre consiste à préparer l'artefact sur un système de fichiers Linux natif.

La preuve réelle de permissions s'exécute pendant la livraison et couvre au moins un répertoire, un nouveau fichier et un fichier mis à jour. La configuration hors réseau vérifie seulement que ce mécanisme existe et échoue de manière fermée.

Les champs `proof` et `recovery` décrivent le comportement actuel du script projet, pas la présence de mots-clés. Chaque réconciliation relit le script, lie ces affirmations à des événements ordonnés et refuse une preuve sans contrôle observable ou une récupération supprimée avant la fin de sa fenêtre annoncée. L'oracle déterministe valide une trace normalisée ; il ne prétend pas analyser arbitrairement TypeScript.
