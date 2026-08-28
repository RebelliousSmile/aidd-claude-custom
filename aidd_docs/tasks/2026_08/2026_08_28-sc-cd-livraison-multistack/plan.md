---
objective: "Chaque plugin sc-* expose une skill cd qui installe une chaîne locale et une procédure de production propres à sa stack, tandis que les exécutions manuelles, CI et PaaS appellent un unique script de déploiement gouverné par un contrat commun."
status: implemented
---

# Plan: Installer une livraison continue cohérente dans les plugins sc-*

## Overview

| Field      | Value |
| ---------- | ----- |
| **Goal**   | Capitaliser les pratiques de lancement local et de mise en production sans effacer les différences entre stacks. |
| **Source** | Brainstorm approuvé dans la conversation du 2026-08-28 ; création de l’issue GitHub demandée mais refusée par l’intégration avec `403 Resource not accessible by integration`. |

## Phases

| #   | Phase | File |
| --- | ----- | ---- |
| 1 | Contrat commun portable et garde anti-dérive | [`phase-1.md`](./phase-1.md) |
| 2 | Contrat projet, propriété et passage langage → automate | [`phase-2.md`](./phase-2.md) |
| 3 | Livraison JavaScript par framework et couche de données | [`phase-3.md`](./phase-3.md) |
| 4 | Livraison PHP et synchronisation WordPress raisonnée | [`phase-4.md`](./phase-4.md) |
| 5 | Livraison Python et façade native arbitrée | [`phase-5.md`](./phase-5.md) |
| 6 | Releases Rust et façade native arbitrée | [`phase-6.md`](./phase-6.md) |
| 7 | Livraison statique possédée par sc-css | [`phase-7.md`](./phase-7.md) |
| 8 | CI et fournisseurs managés possédés par sc-tiers | [`phase-8.md`](./phase-8.md) |
| 9 | Preuves intégrées, documentation et distribution | [`phase-9.md`](./phase-9.md) |

## Resources

| Source | Verified |
| ------ | -------- |
| [pnpm run](https://pnpm.io/cli/run) | Un script nommé dans `package.json` est appelable directement par `pnpm`, reçoit les arguments suivants et constitue une façade stable pour JavaScript. |
| [Composer scripts](https://getcomposer.org/doc/articles/scripts.md) | Le `composer.json` racine peut exposer des commandes projet sous forme d’exécutable, callback PHP ou commande Symfony Console. |
| [uv — running commands](https://docs.astral.sh/uv/concepts/projects/run/) | `uv run` exécute une commande ou un script dans l’environnement verrouillé du projet ; il fournit une option Python faisable sans être imposé aux projets qui utilisent un autre gestionnaire. |
| [Cargo aliases](https://doc.rust-lang.org/cargo/reference/config.html#alias) | `.cargo/config.toml` peut versionner des alias de commandes ; la forme exacte de la façade de release doit néanmoins être prouvée sur une fixture avant adoption. |
| [wp-env](https://developer.wordpress.org/block-editor/reference-guides/packages/packages-env/) | `wp-env` fournit le runtime WordPress local sur Docker, les commandes start, stop, run et les opérations destructrices explicitement signalées. |
| [GitHub Actions — writing workflows](https://docs.github.com/en/actions/how-tos/write-workflows) | Un workflow versionné peut installer la stack puis appeler la commande de déploiement du projet, sans recopier sa logique. |
| [GitLab CI/CD YAML](https://docs.gitlab.com/ci/yaml/) | Un job de production peut rester manuel et exécuter le même script projet via `script`, avec secrets portés par les variables CI/CD. |
| [Railway CLI](https://docs.railway.com/cli) | `railway up` déploie le répertoire courant et accepte des jetons dédiés en CI ; l’adaptateur peut donc rester derrière le script commun. |
| [Heroku — deploying with Git](https://devcenter.heroku.com/articles/git) | La primitive de livraison Git reste `git push heroku main` et peut être encapsulée par la procédure projet unique. |

## Decisions

| Decision | Why |
| -------- | --- |
| Conserver seulement les environnements `local` et `production`. | Le flux réel valide localement puis livre en production ; ajouter staging créerait une branche jamais exercée. |
| Faire de `deploy:*` une famille strictement orientée `local → production`, et réserver `pull:*` au sens inverse. | Le sens devient lisible dans toute stack et une inversion destructive ne peut pas se cacher derrière `sync`. |
| Dériver les références communes d’une source unique, puis vérifier leurs copies empaquetées octet pour octet. | Chaque plugin doit rester installable seul, mais six copies maintenues à la main feraient diverger le tronc commun. |
| Donner le runtime et la base aux plugins de langage, la livraison statique à `sc-css`, et les adaptateurs CI/PaaS à `sc-tiers`. | Cette frontière évite que deux skills écrivent des scripts concurrents dans un projet composite. |
| Faire appeler par `automata` la commande `deploy:*` déjà installée, sans deuxième implémentation. | Le chemin manuel et le chemin automatisé accumulent ainsi les mêmes corrections et gardes. |
| Matérialiser le passage entre plugins dans `deploy/contract.json`, descriptif sans secret et validé contre la façade réellement installée. | `sc-tiers` doit pouvoir lire commande, répertoire, propriétaire, opérations et politique de déclenchement sans redétecter la stack ni inventer une seconde procédure. |
| Autoriser un seul propriétaire de façade racine et des contributeurs bornés par composant ou workspace. | Un projet composite peut combiner PHP, JavaScript et CSS, mais ses sous-stacks doivent alimenter la commande racine au lieu de créer plusieurs procédures quotidiennes. |
| Garder le validateur JavaScript sous `tools/` comme oracle du marketplace, sans le distribuer comme dépendance runtime. | Les projets Python, Rust ou PHP ne doivent pas recevoir Node pour satisfaire le contrat ; leurs scripts natifs portent les préflight d’exécution, tandis que les skills lisent le schéma portable lors de la réconciliation. |
| Rejouer une configuration par réconciliation bornée, jamais par écrasement global. | La skill doit améliorer les projets existants et préserver leurs scripts, secrets et choix locaux. |
| Exiger pour toute mutation de production une identité de source affichée, une vérification après livraison et une voie de récupération déclarée. | La même procédure peut partir d’un checkout CI ou d’un workspace local ; elle doit rendre cette différence visible et ne jamais annoncer un succès sans preuve ni remède. |
| Reporter l’arbitrage exact des façades Python et Rust à une preuve sur fixture dans leurs phases. | Le besoin impose une façade native mais ne choisit pas encore entre les gestionnaires et task runners réellement présents. |
