# overcode

*Socle commun de la marketplace : workflows projet-agnostiques qui étendent le framework [AIDD](https://github.com/ai-driven-dev/aidd-framework).*

Plugin principal, installé globalement (`recommended`). Il ne cible pas une stack : il ajoute des workflows transversaux de maintenance, d'analyse, de documentation et de planification, plus des chaînes d'alias pour enchaîner des skills AIDD.

Aucune skill ne code en dur la connaissance d'une stack : les audits détectent la stack puis chargent les **pivots** déposés par les plugins `sc-*` sous `.claude/rules/07-quality/`. Sans pivot, un schéma générique s'applique — et la sortie rend une **quittance** qui sépare quatre états, une ligne par stack : chargé, aucun fournisseur, fournisseur non installé ici, réceptacle sans règle. Détail dans [`docs/concepts.md`](docs/concepts.md).

## Documentation

| Page | Contenu |
|---|---|
| [`docs/concepts.md`](docs/concepts.md) | Le modèle mental — le socle, les pivots, les frontières entre skills voisines, la densité de `control` |
| [`docs/workflow.md`](docs/workflow.md) | Quelle skill pour quelle situation — table de routage et détail par skill |
| [`docs/aliases.md`](docs/aliases.md) | Les dix chaînes d'alias, ce qu'elles enchaînent et leurs garanties |
| [`docs/control.md`](docs/control.md) | Le modèle de `control` — les quatre autorités, les phases, les domaines, le chaînage |

Le processus de chaque skill vit dans son `SKILL.md` et ses `actions/`.

## Skills

| Skill | Invocation | Description |
|---|---|---|
| `alias` | `/overcode:alias <nom>` | Enchaîne des workflows en une commande — dix chaînes pré-écrites |
| `harvest` | `/overcode:harvest` | Maintenance globale — réconcilie le tracker, extrait les décisions, purge l'éphémère |
| `reconcile-normative` | `/overcode:reconcile-normative` | Cohérence du normatif entre archives, mémoire et règles actives |
| `taste` | `/overcode:taste [fichier]` | Pondère la fraîcheur d'un Markdown contre le dépôt ; route les questions code vers audit/assert AIDD. Sans argument : scan borné à 25 documents |
| `foresee` | `/overcode:foresee <cible>` | Route docs/code vers AIDD ; complète l'audit de dépendances par l'horizon d'abandon, d'isolation et de migration |
| `behave` | `/overcode:behave <action>` | Harness de tests comportementaux pour **prompts** — scaffold, run jugé, régression, review |
| `control` | `/overcode:control <action>` | Gouvernance de la suite de tests d'un projet, bornée par une **densité** lue contre la médiane du projet et pondérée par sa **phase** déclarée. **Ne se déclenche jamais seule.** |
| `web-optimize` | `/overcode:web-optimize` | Audit perf web (LCP, CLS, INP, bundle, N+1 au rendu) → roadmap priorisée |
| `data-optimize` | `/overcode:data-optimize` | Audit perf de la couche données (N+1, index, pagination, cache, quota) |
| `seo-optimize` | `/overcode:seo-optimize` | Audit SEO et GEO → roadmap priorisée + copy prêt à coller |
| `ap-optimize` | `/overcode:ap-optimize` | Audit d'une implémentation ActivityPub (inbox, outbox, signatures, fan-out, AS2) |
| `readme` | `/overcode:readme` | Rédige ou met à jour un README.md (`write` depuis zéro, `update` par section) |
| `changelog` | `/overcode:changelog` | Génère le CHANGELOG depuis git (Keep a Changelog) ; `curate` comble et condense l'historique |
| `decompose` | `/overcode:decompose` | Décompose un objectif en graphe de dépendances (méthode Mikado) |
| `journey` | `/overcode:journey` | Exécute un parcours utilisateur depuis une issue GitHub/GitLab (Playwright) |
| `status` | `/overcode:status` | Santé projet — synthèse de la mémoire, rapport complet, audit de la mémoire elle-même |
| `baby` | `/overcode:baby` | Explique, réécrit ou compare un sujet en langage simple, sans jargon non défini |
| `research` | `/overcode:research` | Recherche documentaire cross-référencée et extraction de terminologie |

Chaînes d'alias fournies : `rechallenge`, `endtask`, `bump-plugin`, `previously`, `smarten`, `skillconf`, `weeklyemail`, `gitit`, `mirror`, `codex-vision` — détail dans [`docs/aliases.md`](docs/aliases.md).

## Licence

MIT — voir [LICENSE](../../LICENSE).
