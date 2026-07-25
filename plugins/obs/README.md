# obs

*Gestion personnelle de notes Obsidian : projets Pro, tri des emails, organisation de l'arborescence `Documents/`, recherche documentaire et ingestion de sources.*

Plugin personnel orienté coffre Obsidian (chemins et conventions propres à l'auteur).

## Skills

| Skill | Déclencheur | Description |
|---|---|---|
| `project` | `/obs:project` | Gestion des projets Pro (**communication → information**) : create, fill, reorganize, log-session, log-meeting, add-invoice, **distill**, export-rag |
| `mail` | `/obs:mail` | Trie, résume, fusionne et classe les emails exportés en Markdown dans le coffre — plus `reply` (information → communication) : rédige un brouillon de réponse assisté, jamais envoyé |
| `tree` | `/obs:tree` | Organiseur de l'arborescence `Documents/`, piloté par un **cache** (pas de layout figé) : index, check, fix, sort (tri par arbitrage), judge (arbitrage interactif nœud par nœud), destinations (export de la carte de routage pour `email-to-markdown`) |
| `filler` | `/obs:filler` | Gestion de fichiers de contenu dans n'importe quel répertoire — réduction continue : survey, sort, digest, index (fichier de navigation par wikilinks), merge, condense, synthesize (N communications → 1 document d'information, la forme email disparaît), clean |
| `research` | `/obs:research` | Recherche documentaire cross-référencée ; extraction de terminologie |
| `extract-pdf` | `/obs:extract-pdf` | Pipeline multi-sessions d'extraction de gros PDF vers les sources |

> `research` et `extract-pdf` opèrent sur le modèle générique `references/domain-layout.md`. Ce modèle référence encore un "profil JDR" hérité de l'époque où `ttrpg` et `writing` consommaient ces skills — plugins désormais supprimés ; à réévaluer si ce profil n'a plus d'usage.

## Licence

MIT — voir [LICENSE](../../LICENSE).
