# pdf

*Ingestion de sources PDF : découper un gros PDF et l'extraire en Markdown brut, session après session.*

Extrait du plugin `obs` le 2026-08-20 : l'extraction PDF ne dépend d'aucun coffre Obsidian et vit mieux seule.

## Skills

| Skill | Déclencheur | Description |
|---|---|---|
| `extract-pdf` | `/pdf:extract-pdf` | Pipeline multi-sessions d'extraction de gros PDF vers les sources brutes d'un domaine |

Le skill opère sur le modèle générique `references/domain-layout.md` (domaine `R`, buckets de travail `R/_<bucket>/`, `bank.yml`, `sources/` brut vs `reference/` synthétisé). Il produit **uniquement** la couche brute ; la ventilation vers la couche synthétisée est un rôle aval.

## Scripts

| Script | Rôle |
|---|---|
| `skills/extract-pdf/scripts/extract-pdf.py` | Orchestrateur multi-sessions (`--resume`, `--retry`, `--status`, `--distribute`, `--normalize`) |
| `skills/extract-pdf/scripts/split-pdf.py` | Découpage du PDF en chunks |
| `skills/extract-pdf/scripts/normalize-text.py` | Normalisation du texte extrait |

## Licence

MIT — voir [LICENSE](../../LICENSE).
