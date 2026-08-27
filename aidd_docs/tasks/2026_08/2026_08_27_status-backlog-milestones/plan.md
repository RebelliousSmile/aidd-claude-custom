---
objective: "Le backlog documentaire est synchronisé par `status`, filtrable et groupable par milestone, et `previously` peut le régénérer sans dupliquer son contenu dans l'instantané projet."
status: in-progress
---

# Plan: Faire de `status` l'autorité du backlog et de ses milestones

## Overview

| Field      | Value |
| ---------- | ----- |
| **Goal**   | Déplacer la synchronisation du backlog vers `status`, l'enrichir des milestones et la brancher en option dans `previously` |
| **Source** | Brainstorm de la conversation du 2026-08-27 |

## Phases

| #   | Phase | File |
| --- | ----- | ---- |
| 1   | Transfert de l'autorité et des preuves vers `status` | [`phase-1.md`](./phase-1.md) |
| 2   | Filtrage, regroupement et compatibilité des milestones | [`phase-2.md`](./phase-2.md) |
| 3   | Intégration dans `previously` sans duplication | [`phase-3.md`](./phase-3.md) |
| 4   | Documentation, décision et distribution majeure | [`phase-4.md`](./phase-4.md) |

## Resources

| Source | Verified |
| ------ | -------- |
| [GitHub CLI — `gh issue list`](https://cli.github.com/manual/gh_issue_list) | `--json milestone` est disponible et le filtre natif accepte un numéro ou un titre de milestone. |
| [GitHub CLI — `gh api`](https://cli.github.com/manual/gh_api) | `--paginate` suit toutes les pages d'un endpoint REST et permet de remplacer la limite de `gh issue list`. |
| [GitHub REST API — repository issues](https://docs.github.com/en/rest/issues/issues#list-repository-issues) | L'endpoint se pagine, expose l'objet milestone et renvoie aussi des pull requests, reconnaissables à leur clé `pull_request` et donc à exclure du backlog. |
| [GitHub REST API — milestones](https://docs.github.com/en/rest/issues/milestones) | Le catalogue expose `title`, `state` et `due_on`, accepte `state=all` et se pagine. |
| [GitLab CLI — `glab issue list`](https://docs.gitlab.com/cli/issue/list/) | La sortie JSON est disponible, mais `--milestone` est documenté comme un identifiant ; le filtrage portable ne doit donc pas lui transmettre directement un titre. |
| [GitLab CLI — `glab milestone list`](https://docs.gitlab.com/cli/milestone/list/) | Le catalogue JSON accepte le projet, les milestones d'ancêtres, la pagination et contient les données nécessaires au tri. |
| [GitLab Issues API](https://docs.gitlab.com/api/issues/) | Une issue expose un objet `milestone` avec notamment `title` et `due_date`. |
| [GitLab Project milestones API](https://docs.gitlab.com/api/milestones/) | Le catalogue projet expose `title`, `state` et `due_date` et permet une correspondance exacte par titre. |

## Decisions

| Decision | Why |
| -------- | --- |
| `status` devient l'unique propriétaire du backlog et l'alias public `backlog` disparaît | Le backlog est un état projet durable ; deux routes propriétaires feraient diverger validation, collecte et rendu. |
| Le filtre est appliqué localement sur un titre exact et sensible à la casse, tandis que l'identité d'un groupe reste l'identifiant provider | GitHub et GitLab n'ont pas le même contrat CLI pour `--milestone`; l'identifiant empêche en plus de fusionner deux milestones GitHub homonymes. |
| Le catalogue de milestones est collecté indépendamment des issues | Seul le catalogue distingue un projet sans aucune milestone d'un projet qui en possède mais dont les issues ouvertes n'en utilisent aucune. |
| Les groupes emploient un sous-titre généré reconnaissable seulement avec au moins une issue canonique dessous, tandis que les anciennes lignes plates restent reconnues | Le remplacement borné de DEC-011 doit pouvoir retirer des groupes devenus obsolètes sans absorber une sous-section manuelle isolée comme `### Notes historiques`. |
| Un échec de synchronisation demandée par `previously` arrête l'alias avant le snapshot | Continuer produirait un instantané apparemment réussi adossé à un backlog que la commande avait promis de rafraîchir. |
| Le changement est distribué en `overcode` 5.0.0 | La suppression de `/overcode:alias backlog` est une rupture de l'interface publique, même si une nouvelle route remplace la capacité. |
