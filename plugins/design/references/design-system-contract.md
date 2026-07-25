# Design system contract

The single source of truth for **where** the design system lives in a project and **what files** compose it. Every `design` skill reads and writes against this contract so that `define`, `destructure`, `adjust`, `enforce`, and `diffuse` stay interoperable.

## Les 4 artefacts et leur racine

Le contrat est un répertoire de quatre artefacts adressables, identifiés par une racine. Ils cristallisent à `adjust` ; avant ce point la matière est malléable.

| Fichier | Contenu | Autorité | Statut · consommateur |
|---------|---------|----------|----------------------|
| `design/release.json` | **Racine** — identité, version par artefact, hash de source, provenance, statut de maturité | Source d'identité | **exécutable** — `lint-core.mjs` (présence + les trois artefacts dont il dérive ses règles), `tools/status.py` |
| `design/tokens.json` | Valeurs (couleurs, espacements, typographie, breakpoints…) au format W3C DTCG | Source des valeurs | **exécutable** — `lint-core.mjs` Règles 2/4, `config-gen.py`, générateurs d'adapters |
| `design/components.json` | Anatomie des composants (noms canoniques, éléments, variantes, contextes de fond) | Source de nomenclature | **exécutable** — `lint-core.mjs` Règles 1/5, `config-gen.py` |
| `design/policies.json` | Politiques transverses (mode, usage des tokens, préfixes utilitaires, table des adapters) | Source des politiques | **exécutable** — `lint-core.mjs` Règles 1/3/4, pivots `sc-*` |
| `design/oracle.json` | Cibles de mesure par composant | Source des hints de mesure | **exécutable** — `config-gen.py` |

`design/design-system.md` (charte prose) est une **entrée** du contrat, pas un artefact : aucun outil ne la lit, `release.json § charter` enregistre sa présence et sa version, et sa concordance avec `components.json` est vérifiée une fois, au figeage, par `adjust/02-freeze.md § Étape 2 Règle 4`.

**Règle fondamentale : une donnée vit dans un seul artefact.**
- Les valeurs numériques/couleurs/dimensions → `tokens.json` exclusivement.
- La nomenclature des composants → `components.json` exclusivement.
- Les politiques transverses → `policies.json` exclusivement.
- Les hints de mesure → `oracle.json` exclusivement.
- Les versions, hashes, provenance et statut → `release.json` exclusivement.
- La prose et le narratif → `design-system.md` exclusivement.

Champ par champ, étiquetage exécutable/informationnel et redistribution depuis un contrat 1.x : `contract-schema.md`.

**Un contrat sans `release.json` est un contrat 1.x.** `lint-core.mjs` le détecte, sort en 3 et imprime la commande de migration (`adjust/actions/03-migrate.md`). Aucun chemin de lecture 1.x ne subsiste.

## Project layout

The design system home is `design/` at the project root (create it if absent).

```
design/
  release.json              # racine — versions par artefact, hashes, provenance, statut (écrit par adjust)
  tokens.json               # W3C DTCG tokens (valeurs canoniques)
  components.json           # anatomie des composants (écrit par adjust)
  policies.json             # mode, usage des tokens, préfixes utilitaires, table des adapters (écrit par adjust)
  oracle.json               # cibles de mesure par composant (écrit par adjust)
  design-system.md          # entrée — charte prose (statut brouillon → figé à adjust)
  adapters/
    tokens.css              # generated — CSS custom properties (:root)
    …                       # generated — un fichier par consommateur présent, aucun autre
  wireframes/
    <story-slug>.html       # living HTML preview, mobile-first, links ../adapters/tokens.css
  critique/
    <yyyy_mm_dd>-<cible>.md # non-contractuel — rapport destructure persisté par défaut (historique, jamais versionné)
```

`design/critique/` n'est **pas** un artefact du contrat : c'est un rapport informationnel, non versionné, produit par `destructure` (voir Consumption rules ci-dessous). L'ancien chemin `design/destructure-report.md` reste un alias accepté en lecture pour compatibilité.

