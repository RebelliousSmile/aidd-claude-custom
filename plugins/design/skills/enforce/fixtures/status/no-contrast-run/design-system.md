---
version: 1.0.0
---

# Charte — contrat utility-first (fixture no-contrast-run)

Charte présente mais aucune vérification de contraste enregistrée : `release.json § checks`
vaut `null`. `tools/status.py` fait monter le statut à `normalized` (charte présente) sans
pouvoir atteindre `validated`, faute de vérifications enregistrées — et le gap `contrast`
plafonne explicitement à `validated`.

## Inventaire des composants

Aucun composant nommé : ce contrat est utility-first, `components.json` est vide.
