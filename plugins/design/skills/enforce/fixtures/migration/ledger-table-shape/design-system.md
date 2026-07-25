---
status: figé
version: 1.0.0
---

# Design system

## Provenance

Fixture de migration — classe de cas : **ledger en forme tableau**. Le projet tient son
registre de dérogations sous forme d'un unique tableau pipe (`ds-deviation-ledger.md`), pas
en blocs `### DEV-NNN` à champs. `migrate-contract.py --ledger` attend des blocs à en-tête :
il ne reconnaît aucun titre et lit **0 entrée** (`ENTRIES 0`). Un `deviations.json` déjà
présent, tenu à la main et **plus riche que toute sortie du parseur**, existe à côté. Lancer
l'écriture émettrait `{"active": []}` par-dessus lui — la perte d'une dérogation sanctionnée.
Résolution : la passe ledger n'est pas jouée ; le `deviations.json` existant fait autorité et
reste intact. La passe contrat ne le touche jamais (ni écrit par `split()`, ni copié dans la
sauvegarde). `deviations.json` est optionnel comme `oracle.json` ; ici il existe et vaut.

## Inventaire des composants

| Composant | Rôle |
|---|---|
| card | conteneur |
