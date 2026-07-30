---
type: plan
statut: livre
parent: 2026_07_30-10-pivots-testing-fournisseurs-master.md
part: 2
objective: "Donner au champ Domain resolution son premier fournisseur, dans le seul pivot mur, et rectifier une affirmation fausse du CHANGELOG sc-js"
success_condition: "rg -q '^## (Domain resolution|Resolution de domaine)' plugins/sc-js/skills/sniff/references/capabilities/tools/testing.md"
iteration: 0
created_at: 2026-07-30T13:30:51Z
---

# Part 2 — `Domain resolution` dans `sc-js`, et rectification du CHANGELOG

## Feature

Le contrat definit *Domain resolution* (`pivot-contract.md:27`) : comment une stack exprime un **domaine fonctionnel** dans le systeme de fichiers et dans les identifiants. Quatre actions de `overcode:control` le lisent (`01-write:10,31`, `02-audit:9`, `04-strengthen:11,54`, `05-stats:11,133`, plus `06-align:116`). **Aucun pivot ne le fournit** : `sc-js` porte 9 sections, aucune n'est celle-la. Le champ est optionnel et son repli s'applique donc partout — mais il n'a alors aucun exemple, et les quatre pivots a venir devraient l'inventer chacun de leur cote.

Second point, independant mais du meme fichier : `plugins/sc-js/CHANGELOG.md:9` affirme du renommage `Tier thresholds` → `Anchor boundary` que *« Le contenu est conserve tel quel »*. C'est faux — le meme commit (`628e067`) a retire les attributions de tier de la section. DEC-007 §3 porte la meme phrase.

## Projection d'architecture

**Modifie**
- `plugins/sc-js/skills/sniff/references/capabilities/tools/testing.md` — ajout d'une section *Domain resolution* (10e champ)
- `plugins/sc-js/CHANGELOG.md` — rectification de l'entree 0.14.0 + entree 0.15.0
- `aidd_docs/internal/decisions/007-phase-as-classifying-authority.md` §3 — meme rectification, sous forme d'addendum date (on n'edite pas un ADR, on l'amende)
- `.claude-plugin/marketplace.json` — `sc-js` 0.14.0 → **0.15.0**

**Cree / supprime** — rien.

## Contenu attendu de la section

Ce que le champ doit repondre, et **seulement** cela : comment trouver un domaine deja nomme dans un codebase JS/TS. Les formes a couvrir — arbres `pages/<domaine>/` et `app/<domaine>/` (routing par systeme de fichiers), `features/<domaine>/` et `modules/<domaine>/`, suffixes d'identifiants (`*.guard.ts`, `*.service.ts`, `<Domaine>Provider`), conventions de monorepo (`packages/<domaine>/`).

Trois interdits, tires du contrat :
- **aucune liste de domaines** — quels domaines un produit possede est etabli ailleurs, par catalogue et confirmation
- **ne jamais primer** sur une resolution enoncee explicitement a propos du code du projet ; le champ **complete** un domaine deja nomme
- **ne pas fusionner** avec *Source glob & exclusions* : l'un est structurel, l'autre semantique

Et les regles generales du contrat : ne nommer aucun consommateur, une seule section pour le champ, titre enoncant le champ. `sc-js` ecrit ses titres de section en anglais verbatim — garder la convention du fichier, donc `## Domain resolution`.

## Phases

### Phase 1 — Section `Domain resolution`
- [x] Rediger la section a partir des conventions reellement observees dans les autres fichiers `capabilities/` de `sc-js` (DEC-001 : DRY inter-pivots, ne pas redupliquer ce que `frameworks/*.md` dit deja)
- [x] Verifier l'absence de liste de domaines, l'absence de nom de consommateur, l'absence de chevauchement avec *Source glob & exclusions*
- **Critere d'acceptation** : la section repond « comment les trouver ici », jamais « lesquels existent » ; lisible seule, sans ouvrir un consommateur

> **Le risque de redite ne s'est pas materialise, et pour une raison a corriger dans le plan** : `sc-js` n'a **aucun** repertoire `capabilities/frameworks/`. Le plan citait `frameworks/next.md`, qui n'existe pas. L'arbre porte `perf/nuxt.md`, `perf/sveltekit.md`, `server/express-mvc.md`, `state/pinia.md`. Un seul y touche a la structure de repertoires — `server/express-mvc.md`, qui documente une decoupe **par couche** (`routes/`, `controllers/`, `services/`). La section n'a donc rien a reprendre : elle enonce au contraire que cette decoupe-la **ne porte pas** le domaine, ce que le fichier voisin ne dit pas et n'a pas a dire.

### Phase 2 — Rectifications
- [x] `CHANGELOG.md` : corriger l'affirmation de 0.14.0 (le contenu **a** change : les attributions de tier ont ete retirees) et ajouter l'entree 0.15.0
- [x] DEC-007 : addendum date corrigeant §3, sans reecrire la decision
- **Critere d'acceptation** : plus aucune trace de « contenu conserve tel quel » a propos de ce renommage

### Phase 3 — Version
- [x] `marketplace.json` : `sc-js` 0.15.0, meme commit que le contenu
- **Critere d'acceptation** : arbre propre

> **Un ecart trouve en passant, hors perimetre annonce de la part** : `marketplace.json` portait encore `version: 3.6.0` alors que le `CHANGELOG` racine publiait deja l'entree **3.7.0** de la part 1. Le bump du marketplace lui-meme avait ete oublie. Corrige ici, dans le meme arbre non commite — c'est exactement le cas que la regle « bump et contenu dans le meme commit » existe pour empecher, et il a failli partir en silence.

## Risques

| Risque | Mitigation |
|---|---|
| La section derive vers un catalogue de domaines | Relecture explicite contre l'interdit du contrat avant de figer |
| Redite avec `frameworks/next.md` / `frameworks/*.md` sur le routing | DEC-001 : referencer, ne pas recopier |
| La forme posee ici devient un gabarit implicite mal calibre pour Rust ou PHP | Part 4 autorise a diverger et a amender le contrat si necessaire |

## Log

| Date | Evenement |
|---|---|
| 2026-07-30 | Cree |
| 2026-07-30 | Phase 2 livree seule (rectification DEC-007 §3 + CHANGELOG sc-js 0.14.1, racine, overcode) — le champ restait sans fournisseur |
| 2026-07-30 | **Phases 1 et 3 livrees, part close.** Section `## Domain resolution` inseree entre `## Known tooling gotchas` et `## Canonical E2E tool` (ordre du contrat). Trois interdits tenus : aucune liste de domaines, aucun consommateur nomme, ligne de demarcation explicite contre `Source glob & exclusions`. `sc-js` 0.15.0 (`plugin.json` + `marketplace.json`), `README:72` aligne. `pnpm test` vert. `success_condition` satisfaite |
