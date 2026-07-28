# Critique — <cible>

Squelette canonique du rapport persisté par `destructure/actions/01-challenge.md`. Chemin d'écriture : `design/critique/<yyyy_mm_dd>-<cible>.md`. Non-contractuel — cf. `references/design-system-contract.md`.

- **Date** : <yyyy-mm-dd>
- **Cible** : <chemin ou description de l'élément critiqué>
- **Mode** : entonnoir | standalone
- **Score de distinction** : XX/100

## Mesures

<sprawl (couleurs, tailles de police, espacements, breakpoints), densité de valeurs en dur vs tokens, doublons de composants, emoji-comme-icônes — uniquement en mode standalone sur un existant ; des comptes, pas des impressions>

## Contrastes mesurés

Sortie de `adapters/a11y/contrast.py` (`01-challenge.md § étape 2-bis`), reportée telle quelle. Des ratios, jamais un avis.

| Thème | Origine | Avant-plan | Fond | Ratio | AA |
|---|---|---|---|---|---|
| <thème> | <composant> \| (rôle) | <token.path> | <token.path> | <n.nn> | ✅ \| ❌ |

**Couverture** : <appariées>/<déclarées> feuilles couleur — non appariées par branche : <branche n, …>

<Si zéro paire : le dire ici en toutes lettres. Ce n'est pas un contraste à améliorer, c'est un contrôle impossible, et `adjust/02-freeze` refusera de figer. La table ci-dessous devient alors la sortie principale du rapport.>

### Appariements à déclarer

Un composant par ligne : ce que `components.json § .foregrounds × .backgrounds` devra porter au figeage. Produit ici parce qu'ici il ne coûte encore rien.

| Composant | Fonds | Avant-plans |
|---|---|---|
| <nom> | <token.path, …> | <token.path, …> |

## Critique par lentille

### Générique vs distinctif

<quoi de convenu, de "stock framework" ; où la personnalité ne transparaît pas>

### Cohérence interne

<tokens qui se contredisent, rythme d'espacement irrégulier, échelle de type bancale>

### Accessibilité

<lecture des ratios de la section « Contrastes mesurés » — ne pas les répéter, en tirer les conséquences de direction ; cibles tactiles, focus, emoji porteurs de sens ; risques non mesurables (opacity, color-mix, voiles, dégradés) nommés et renvoyés à G6>

### Tendances & fraîcheur

<où la direction date, où elle suit une mode fragile>

### Divergence d'inspiration

<quelles autres références/familles visuelles ouvriraient un autre territoire>

## Pistes d'évolution

- **<nom de la piste>** — inspiration/principe : <...>. Effet attendu : <...>. Coût contrat : `rentre dans le contrat` | `demande un re-figeage`.

## Verdict

<la piste à plus fort levier, une ligne>
