# design

*Plugin de design system en entonnoir : du brief ou de la référence jusqu'à des éléments répétables vérifiés par un gate de lint.*

Principe directeur : **la seule référence opposable est celle qu'un outil sait lire** — pas la charte (prose), pas les maquettes (divergentes), mais les artefacts JSON racinés par `release.json`, dont un linter dérive ses règles à chaque livraison.

## Ce que les gates garantissent — et ce qu'ils ne garantissent pas

Deux gates de natures différentes, qui doivent être verts ensemble et dont aucun ne remplace l'autre : le **vocabulaire** (`lint-core.mjs`, référence interne — le contrat) et la **fidélité** (`measure.py`, référence externe — la maquette résolue). Chacun a une portée bornée, et ce qu'ils ne couvrent pas — contraste, rôles ARIA, fond réellement appliqué, fichiers hors cibles déclarées — est un **gap déclaré**, pas une vérification silencieuse. Énoncé complet : [`references/gate-natures.md`](references/gate-natures.md).

Le vocabulaire de classes est **ouvert par défaut** — une classe dont le bloc n'est pas déclaré est traitée comme utilitaire ; il ne se referme que sous `--strict`, en `warning`, sur les seules classes de forme BEM. Détail : `skills/enforce/SKILL.md § Périmètre de lint-core.mjs`.

## Flux

```
define → destructure → adjust → enforce → diffuse
  ↓           ↓            ↓         ↓         ↓
poser      challenger     figer    verrou    produire
```

- **define** — pose, écoute, construit la matière : tokens de travail, inventaire composants candidat, charte brouillon. Depuis une référence (screenshot, Figma, URL) ou un brief. Peut injecter le profil mobile-first/a11y optionnel.
- **destructure** — challenge la direction avant de la figer : critique des angles (a11y, cohérence, mobilité…), pistes alternatives. Pendant design de `aidd-refine:challenge`.
- **adjust** — arbitre les maquettes divergentes (motif dominant gagne ; gate humain sur les cas non tranchables), **fige le contrat** et **migre un contrat 1.x** vers le format 2.0.
- **enforce** — dérive un linter portable (`lint-core.mjs`) du contrat figé, câble 4 gates (import `tokens.css`, règles de génération, success_condition des plans, pre-commit). Pivot vers `sc-php:design-bridge` ou `sc-js:design-bridge` pour une réalisation native idiomatique. **Depuis 1.1.0 : un 2ᵉ gate de *fidélité*** (`05-fidelity-gate`) mesure le rendu vs la maquette résolue (voir copycat).
- **diffuse** — produit des éléments répétables (spec neutre + baseline HTML/CSS ou pivot sc-*). **Refus absolu de livrer si lint exit 1.**

## Contrat (figé à `adjust`)

Quatre artefacts, racinés par `design/release.json`. Chacun a un lecteur nommé ; `release.json` porte les versions, les empreintes, la provenance et le statut de maturité.

| Artefact | Contenu | Lecteur |
|----------|---------|---------|
| `design/tokens.json` (W3C DTCG) | valeurs nommées, source unique | `lint-core.mjs`, adapters |
| `design/components.json` | anatomie des composants | `lint-core.mjs` |
| `design/policies.json` | `mode`, `$utilityPrefixes`, `usage`, table des adapters | `lint-core.mjs` |
| `design/oracle.json` | cibles de mesure de fidélité | `config-gen.py` |

`design/design-system.md` est une **entrée** du contrat, pas un artefact : charte prose, écrite par un humain ; sa présence et sa version sont constatées dans `release.json`. Aucun outil ne la lit.

**Règle cardinale : une donnée vit dans un seul artefact.** Toute couleur dans un composant = token `color.*`. Toute classe dont le bloc est déclaré dans `components.json` doit y figurer entièrement (élément ou modificateur) — les autres sont traitées comme utilitaires.

Un contrat sans `release.json` est au format 1.x : le linter ne le parse pas, il sort en **3** et nomme la commande de migration (`tools/migrate-contract.py`).

## Skills

