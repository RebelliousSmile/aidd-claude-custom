---
objective: "Un thème WordPress FSE produit par sc-php doit charger les styles issus du contrat design et prouver que chaque propriété déclarée par les feuilles de composant DS est effectivement gouvernée par ce composant sur le front et dans l’éditeur."
status: implemented
---

# Plan: Gouvernance de cascade design dans WordPress FSE

## Overview

| Field      | Value |
| ---------- | ----- |
| **Goal**   | Fermer les écarts de routage, de rendu natif et de vérification qui permettent aux styles core WordPress de gagner malgré la présence des classes DS. |
| **Source** | Audit utilisateur du 2026-08-14 : compatibilité des règles de création WordPress FSE de `sc-php` avec le plugin `design`. |

## Phases

| #   | Phase | File |
| --- | ----- | ---- |
| 1   | Router un rendu FSE composite vers PHP et CSS | [`phase-1.md`](./phase-1.md) |
| 2   | Corriger le scaffold et le rendu natif FSE | [`phase-2.md`](./phase-2.md) |
| 3   | Prouver la propriété réelle de la cascade | [`phase-3.md`](./phase-3.md) |
| 4   | Verrouiller les régressions et publier les contrats alignés | [`phase-4.md`](./phase-4.md) |

## Decisions

| Decision | Why |
| -------- | --- |
| Un rendu FSE est un artefact composite routé vers `sc-php` pour le markup/runtime et vers `sc-css` pour les feuilles. | Faire générer le CSS par `sc-php` violerait la frontière existante « langage de la preuve » ; ne router que PHP laisse les classes DS sans réalisation CSS garantie. |
| Le gate de cascade vérifie la déclaration gagnante dans un navigateur réel, en plus du lint statique. | La présence d’une classe et la valeur calculée ne prouvent pas que le composant DS gouverne la propriété ; presets, styles inline, `!important`, layers et sélecteurs core ne se départagent qu’après composition réelle. |
| La surface des propriétés gouvernées est dérivée des déclarations réellement émises dans les feuilles de composant DS, complétées par les hints optionnels d’`oracle.json`. | `components.json` décrit l’anatomie, pas les propriétés ; lui ajouter ce rôle élargirait inutilement le contrat et dupliquerait la feuille qui porte déjà la réalisation. Une feuille sans déclaration ne peut pas produire un faux pass : sa preuve reste non réalisée. |
| La preuve d’ownership étend le verdict de fidélité existant au lieu de créer une règle `pivotReports`. | Le contrat connaît déjà le gate de fidélité et `measure.py` en calcule le verdict ; un rapport de pivot sans règle `policies.json` correspondante serait rejeté comme preuve non déclarée. |
| Les classes DS restent sur le bloc natif et l’adaptateur FSE traduit les blocs à élément peint interne par des sélecteurs hôtes connus. | `core/button` et `core/navigation-link` ne placent pas nécessairement `className` sur l’ancre réellement peinte ; le manifeste reste agnostique et le mapping appartient à la plateforme. |
| `sc-php` produit l’adapter `fse-bindings.css`; `sc-css` produit les styles génériques et contrôle toutes les feuilles chargées, adapter compris. | Le binding dépend du DOM WordPress et appartient donc au pivot de plateforme, tandis que sa conformité statique reste une preuve de langage CSS. Cette séparation évite deux producteurs sur un même fichier. |
| Le wrapper `pnpm wp` devient l’unique accès WP-CLI de toute la chaîne `sc-php`. | Le scaffold garantit `COMPOSE_PROJECT_NAME`; une commande wp-env nue contourne cette garantie et peut viser un service CLI introuvable. |
