# Explain

Restitue la carte de l'entonnoir à la granularité demandée. Répond à *ce que c'est*, pas à *quoi lancer* (`02-route`).

## Inputs

- Une question descriptive sur le plugin.
- La cible de granularité, explicite ou déduite de la question : entonnoir entier · un verbe · une action · un gate · un artefact.

## Process

1. Résoudre la granularité. À défaut d'indice, restituer l'entonnoir entier.
2. Lire `${DESIGN_PLUGIN_ROOT}/skills/detail/references/funnel-map.md` et en extraire la tranche demandée — rôle, entrée, sortie, artefacts, état du contrat, gate.
3. Pour le **comment** d'un verbe (son processus), citer son fichier autoritaire au lieu de le paraphraser. La carte donne le quoi ; le processus appartient au `SKILL.md` du verbe (dec-001).
4. Pour un gate, renvoyer à `references/gate-natures.md` et `references/maturity-status.md` ; pour le squelette de plateforme, à `references/sc-pivot-contract.md`.

## Outputs

- La tranche de carte à la granularité demandée, chaque verbe cité avec le chemin de son fichier autoritaire.
- Aucun artefact écrit.

## Test

Demander « que fait `enforce` » rend la ligne `enforce` de la carte (rôle, entrée, sortie, artefacts, état, gate) **et** le chemin `skills/enforce/SKILL.md`, **sans** reproduire les étapes de son processus. Demander la carte sans cible rend les sept verbes, chacun une fois.
