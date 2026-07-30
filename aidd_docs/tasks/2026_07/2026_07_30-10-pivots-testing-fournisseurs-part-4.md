---
type: plan
statut: propose
parent: 2026_07_30-10-pivots-testing-fournisseurs-master.md
part: 4
objective: "Ecrire le pivot testing de sc-rust et, ce faisant, mettre a l'epreuve les trois hypotheses du contrat que Rust contredit"
success_condition: "test -f plugins/sc-rust/skills/sniff/references/capabilities/tools/testing.md"
iteration: 0
created_at: 2026-07-30T13:30:51Z
depends_on: [2]
---

# Part 4 — Pivot `sc-rust`, et mise a l'epreuve du contrat

## Feature

`sc-rust` (0.4.5) porte 3 dossiers `capabilities/` et 7 fichiers, sans `testing.md`. Ce pivot n'a pas seulement une valeur de couverture : c'est le **premier cas qui contredit le contrat**, ecrit jusqu'ici sur des hypotheses JS.

**Trois hypotheses a l'epreuve.**

1. **`Test file glob` suppose que les tests vivent dans des fichiers dedies.** En Rust, les tests unitaires vivent dans le fichier source lui-meme, sous `#[cfg(test)] mod tests`. Un glob de fichiers ne les voit pas — et pire, il les compterait comme *fichier de production non teste*. Seuls les tests d'integration (`tests/*.rs`) et les doctests sont dans des fichiers dedies.
2. **`Coverage command` suppose un reporter fourni par l'outillage de test.** `cargo test` n'en produit aucun : la couverture passe par un outil **tiers** (`cargo-tarpaulin`, `cargo-llvm-cov`), qui peut ne pas etre installe. Le champ doit dire quoi faire quand l'outil est absent — ce qui n'est pas le meme cas que « champ absent ».
3. **`Anchor boundary` suppose un runtime navigateur.** Ce que le contrat donne en exemple (defaut de rendu qu'un vrai navigateur applique, mismatch d'hydratation) n'existe pas ici. La frontiere reelle d'un binaire Rust, c'est le processus lance, le socket ouvert, le fichier ecrit sur un vrai systeme de fichiers.

Le contrat prevoit qu'un champ introuvable soit **absent** avec son repli. Il ne prevoit pas qu'un champ soit **mal pose** pour une stack. C'est cette distinction que cette part doit trancher.

## Projection d'architecture

**Cree**
- `plugins/sc-rust/skills/sniff/references/capabilities/tools/testing.md`

**Modifie**
- `plugins/overcode/skills/control/references/pivot-contract.md` — **seulement si une hypothese est refutee** (amendement du champ concerne, pas reecriture)
- `plugins/overcode/docs/control.md` + ADR — si amendement, meme chaine que la part 1 (DEC-006)
- `plugins/sc-rust/CHANGELOG.md`, `.claude-plugin/marketplace.json` — `sc-rust` 0.4.5 → **0.5.0**
- `plugins/overcode/CHANGELOG.md` + bump si amendement du contrat

**Supprime** — rien.

## Traitement propose des trois hypotheses

Aucun n'est acquis : chacun est une **proposition a valider a l'ecriture**, pas une conclusion.

1. *Test file glob* → le champ rend **deux motifs de nature differente** : un glob de fichiers (`tests/**/*.rs`) et un motif intra-fichier (`#[cfg(test)]`). Si le contrat n'admet qu'un glob, il est amende pour admettre un motif de contenu. **Consequence a ne pas rater** : *Source glob & exclusions* et *Test file glob* deviennent **non disjoints** — un meme fichier est source et test. Le contrat suppose implicitement qu'ils le sont.
2. *Coverage command* → le champ nomme l'outil tiers, la commande qui produit un rapport machine-lisible par fichier, **et** la detection de son absence. Un outil absent n'est pas un champ absent : le champ existe et dit ce qui manque. Si le contrat ne distingue pas les deux, l'ajouter.
3. *Anchor boundary* → reecrit la frontiere en termes de processus, socket et systeme de fichiers reels. Nommer ce qui **n'ancre pas** malgre l'apparence : `#[tokio::test]` sur un runtime de test, un `TempDir`, un serveur monte in-process. Rappel contrat:24 : le champ **positionne** la frontiere, il ne dit **jamais** quelle preuve un cas merite.

## Fixture

**Aucune identifiee.** C'est l'objet de l'arbitrage A3 du master. Sans projet Rust reel, ce pivot est ecrit sur documentation et non sur mesure — et un pivot faux est pire qu'un pivot absent, puisque le contrat prevoit l'absence. Trois issues : fournir une fixture, marquer chaque champ non verifie comme tel, ou ne livrer que les champs verifiables.

## Phases

### Phase 1 — Confronter les trois hypotheses au contrat
- [ ] Pour chacune : le contrat la couvre-t-il deja par son repli, ou est-il mal pose ?
- [ ] Trancher, par hypothese : pivot seul, ou pivot + amendement du contrat
- **Critere d'acceptation** : la decision est ecrite par hypothese, avec son motif ; « on verra a l'ecriture » n'est pas une reponse

### Phase 2 — Amendement du contrat si necessaire
- [ ] `docs/control.md` d'abord, `pivot-contract.md` ensuite, ADR pour le rationnel (DEC-006)
- [ ] Verifier l'effet retroactif sur les pivots deja ecrits (`sc-js`, `sc-python`)
- **Critere d'acceptation** : aucun pivot deja livre ne devient non conforme sans etre repris

### Phase 3 — Redaction du pivot
- [ ] 10 sections, langue du plugin, table de correspondance si les titres divergent
- [ ] Marquer explicitement tout champ non verifie contre un projet reel
- **Critere d'acceptation** : le pivot est lisible seul ; aucune commande n'est presentee comme verifiee si elle ne l'est pas

### Phase 4 — Version
- [ ] `sc-rust` 0.5.0 (+ bump `overcode` si le contrat a bouge), meme commit que le contenu
- **Critere d'acceptation** : arbre propre

## Risques

| Risque | Mitigation |
|---|---|
| Pivot ecrit sans terrain | A3 ; a defaut, marquage explicite des champs non verifies |
| Amender le contrat sur un seul cas | Formuler l'amendement en termes de stack en general, pas « pour Rust » |
| L'amendement casse `sc-js`/`sc-python` deja livres | Phase 2 controle la retroactivite avant de figer |
| Source et test cessent d'etre disjoints, en silence | Enonce explicitement en phase 1, hypothese 1 |

## Log

| Date | Evenement |
|---|---|
| 2026-07-30 | Cree |
