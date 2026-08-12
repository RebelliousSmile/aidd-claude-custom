---
status: done
---

# Phase 1 — Packaging Codex portable

## Travail

- Ajouter le manifeste `.codex-plugin/plugin.json` sans retirer le manifeste Claude.
- Aligner identité, version et description entre les deux manifestes et la marketplace.
- Normaliser les frontmatters des sept skills au sous-ensemble Codex portable.
- Documenter et vérifier le socle AIDD installé : context, dev et refine.

## Acceptation

- `validate_plugin.py plugins/design` sort en 0.
- `quick_validate.py` sort en 0 sur les sept skills.
- La garde de cohérence détecte toute dérive entre les deux manifestes et la marketplace.
