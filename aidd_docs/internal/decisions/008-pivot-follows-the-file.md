# Decision: le pivot suit le fichier — un projet a autant de plugins applicables que de stacks

| Field   | Value |
|---------|-------|
| ID      | DEC-008 |
| Date    | 2026-07-30 |
| Feature | `overcode:control` — contrat de pivot `testing`, résolution polyglotte |
| Status  | Accepted |
| Antécédents | **DEC-004** — consommation d'un pivot `sc-*` par un autre plugin ; §5 (le contrat est une interface publique) qualifie le présent changement. **DEC-007** — la phase est l'autorité classante ; la présente décision ne touche à aucune autorité, seulement à la résolution du fournisseur |

## Context

`references/pivot-contract.md` › *Detecting the active language plugin* disait : *« whichever language plugin is already installed and applicable is reused »*, au **singulier**. Rien n'énonçait ce qui se passe quand deux le sont.

Or c'est le cas ordinaire :

| Dépôt | Deux stacks dans un seul arbre |
|---|---|
| `suddenly/_code/app` | backend Django + `frontend/package.json` |
| `choix-narratifs/_code` | Astro/TS + `engine/` en Rust, un seul `package.json` déclarant `vitest run` **et** `cargo test --manifest-path engine/Cargo.toml` |
| `lyremember/_code/app` | Vue/Vite + `rust-backend/` + pytest |
| `scriptami/_code/wp-2026` | 52 fichiers PHP + une chaîne de lint Node |

Sur `choix-narratifs`, les tests TS vivent dans `tests/narrative/*.test.ts`, les tests Rust vivent **dans les fichiers source** de `engine/core/src/` (`#[cfg(test)]`). Aucun *Test file glob* d'une stack n'atteint la population de l'autre.

Deux suites d'évals portaient déjà une cause de N/A qui en dépendait (`domains-scenarios.md:316`), avec la mention qu'elle *« se lira comme fausse à la première vérification »*.

## Decision

**Le pivot suit le fichier.** La détection rend un **ensemble**, jamais un gagnant. Chaque plugin applicable contribue son pivot, et un champ est résolu par le pivot du plugin dont la stack contient le fichier considéré.

Quatre conséquences, énoncées dans le contrat pour qu'aucun consommateur n'ait à s'en inventer une :

1. **Les énumérations sont des unions, et elles disent ce qu'elles ont combiné.** Un fichier qu'aucun glob ne prend n'est pas *pas un test* — c'est un fichier hors des stacks énumérées, rapporté comme tel. Une sous-énumération se lit exactement comme une population propre.
2. **Rien n'est sommé entre stacks.** Décomptes, densités, chiffres de couverture et lignes d'outillage sont rendus par stack, la stack nommée. Un nombre unique sur deux populations comptées par deux conventions énonce une quantité que rien n'a mesurée.
3. **L'absence se dit d'une stack, jamais du run.** *« Aucun pivot disponible »* dit d'un projet polyglotte est faux dès qu'une de ses stacks en a un.
4. **Un même champ répondu différemment par deux pivots n'est pas un conflit à arbitrer** — les deux réponses portent sur des fichiers différents. Un consommateur qui exige une réponse unique pour tout le projet pose une question que le projet n'a pas.

L'applicabilité se relit au `scope` du run, pas une fois pour le dépôt : un plugin applicable au dépôt mais à aucun fichier sous `scope` ne contribue rien à ce run.

## Rationale

**L'alternative était l'élection au manifeste** — désigner la stack dominante et lire son pivot pour tout le projet. Elle est rejetée sur un contre-exemple, pas sur un principe : sur `app`, la présence d'un `package.json` élirait `sc-js`, c'est-à-dire le seul des deux plugins dont la stack ne porte pas les 80 fichiers `test_*.py`. Une élection choisit un fournisseur ; ce qu'il faut choisir est une **correspondance**, et la seule qui ne se trompe jamais est celle que le fichier porte lui-même.

**Ce que la règle ne fait pas.** Elle ne donne aucune autorité nouvelle à un pivot. La borne de DEC-007 tient intégralement : le pivot fournit du savoir de stack, il ne classe pas. Multiplier les fournisseurs multiplie le savoir disponible, jamais le nombre d'instances qui tranchent — la cellule de la matrice reste seule à le faire.

**Ce qu'elle coûte au consommateur.** Six actions rendaient une valeur unique là où il en faut une par stack. Le coût réel n'est pas la pluralité, c'est l'**attribution** : une ligne rendue sans nommer sa stack devient indistinguable d'une ligne rendue pour le projet entier, et c'est le mode d'échec que les quatre conséquences ferment une à une.

## Compatibility

**Additif, pas cassant.** Aucun champ n'est renommé, retiré ni reformulé ; aucun pivot livré n'a à changer. Le contrat rend plurielle une résolution qui était singulière — un cas de plus traité. DEC-004 §5 qualifie de majeur ce qui rend un pivot existant illisible ; ici un pivot existant reste lu à l'identique, simplement plus seul. D'où `overcode` **4.0.0 → 4.1.0**.

## Consequences

- `references/pivot-contract.md` : section *Detecting the applicable language plugins* réécrite, sous-section *The pivot follows the file* ajoutée, *Locating the testing pivot* et *Absence* mises au pluriel.
- Les six actions consommatrices alignées : `01-write`, `02-audit`, `03-configure`, `04-strengthen`, `05-stats`, `06-align`.
- `02-audit` : l'**énumération partielle** devient un constat au même titre que l'énumération vide.
- `05-stats` : `ratio`, `counting` et le bloc `TOOLING` rendus une fois par stack ; le reste de l'instantané reste au niveau projet.
- **Reste à vérifier en vol** : la règle n'a encore tourné sur aucune fixture polyglotte. `choix-narratifs/_code` est le terrain — deux runners déclarés dans un manifeste, deux conventions de test incompatibles, en lecture seule.
