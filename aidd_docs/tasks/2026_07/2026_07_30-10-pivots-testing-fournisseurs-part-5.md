---
type: plan
statut: propose
parent: 2026_07_30-10-pivots-testing-fournisseurs-master.md
part: 5
objective: "Ecrire les pivots testing de sc-php et sc-css, en creant d'abord l'arbre capabilities absent de sc-css, et cloturer le manifeste"
success_condition: "test -f plugins/sc-php/skills/sniff/references/capabilities/tools/testing.md && test -d plugins/sc-css/skills/sniff/references/capabilities"
iteration: 0
created_at: 2026-07-30T13:30:51Z
depends_on: [2, 4]
---

# Part 5 — Pivots `sc-php` et `sc-css`, cloture

## Feature

Deux derniers fournisseurs, de difficulte tres inegale.

**`sc-php`** (0.9.0) — arbre `capabilities/` existant, 5 dossiers, 10 fichiers, dont un `testing/bruno.md`. Il manque `testing.md`. Cas ordinaire.

**`sc-css`** (0.3.3) — **aucun `skills/sniff/references/`, aucun `capabilities/`** : la skill `sniff` compte 3 fichiers. Son `02-install-pivots.md` declare pourtant **6 pivots dont 0 existe sur disque**. Deux questions distinctes : (i) creer l'arbre, (ii) un pivot `testing` a-t-il seulement un sens en CSS ?

La question (ii) est reelle. Le contrat demande un runner de tests, un compte de tests, une couverture par fichier. CSS n'a pas de runner de tests natif ; ce qui s'en approche, ce sont les tests de regression visuelle, qui sont des tests **E2E d'un projet**, pas des tests de la stack CSS. **Conclure « pas de pivot legitime » est une sortie autorisee** de cette part — le contrat prevoit l'absence, et un pivot creux vaut moins qu'un pivot absent.

## Projection d'architecture

**Cree**
- `plugins/sc-php/skills/sniff/references/capabilities/tools/testing.md`
- `plugins/sc-css/skills/sniff/references/capabilities/` — l'arbre, **si** (ii) conclut qu'un pivot a un sens
- `plugins/sc-css/skills/sniff/references/capabilities/tools/testing.md` — idem

**Modifie**
- `plugins/sc-php/CHANGELOG.md` — `sc-php` 0.9.0 → **0.10.0**
- `plugins/sc-css/CHANGELOG.md` — `sc-css` 0.3.3 → **0.4.0** (si pivot livre)
- `.claude-plugin/marketplace.json` — bumps + `marketplace` 3.6.0 → **3.7.0**
- `version.txt` — porte `3.1.0`, **incoherent** avec `marketplace.json` ; a aligner ou a supprimer s'il ne sert plus

**Supprime** — rien ; `capabilities/testing/bruno.md` de `sc-php` reste ou il est (pivot Bruno, autre nature).

## `sc-php` — points a etablir

- *Test runner(s)* — PHPUnit et/ou Pest ; detection par `composer.json` et par la presence de `phpunit.xml`.
- *Test file glob* — `tests/**/*Test.php` ; le suffixe `Test` est la convention PHPUnit, Pest diverge.
- *Coverage command* — necessite **Xdebug ou PCOV** : comme pour Rust, l'outil peut manquer, et le champ doit le detecter. `--coverage-clover` pour un rapport machine-lisible par fichier, produit **hors gate**.
- *Source glob & exclusions* — `vendor/` jamais classifiable ; en WordPress, `wp-admin/`, `wp-includes/`, les themes et plugins tiers.
- *Anchor boundary* — la frontiere reelle est la requete HTTP servie par un vrai serveur ; ce qui n'ancre pas : `WP_UnitTestCase` (in-process, base de test), un double de `wpdb`.
- *Risk signals* — paiement, auth, requetes SQL construites a la main, `unlink`/suppression, options globales ; frontieres externes detectees dans `composer.json` et dans les appels `wp_remote_*`.
- *Domain resolution* — arbres `src/<Domaine>/`, PSR-4 dans `composer.json`, suffixes `<Domaine>Controller`/`<Domaine>Repository`.

Une fixture PHP/WordPress reelle existe sur le poste (projet Mauceri) et peut servir a la verification. **Lecture seule, dry-run.**

## Phases

### Phase 1 — `sc-php`
- [ ] Verifier chaque commande contre un projet PHP reel si A3 le permet
- [ ] Rediger les 10 sections, langue du plugin, table de correspondance si les titres divergent
- [ ] Relire contre le contrat **tel qu'amende par la part 4**
- **Critere d'acceptation** : chaque question du contrat repondable en lisant le seul pivot

### Phase 2 — `sc-css` : trancher avant de creer
- [ ] Repondre a (ii) : un pivot `testing` CSS a-t-il un contenu non creux ? Passer les 10 champs un par un et compter ceux qui recoivent une reponse reelle
- [ ] Si non : ne rien creer, ecrire la conclusion et son motif dans l'issue #10, laisser `sc-css` en 0.3.3
- [ ] Si oui : creer `skills/sniff/references/capabilities/` puis le pivot
- **Critere d'acceptation** : la decision est adossee a un decompte de champs, pas a une impression

### Phase 3 — Coherence du manifeste
- [ ] `marketplace.json` : bumps des plugins touches + `marketplace` 3.7.0
- [ ] `version.txt` (3.1.0) aligne ou retire
- [ ] `index.json` inchange (ne porte pas de versions)
- **Critere d'acceptation** : une seule source de verite de version ; `git status` propre avant tout install

### Phase 4 — Cloture
- [ ] Relire les 5 pivots livres les uns contre les autres : meme emplacement, memes titres de champ, aucune divergence non declaree
- [ ] Mettre a jour l'issue #10 : item 1 deja fait avant ce plan, `sc-godot` hors perimetre avec son motif, sort de `sc-css`
- **Critere d'acceptation** : `find plugins -name testing.md -path '*capabilities*'` rend le nombre attendu, et chaque absence restante a un motif ecrit

## Risques

| Risque | Mitigation |
|---|---|
| Fabriquer un pivot CSS creux pour cocher la case | Phase 2 : decompte des champs reellement repondus, sortie « pas de pivot » autorisee |
| Les faux pivots declares de `sc-css` sont traites ici | Hors perimetre (#11) sauf ce que la creation de l'arbre impose |
| `version.txt` re-diverge | Trancher : source unique, ou suppression |
| Pivots incoherents entre eux apres 5 redactions successives | Phase 4 : relecture croisee obligatoire |

## Log

| Date | Evenement |
|---|---|
| 2026-07-30 | Cree |
