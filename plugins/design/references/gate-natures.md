# Les deux natures de gate

Énoncé canonique. Toute affirmation sur ce que les gates garantissent renvoie ici et ne le réécrit pas.

Un contrat figé se vérifie contre deux références de natures différentes. Aucune ne remplace l'autre : elles ne répondent pas à la même question et ne peuvent pas se déduire l'une de l'autre.

| Gate | Oracle | Référence | Établit | N'établit pas |
|---|---|---|---|---|
| **Vocabulaire** | `lint-core.mjs` (Node, 5 règles dérivées du contrat) + import de la feuille de tokens | `tokens.json` · `components.json` · `policies.json` — **interne** | aucune classe ni référence de token hors contrat, **dans le markup effectivement passé au linter** | CSS, liaisons dynamiques, contenu stocké, fichiers de thème de plateforme, couverture des fichiers, rendu calculé |
| **Fidélité** | `measure.py` (`getComputedStyle`, par breakpoint) | la référence visuelle résolue par `adjust` — **externe** | style calculé conforme **sur les éléments mappés**, par breakpoint | tout élément non mappé, tout breakpoint non mesuré |

Le gate de vocabulaire est **aveugle au rendu calculé**. On peut être lint-vert et visuellement faux :

- le bon token existe et est « utilisé », mais le markup applique le **mauvais** ;
- une cascade ou une spécificité fait diverger la valeur **calculée** de l'intention ;
- aucune réduction responsive là où la référence en prévoit une.

Symétriquement, un rendu fidèle peut reposer sur un vocabulaire hors contrat, indétectable à la mesure.

**Ce que ni l'un ni l'autre ne couvre** : contraste, rôles ARIA, fond réellement appliqué, et tout fichier hors des cibles déclarées. Ce sont des **gaps déclarés**, pas des vérifications silencieuses.

Le gate de fidélité lit le registre d'écarts (`references/deviation-ledger-template.md`) pour distinguer un écart sanctionné d'une dérive.

**Quand la fidélité ne s'applique pas.** Sans référence visuelle externe, l'oracle n'a rien à mesurer et le gate de vocabulaire s'applique seul : limite énoncée dans `skills/enforce/actions/05-fidelity-gate.md § Chemin construction-depuis-brief`.
