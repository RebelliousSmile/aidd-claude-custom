# obs

*Gestion personnelle de notes Obsidian : arborescence `Documents/`, répertoires de contenu, projets Pro, tri des emails exportés.*

Plugin personnel orienté coffre Obsidian (conventions propres à l'auteur). Depuis la version 0.38.0, **tout le travail est fait par des scripts Python déterministes** : les skills ne décrivent plus une procédure à exécuter par le modèle, elles disent quelle commande lancer et ce qu'elle garantit. Aucun appel LLM n'est nécessaire pour trier, classer, indexer, fusionner ou archiver.

## Skills

| Skill | Déclencheur | Commandes |
|---|---|---|
| `tree` | `/obs:tree` | Organiseur de l'arborescence `Documents/`, piloté par un cache : `index`, `check`, `fix`, `sort`, `destinations` |
| `filler` | `/obs:filler` | Réduction continue d'un répertoire de contenu : `survey`, `sort`, `index`, `merge`, `clean` |
| `project` | `/obs:project` | Notes de projet de `Pro/Projets/` : `create`, `invoice`, `export-rag` |
| `mail` | `/obs:mail` | Tri des emails exportés selon `mail-config.yaml` : `triage`, `init-config` |

## Scripts

| Script | Rôle |
|---|---|
| `scripts/tree.py` | Cache d'arborescence, invariants I1–I4, dérive, placement, carte de routage |
| `scripts/filler.py` | Inventaire, regroupement, index de navigation, fusion, archivage |
| `scripts/project.py` | Création depuis gabarits, ligne de facture, export de contexte RAG |
| `scripts/mail.py` | Moteur de règles de tri du courrier, archivage daté |
| `scripts/obslib.py` | Socle commun : ancre, frontmatter, plan dry-run, intégrité des liens (utilisée par `filler`), garde-fous |
| `scripts/tests/test_obs_scripts.py` | Suite `unittest` (stdlib) sur fixtures temporaires |

Bibliothèque standard uniquement, Windows / Linux / macOS. Chaque commande est en **dry-run par défaut** : rien n'est écrit sans `--apply`.

```bash
python3 scripts/tree.py check ~/Documents/Perso/Finance
python3 scripts/filler.py survey ~/Documents/Pro/Projets/acme/2026/06
python3 -m unittest discover -s scripts/tests -v
```

## Ce que le plugin ne fait plus

Résumer, distiller, synthétiser un fil humain, rédiger une réponse, arbitrer le sens d'un contenu : ces opérations demandaient un jugement de lecture. Elles ont été retirées plutôt que simulées. Le socle mécanique reste, et il est vérifiable.

L'extraction de PDF est partie dans le plugin [`pdf`](../pdf/README.md).

## Licence

MIT — voir [LICENSE](../../LICENSE).
