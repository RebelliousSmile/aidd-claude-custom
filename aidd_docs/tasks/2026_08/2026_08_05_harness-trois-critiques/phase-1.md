---
status: done
---

# Instruction: le bezel sort du modèle de boîte

## Architecture projection

> Tree of the final files. ✅ create · ✏️ modify · ❌ delete

```txt
.
└── plugins/design/
    ├── adapters/harness/harness.py   ✏️ CSS l. 247-248 : border → outline, marges compensées
    └── tools/harness-selftest.sh     ✏️ +2 assertions sur la CSS produite
```

## User Journey

```mermaid
flowchart TD
  A[Auteur écrit .hero { padding-inline: 5% }] --> B[harness.py génère le cadre mobile]
  B --> C{Le bezel est dans la boîte ?}
  C -->|Avant : border 8px| D[Contenu 359 px au viewport 375<br/>padding mesuré 17,94 px]
  C -->|Après : outline 8px| E[Contenu 375 px au viewport 375<br/>padding mesuré 18,75 px = celui de la maquette]
  D --> F[measure.py : écart imputé à l'implémentation]
  E --> G[measure.py : conforme]
```

## Wireframe

```txt
AVANT — border participe à la boîte (box-sizing: border-box)
┌──────────────────────────────────────────┐
│▓▓▓▓▓▓▓▓▓▓▓▓ border 8px #1F2A37 ▓▓▓▓▓▓▓▓▓▓│  max-width: 390px
│▓┌──────────────────────────────────────┐▓│
│▓│  #page-container — 374 px            │▓│  ← ce que la CSS de l'auteur voit
│▓└──────────────────────────────────────┘▓│
└──────────────────────────────────────────┘
  |<----------- 390 px déclarés ----------->|

APRÈS — outline est peint hors de la boîte
   ▒▒▒▒▒▒▒▒▒▒ outline 8px #1F2A37 ▒▒▒▒▒▒▒▒▒▒     margin porté de 32 → 40
  ┌──────────────────────────────────────────┐   (32 + 8, gap visuel inchangé)
  │  #page-container — 390 px                │   max-width: 390px
  └──────────────────────────────────────────┘
  |<----------- 390 px déclarés ----------->|
```

## Tasks to do

### `1)` Remplacer la bordure du cadre par un `outline`

> Rendre à `max-width` la largeur qu'elle déclare, sans toucher au reste de la CSS.

1. `harness.py:247` (`.preview-frame.tablet`) : `border: 10px solid #1F2A37` → `outline: 10px solid #1F2A37`, `margin: 24px auto` → `margin: 34px auto`.
2. `harness.py:248` (`.preview-frame.mobile`) : `border: 8px solid #1F2A37` → `outline: 8px solid #1F2A37`, `margin: 32px auto` → `margin: 40px auto`.
3. Laisser `border-radius`, `overflow: hidden` et la transition `.4s` inchangés — l'`outline` suit le rayon, et rien d'autre ne dépend de la bordure.
4. Effet attendu, à ne pas « corriger » : le contenu était écrêté au rayon intérieur (32 − 8 = 24) et l'est maintenant au rayon déclaré (32). Les angles du contenu deviennent légèrement plus ronds. C'est cosmétique et conforme à un écran d'appareil.
5. Ne toucher aucune des trois occurrences documentaires — `SKILL.md:46`, `SKILL.md:145`, `references/harness-contract.md:49` : elles annoncent 834 / 390 comme **largeurs d'échantillon**, ce que le correctif rend enfin vrai de la boîte de contenu dès que la fenêtre est plus large que l'échantillon.

### `2)` Verrouiller la géométrie côté selftest

> Empêcher qu'une bordure revienne sur le cadre sans qu'un test le dise.

1. Ajouter une assertion : la CSS produite contient `outline: 8px` et `outline: 10px`.
2. Ajouter une assertion d'interdiction : aucune ligne `.preview-frame.tablet` / `.preview-frame.mobile` ne porte `border:` (le `border-radius` reste autorisé — cibler `border:` avec les deux-points).
3. Suivre la forme des assertions existantes (`check()` / `grep -q`), pas une nouvelle mécanique.

### `3)` Mesurer la boîte au navigateur, une fois

> Refaire la contre-épreuve de l'audit sur le fichier corrigé.

1. Générer une maquette 1 page portant `.hero { padding-inline: 5% }`.
2. Rejouer la séquence de `_prepare_mockup` (`setViewport('mobile')`, masquage `.preview-bar`, attente 400 ms) **à 375 × 812 — le viewport réel de l'oracle** (`adapters/measure/config-gen.py:55`), pas 390.
3. Relever `#page-container.clientWidth`, `getComputedStyle(.hero).paddingLeft`, `document.documentElement.scrollWidth`.
4. Refaire le relevé **à 1440 de large**, `setViewport('mobile')` : c'est le seul cas où le bezel est réellement peint, et donc le seul où sa visibilité se mesure.
5. Consigner les deux relevés dans le message de commit de cette phase — avec un commit par phase, la preuve d'une phase ne doit pas atterrir trois commits plus loin.

## Test acceptance criteria

| Task | Acceptance criteria |
| ---- | ------------------- |
| 1 | La boîte de contenu occupe toute la largeur disponible : à 375 de fenêtre, `#page-container.clientWidth === window.innerWidth` (375, pas 359) ; à fenêtre large, elle vaut **390** en mobile et **834** en tablet, pas 374 et 814. Le `max-width` ne borne qu'au-dessus de l'échantillon — à 375, c'est la scène qui contraint. |
| 1 | À CSS d'auteur identique, `paddingLeft` du `.hero` relevé dans le cadre mobile est **égal chaîne pour chaîne** à celui relevé sur la maquette de référence au même viewport — l'oracle n'a aucune tolérance. |
| 1 | À 1440 de fenêtre, le bezel est **peint** : capture d'écran du cadre montrant le liseré sombre sur les quatre côtés. `getComputedStyle(...).outlineWidth` ne suffit pas — il rend `8px` même quand `.preview-stage` écrête entièrement l'`outline`, ce qui arrive dès que la fenêtre vaut la largeur de l'échantillon. |
| 1 | `document.documentElement.scrollWidth` est égal à la largeur du viewport : l'`outline` n'introduit pas de défilement horizontal. |
| 2 | Réintroduire `border: 8px solid #1F2A37` sur `.preview-frame.mobile` fait échouer `bash tools/harness-selftest.sh` avec un code non nul. |
| 2 | `pnpm test` reste vert sur le générateur corrigé. |
| 3 | Les deux relevés — 375 × 812 et 1440 de large — sont écrits dans le message de commit de la phase, chacun avec son viewport et la CSS d'auteur utilisée. |
