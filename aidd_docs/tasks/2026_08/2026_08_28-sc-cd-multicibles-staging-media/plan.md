---
objective: "Les plugins sc-* décrivent et éprouvent plusieurs cibles staging ou production, server ou automata, avec une façade commune et des politiques sûres pour le code, le schéma, les données et les médias différentiels."
status: in-progress
---

# Plan: Étendre SC-CD aux cibles multiples et aux données persistantes

## Overview

| Field      | Value |
| ---------- | ----- |
| **Goal**   | Faire évoluer la livraison CD existante d'une cible de production unique vers des cibles nommées, indépendantes et gouvernées par surface. |
| **Source** | Brainstorm approuvé dans la conversation du 2026-08-28, fondé sur `C:\Users\fxgui\Documents\Code\Perso\DEPLOYMENT.md` et sur les cas Suddenly et Scriptami. |

## Phases

| # | Phase | File |
| --- | ----- | ---- |
| 1 | Contrat v2 multi-cibles et migration v1 | [`phase-1.md`](./phase-1.md) |
| 2 | Protocole différentiel pour données et médias | [`phase-2.md`](./phase-2.md) |
| 3 | Livraison Python éprouvée sur une topologie fédérée | [`phase-3.md`](./phase-3.md) |
| 4 | Livraison PHP et miroir WordPress de présentation | [`phase-4.md`](./phase-4.md) |
| 5 | Livraison JavaScript multi-cibles | [`phase-5.md`](./phase-5.md) |
| 6 | Releases Rust indépendantes | [`phase-6.md`](./phase-6.md) |
| 7 | Livraison statique multi-cibles | [`phase-7.md`](./phase-7.md) |
| 8 | Fournisseurs multi-cibles et passage server vers automata | [`phase-8.md`](./phase-8.md) |
| 9 | Preuves intégrées, runbook et distribution | [`phase-9.md`](./phase-9.md) |

## Resources

| Source | Verified |
| ------ | -------- |
| [rsync manual](https://download.samba.org/pub/rsync/rsync.1) | `--dry-run --itemize-changes` fournit un aperçu stable, `--delete` doit être gardé, `--checksum` compare le contenu au prix d'I/O disque et le transfert distant peut utiliser l'algorithme delta. |
| [GitHub Actions jobs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-jobs) | Une matrice peut exécuter la même enveloppe avec plusieurs paramètres de cible sans recopier la logique applicative. |
| [Railway CLI deployment](https://docs.railway.com/cli/deploying) | La CLI sait viser explicitement un service et un environnement ; ces identifiants peuvent rester des métadonnées de cible. |
| [alwaysdata SSH](https://help.alwaysdata.com/en/docs/web-hosting/remote-access/ssh/) | Alwaysdata fournit SSH/SFTP sans accès root ; les capacités effectives de transfert doivent rester profilées par cible. |
| [alwaysdata API](https://help.alwaysdata.com/en/docs/development/api/) | Le redémarrage d'un site est une action API distincte adressée par identifiant et authentifiée par un secret hors contrat. |

## Decisions

| Decision | Why |
| -------- | --- |
| Introduire un contrat projet v2 au lieu d'étendre silencieusement la v1. | La v1 impose une cible unique, seulement `production`, et autorise des flux `pull:*` incompatibles avec la topologie clarifiée. |
| Décrire chaque cible par un identifiant, une phase `staging` ou `production`, un mode `server` ou `automata`, un fournisseur et des opérations explicites. | Un même projet peut avoir plusieurs instances indépendantes, par exemple Railway automatisé et Alwaysdata manuel. |
| Garder une seule façade applicative et lui faire sélectionner la cible par une invocation déclarée. | Le passage de `server` à `automata` ne doit changer ni la procédure ni son verdict. |
| Gouverner séparément `code`, `schema`, `data` et `media`. | En production le code et les migrations viennent du local, alors que les données et médias appartiennent à chaque instance distante. |
| N'autoriser que des livraisons initiées par la façade du projet, depuis le workspace ou un checkout automatisé de la même source ; ne représenter aucune relation cible-à-cible. | Un automate doit pouvoir matérialiser le commit local publié sans qu'un serveur de destination devienne la source d'un autre. |
| Autoriser le miroir destructif des données et médias seulement en staging, après aperçu ; l'interdire en production. | Le staging reflète le local, tandis que la production peut recevoir des modifications de back-office qui doivent survivre aux livraisons. |
| Exiger un inventaire de contenu fiable et transférer seulement les éléments nouveaux ou différents. | Les médias inchangés ne doivent plus être renvoyés ; le coût accepté est le calcul ou la lecture d'empreintes. |
| Verrouiller les mutations par cible et non par projet entier. | Deux cibles indépendantes peuvent être livrées en parallèle, mais deux opérations concurrentes sur la même cible restent dangereuses. |
| Faire de la promotion staging vers production une transition fail-closed protégée par une révision de cycle de vie sur la cible. | Une ancienne enveloppe staging doit échouer au préflight même si elle est relancée depuis un ancien checkout. |
| Exiger la quiescence des écritures applicatives pendant une promotion sur place. | Le verrou de livraison seul n'empêche pas un utilisateur de modifier le back-office entre le dernier miroir et la bascule d'autorité. |
