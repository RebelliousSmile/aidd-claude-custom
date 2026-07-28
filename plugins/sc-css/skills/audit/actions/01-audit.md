# Audit

## Rôle

Analyser les fichiers CSS du projet sur les 5 dimensions et produire un rapport structuré.

## Procédure

### 01 — Spécificité

1. Parser les sélecteurs de tous les fichiers CSS. **Calcul de spécificité correct obligatoire** : `:where()` = 0 ; `:is()` / `:not()` / `:has()` = spécificité de leur argument le plus fort. Un parseur qui compte les segments à plat produit de faux conflits sur tout code moderne — et contredirait la dimension 05, qui recommande précisément ces sélecteurs. Sans ce calcul, n'émettre aucun finding de spécificité.
2. **`!important` — verdict conditionné à la topologie de layer _mesurée_, jamais supposée** :
   - Aucune `@layer` dans le projet, **ou** l'hôte émet des styles hors layer (à constater dans la feuille rendue, pas à présumer) → `!important` est un mécanisme d'override porteur : dans la cascade, `important-unlayered` et `important-layered` battent le `normal-unlayered`, lui-même prioritaire sur toute layer. Marquer `info`, **jamais `error`** : le retirer casserait l'override.
   - Projet intégralement layered **et** `!important` prouvablement redondant au vu de l'ordre réel des layers → `error`.
3. **ID (`#`) et profondeur > 3 → `warning` motivé** (pas `error`) : ni un ID ni une chaîne profonde ne sont un défaut en soi. **Exempter les sélecteurs que l'auteur ne possède pas** — id/classe injecté par l'hôte ou un tiers, absent des sources de markup du projet : on ne peut ni les renommer ni garantir qu'aucun override n'en dépend.
4. Séparer **haute spécificité** (pas un défaut : parfois voulue) de **conflit de spécificité** — le vrai signal : deux règles, même propriété, même cible, spécificités différentes qui se départagent. Marquer `warning` sur le conflit seul, en **nommant les deux règles**.

### 02 — Code mort

1. Collecter tous les sélecteurs CSS.
2. Cross-référencer contre les classes/IDs des **sources scannées** : `**/*.html`, `**/*.php`, `**/*.jsx/tsx`, `**/*.vue` (selon le projet).
3. **Ne jamais émettre le verdict `mort` / `unused`.** Un scan statique ne voit pas les classes composées à l'exécution (concaténation, interpolation), le contenu stocké (CMS, base de données) ni les noms calculés au runtime. Émettre au plus `info: non-référencé-dans-les-sources-scannées`, en **listant dans le finding le glob effectivement scanné** — la décision de retrait exige une preuve que l'audit read-only n'a pas.
4. **Exclure** tout fragment de classe apparaissant dans une concaténation / interpolation (`'grad--g' + n`, `` `card-${x}` ``) : il est *composé*, quel que soit le langage — le rapprocher d'un sélecteur littéral et le déclarer non-référencé est un faux positif.
5. **Précondition déclarée** : ce scan n'est fiable que si la surface de classes est entièrement littérale dans les sources scannées. Le constater et le déclarer dans le rapport ; ne pas le supposer.
6. `@keyframes` déclarées mais jamais référencées par `animation-name` dans les sources scannées → `info`.

### 03 — Magic numbers

