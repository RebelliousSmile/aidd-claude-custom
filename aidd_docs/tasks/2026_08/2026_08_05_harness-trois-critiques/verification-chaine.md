# La chaîne rejouée contre un WordPress FSE réel

> Phase 4. Deux passes de l'oracle de fidélité sur **le même site**, **le même balisage**,
> **le même contrat** : seul le générateur de maquette change entre elles. C'est ce qui rend
> l'écart imputable au correctif et à rien d'autre.

## Terrain

| Élément | Valeur |
| ------- | ------ |
| Racine jetable | `C:\Users\fxgui\Documents\LLM\_fse-harness` (hors dépôt) |
| Scaffold | flow `sc-php:setup` `01 → 02 → 06`, substitutions littérales |
| `COMPOSE_PROJECT_NAME` | `fse-harness` (dérivé du dossier, posé dans `start/stop/wp.ps1`) |
| WordPress | 7.0.2 · port 8893 · `phpVersion` 8.2 |
| Thème actif | `wp_get_theme()->get_stylesheet()` → `fse-harness` (pas `twentytwentyfive`) |
| Porte d'entrée | `.wp-site-blocks` présent · `document.body.innerText.trim().length > 0` → vrai |
| Page mesurée | `http://localhost:8893/fidelite/` — le balisage partagé en `wp:html` |
| Voisinage | le projet Docker `code-*` (ports 8514 / 8889) n'a pas été touché |

## Contrat

Le plugin `design` ne livre **aucune fixture de contrat complet** : `adapters/measure/` ne
contient que `configs/example.json` et un test de normalisation couleur. Le contrat de cette
vérification a donc été écrit pour l'occasion, hors dépôt
(`<scratchpad>/p4/contract/`) : `tokens.json`, `components.json`, `policies.json`,
`release.json`, `deviations.json`, plus l'adaptateur `adapters/tokens.css` **produit par
`tools/generate.py`** — jamais dérivé par le harness (option C).

Les tokens déclarent `breakpoint.mobile` / `breakpoint.tablet` / `breakpoint.desktop`. C'est
ce qui décide du nombre d'échantillons, cf. `adapters/measure/config-gen.py:54-67` : sans token
`tablet`/`md`, l'oracle n'aurait posé que mobile et desktop.

**Échantillons effectivement produits — relevés, pas supposés : 3.**

| Échantillon | Fenêtre oracle | `mockup_viewport` | Largeur d'échantillon côté maquette |
| ----------- | -------------- | ----------------- | ----------------------------------- |
| mobile | 375 × 812 | `mobile` | 390 px |
| tablet | 834 × 1194 | `tablet` | 834 px |
| desktop | 1440 × 900 | `desktop` | fluide |

Le config oracle porte **7 cibles** (2 racines de composant + 5 éléments BEM) × **18 propriétés**
× 3 échantillons = 126 comparaisons par échantillon.

## Commandes

```bash
# Contrat → adaptateur stylesheet (le même fichier alimente les deux côtés)
python plugins/design/tools/generate.py --contract <sp>/p4/contract

# Générateur AVANT correctif — extrait hors dépôt, l'arbre n'est pas touché
rtk git show 7c7997f:plugins/design/adapters/harness/harness.py > <sp>/p4/gen-avant/harness.py

# Les deux maquettes, mêmes arguments, remplissage identique par <sp>/p4/fill.py
python <sp>/p4/gen-avant/harness.py            --out <sp>/p4/site-avant/index.html \
  --title "Chaine phase 4" --lang fr --pages "home:Accueil" --contract <sp>/p4/contract
python plugins/design/adapters/harness/harness.py --out <sp>/p4/site-apres/index.html \
  --title "Chaine phase 4" --lang fr --pages "home:Accueil" --contract <sp>/p4/contract

# Config oracle, un par référence — l'implémentation est la même URL des deux côtés
python plugins/design/adapters/measure/config-gen.py \
  --components <sp>/p4/contract/components.json --tokens <sp>/p4/contract/tokens.json \
  --reference-url http://127.0.0.1:8791/site-avant/index.html \
  --implementation-url http://localhost:8893/fidelite/ --page home --out <sp>/p4/config-avant.json

# Les deux passes
python plugins/design/adapters/measure/measure.py --config <sp>/p4/config-avant.json \
  --ledger-registry <sp>/p4/contract/deviations.json --out <sp>/p4/report-avant.json
python plugins/design/adapters/measure/measure.py --config <sp>/p4/config-apres.json \
  --ledger-registry <sp>/p4/contract/deviations.json --out <sp>/p4/report-apres.json
```