| Skill | Invocation | Description |
|-------|-----------|-------------|
| `define` | `/design:define` | Extraction depuis références/brief → tokens + inventaire + charte brouillon. Profil mobile-first optionnel. |
| `destructure` | `/design:destructure` | Challenge la direction design — critique multi-angles + pistes alternatives. |
| `adjust` | `/design:adjust` | Arbitrage maquettes + figeage du contrat (tokens · components · policies · oracle, racine release.json) + migration 1.x → 2.0. |
| `enforce` | `/design:enforce` | Linter portable dérivé du contrat · 4 gates · pivot sc-php/sc-js · lint instances/DB. |
| `diffuse` | `/design:diffuse` | Éléments répétables sous gate lint · baseline HTML/CSS · pivot sc-php/sc-js. |
| `harness` | `/design:harness` | Génère le harness HTML autonome (`setPage`/`setViewport`) piloté par l'oracle de fidélité et le fan-out `copycat`. |

## Enforcement hybride

`enforce` et `diffuse` fonctionnent en mode hybride :

1. **Baseline** — `lint-core.mjs` portable (Node.js, aucune dépendance), dérivé du contrat à l'exécution.
2. **Pivot** (si disponible) — `sc-php:design-bridge` (WP FSE, PHP) ou `sc-js:design-bridge` (Vue/React/TS) pour une réalisation native idiomatique.

Dégradation gracieuse : pas de sc-\<techno\> → baseline active, non bloquant.

## copycat — réplication de maquette mesurée (1.1.0)

`copycat` industrialise la copie conforme d'une maquette arbitraire vers le contrat, **sans nouveau verbe** (l'entonnoir reste à 5). C'est :

- un **agent** (`agents/copycat.md`, `model: sonnet`) — opérateur **par page** : mesure les styles calculés, classe chaque écart à sa couche, propose des contributions tokens/composants. Trois frontières : il PROPOSE (n'arbitre/fige jamais), la mesure vit dans le **script déterministe**, et c'est une **feuille** (ne spawn aucun agent).
- un **oracle Python** (`adapters/measure/`) — `getComputedStyle` **par breakpoint** (Mode A extraction / Mode B diff), cross-OS, sans dépendance Node.
- deux **câblages** dans l'entonnoir :
  - `define/05-copycat-fanout` — fan-out parallèle (1 agent/page, `Agent`/`Workflow`) → table de correspondance agrégée au **checkpoint humain** (avant `adjust`) ; conflits inter-pages remontés, pas arbitrés.
  - `enforce/05-fidelity-gate` — **2ᵉ gate** : fidélité du rendu vs la maquette résolue (référence **externe**), en plus du lint vocabulaire (référence **interne**) ; les deux doivent être verts, chacun dans sa portée (`references/gate-natures.md`).

Responsive : règle **ask-or-derive** — mesurer chaque breakpoint si la maquette le fournit, sinon déduire du profil mobile-first et **flaguer** (le tablette est le cas « derive » canonique). Écarts tolérés tracés dans `ds-deviation-ledger.md` (DRY/SOLID d'abord, pixel-identique sinon).

## Artefacts produits dans le projet

```
design/
  release.json           # racine — versions, empreintes, provenance, statut
  tokens.json            # valeurs — W3C DTCG, source unique
  components.json        # anatomie — nomenclature déclarée, base du linter
  policies.json          # mode, préfixes utilitaires, usage, adapters
  oracle.json            # cibles de mesure de fidélité
  design-system.md       # entrée — charte prose, figée après adjust
  lint/
    lint-core.mjs        # linter portable dérivé du contrat
    migrate-contract.py  # migration 1.x → 2.0, nommée par l'exit 3 du linter
    status.py            # statut de maturité, importé par la migration
    .lintrc.json         # chemins cibles
```

## Démarrage rapide

```
/design:define          # poser le contrat depuis brief ou référence
/design:destructure     # challenger avant de figer (optionnel mais recommandé)
/design:adjust          # arbitrer + figer le contrat (ou migrer un contrat 1.x)
/design:enforce         # câbler le linter + les 4 gates
/design:diffuse <comp>  # produire sous gate
```

## Profil mobile-first optionnel

`define` propose le profil `profile-mobile-first.md` (7 conventions : mobile-first authoring, enrichissement progressif, UX mobile-only, tokens sans magic number, composants à variantes, baseline a11y, iconographie sans emoji). Il s'installe dans `.claude/rules/08-design/` uniquement si retenu.

## Licence

MIT — voir [LICENSE](../../LICENSE).
