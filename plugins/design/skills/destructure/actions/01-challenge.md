# Challenge

Rethink une direction de design et l'ouvrir : critiquer ce qui est convenu, incohérent ou risqué, puis proposer des pistes d'évolution contrastées et actionnables. Lecture seule sur le contrat gelé et le code source — le rapport est persisté par défaut sous son propre chemin dédié.

## Inputs

- `target` (required) — entrée polymorphe, l'une de :
  - la **sortie de define** : `design/tokens.json` + `design/design-system.md` (brouillon) — mode entonnoir
  - un **élément existant isolé** : un chemin de composant (`design/components/card.md`), une page, un token set, ou un fragment d'UI en production — mode standalone
- Les lentilles de critique : `references/critique-lenses.md`.
- Le schéma de tokens : `${DESIGN_PLUGIN_ROOT}/references/token-schema.md`.
- L'adaptateur de contraste, lu en exécution : `${DESIGN_PLUGIN_ROOT}/adapters/a11y/contrast.py`.

## Process

1. **Cadrer la cible et le mode** :
   - Mode entonnoir → lire la matière de `define`.
   - Mode standalone → lire l'élément ciblé. **Si un contrat figé existe** (`design/release.json` et les artefacts qu'il déclare, plus `design/design-system.md`), le lire d'abord pour situer chaque piste : rentre-t-elle dans le vocabulaire du contrat actuel, ou demande-t-elle un re-figeage par `adjust` ?
2. **Mesurer avant de juger** (hérité d'ex-diagnose, sur un existant) : valeurs distinctes et sprawl (couleurs, tailles de police, espacements, breakpoints), densité de valeurs en dur vs tokens, doublons de composants, emoji-comme-icônes. Rapporter des comptes, pas des impressions.

2-bis. **Calculer les contrastes, ne pas les apprécier.** Dès que des tokens couleur existent, lancer l'adaptateur du figeage — le même, jamais une seconde implémentation du ratio WCAG :
   ```
   python ${DESIGN_PLUGIN_ROOT}/adapters/a11y/contrast.py --contract design/ --json --allow-unpaired
   ```
   `--allow-unpaired` est ici la bonne conduite et non une dérogation : cette action ne fige rien, elle constate. Lecture seule respectée — l'adaptateur n'écrit pas.

   Trois lectures, dans cet ordre :
   - **des paires échouent** → chacune est une trouvaille chiffrée : `<fg> sur <bg> @ <thème> = <ratio>`, à classer `risque-a11y` avec son ratio, jamais « risque de ne pas tenir ».
   - **`coverage.unpaired` non vide** → nommer les branches concernées et leur compte. Une couleur non appariée n'est pas une couleur sûre, c'est une couleur que personne n'a regardée.
   - **aucune paire du tout** (`results` vide) → c'est la trouvaille la plus forte que cette action puisse produire, et la seule qui ait une date de péremption : `adjust/02-freeze` **refusera** de figer dans cet état (`${DESIGN_PLUGIN_ROOT}/skills/adjust/references/manifest-schema.md § Invariant 7`). En mode entonnoir c'est l'état normal — `components.json` n'existe pas encore — et la piste attendue est alors **la liste des appariements à déclarer** : pour chaque composant pressenti, quels chemins portent du texte sur quels fonds. C'est la matière que `.foregrounds` demandera, produite au moment où elle ne coûte encore rien.

   Sans tokens couleur résolubles, dire que le volet n'a pas tourné et pourquoi. Ne jamais rendre un avis de contraste à la place d'un ratio.
3. **Passer les lentilles** de `references/critique-lenses.md` sur la direction :
   - **Générique vs distinctif** — quoi de convenu, de "stock framework" ; où la personnalité ne transparaît pas.
   - **Cohérence interne** — tokens qui se contredisent, rythme d'espacement irrégulier, échelle de type bancale.
   - **Accessibilité** — les ratios de l'étape 2-bis (mesurés, jamais estimés), cibles tactiles, focus, emoji porteurs de sens.
   - **Tendances & fraîcheur** — où la direction date, où elle suit une mode fragile.
   - **Divergence d'inspiration** — quelles autres références/familles visuelles ouvriraient un autre territoire.
4. **Générer 2–4 pistes contrastées par axe critiqué** : chaque piste nomme une inspiration ou un principe directeur concret, l'effet attendu, et le coût (rentre dans le contrat actuel / demande un re-figeage). Diverger, ne pas trancher.
5. **Classer** chaque trouvaille : `générique` / `incohérent` / `risque-a11y` / `occasion-manquée`.
6. **Scorer** la distinction de la direction (voir Outputs) et donner un verdict d'une ligne : la piste la plus à fort levier.
7. **Écrire le rapport (par défaut)** sous `design/critique/<yyyy_mm_dd>-<cible>.md`, sauf opt-out explicite (`--no-write` ou "ne sauvegarde pas") — voir Outputs.

## Outputs

Un rapport structuré, remis dans la conversation **et écrit par défaut sur disque** — squelette : `references/critique-report-template.md`.

- **Chemin canonique** : `design/critique/<yyyy_mm_dd>-<cible>.md` (historique daté, un fichier par exécution, jamais d'écrasement). `<cible>` est un slug dérivé de l'élément critiqué (nom de composant, de page, ou `design-system` en mode entonnoir).
- **Alias rétrocompatible** : `design/destructure-report.md` reste un chemin accepté en lecture pour les rapports antérieurs à cette convention ; ce n'est plus le chemin d'écriture.
- **Opt-out explicite** : `--no-write`, ou une demande explicite ("ne sauvegarde pas") — le rapport reste alors conversationnel uniquement.
- **Réconciliation lecture seule** : cette écriture ne contrevient pas à l'invariant — `destructure` n'édite jamais un artefact du contrat, `release.json`, `design-system.md` ni le code source ; le rapport de critique est un artefact séparé, non-contractuel (cf. `${DESIGN_PLUGIN_ROOT}/references/design-system-contract.md`).

```text
Score de distinction : XX/100

# Cible & mode
# Mesures (sprawl, densité, doublons, emoji)   ← si existant
# Contrastes mesurés (paires échouées avec ratio · couverture : appariées / déclarées · non appariées par branche)
# Critique par lentille
  - Générique vs distinctif
  - Cohérence
  - Accessibilité
  - Tendances
  - Inspiration
# Pistes d'évolution (2–4 par axe, contrastées, actionnables, avec coût contrat)
# Verdict : la piste à plus fort levier
```

## Test

Le rapport ne modifie jamais un artefact du contrat, `release.json`, `design-system.md` ni le code source ; par défaut il est écrit sous `design/critique/<yyyy_mm_dd>-<cible>.md`, sauf opt-out explicite (`--no-write` / "ne sauvegarde pas", auquel cas il reste conversationnel uniquement) ; il accepte les deux entrées (sortie define ET élément existant) ; en standalone sur un projet figé, le manifeste/charte ont été lus et chaque piste indique si elle rentre dans le contrat ou demande un re-figeage ; chaque piste est actionnable (inspiration/principe nommé, pas un vœu) ; un score de distinction et un verdict à fort levier sont présents ; l'emoji-comme-icône est signalé s'il existe ; dès que des tokens couleur existent, la section contraste porte des **ratios issus de `contrast.py`** et la couverture appariées/déclarées — un avis de contraste sans chiffre est un échec de cette action, et zéro paire appariée est rapporté comme le refus de figeage à venir, accompagné de la liste des appariements à déclarer.
