---
objective: "Le générateur design:harness respecte l'espace de codes 0/2/3 qu'il déclare, ne sort en 0 que sur un fichier syntaxiquement valide, produit un harness accessible et titré, et une preuve exécutable branchée sur pnpm test le vérifie — de bout en bout contre le bootstrap WordPress FSE."
status: in-progress
---

# Plan: durcissement de `design:harness`

## Overview

| Field      | Value                                                                                                                          |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **Goal**   | Fermer les 17 constats de l'audit du 2026-08-05 et le 18ᵉ trouvé au challenge, et rendre la fermeture opposable par un test qui casse si elle régresse |
| **Source** | `aidd_docs/tasks/2026_08/2026_08_05_audit/{code-quality,ui,tests}.md` — audit `design:harness`, 3 piliers, 17 constats mesurés |

## Phases

| #   | Phase                                     | File                         |
| --- | ----------------------------------------- | ---------------------------- |
| 1   | Espace de codes et validation des entrées | [`phase-1.md`](./phase-1.md) |
| 2   | Le harness produit                        | [`phase-2.md`](./phase-2.md) |
| 3   | La preuve opposable                       | [`phase-3.md`](./phase-3.md) |
| 4   | Chaîne complète contre WordPress FSE      | [`phase-4.md`](./phase-4.md) |

## Resources

| Source                                                                                       | Verified                                                                                                                     |
| -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html`                            | Un contrôle de formulaire doit porter un nom accessible ; `aria-label` sur le `select` suffit quand aucun `<label>` visible n'existe |
| `https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-pressed`     | `aria-pressed` est l'attribut d'état d'un bouton bascule ; il doit être maintenu en même temps que la classe visuelle              |
| `https://docs.python.org/3/library/html.html#html.escape`                                     | `html.escape(s, quote=True)` est stdlib — compatible avec la contrainte « stdlib only » du générateur                             |

## Decisions

| Decision                                                                                                                            | Why                                                                                                                                                                                                            |
| ------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `harness-selftest.sh` reste dans le plugin ; c'est `tools/eval/design-harness.mjs` qui l'invoque, il n'est pas porté en Node        | Le `.sh` est distribué avec le plugin et reste lançable à la main hors marketplace. Le porter créerait deux preuves à maintenir, ou en laisserait une orpheline — c'est-à-dire le défaut qu'on corrige            |
| L'espace de codes 0/2/3 vaut pour **tout** le programme, pas seulement sous `--contract`                                             | `references/harness-contract.md:26` l'énonce sans restriction et cite le chemin « aucune page », hors `--contract` ; `harness.py:435` l'affirme en commentaire. `SKILL.md:62` restreint à `--contract` — c'est cette phrase-là qui est fausse et qui s'aligne |
| Le repli visuel d'une fonction de page qui jette est un **état rendu**, pas une exception propagée                                   | `measure.py:191` appelle `window.setPage(k)` sans garde : propager fait planter l'oracle au lieu de lui donner un verdict, et laisse le cadre sur la page précédente — l'oracle mesurerait la mauvaise page       |
| `harness-selftest.sh` reste du **POSIX `sh`**, il n'est pas promu en bash                                                            | Le shebang dit `sh` (`:1`), l'en-tête d'usage lance `bash` (`:7`) : il tourne sous les deux et c'est la propriété à préserver. La phase 3 y ajoute une dizaine d'assertions ; le moindre bashisme la détruirait sans que le runner s'en aperçoive |
| Une clé de page est un **slug**, et `validate_pages()` refuse tout ce qui ne dérive pas un identifiant JS valide                     | Mesuré : `--pages '/contact/:C'` sort en **0** et écrit `function page/contact/()`. Le fichier est mort — `pages is not defined` — mais `window.setPage` existe, donc le garde de l'oracle ne voit rien et `page.evaluate` lève. Un générateur qui livre du JS invalide en vert est le pire défaut de la liste, et il n'était dans aucun des trois rapports d'audit |

## Estimation

L'unité coûteuse n'est pas la même selon la phase.

- **Phases 1 à 3** : l'unité est le point de modification dans `harness.py` (≈ 10) puis l'assertion de selftest à écrire (≈ 8). **1 session par phase**, elles sont indépendantes entre elles. La phase 3 porte en plus la déclaration d'une table d'actions dans `skills/harness/SKILL.md` — travail de rédaction, pas de code, mais c'est lui qui fait sortir la skill de l'état « couverture non vérifiable ».
- **Phase 4** : l'unité est le cycle wp-env complet — 70 s de démarrage mesurés le 2026-08-05, plus le remplissage du harness et l'écriture du JSON de configuration de l'oracle, qui n'existe pas encore pour ce site. **1 session, 2 si l'oracle demande un aller-retour de calibration.**

**Total : 3 à 4 sessions.**

## Portée optionnelle

La tâche 4 de la phase 1 (substitution en une passe) est la seule du plan qui ne ferme aucun constat mesuré : elle couvre un `--title` contenant `%%PAGE_OPTIONS%%`, que personne ne produira. L'échappement du titre (phase 1, tâche 3.3) suffit au risque réel. **À faire seulement si la phase 1 tient dans sa session** ; à couper sinon, sans dette.

## Requalification par rapport à l'audit

Un constat s'ajoute, deux changent de sévérité — dit ici plutôt que laissé dans les rapports :

- **Nouveau, découvert au challenge, non couvert par l'audit — 🔴.** Une clé de page qui n'est pas un identifiant JS valide produit un harness syntaxiquement mort **en exit 0**. Les trois piliers de l'audit sont passés à côté : `code-quality` a bien vu la collision `-`/`_`, mais pas que la même fonction `key_to_fn` accepte n'importe quel caractère. C'est le seul défaut du lot qui rende le fichier généré inutilisable au lieu de dégradé.

- **`ui.md`, absence de `h1` — 🔴 → 🟡.** L'argument « `measure.py` scanne `h1, h2` » ne tient qu'à moitié : l'oracle mesure un harness **rempli**, où `placeholder()` a été remplacé par du contenu réel. Ce qui reste vrai, et qui suffit à traiter la ligne : le repli « Page introuvable » n'a pas de `h1` même après remplissage, une page pas encore remplie non plus, et le code d'échafaudage montre un `<h2>` à l'agent trois lignes après lui avoir prescrit un `h1`.
- **`code-quality.md`, `--pages-json` → exit 1 — reste 🔴, mais le grief se déplace.** `SKILL.md:62` restreint la règle à `--contract`, donc `SKILL.md` n'est pas violé. C'est `harness-contract.md:26` qui l'est, et c'est la référence normative. La divergence entre les deux textes devient elle-même une correction (phase 1).
