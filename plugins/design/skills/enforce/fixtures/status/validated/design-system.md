---
version: 1.0.0
---

# Charte — contrat utility-first (fixture validated)

Charte présente et vérifications enregistrées : `release.json § checks` porte un contraste et
un contrôle d'états, tous deux exécutés. Le contraste échoue sur une paire — d'où un gap
`contrast` qui plafonne à `validated`. `tools/status.py` monte donc à `validated` (charte +
checks enregistrés), sans atteindre `production-ready`, faute de contraste vert partout.

## Inventaire des composants

Aucun composant nommé : ce contrat est utility-first, `components.json` est vide.