`7c7997f` est le parent du commit de la phase 1 (`8c3b26b`). L'extraction s'est faite par
redirection vers un fichier hors dépôt : `git status` ne montre **aucune entrée sous
`plugins/design/`** après l'opération.

Le seul écart entre les deux fichiers HTML générés est la règle du bezel — 10 lignes de `diff`,
toutes dans le bloc `.preview-frame.tablet` / `.preview-frame.mobile` et son commentaire.

## Passe « avant » — générateur `7c7997f`

```
mobile   : 122 match · 4 diff · 0 ledgered · 0 missing
tablet   : 122 match · 4 diff · 0 ledgered · 0 missing
desktop  : 126 match · 0 diff · 0 ledgered · 0 missing
VERDICT  : OPEN — 8 unledgered style diff(s)
```

| Échantillon | Cible | Propriété | Maquette | Implémentation |
| ----------- | ----- | --------- | -------- | -------------- |
| mobile | Hero · Card | `paddingLeft` / `paddingRight` | `17.9375px` | `18.75px` |
| tablet | Hero · Card | `paddingLeft` / `paddingRight` | `40.6875px` | `41.6875px` |
| desktop | — | — | aucun écart | aucun écart |

## Passe « après » — générateur `HEAD` (`53be804`, phases 1-3 appliquées)

```
mobile   : 126 match · 0 diff · 0 ledgered · 0 missing
tablet   : 126 match · 0 diff · 0 ledgered · 0 missing
desktop  : 126 match · 0 diff · 0 ledgered · 0 missing
VERDICT  : CLOSED
```

## Verdict comparé

| Échantillon | Avant | Après | Écart |
| ----------- | ----- | ----- | ----- |
| desktop | 126 match · 0 diff | 126 match · 0 diff | **identique** — l'échantillon desktop n'a pas de bezel, le correctif n'y touche pas |
| mobile | 4 diff | 0 diff | `paddingLeft/Right` 17.9375 → **18.75 px**, la valeur de l'implémentation |
| tablet | 4 diff | 0 diff | `paddingLeft/Right` 40.6875 → **41.6875 px**, la valeur de l'implémentation |
| global | `OPEN` | `CLOSED` | 8 écarts non registrés → 0 |

### Explication de chaque écart

Les seules propriétés qui bougent sont dérivées d'un pourcentage de largeur — le balisage
partagé pose `padding-left/right: 5%` sur `.hero` et `.card` précisément pour cela. Aucune
propriété absolue (`fontSize`, `color`, `borderRadius`, `boxShadow`, `transitionDuration`…)
ne diffère entre les deux passes : le correctif ne déborde pas.

L'écart mesuré vaut exactement le bezel retiré de la boîte de contenu :

| Échantillon | Bezel | Largeur amputée | 5 % de l'amputation | Delta mesuré |
| ----------- | ----- | --------------- | ------------------- | ------------ |
| mobile | 8 px × 2 | 16 px | 0.8 px | `18.75 − 17.9375` = **0.8125 px** |
| tablet | 10 px × 2 | 20 px | 1 px | `41.6875 − 40.6875` = **1 px** |

`border` + `box-sizing: border-box` rabotait la boîte de contenu de l'échantillon : 390 − 16 = 374
et 834 − 20 = 814. L'oracle facturait la différence à une implémentation conforme. `outline` est
de l'encre pure, hors du modèle de boîte : la boîte de contenu retrouve la largeur de
l'échantillon, et les valeurs dérivées d'un pourcentage coïncident au caractère près — l'oracle
compare des chaînes normalisées, sans tolérance.

## Réserves

- Le contrat de cette vérification a été écrit pour la mesure : il est minimal, et la conformité
  `CLOSED` obtenue n'atteste que de cette page, pas d'un projet réel.
- Le balisage partagé neutralise la contrainte de layout FSE (`main.wp-block-group`,
  `.wp-block-post-content` → `max-width: none`). Sans cela, la boîte de référence de
  l'implémentation vaut `contentSize` (720 px) et les deux côtés mesurent des pourcentages de
  largeurs différentes — un écart de contrat, pas de générateur.
- Le remplissage de page vise la déclaration **réelle** de `pageHome`, qui émet des guillemets
  doubles ; les exemples en commentaire du fichier généré en émettent des simples. Viser les
  simples remplit la documentation et laisse la page vide : l'oracle rend alors 21 cibles
  `missing`, ce qui a été observé au premier essai.