1. Extraire les valeurs de propriétés (`color`, `background-color`, `font-size`, `margin`, `padding`, `gap`, `border-radius`, `box-shadow`).
2. Exclure les triviales — `var(--)`, `inherit`, `auto`, `0`, `100%`, `currentColor` — **et les littéraux structurels / relationnels** : ratios sans unité (`line-height`, `aspect-ratio`), `50%`, filets `1px`, composites multi-stop (`box-shadow`, dégradés), et tout résidu littéral à l'intérieur d'un `calc()` qui contient déjà une `var()`. Ce ne sont pas des tokens manquants.
3. Si `design/tokens.json` est présent, rapprocher **par rôle sémantique, pas par valeur brute** : un littéral ne se compare qu'aux tokens de la catégorie de sa propriété (couleur ↔ tokens couleur, espacement ↔ tokens espacement — `16px` de `margin` ne « viole » pas un token `font-size: 16px`).
   Le rapprochement admet une **tolérance de proximité** — un rayon autour de chaque token à l'intérieur duquel un littéral est réputé « aurait dû être ce token ». Le but est l'**uniformité** : des valeurs presque-égales éparpillées (`15px` / `16px` / `17px` là où l'échelle voulait un pas) donnent une UI mal réglée que l'égalité stricte laisserait invisible.
   - **Couleurs** : distance perceptuelle (CIEDE2000 / OKLab, jamais RGB brut). Rayon `ΔE ≤ 2` (écart imperceptible).
   - **Espacement / typographie** : rayon `±1px` **ou** `±3 %` du token, le plus grand des deux.

   Verdicts :
   - Littéral == un token de la bonne catégorie (`ΔE = 0` / valeur identique) → `warning: remplacer par var(--token)` — **rendu identique**, remplacement sûr (auto-applicable en aval).
   - Littéral **dans le rayon** mais ≠ token → `warning: proche de var(--token) — uniformité` — **le rendu changerait** (ex. `15px → 16px`) : à valider par un humain, jamais muté en silence. On ne prouve pas que c'est une faute ; on signale un défaut d'uniformité probable.
   - **Plusieurs tokens** dans le rayon → lister les candidats, **ne pas asserter** un seul remplacement (une même zone de valeur porte plusieurs intentions).
   - Littéral **hors de tout rayon** → `info` (« non tokenisé » — valeur distincte, one-off assumé). *Ce n'est pas une violation.*

   **Cette dimension n'émet jamais `error`.** Un littéral proche d'un token n'est pas *prouvablement* une faute (il peut être un choix délibéré) : le signal juste est `warning` (« regarde »), pas `error` (« c'est faux »). Réserver `error` au prouvable protège `improve` / `legacy` d'un faux positif mutable ; le garde-fou de rendu d'`improve` (« ne change pas le rendu sans le signaler ») empêche par ailleurs tout remplacement silencieux d'un littéral hors-token.

4. Si pas de contrat design : `info` sur toute valeur littérale non triviale et non structurelle — il n'existe aucune référence contre laquelle statuer, donc aucun `error` possible.

### 04 — A11y

1. **Contraste — ne calculer un ratio que sur des entrées résolues.** Le calcul WCAG exige : les deux couleurs résolues en littéral **opaque** (graphe de tokens résolu, aucune `var()` en attente), **appariées sur la même surface rendue** (le fond vit souvent sur un ancêtre et la couleur sur l'élément — l'appariement dépend de la cascade rendue, pas de la feuille seule), sous un **thème unique**.
   - Entrées résolues, opaques, appariées → ratio (luminance relative) : `error` < 4.5:1 (AA), `warning` < 3:1 (AA large). **Nommer le thème** sous lequel le ratio est calculé.
   - Couleur en `var()` non résolue, fond non apparié, alpha / dégradé / image, ou multi-thème → `info: contraste non calculable`, en listant ce qui manque. **Ne pas fabriquer de chiffre.** (Posture alignée sur le plugin design, qui déclare le contraste comme gap non vérifié.)
2. `outline: none` / `outline: 0` : l'alternative de focus se résout contre la **cascade globale**, pas contre le même sélecteur — une stratégie `:focus-visible` globale ou un anneau `box-shadow` déclaré ailleurs est correcte. En scan partiel (fichier par fichier), ne pas asserter l'absence → `info: vérifier la stratégie de focus globale`.
3. `animation` / `transition` : un reset `@media (prefers-reduced-motion: reduce)` global est le bon pattern et couvre tout le projet d'un bloc. En scan partiel, ne pas flaguer chaque animation parce que le reset vit ailleurs → `info: vérifier le reset de motion global`.

### 05 — Opportunités modernes

1. Patterns remplaçables par `:is()` / `:where()` : listes de sélecteurs identiques sauf un segment (`a:hover, button:hover, input:hover` → `:is(a,button,input):hover`).
2. Patterns remplaçables par `:has()` : combinaisons `parent + child` qui testent un état parent via JS classes (`.has-open-dropdown .menu` → `.menu:has(+ .dropdown[open])`).
3. Container queries : media queries qui testent la largeur viewport pour des composants réutilisés dans des contextes variables → candidats `@container`.
4. Nesting natif : blocs `.parent { ... } .parent .child { ... }` → `@nest` ou nesting CSS natif (si PostCSS).
5. Marquer `info` pour chaque opportunité — haut effort mais gain de maintenabilité.
