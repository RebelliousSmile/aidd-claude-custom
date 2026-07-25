# Couplage harness ↔ contrat (`--contract`)

Le harness scaffolde une maquette de référence sans rien savoir d'un contrat. `--contract <dir>` est **opt-in** : sans lui, le scaffold est inchangé et sort en 0. Avec lui, la maquette **inline la feuille de tokens déjà générée** du contrat, pour que la référence parle les mêmes tokens que ceux contre lesquels l'implémentation est lintée.

## Option C — inline, jamais dérivé

`--contract` résout **l'entrée `policies.json § adapters[]` dont `consumer` vaut `"stylesheet"`**, lit son `artifact` tel que produit par `tools/generate.py`, et l'inline dans un `<style>` placé **avant le chrome** (les `:root { --… }` sont définis avant tout markup qui les référence). Le harness ne dérive ni ne régénère : il ne lit pas `tokens.json`, n'émet aucun adapter, ne reproduit pas `generate.py § emit_css`. Un seul producteur de la feuille de tokens — `generate.py` — un seul lecteur ici (`write-system-procedure.md § Adapter emission rule`).

L'ordre est un non-conflit : `emit_css` n'émet que des propriétés personnalisées `:root`, aucune règle d'élément, et le chrome du harness utilise ses propres littéraux. Placer la feuille en premier garantit seulement que les vars existent avant usage ; il n'y a pas de bataille de cascade.

Quand la feuille est inline, le cadrage LLM du fichier généré (bloc d'en-tête `<!-- … -->` et règles `//` au-dessus du registre `pages`) instruit l'auteur : **consommer les tokens via `var(--…)`, ne jamais coder en dur couleur / espacement / typographie** — sinon l'auteur contourne la source unique de vérité que le couplage existe pour imposer.

## Espace de codes de sortie (sous `--contract` uniquement)

Le harness participe à l'espace fixe du plugin (`master § Exit-code space`) **seulement** sous `--contract`. Sans le flag, il sort toujours en 0.

| Situation | Code | Message |
|---|---|---|
| Feuille inline, ou pas de flag | 0 | — |
| `--contract` mais aucun adapter `consumer:"stylesheet"` déclaré | 0 | un avertissement stderr, poursuite en scaffold |
| `release.json` **absent** (contrat 1.x) | 3 | nomme `tools/migrate-contract.py` |
| `release.json` présent mais **JSON invalide** | 2 | nomme `release.json` — un contrat corrompu n'est pas 1.x, seule l'absence l'est |
| `policies.json` absent, illisible ou pas un objet | 2 | nomme l'artefact |
| Adapter `stylesheet` déclaré, fichier **absent ou illisible** | 2 | nomme `tools/generate.py` comme correctif (option C : jamais de dérivation ici) |

Le harness n'émet **jamais** 1 ni 4. Le chemin historique « aucune page » sort désormais en 2 (erreur d'invocation), non en 1. `3` est réservé à l'absence de `release.json` seule ; toute autre lecture en échec est un 2 ; `4` reste au seul `run-gates.py` (seuil de maturité).

## Trois échantillons device, jamais de media query

Le harness rend **trois vues discrètes par classe** — desktop (fluide) · tablet 834 · mobile 390 — basculées par `window.setViewport('desktop'|'tablet'|'mobile')`. Ce sont des **échantillons device**, pas des breakpoints : `834` et `390` sont des largeurs fixes, **rien n'est dérivé de `tokens.json § breakpoint.*`**. Le template ne contient **aucune media query** ; les variations d'auteur s'écrivent en classe (`.preview-frame.mobile <sel>` / `.preview-frame.tablet <sel>`).

## Accord measure / oracle — l'ensemble fermé de viewports

L'oracle de fidélité (`adapters/measure/measure.py`) pose la vraie largeur de contexte par breakpoint **et** bascule la classe du cadre via `setViewport` : les échantillons par classe sont exactement ce que l'oracle pilote déjà. `config-gen.py § _derive_breakpoints` stampe un `mockup_viewport ∈ {desktop, tablet, mobile}` — toute clé `tokens.breakpoint.*` hors de `_BP_MAP` est ignorée (`config-gen.py:110-112`), le nom est pris dans `_BP_MAP` (`:121-122`), et le fallback est mobile+desktop (`:55-56`). L'ensemble est donc **clos par construction**, pas une chose à vérifier au runtime, et il coïncide avec les trois échantillons exposés par le harness.
