---
name: project
description: Manages Obsidian project notes stored in Pro/Projets — create a project from templates, add an invoice to commercial.md, export a RAG context file. Runs as a deterministic script, no model call. Use when the user invokes obs:project with a project management intent. Do NOT use for software architecture bootstrap — use `aidd-context:01-bootstrap` instead.
author: fxgui
version: 0.38.0
vibe_version: ">=1.0.0"
permissions:
  - files
  - bash
tags:
  - documentation
  - obsidian
  - notes
---

Read [host portability](../../references/host-portability.md) before resolving plugin files, invoking sibling skills, or persisting project guidance.

# Project

Manages project notes stored under the vault's `Pro/Projets/` directory: create a project from its templates, record an invoice, export a RAG context file.

Everything runs through `${OBS_PLUGIN_ROOT}/scripts/project.py`. Run the command, read its output, relay it.

## Model — communication → information

A project splits into two layers:

- **Dated communication (transient).** `Pro/Projets/<name>/YYYY/MM/` holds raw, dated content — emails and other documents. It is communication, not yet knowledge, and it decays.
- **Distilled information (durable).** The structural files (`projet.md`, `commercial.md`, `backlog.md`, …) hold the project's durable, classified knowledge.

Moving the first into the second requires reading and judging content; it is not scriptable and no longer lives here. For the mechanical half of the reduction — inventory, grouping, merging, archiving of a month directory — use `obs:filler` on `Pro/Projets/<name>/YYYY/MM/`.

## Commands

| Command | Role | Invocation |
| --- | --- | --- |
| `create` | Create the project folder and its template files | `python project.py create <nom> --type commercial\|open-source\|personnel [--apply]` |
| `invoice` | Append an invoice row to `commercial.md` and update the billing summary | `python project.py invoice <nom> --objet <texte> --montant <HT> [--date AAAA-MM-JJ] [--statut émise\|payée\|en attente\|annulée] [--apply]` |
| `export-rag` | Build a RAG context file from the project's structural files | `python project.py export-rag <nom> [--out <chemin>] [--apply]` |

`--anchor <chemin>` (default: the CWD) is the starting point for discovering `Pro/`.

## Default flow

- "new project", "create project", "crée le projet <nom>" → `create`
- "add invoice", "new invoice", "ajoute une facture" → `invoice`
- "export RAG", "export context", "project notes" → `export-rag`

Ask for the project name if it is not supplied. Always run without `--apply` first and show the plan.

## Ce que le script garantit

- **Projects root — discovered, never hardcoded.** The `Pro/` anchor is resolved by walking up from `--anchor`; the real vault lives under `Documents/`, not `Public/Notes/`.
- **Templates ship with the plugin.** They live at `references/projet-template/`, never in the vault.
- **Nothing without `--apply`.** No deletion, ever; an existing project is never overwritten.
- **Dates are `AAAA-MM-JJ` everywhere.**
- **No credentials in Markdown.** The `## Accès` section of `projet.md` carries `→ BW: <coffre> > <chemin>` references only — the vault path, never the secret.
- **`export-rag` reports what is missing.** A section still identical to its template counts as empty and is listed as such rather than exported as content.

## External data

- `${OBS_PLUGIN_ROOT}/scripts/project.py` — the implementation. `--help` on any subcommand.
- `references/projet-template/` — file templates per type (`projet.md`, `memory.md`, `backlog.md`, plus `commercial.md`/`communication.md`/`objectifs.md`).
