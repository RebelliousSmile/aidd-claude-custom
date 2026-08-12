---
name: adjust
description: Freezes a draft or a scoped delta into the versioned design contract and migrates legacy contracts. Use when the user wants to arbitrate, canonicalize, freeze, re-freeze, or migrate design-system decisions.
---

# adjust

## Rôle dans l'entonnoir

```
define (malléable) → destructure (malléable) → adjust (FIGEAGE) → enforce → diffuse
```

`adjust` est le point de non-retour : tout ce qui entre sort figé. Il est cependant **rejouable** — si `destructure` identifie une piste requérant un re-figeage (coût contrat `demande un re-figeage`), `adjust` rejoue le delta, bumpe la version et `enforce` propage.

## Ce que adjust produit

| Artefact | Statut après adjust |
|----------|---------------------|
| `design/tokens.json` | Canonisé (dédupliqué, groupes requis vérifiés) |
| `design/components.json` | Créé ou mis à jour — anatomie déclarée ; le vocabulaire qu'elle induit est **ouvert par défaut**, cf. `references/manifest-schema.md § Invariants` |
| `design/policies.json` | `mode`, préfixes utilitaires, règles d'usage, table des adapters |
| `design/oracle.json` | Cibles de mesure par composant |
| `design/release.json` | Racine : versions par artefact, empreintes, provenance, statut de maturité |
| `design/design-system.md` | `status: figé` · version bumped · Provenance mise à jour |

## Ce que adjust NE fait PAS

- Adjust ne critique pas la direction visuelle (→ `destructure`).
- Adjust n'installe pas de linter ni ne câble des gates (→ `enforce`).
- Adjust ne produit pas d'éléments répétables ni d'exports (→ `diffuse`).

## Flux

```
01-arbitrate → résolution des conflits → 02-freeze → contrat figé
03-migrate   → contrat 1.x → contrat 2.0 (hors flux, à la demande)
```

1. **01-arbitrate** — collecte la matière malléable (define output + pistes destructure), compte les occurrences de chaque option, tranche automatiquement sur motif dominant (≥ 2/3), expose les cas non tranchables à l'humain.
2. **02-freeze** — prend le brief d'arbitrage résolu, canonise `tokens.json`, écrit les cinq artefacts et `release.json`, marque `design-system.md` figé, bumpe les versions.
3. **03-migrate** — convertit un contrat 1.x existant. Pilote `tools/migrate-contract.py` et vérifie la non-régression du verdict. Ne s'enchaîne pas avec `01`/`02` : c'est une entrée indépendante, déclenchée par un exit 3 du linter ou par une demande explicite.

## Mode re-figeage

Si le contrat existe déjà (projet déjà figé), `adjust` rejoue uniquement sur le **delta** (nouvelles pistes ou tokens modifiés). Les composants et tokens non touchés sont conservés. La version est bumped minor (delta additif) ou major (renommage/suppression). Un contrat encore en 1.x se migre d'abord (`03-migrate`) — un re-figeage ne fait pas la conversion au passage.

## Références

- `${CLAUDE_PLUGIN_ROOT}/references/contract-schema.md` — les cinq artefacts, la racine `release.json`, la redistribution depuis un contrat 1.x
- `${CLAUDE_PLUGIN_ROOT}/skills/adjust/references/manifest-schema.md` — structure et invariants de `components.json`
- `${CLAUDE_PLUGIN_ROOT}/references/design-system-contract.md` — règles de consommation du contrat
- `${CLAUDE_PLUGIN_ROOT}/references/token-schema.md` — groupes requis, liaison tokens ↔ artefacts
