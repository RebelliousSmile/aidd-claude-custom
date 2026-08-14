---
objective: "Moderniser foresee et taste en déléguant leurs capacités redondantes aux skills AIDD actuelles, sans casser leurs points d’entrée Overcode ni perdre leurs apports propres."
status: implemented
---

# Plan: Moderniser foresee et taste par délégation AIDD

## Overview

| Field      | Value |
| ---------- | ----- |
| **Goal**   | Remplacer les analyses locales devenues redondantes par des délégations AIDD portables, tout en conservant l’horizon de dépendances de foresee et la fraîcheur documentaire de taste. |
| **Source** | Brainstorm de la conversation du 2026-08-14 et inspection des versions installées aidd-context 2.6.1, aidd-dev 2.4.1 et aidd-refine 2.2.4. |

## Phases

| #   | Phase | File |
| --- | ----- | ---- |
| 1 | Contrat commun de délégation AIDD | [`phase-1.md`](./phase-1.md) |
| 2 | Recentrage de foresee sur l’horizon de dépendances | [`phase-2.md`](./phase-2.md) |
| 3 | Recentrage de taste sur la fraîcheur documentaire | [`phase-3.md`](./phase-3.md) |
| 4 | Gardes, documentation et validation intégrée | [`phase-4.md`](./phase-4.md) |

## Decisions

| Decision | Why |
| -------- | --- |
| Conserver les invocations publiques `overcode:foresee` et `overcode:taste` comme routeurs. | Préserver les habitudes et les intégrations existantes tout en remplaçant l’implémentation obsolète. |
| Faire des skills AIDD actuelles l’autorité pour les audits de code, angles morts, challenge et fact-check. | Éviter deux moteurs concurrents et bénéficier des contrats AIDD désormais plus précis et maintenus. |
| Ne conserver localement que le risque prospectif de dépendance et la vérification documentaire contre le dépôt. | Ces deux capacités restent distinctes des surfaces AIDD installées. |
| Arrêter explicitement lorsqu’une skill AIDD requise est absente, sans réactiver l’ancien moteur local. | Une dégradation silencieuse recréerait immédiatement la dette supprimée. |
| Résoudre une capacité, pas une version ni un chemin de cache AIDD codé en dur. | Les packages AIDD continuent d’évoluer ; le contrat doit détecter leur catalogue installé et rendre toute incompatibilité visible. |
| Conserver la lecture seule des analyses Overcode, même lorsqu’une délégation AIDD possède un autre type de sortie. | Un routeur ne doit ni modifier silencieusement la cible ni fusionner des résultats dont les sémantiques diffèrent. |
| Rendre les choix ambigus interactifs plutôt que lancer plusieurs audits implicites. | Une question ciblée préserve l’intention et borne le coût des délégations. |
