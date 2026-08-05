---
objective: "Le cadre device mesure la largeur qu'il déclare, aucun harness dont le JS est mort ne passe au vert, et un contrat tiers ne peut plus exécuter de JS ni faire entrer un fichier arbitraire dans la maquette."
status: in-progress
---

# Plan: harness — les trois critiques

## Overview

| Field | Value |
| ----- | ----- |
| **Goal** | Fermer les trois 🔴 de l'audit du 05/08 sur le harness généré, puis rejouer la chaîne complète contre un WordPress FSE réel. |
| **Source** | `aidd_docs/tasks/2026_08/2026_08_05_audit-harness-genere/` — `ui.md` 🔴 (bezel), `tests.md` 🔴 (selftest aveugle au runtime), `security.md` 🔴 (`</style>` + traversée de chemin) |

## Phases

| # | Phase | File |
| --- | ----- | ---- |
| 1 | Le bezel sort du modèle de boîte | [`phase-1.md`](./phase-1.md) |
| 2 | Le fichier généré est exécuté, pas seulement grepé | [`phase-2.md`](./phase-2.md) |
| 3 | Le chemin `--contract` cesse d'accepter n'importe quoi | [`phase-3.md`](./phase-3.md) |
| 4 | La chaîne rejouée contre le bootstrap WordPress FSE | [`phase-4.md`](./phase-4.md) |

## Resources

| Source | Verified |
| ------ | -------- |
| `node:vm`, sans drapeau expérimental — `node --version` = **v23.4.0**, relevé | Prototype exécuté : les deux `<script>` du harness généré tournent dans un contexte vm contre un stub DOM de ~40 lignes, **sans aucune dépendance**. Sain → `setPage`/`setViewport` `function`, conteneur 151 caractères après `init()`, `setViewport('mobile')` pose la classe, clé inconnue → « Page introuvable ». Mort (accolade non fermée injectée) → `SyntaxError: Unexpected end of input`, exit 1. |
| `package.json` du dépôt | Aucune dépendance, aucun `node_modules` : `pnpm test` n'est que six scripts node. **Playwright n'est pas disponible ici** — une assertion navigateur headless est hors d'atteinte pour `pnpm test`, ce qui tranche la forme de la phase 2. |
| `aidd_docs/tasks/2026_08/2026_08_05-constat-bootstrap-wordpress-fse.md` | Le site scaffoldé était blanc (défaut n° 1), ce qui a fait renoncer à la confrontation `measure.py` (l. 70). Corrigé en `sc-php` 0.10.3 : la phase 4 peut désormais faire ce que le constat n'a pas pu faire. La même ligne 70 affirme « largeurs 390 / 834 / desktop fluide conformes » — c'est précisément la mesure que la phase 1 invalide. **Elle n'enregistre en revanche aucune valeur de verdict** : la ligne de base de comparaison n'existe pas et doit être fabriquée sur le site remonté, avant correctif (phase 4, tâche 2). |
| `plugins/design/adapters/measure/config-gen.py:54-67` | Les échantillons de l'oracle relevés dans la source, pas supposés : par défaut **mobile 375 × 812** et **desktop 1440 × 900** seulement ; **tablet 834 × 1194** n'existe que si le contrat déclare un token de breakpoint `tablet`/`md`. Conséquence directe : le mobile se mesure à **375**, pas à 390 — le `max-width: 390px` du cadre ne borne jamais pendant la mesure, c'est la scène qui contraint. Les critères d'acceptation de la phase 1 sont écrits en relation, pas en valeur absolue, à cause de cela. |
| `plugins/design/adapters/harness/fixtures/2x/policies.json` | Forme des fixtures de contrat (`release.json` + `policies.json` + `adapters/tokens.css`), reproduite telle quelle pour les deux fixtures de refus de la phase 3. |

## Decisions

| Decision | Why |
| -------- | --- |
| Le bezel devient un `outline`, pas un `padding` de compensation ni un wrapper | `outline` ne participe pas au modèle de boîte : `max-width: 390px` redevient 390 px de contenu sans toucher au reste de la CSS. Un wrapper ajouterait un nœud entre `.preview-frame` et `#page-container` que l'oracle et les sélecteurs d'auteur (`.preview-frame.mobile <sel>`) verraient. |
| `box-sizing: content-box` sur le seul cadre est rejeté, bien qu'il corrige aussi la boîte de contenu | Il porterait l'élément à 406 px pour un échantillon de 390 : dès que la fenêtre vaut la largeur de l'échantillon — le cas de mesure exact — le débordement devient **scrollable**, une barre apparaît et la boîte de contenu retombe sous la valeur visée. L'`outline` ne produit que du débordement d'encre. C'est le rival évident du correctif ; la raison du refus est écrite ici pour qu'il ne soit pas reproposé. |
| Contrepartie assumée : le bezel est écrêté quand la fenêtre vaut la largeur de l'échantillon | `.preview-stage` porte `overflow-y: auto`, donc l'axe horizontal calcule `auto` lui aussi et écrête l'encre débordante. Le bezel n'est peint qu'à fenêtre large — soit tous les usages humains, jamais les mesures. Aucune solution ne peut à la fois tenir la largeur d'échantillon et peindre un liseré extérieur dans une fenêtre de cette largeur. |
| Le sort du `2.9.1` non commité se tranche **avant** la phase 1 | L'arbre porte la passe de durcissement 2.9.1 non commitée. Soit elle est commitée telle quelle avant d'ouvrir ce lot, soit elle est absorbée dans 2.10.0 et son entrée CHANGELOG disparaît — sinon le CHANGELOG annonce une version qui n'a jamais existé. La règle du marketplace (bump et contenu dans le même commit, pas d'install sur un arbre sale) rend ce choix obligatoire. **Préalable au lot, pas une tâche du lot** : il se règle avant le premier commit de la phase 1 ; la phase 4 ne fait que vérifier qu'il l'a été. |
| Le contrôle runtime lit le **HTML généré**, pas un `control.js` source | Extraire le JS du template (constat 🟡 `code-quality`) ne couvrirait pas les parties interpolées — fonctions de page et registre — qui sont justement ce que le générateur fabrique. Lire la sortie prouve ce qui est livré, et laisse le refactor de template hors de ce lot. |
| Le contrôle runtime est en node stdlib, pas en navigateur headless | Playwright n'est pas une dépendance du dépôt et `pnpm test` n'en a aucune. Un stub DOM couvre le contrat exposé (`setPage`/`setViewport`/conteneur/classes) ; ce qu'il ne couvre pas — la **mise en page**, donc la largeur de contenu du cadre — est mesuré une fois au navigateur en phase 1 et rejoué en phase 4, pas à chaque `pnpm test`. |
| Version `2.10.0`, pas `2.9.2` | La géométrie du fichier produit change (les mesures device d'un même CSS ne rendent plus les mêmes valeurs) et le chemin `--contract` refuse désormais des entrées qu'il acceptait. Ce n'est pas un correctif silencieux. Le bump et le CHANGELOG partent dans le commit final, avec le contenu, conformément à la règle du marketplace. |
| Le 🟡 `#constructor` (registre exposé à `Object.prototype`) reste hors périmètre | La demande porte sur les trois 🔴. Le prototype de la phase 2 le reproduit déjà (`innerHTML` reçoit `[object Object]`) : une fois le contrôle runtime en place, c'est une assertion d'une ligne et un `Object.create(null)`. À décider après ce lot. |
