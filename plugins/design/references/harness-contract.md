# Couplage harness ↔ contrat (`--contract`)

Le harness scaffolde une maquette de référence sans rien savoir d'un contrat. `--contract <dir>` est **opt-in** : sans lui, le scaffold est inchangé. Avec lui, la maquette **inline la feuille de tokens déjà générée** du contrat, pour que la référence parle les mêmes tokens que ceux contre lesquels l'implémentation est lintée.

## Option C — inline, jamais dérivé

`--contract` résout **l'entrée `policies.json § adapters[]` dont `consumer` vaut `"stylesheet"`**, lit son `artifact` tel que produit par `tools/generate.py`, et l'inline dans un `<style>` placé **avant le chrome** (les `:root { --… }` sont définis avant tout markup qui les référence). Le harness ne dérive ni ne régénère : il ne lit pas `tokens.json`, n'émet aucun adapter, ne reproduit pas `generate.py § emit_css`. Un seul producteur de la feuille de tokens — `generate.py` — un seul lecteur ici (`write-system-procedure.md § Adapter emission rule`).

L'ordre est un non-conflit : `emit_css` n'émet que des propriétés personnalisées `:root`, aucune règle d'élément, et le chrome du harness utilise ses propres littéraux. Placer la feuille en premier garantit seulement que les vars existent avant usage ; il n'y a pas de bataille de cascade.

Quand la feuille est inline, le cadrage LLM du fichier généré (bloc d'en-tête `<!-- … -->` et règles `//` au-dessus du registre `pages`) instruit l'auteur : **consommer les tokens via `var(--…)`, ne jamais coder en dur couleur / espacement / typographie** — sinon l'auteur contourne la source unique de vérité que le couplage existe pour imposer. Le cadrage copie aussi, sans les reformuler, `policies.json § mode` et chaque règle valide de `usage.rules[]` (`id` + `description`). Cette copie rend le fichier autonome pour l'auteur sans créer un second producteur normatif : le contrat reste l'autorité et le harness ne dérive aucune règle.

## Grounding des pages et zones auteur

Les objets de `--pages-json` acceptent, en plus de `key`, `label` et `group`, trois champs chaîne optionnels : `route`, `source` et `theme`. Le bloc `CONTEXTE DES PAGES` les copie dans le commentaire LLM afin que l'auteur inspecte une preuve nommée au lieu d'inventer le contenu. Le registre `pageMetadata` conserve les mêmes valeurs au runtime ; avant chaque rendu, `theme` est appliqué comme `data-theme` sur `#page-container`, ou retiré si la page n'en déclare pas.

Le LLM ne reçoit plus l'instruction contradictoire de modifier « uniquement » une fonction tout en écrivant ailleurs dans le `<head>`. Deux zones auteur sont explicites : le corps de la fonction de page pour le HTML, et le bloc `AUTHOR PAGE STYLES` pour le CSS. Le registre, les métadonnées, le chrome et les scripts de contrôle restent hors édition.

## Espace de codes de sortie (tout le programme)

Le harness participe à l'espace fixe du plugin (`master § Exit-code space`) sur **tous** ses chemins, pas seulement sous `--contract`. Aucune entrée malformée ne remonte de traceback Python à l'appelant.

### Chemin contrat (`--contract`)

| Situation | Code | Message |
|---|---|---|
| Feuille inline, ou pas de flag | 0 | — |
| `--contract` mais aucun adapter `consumer:"stylesheet"` déclaré | 0 | un avertissement stderr, poursuite en scaffold |
| `release.json` **absent** (contrat 1.x) | 3 | nomme `tools/migrate-contract.py` |
| `release.json` présent mais **JSON invalide** | 2 | nomme `release.json` — un contrat corrompu n'est pas 1.x, seule l'absence l'est |
| `policies.json` absent, illisible ou pas un objet | 2 | nomme l'artefact |
| Adapter `stylesheet` déclaré, fichier **absent ou illisible** | 2 | nomme `tools/generate.py` comme correctif (option C : jamais de dérivation ici) |

### Chemin pages (`--pages` / `--pages-json`)

| Situation | Code | Message |
|---|---|---|
| Jeu de pages valide | 0 | — |
| `--pages-json` absent, illisible ou non-UTF-8 | 2 | nomme le chemin et la cause |
| `--pages-json` syntaxiquement invalide | 2 | nomme le chemin et l'erreur du parseur |
| `--pages-json` ni liste ni objet, ou objet sans liste `pages` | 2 | nomme le chemin |
| Entrée `--pages-json` qui n'est pas un objet, ou sans `key` de type chaîne | 2 | nomme l'**index** fautif |
| `group`, `route`, `source` ou `theme` présent mais non chaîne | 2 | nomme l'index et le champ fautif |
| Clé de page vide ou blanche | 2 | nomme l'index |
| Clé de page dupliquée | 2 | nomme la clé et les deux index |
| Deux clés dérivant le même nom de fonction (`my-page`/`my_page`, `A-b`/`a-b`) | 2 | nomme les deux clés et le nom dérivé |
| Clé ne dérivant pas un identifiant JS valide (`/contact/`, `blog/post`) | 2 | nomme la clé, le nom dérivé, et rappelle qu'une clé est un slug |
| Aucune page définie | 2 | `Error: no pages defined.` |

Une clé de page est un **slug**. La validation compare les **noms dérivés** par `key_to_fn`, jamais les clés brutes, et le test de validité est `key_to_fn(k).isidentifier()` : Python et JS suivent tous deux UAX-31, donc le test est plus strict que JS sans jamais l'être à tort — `café` passe, là où une regex ASCII le rejetterait. Le préfixe `page` interdit par construction toute collision avec un mot réservé. Sans cette validation, `--pages '/contact/:C'` écrivait `function page/contact/()` et sortait en **0** : un fichier mort livré en vert, dont l'oracle ne voit rien puisque `window.setPage` est posé par un autre `<script>` que celui qui meurt.

Le harness n'émet **jamais** 1 ni 4. Le chemin historique « aucune page » sort désormais en 2 (erreur d'invocation), non en 1. `3` est réservé à l'absence de `release.json` seule ; toute autre lecture en échec est un 2 ; `4` reste au seul `run-gates.py` (seuil de maturité).

