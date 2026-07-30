---
type: plan
statut: livre
parent: 2026_07_30-10-pivots-testing-fournisseurs-master.md
part: 1
objective: "Ecrire la regle de selection du pivot testing quand plusieurs plugins de langage sont applicables au meme projet"
success_condition: "rg -q '^### Le pivot suit le fichier' plugins/overcode/docs/control.md && rg -q '^### The pivot follows the file' plugins/overcode/skills/control/references/pivot-contract.md && ls aidd_docs/internal/decisions/008-*.md"
iteration: 0
created_at: 2026-07-30T13:30:51Z
blocked_by: "arbitrage A1 et A2 du master — leve le 2026-07-30 (A1 = option B, A2 = additif)"
---

# Part 1 — Regle de detection polyglotte

## Feature

`pivot-contract.md:7` resout la stack au singulier : *« whichever language plugin is already installed and applicable is reused »*. Un projet a plusieurs stacks n'a pas de reponse. Le cas n'est pas theorique : la fixture `app` est un Django de 80 fichiers de test qui porte un `frontend/package.json` — `sc-js` y est detectable et fournit un pivot, `sc-python` est la vraie stack mesuree et n'en fournit aucun. `domains-scenarios.md:316` enregistre deja que la cause de N/A de S3 *« se lira comme fausse la premiere fois que quelqu'un la verifiera »*.

## Projection d'architecture

**Modifie**
- `plugins/overcode/docs/control.md` — la **regle et son motif**, sans etape de procedure (DEC-006)
- `plugins/overcode/skills/control/references/pivot-contract.md` §*Detecting the active language plugin* — la **procedure**
- `plugins/overcode/CHANGELOG.md`
- `.claude-plugin/marketplace.json` — `overcode` 4.0.0 → **4.1.0** (ou 5.0.0 si A2 tranche « rupture »)

**Cree**
- `aidd_docs/internal/decisions/008-polyglot-pivot-resolution.md` — le **rationnel**, les options ecartees et pourquoi

**Supprime** — rien.

## Regle proposee (option B du master, a confirmer)

Trois enonces, indissociables :

1. **Le pivot suit le fichier, pas le projet.** Chaque plugin de langage applicable contribue son pivot ; un champ est resolu contre le pivot de la stack a laquelle appartient le fichier en cours de jugement.
2. **Un champ agrege est rendu par stack, jamais somme.** *Test-count command* sur un projet a deux stacks rend deux nombres nommes ; un total unique masquerait un denominateur.
3. **L'absence est locale.** Une stack sans pivot degrade en verifications generiques **pour cette stack seulement** ; les autres restent affinees. La sortie nomme, par stack, si le champ etait affine ou generique.

Le troisieme enonce est ce qui rend la regle compatible avec §*Absence* du contrat : l'absence reste un cas normal, elle cesse simplement d'etre globale.

## Phases

### Phase 1 — Trancher et poser le rationnel
- [x] Confirmer A1 (regle) et A2 (portee du bump) aupres de l'utilisateur
- [x] Ecrire `008-polyglot-pivot-resolution.md` : contexte (ligne 7 au singulier + cas `app`), decision, options A/B/C ecartees avec motif, consequences sur §*Absence* et sur les champs agreges
- **Critere d'acceptation** : l'ADR permet de rejouer la decision sans relire ce plan

> Le fichier est nomme `008-pivot-follows-the-file.md`, pas `008-polyglot-pivot-resolution.md` : le titre enonce la regle retenue plutot que le probleme pose. Le `success_condition` visait deja `008-*.md`, il n'en depend pas.

### Phase 2 — Page puis skill, dans cet ordre (DEC-006)
- [x] `docs/control.md` : la regle + son motif, aucune etape de `## Process`
- [x] `pivot-contract.md` §*Detecting the active language plugin* : la procedure — comment enumerer les plugins applicables, comment rattacher un fichier a une stack, quoi faire d'un fichier qu'aucune stack ne revendique
- [x] Verifier qu'aucun autre passage du contrat ne presuppose le singulier (§*Locating*, §*Absence*)
- **Critere d'acceptation** : les deux documents disent la meme regle, avec la division de travail de DEC-006 ; ~~`rg 'polyglot'` rend les deux~~ — **critere errone, corrige**

> **Le `success_condition` d'origine echouait sur une livraison correcte, et c'est le critere qu'il fallait changer, pas la livraison.** Il grepait `polyglot` dans `docs/control.md`, page redigee **en francais** : la regle y est `### Le pivot suit le fichier` (l. 119) et le mot anglais n'a aucune raison d'y figurer. Il est en revanche present dans `pivot-contract.md:19`, page anglaise. Un critere qui exige le meme mot dans deux documents de langues differentes mesure la langue, pas la regle. Remplace par le titre de section reellement porte par chaque page, dans sa langue.

### Phase 3 — Consommateurs
- [x] Relire les 4 actions qui lisent un champ de pivot (`01-write`, `02-audit`, `04-strengthen`, `05-stats`) : aucune ne doit supposer un pivot unique
- [x] `SKILL.md` et `phase-framework.md` : meme controle
- **Critere d'acceptation** : aucune formulation au singulier ne subsiste chez un consommateur

> Six actions touchees au final, et non quatre : `03-configure` et `06-align` lisaient aussi le pivot au singulier.

### Phase 4 — Version
- [x] `CHANGELOG.md` overcode : entree 4.1.0 decrivant la regle, pas le refactoring
- [x] `marketplace.json` : bump — **meme commit que le contenu**
- **Critere d'acceptation** : `git status` propre avant tout install

> **Le bump du marketplace lui-meme avait ete oublie ici** : `overcode` passait bien a 4.1.0, mais la cle `version` racine de `marketplace.json` restait a `3.6.0` alors que le `CHANGELOG` racine publiait deja `3.7.0`. Rattrape pendant la part 2. Le critere « arbre propre » ne l'aurait pas attrape — un manifeste incoherent est un arbre parfaitement propre.

## Risques

| Risque | Mitigation |
|---|---|
| La regle ecrite dans la page derive de celle du contrat | Rediger la page en premier, le contrat comme sa procedure — jamais l'inverse |
| Un fichier n'appartient a aucune stack detectee | La procedure doit le nommer explicitement (repli generique, pas erreur) |
| A2 lu comme rupture apres coup | Trancher avant la phase 1, pas apres la redaction |

## Log

| Date | Evenement |
|---|---|
| 2026-07-30 | Cree, bloque sur A1/A2 |
| 2026-07-30 | A1 tranche option B, A2 tranche additif — deblocage |
| 2026-07-30 | **Livree** : DEC-008 `008-pivot-follows-the-file.md`, `docs/control.md` (regle + motif), `pivot-contract.md` (detection = ensemble, `### The pivot follows the file`), six actions alignees, `02-audit` traite l'enumeration partielle, `05-stats` rend par stack. `overcode` 4.1.0, marketplace 3.7.0. `pnpm test` vert |
| 2026-07-30 | **Cloture** : `success_condition` corrigee (elle grepait un mot anglais dans une page francaise et echouait sur la livraison), phases cochees, `statut: livre`. Ecart de manifeste rattrape en part 2 et consigne en phase 4 |
