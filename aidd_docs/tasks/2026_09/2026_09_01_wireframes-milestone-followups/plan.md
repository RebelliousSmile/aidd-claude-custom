---
objective: "Les 5 issues ouvertes de la milestone GitHub design:wireframes (#19-23) sont résolues et le SKILL.md référence l'étape wireframe de aidd-dev:01-plan."
status: implemented
---

<!-- Fill or omit these sections; never add, rename, or reorder one. -->

# Plan: Suites design:wireframes — milestone #19-23

## Overview

| Field      | Value                   |
| ---------- | ----------------------- |
| **Goal**   | Documenter l'environnement de rendu, clarifier la règle harness au normalize, enrichir les signaux d'inventaire (unités/transitions/annotations), documenter l'intake Artifact, et référencer l'étape wireframe du plan dans le routing SKILL.md |
| **Source** | GitHub issues #19, #20, #21, #22, #23 — milestone `design:wireframes`, repo `RebelliousSmile/my-claude-marketplace` |

## Phases

| #   | Phase        | File                         |
| --- | ------------ | ----------------------------- |
| 1   | Documentation — environnement de rendu, règle harness, routing plan | [`phase-1.md`](./phase-1.md) |
| 2   | wireframes-analyze.py — signaux d'inventaire enrichis | [`phase-2.md`](./phase-2.md) |
| 3   | Documentation — intake HTML issu d'un Artifact Claude | [`phase-3.md`](./phase-3.md) |

## Resources

<!-- External sources only (URLs, docs), not code files. Omit if none consulted. -->

| Source | Verified          |
| ------ | ----------------- |
| `gh issue view` #19-23 (repo `RebelliousSmile/my-claude-marketplace`) | Corps, labels et milestone de chacune des 5 issues |

## Decisions

<!-- Architecture-magnitude only, one you'd regret reversing. Omit if none qualify. -->

| Decision   | Why   |
| ---------- | ----- |
| #23 — `normalize` préremplit `harness.key`/`label`/`group` seulement quand la source nomme sans ambiguïté une route/écran ; laisse le bloc absent sinon | Le brief d'origine (`2026_09_01-design-wireframes-brief.md`) dit ces champs se remplissent « lorsqu'ils sont connus », sans les réserver à `promote` ; et `normalize` s'arrête déjà avant d'écrire sur toute ambiguïté sémantique (`wireframe-normalization.md`) — la même règle s'applique ici plutôt que d'inventer un slug |
| #20 — documentation seule pour l'intake Artifact, aucun strip automatique dans l'outillage | Le préambule frame-runtime est un chrome de visionneuse claude.ai non versionné, non contractuel ; l'automatiser reviendrait à faire dépendre `wireframes-analyze.py` d'une structure tierce non gouvernée, avec un risque de silence sur un mauvais découpage (chrome conservé ou contenu auteur tronqué) |
| #21 — pas de script d'installation dédié, seulement une référence documentant l'install standard (`pip install -r adapters/measure/requirements.txt` hors `--target /tmp`) + `WIREFRAMES_CHROMIUM` | L'install `/tmp` de l'issue est un contournement ad hoc, pas une contrainte de l'outillage ; documenter l'install standard supprime le besoin de `PYTHONPATH` plutôt que d'outiller le contournement |
