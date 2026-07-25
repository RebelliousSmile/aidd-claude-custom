# Deviation ledger — table-shape 1.x fixture (migration input)

> A ledger the project keeps as a single pipe table, not as `### DEV-NNN` fielded blocks.
> `migrate-contract.py --ledger` matches no heading here and reads 0 entries. The richer
> `deviations.json` beside this file is authoritative and must not be overwritten.

| Id | Élément(s) | Valeur maquette | Valeur contrat | Règle générale |
|----|-----------|-----------------|----------------|----------------|
| DEV-001 | card__title | fontSize 16px | fontSize 17px | échelle de corps fluide partagée |
| DEV-002 | card__lede | lineHeight 1.4 | lineHeight 1.5 | token de corps unique |
| DEV-003 | card | color #6b7280 | (en attente) | gris hors rampe, token de remplacement non choisi |
