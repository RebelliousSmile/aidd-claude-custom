---
objective: "Faire passer les défauts comportementaux L7 et S11 sans régression des routes AIDD, des recommandations taste ni du contrôle négatif S17."
status: in-progress
---

# Plan: Corriger les défauts behave de foresee et taste

## Overview

| Field      | Value |
| ---------- | ----- |
| **Goal**   | Compléter l'erreur de skill AIDD absente et dissocier regroupement inter-fichiers et seuil de réécriture documentaire, puis confirmer les deux correctifs par les suites behave existantes. |
| **Source** | Runs initiaux du 2026-08-14 dans `foresee/evals/legacy-flags-scenarios.md` (L7 FAIL) et `taste/evals/scan-boundaries-scenarios.md` (S11 FAIL réel, S17 contrôle négatif). |

## Phases

| #   | Phase | File |
| --- | ----- | ---- |
| 1 | Corriger les deux contrats et confirmer les bascules | [`phase-1.md`](./phase-1.md) |