## Trois échantillons device, jamais de media query

Le harness rend **trois vues discrètes par classe** — desktop (fluide) · tablet 834 · mobile 390 — basculées par `window.setViewport('desktop'|'tablet'|'mobile')`. Ce sont des **échantillons device**, pas des breakpoints : `834` et `390` sont des largeurs fixes, **rien n'est dérivé de `tokens.json § breakpoint.*`**. Le template ne contient **aucune media query** ; les variations d'auteur s'écrivent en classe (`.preview-frame.mobile <sel>` / `.preview-frame.tablet <sel>`).

## Accord measure / oracle — l'ensemble fermé de viewports

Deux valeurs se répondent de part et d'autre de la frontière, sans qu'aucune ne dérive de l'autre : le cadre s'anime en `transition: max-width .4s` (`harness.py:245`) et l'oracle attend `wait_for_timeout(400)` après la bascule (`measure.py:195`). Mesuré le 2026-08-05 : à t=400 ms la largeur mobile est stabilisée à 390 px — la valeur est juste, c'est son implicite qui ne l'était pas. Raccourcir la transition est sans risque ; l'allonger sans toucher à l'attente ferait mesurer un cadre en cours d'animation, silencieusement.

L'oracle de fidélité (`adapters/measure/measure.py`) pose la vraie largeur de contexte par breakpoint **et** bascule la classe du cadre via `setViewport` : les échantillons par classe sont exactement ce que l'oracle pilote déjà. `config-gen.py § _derive_breakpoints` stampe un `mockup_viewport ∈ {desktop, tablet, mobile}` — toute clé `tokens.breakpoint.*` hors de `_BP_MAP` est ignorée (`config-gen.py:110-112`), le nom est pris dans `_BP_MAP` (`:121-122`), et le fallback est mobile+desktop (`:55-56`). L'ensemble est donc **clos par construction**, pas une chose à vérifier au runtime, et il coïncide avec les trois échantillons exposés par le harness.
