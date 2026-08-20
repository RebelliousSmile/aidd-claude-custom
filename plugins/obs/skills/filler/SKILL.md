---
name: filler
description: Manage content files in any directory — inventory, sort, index, merge, and clean. Runs as a deterministic script, no model call. Use when the user points to a folder and wants to triage, reorganize or consolidate its files. Do NOT use for structured Obsidian project lifecycle (use project), email triage (use mail), or Documents/ tree management (use tree).
author: fxgui
version: 0.38.0
vibe_version: ">=1.0.0"
permissions:
  - files
  - bash
tags:
  - obsidian
  - organization
  - notes
  - documentation
  - sorting
---

Read [host portability](../../references/host-portability.md) before resolving plugin files, invoking sibling skills, or persisting project guidance.

# obs:filler — Gestion de fichiers de contenu

Opère sur n'importe quel répertoire de fichiers de contenu : inventorier ce qui s'y trouve, le classer par entité, produire un index, fusionner une sélection, éliminer les entrées vides, redondantes ou obsolètes.

Tout passe par `${OBS_PLUGIN_ROOT}/scripts/filler.py`. Lancer la commande, lire sa sortie, la relayer. Ne pas refaire son travail à la main ni le doubler d'un tri manuel.

## Philosophie

L'objectif n'est pas l'organisation — c'est la **réduction continue**. Le contenu a un cycle de vie : ce qui est essentiel aujourd'hui devient superflu demain. Il n'existe pas d'état final « rangé ». Chaque passage doit laisser moins de fichiers et plus de signal ; un fichier qui survit à plusieurs passes a prouvé sa valeur.

Ce que la réduction demande de comprendre — résumer, distiller, synthétiser un fil humain — n'est pas scriptable et ne vit plus dans cette skill. Ce qui reste est le socle mécanique : inventorier, regrouper, indexer, concaténer, écarter.

## Commands

| Commande | Rôle | Invocation |
| --- | --- | --- |
| `survey` | Inventorier : nombre de fichiers, types, plage de dates, volume, signalements, triage recommandé | `python filler.py survey <répertoire> [--recursive]` |
| `sort` | Regrouper en sous-répertoires par entité, date, type ou sujet — assets co-déplacés | `python filler.py sort <répertoire> [--scheme entity\|date\|type\|topic] [--owner <email>] [--apply]` |
| `index` | Écrire un index de navigation (wikilinks groupés) au niveau `<Subcategory>` | `python filler.py index <répertoire> [--group-by thread\|sender\|date\|type] [--out <nom>] [--apply]` |
| `merge` | Concaténer une sélection en un document unique avec sommaire, sources intactes | `python filler.py merge <répertoire> [--glob <motif>] [--order date\|alpha] [--out <nom>] [--apply]` |
| `clean` | Écarter vides, doublons, périmés et orphelins — archivage par défaut | `python filler.py clean <répertoire> [--criteria empty,duplicate,old:AAAA-MM-JJ,orphan] [--delete] [--apply]` |

## Default flow

Point d'entrée par défaut : `survey`, sauf si l'utilisateur nomme explicitement une commande. `survey` termine par le triage recommandé (`clean`, `merge`, `keep`) pour chaque groupe qu'il a détecté.

| L'utilisateur dit | Commande |
|-------------------|----------|
| « inventorie / liste / qu'est-ce qu'il y a » | `survey` |
| « trie / classe / organise / range / par expéditeur » | `sort` |
| « indexe / crée un index / MOC / liste les liens » | `index` |
| « rassemble / fusionne / merge / consolide » | `merge` |
| « nettoie / supprime / archive / purge » | `clean` |
| (chemin seul, sans verbe) | `survey` |

Enchaînement usuel sur un répertoire neuf : `survey → sort entity → merge (groupes homogènes) → clean`.

Toujours lancer sans `--apply` d'abord et montrer le plan. Ne relancer avec `--apply` qu'une fois le plan vu et accepté.

## Ce que le script garantit

- **Portée limitée.** Seuls les fichiers directement dans le répertoire sont traités, sauf `--recursive` sur `survey`. Les fichiers et répertoires préfixés `_` sont du matériel de travail, jamais de la matière première.
- **Rien sans `--apply`.** Le plan est affiché, l'écriture attend le drapeau.
- **`clean` archive, il ne supprime pas.** Les fichiers écartés vont dans `<Subcategory>/_archive/` ; `--delete` est nécessaire pour détruire, et le script signale d'abord les fichiers qui pointaient vers la cible.
- **Pas d'écrasement silencieux.** Une cible occupée reçoit un suffixe numérique déterministe.
- **`merge` et `index` ne touchent jamais les sources.** `index` ne duplique aucun contenu : wikilinks et titres seulement.
- **Intégrité des liens.** Un déplacement réécrit les liens relatifs sortants, co-déplace l'asset référencé par un seul groupe, et laisse en place — en le signalant — celui que plusieurs groupes réclament.
- **Identifiants jamais lus.** Un fichier au nom de type `.env`, `credentials.*`, `*.key` voit son chemin signalé, jamais son contenu.
- **Médias jamais lus.** Images, audio et vidéo sont exclus de toute lecture de contenu.
- **Répertoire de travail.** Les fichiers produits (`index`, `merge`, `_archive/`) sont déposés au niveau `<Subcategory>` du tree quand il est reconnaissable, sinon dans le répertoire cible lui-même.

## External data

- `${OBS_PLUGIN_ROOT}/scripts/filler.py` — l'implémentation. `--help` sur chaque sous-commande.
- `${OBS_PLUGIN_ROOT}/references/email-md-format.md` — convention de nommage et frontmatter des emails convertis, exploitée par `sort`, `index` et `merge`.
