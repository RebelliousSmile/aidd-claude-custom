---
objective: "Le plugin design expose une skill wireframes qui génère, normalise et valide des planches HTML comparables, puis promeut leurs pages acceptées vers le harness sans altérer les sources."
status: implemented
---

# Plan: Ajouter `design:wireframes`

## Overview

| Field      | Value |
| ---------- | ----- |
| **Goal**   | Livrer le contrat, les outils, les preuves et la publication de `design:wireframes`. |
| **Source** | [`../2026_09_01-design-wireframes-brief.md`](../2026_09_01-design-wireframes-brief.md) |

## Phases

| #   | Phase | File |
| --- | ----- | ---- |
| 1 | Contrat normatif et schéma du manifeste | [`phase-1.md`](./phase-1.md) |
| 2 | Skill publique, générateur et lint statique | [`phase-2.md`](./phase-2.md) |
| 3 | Contrôles visuels rendus | [`phase-3.md`](./phase-3.md) |
| 4 | Normalisation et promotion vers le harness | [`phase-4.md`](./phase-4.md) |
| 5 | Intégration au plugin et preuves comportementales | [`phase-5.md`](./phase-5.md) |
| 6 | Publication et régression complète | [`phase-6.md`](./phase-6.md) |

## Decisions

| Decision | Why |
| -------- | --- |
| Placer `wireframes` hors de l’entonnoir, avant `harness`, sans ajouter une septième classe de lifecycle | La capacité explore une interface et ne modifie aucun contrat de design ; les six classes existantes restent exhaustives sur le lifecycle du contrat. |
| Séparer le manifeste, le chrome canonique et les zones auteur | Le linter peut comparer les productions des LLM sans confondre leur contenu avec l’infrastructure de la planche. |
| Porter le contrat wireframe dans les références partagées du plugin avant d’enregistrer la skill | Le premier incrément reste cohérent et aucune action publique ne pointe vers un outil qui n’existe pas encore. |
| Exiger un lint statique puis un contrôle Chromium pour déclarer une sortie valide | Le manifeste et le DOM suffisent aux invariants structurels, mais les chevauchements, coupures et états réellement visibles exigent un moteur de rendu. |
| Normaliser dans un nouveau shell par applicateur gouverné | La source reste immuable et du HTML ou JavaScript arbitraire ne peut pas prendre possession du chrome de la planche. |
| Consigner l’acceptation dans un reçu détaché lié aux octets exacts de l’artefact | La planche examinée reste immuable et le handoff refuse tout reçu devenu périmé après modification. |
| Réutiliser les interfaces publiques du harness au lieu de dupliquer son shell | Le wireframe reste une source auteur ; le harness conserve seul ses pages, viewports, contrôles et preuves de migration. |
| Publier la capacité en `2.14.0` | Une nouvelle skill publique est une fonctionnalité rétrocompatible et relève d’un bump mineur. |
