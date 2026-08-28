---
objective: "sc-js:cd refuse de propager des permissions synthétiques DrvFs et détecte toute divergence entre le script de livraison et les preuves ou récupérations promises par son contrat."
status: in-progress
issue_number: 18
---

# Plan: Durcir sc-js:cd après un déploiement Windows réel

## Overview

| Field      | Value |
| ---------- | ----- |
| **Goal**   | Empêcher une façade JavaScript générée de publier des modes DrvFs dangereux ou un contrat de récupération devenu faux. |
| **Source** | GitHub issue [#18](https://github.com/RebelliousSmile/my-claude-marketplace/issues/18) — retour `cabinet-partage` Windows/WSL vers Linux mutualisé. |

## Phases

| #   | Phase | File |
| --- | ----- | ---- |
| 1 | Neutraliser les permissions synthétiques aux frontières Windows/WSL | [`phase-1.md`](./phase-1.md) |
| 2 | Vérifier la véracité comportementale de proof et recovery | [`phase-2.md`](./phase-2.md) |
| 3 | Distribuer et valider le correctif sc-js | [`phase-3.md`](./phase-3.md) |

## Resources

| Source | Verified |
| ------ | -------- |
| [Microsoft Learn — File Permissions for WSL](https://learn.microsoft.com/en-us/windows/wsl/file-permissions) | Sous DrvFs, les modes viennent des permissions Windows traduites ou de métadonnées WSL optionnelles ; ils ne sont pas une autorité Unix portable à recopier vers un serveur. |
| [Microsoft Learn — Working across file systems](https://learn.microsoft.com/en-us/windows/wsl/filesystems) | Les lecteurs Windows apparaissent sous `/mnt/<lettre>` dans WSL, ce qui permet de détecter cette frontière sans supposer le contenu des ACL. |
| [rsync(1)](https://download.samba.org/pub/rsync/rsync.1) | `-a` inclut `-p`; `--chmod` transforme les modes fournis à destination et peut distinguer répertoires (`D`) et fichiers (`F`). |

## Decisions

| Decision | Why |
| -------- | --- |
| Corriger l'adaptateur `sc-js:cd` sans modifier le schéma SC-CD v2. | Le contrat commun exige déjà des preuves observables ; les deux lacunes sont dans les instructions et vérifications du producteur JavaScript. |
| Traiter les modes DrvFs comme non fiables plutôt que d'affirmer qu'ils valent toujours `777`. | La documentation Microsoft montre que le résultat dépend des ACL Windows et des métadonnées WSL ; la sécurité vient de modes destination explicites, pas d'une valeur source supposée. |
| Accepter soit un artefact préparé dans un système de fichiers Linux natif, soit une normalisation explicite à destination. | Les deux stratégies rompent la propagation des modes synthétiques sans imposer une commande rsync unique à tous les projets. |
| Éprouver les décisions avec un profil et une trace normalisés, validés par un oracle déterministe. | Le skill doit relire le script et produire des observations vérifiables ; l'oracle peut alors tester les verdicts et l'ordre des événements sans prétendre analyser arbitrairement TypeScript. |
| Laisser `execSync` et la concaténation shell hors périmètre. | Le ticket ne démontre aucune injection active et classe ce point comme observation secondaire, distincte des deux manques prioritaires. |