- If a project already nests UI under a sub-package (monorepo), prefer that package root; record the chosen home at the top of `design-system.md`.
- Never scatter tokens across multiple sources. `tokens.json` is canonical; `adapters/*` are produced by `tools/generate.py` alone and must never be hand-edited — a header banner says so, and `generate.py --check` fails on any edit, with no flag to suppress it. Which adapters get generated is conditioned on the consumers present in the project — canonical rule: `write-system-procedure.md § Adapter emission rule`.
- Les quatre artefacts et `release.json` sont absents avant `adjust` — c'est normal. `define` et `destructure` travaillent sur la matière malléable ; `adjust` est le seul verbe autorisé à les écrire.

## Anatomie des composants

Voir `adjust/references/manifest-schema.md` pour la structure complète, les invariants et les exemples. Résumé :

- Vocabulaire **ouvert par défaut** : une classe dont le bloc n'est pas déclaré est traitée comme utilitaire et ignorée. Une classe dont le bloc *est* déclaré doit correspondre à un `base`, `elements.*` ou `modifiers.*` — sinon `error`. Le vocabulaire ne se referme que sous `--strict`, en `warning`, sur les seules classes de forme BEM.
- Concordance avec la charte : chaque composant de `design-system.md § Inventaire des composants` doit avoir une entrée, et vice-versa. Vérifiée au figeage (`adjust/02-freeze.md § Étape 2 Règle 4`), jamais ensuite.
- Les versions vivent dans `release.json` ; un écart entre artefacts est une donnée, pas une violation.

## `design-system.md` required sections

1. **Provenance** — origin (reference URL/file, or brief summary), date, version, who/what generated it.
2. **Foundations** — narrative summary of color, typography, **iconography** (the single chosen icon library + style, `icon.library`/`icon.style`), spacing, radius, elevation, motion. Points to `tokens.json` for exact values; does not duplicate every number. The **core trio** (palette anchor · type · icon set) is settled and approved first, fast, before the rest. Never emoji as UI iconography.
3. **Responsive strategy** — the named breakpoints, the mobile-first stance, and the three-tier intent: what the **mobile core** must always deliver, what is **enriched** only at ≥ tablet/desktop, and which **mobile-only** UX patterns exist. (See the installed `.claude/rules/08-design/` rules for the binding conventions.)
4. **Component inventory** — table: component · purpose · key options/variants · responsive divergence (one line) · spec file. Says that the vocabulary induced by the promoted manifest is **open by default**: an undeclared block is treated as a utility; only a declared component makes its own elements and modifiers enforceable.
5. **Open questions** — anything assumed or unresolved, so a human can close it.

## Consumption rules

- `define` écrit une matière malléable (tokens de travail + inventaire prose candidat). Elle N'ÉCRIT AUCUN artefact du contrat.
- `destructure` est lecture seule sur le contrat et le code source : il n'édite aucun artefact ni `design-system.md`. Il persiste par défaut son propre rapport sous `design/critique/` (non-contractuel — voir Project layout). En mode standalone sur projet figé : lit `components.json` + `design-system.md` pour situer les pistes par rapport au contrat existant.
- `adjust` est le seul verbe qui écrit les artefacts et `release.json`. Il canonise aussi `tokens.json` et marque `design-system.md` comme figé.
- `enforce` dérive ses règles de lint de `tokens.json` (valeurs), `components.json` (anatomie) et `policies.json` (politiques). Il ne les invente pas.
- `diffuse` produit des éléments répétables sous le gate `enforce`. Tout élément produit doit n'utiliser que les classes et valeurs déclarées dans le contrat.
- When tokens change, regenerate **every emitted** adapter in the same step; never let an adapter drift from `tokens.json`.

## Versioning

- `release.json` porte une version par artefact et la version du design system pris comme un tout. Bump **minor** on additive token/component changes, **major** on a token rename/removal that breaks existing pages. Record the bump reason under `provenance`.
- `design-system.md` carries its own `version:` line; `release.json § charter.version` l'enregistre. Un écart entre versions déclarées est une donnée, jamais une violation.
