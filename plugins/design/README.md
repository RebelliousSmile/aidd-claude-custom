# design

*Plugin de design system en entonnoir : du brief ou de la référence jusqu'à des éléments répétables vérifiés par un gate de lint.*

Principe directeur : **la seule référence opposable est celle qu'un outil sait lire** — pas la charte (prose), pas les maquettes (divergentes), mais les artefacts JSON racinés par `release.json`, dont un linter dérive ses règles à chaque livraison.

## Ce que les gates garantissent — et ce qu'ils ne garantissent pas

Deux gates de natures différentes, qui doivent être verts ensemble et dont aucun ne remplace l'autre : le **vocabulaire** (`lint-core.mjs`, référence interne — le contrat) et la **fidélité** (`measure.py`, référence externe — la maquette résolue). Chacun a une portée bornée, et ce qu'ils ne couvrent pas — rôles ARIA, fond réellement appliqué, fichiers hors cibles déclarées — est un **gap déclaré**, pas une vérification silencieuse. Énoncé complet : [`references/gate-natures.md`](references/gate-natures.md).

Au-dessus des deux, un **seuil de maturité** : la conformité ne s'affirme qu'à partir de `validated`. `tools/run-gates.py` relève le statut du contrat après le lint et **sort en 4** en deçà — violations toujours listées, conformité non affirmée, chemin de remontée nommé. Un contrat migré depuis 1.x entre à `normalized`, donc sous le seuil : aucun droit acquis. Énoncé : [`references/maturity-status.md`](references/maturity-status.md).

Le vocabulaire de classes est **ouvert par défaut** — une classe dont le bloc n'est pas déclaré est traitée comme utilitaire ; il ne se referme que sous `--strict`, en `warning`, sur les seules classes de forme BEM. Détail : `skills/enforce/SKILL.md § Périmètre de lint-core.mjs`.

## Flux

```
detail → define → destructure → adjust → enforce → diffuse
  ↓         ↓          ↓            ↓         ↓         ↓
carte     poser    challenger     figer    verrou    produire
```

- **detail** (verbe 0) — **lecture seule, aucun artefact.** Explique la carte de l'entonnoir (rôle · entrée · sortie · artefacts · gate · fichier autoritaire de chaque verbe) et route une intention vers l'une des six classes de cas agnostiques de la stack (`mockup-multipage`, `brief-only`, `codebase-inherited`, `element-evolution`, `contract-drift`, `element-production`). N'exécute jamais ce qu'il décrit. Quand le pivot `sc-*` correspondant est installé et que la stack correspond, la classe est étendue par le **workflow de plateforme** du pivot (squelette figé par le contrat de pivot). Voir [`references/sc-pivot-contract.md § Workflow de plateforme`](references/sc-pivot-contract.md).
- **define** — pose, écoute, construit la matière : tokens de travail, inventaire composants candidat, charte brouillon. Depuis une référence (screenshot, Figma, URL) ou un brief. Peut injecter le profil mobile-first/a11y optionnel.
- **destructure** — challenge la direction avant de la figer : critique des angles (a11y, cohérence, mobilité…), pistes alternatives. Pendant design de `aidd-refine:challenge`.
- **adjust** — arbitre les maquettes divergentes (motif dominant gagne ; gate humain sur les cas non tranchables), **fige le contrat**, **génère les artefacts dérivés** (`tools/generate.py`) et **migre un contrat 1.x** vers le format 2.0.
- **enforce** — dérive un linter portable (`lint-core.mjs`) du contrat figé, câble 4 gates (import `tokens.css`, règles de génération, success_condition des plans, pre-commit). Pivot vers `sc-php:design-bridge` ou `sc-js:design-bridge` pour une réalisation native idiomatique. **Depuis 1.1.0 : un 2ᵉ gate de *fidélité*** (`05-fidelity-gate`) mesure le rendu vs la maquette résolue (voir copycat).
- **diffuse** — produit des éléments répétables (spec neutre + baseline HTML/CSS ou pivot sc-*). **Refus absolu de livrer si lint exit 1** ; **refus de rendre si `generate.py --check` exit ≠ 0** (artefact dérivé retouché à la main, ou source modifiée sans régénération).

## Contrat (figé à `adjust`)

Cinq artefacts, racinés par `design/release.json` — trois requis, deux optionnels (`oracle.json`, `deviations.json`). Chacun a un lecteur nommé ; `release.json` porte les versions, les empreintes, la provenance et le statut de maturité.

| Artefact | Contenu | Lecteur |
|----------|---------|---------|
| `design/tokens.json` (W3C DTCG) | valeurs nommées, source unique | `lint-core.mjs`, adapters |
| `design/components.json` | anatomie des composants | `lint-core.mjs` |
| `design/policies.json` | `mode`, `$utilityPrefixes`, `usage`, liste d'émission des adapters | `lint-core.mjs`, `tools/generate.py` |
| `design/oracle.json` | cibles de mesure de fidélité | `config-gen.py` |
| `design/deviations.json` | registre des écarts tolérés (`active` sanctionne, `historical` = audit) | `measure.py --ledger-registry`, `tools/generate.py` |

`oracle.json` et `deviations.json` sont **optionnels** ; `tokens.json`/`components.json`/`policies.json` sont requis. `design/design-system.md` est une **entrée** du contrat, pas un artefact : charte prose, écrite par un humain ; sa présence et sa version sont constatées dans `release.json`. Aucun outil ne la lit.

**Règle cardinale : une donnée vit dans un seul artefact.** Toute couleur dans un composant = token `color.*`. Toute classe dont le bloc est déclaré dans `components.json` doit y figurer entièrement (élément ou modificateur) — les autres sont traitées comme utilitaires.

Un contrat sans `release.json` est au format 1.x : le linter ne le parse pas, il sort en **3** et nomme la commande de migration (`tools/migrate-contract.py`).

## Statut de maturité et seuil de conformité (2.4.0)

`release.json § status` porte un statut **calculé** par `tools/status.py` — jamais écrit à la main. C'est une échelle : le premier échelon dont la condition n'est pas remplie arrête la montée, puis un gap enregistré peut plafonner plus bas.

| Statut | Requiert | Autorise |
|--------|----------|----------|
| `extracted` | les artefacts existent | la génération, aucune conformité |
| `normalized` | + charte présente | (contrat migré 1.x entre ici) |
| `validated` | + vérifications enregistrées (`checks`) | **l'invocation de la conformité** (seuil) |
| `production-ready` | + contraste vert sur chaque paire et états déclaratifs complets | certifie l'a11y calculable |

Les écarts connus vivent dans `release.json § gaps[]` (`class` / `caps` / `detail`) et **plafonnent** le statut au lieu d'être notés en prose : charte absente → `extracted` · contraste jamais calculé → `normalized` · une paire de contraste ou un état qui échoue → `validated`. L'a11y calculable est scindée (dec-002) : le **contraste par thème** (`adapters/a11y/contrast.py`, déterministe, au figeage) et la **présence déclarative des états** (`status.py --states`, sans markup) pèsent sur le statut ; les **rôles ARIA** restent du markup réalisé par pivot. Seuil et table complète : [`references/maturity-status.md`](references/maturity-status.md).

## Artefacts dérivés (2.1.0)

Un artefact dérivé n'est jamais écrit à la main. `tools/generate.py` en est le seul producteur : il lit les sources du contrat et émet un fichier par entrée de `policies.json § adapters[]` déclarant un `consumer` — un **rôle** (feuille de style, source pré-processée, configuration de build, fichier de tokens de plateforme), jamais un nom de plateforme. Une entrée sans `consumer` reste déclarative, non émise.

```
python ${CLAUDE_PLUGIN_ROOT}/tools/generate.py --contract design/     # au figeage
python ${CLAUDE_PLUGIN_ROOT}/tools/generate.py --check --contract design/   # avant tout rendu
```

Le figeage grave dans `release.json § generated` l'empreinte de chaque source lue ; `--check` l'oppose ensuite aux fichiers présents. Une retouche manuelle et une source périmée sortent toutes deux en **1**, et **aucun drapeau ne neutralise l'échec** : on change la source, on régénère. Exits : `0` conforme · `1` dérive · `2` invocation ou artefact invalide · `3` contrat 1.x.

## Skills

| Skill | Invocation | Description |
|-------|-----------|-------------|
| `detail` | `/design:detail` | **Verbe 0, lecture seule, aucun artefact.** `explain` : la carte des verbes. `route` : la séquence exécutable pour l'une des six classes de cas agnostiques, étendue par le workflow de plateforme du pivot `sc-*` installé. |
| `define` | `/design:define` | Extraction depuis références/brief → tokens + inventaire + charte brouillon. Profil mobile-first optionnel. |
| `destructure` | `/design:destructure` | Challenge la direction design — critique multi-angles + pistes alternatives. |
| `adjust` | `/design:adjust` | Arbitrage maquettes + figeage du contrat (tokens · components · policies · oracle, racine release.json) + migration 1.x → 2.0. |
| `enforce` | `/design:enforce` | Linter portable dérivé du contrat · 4 gates · pivot par langage · lint des instances existantes. |
| `diffuse` | `/design:diffuse` | Éléments répétables sous gate lint · baseline HTML/CSS · pivot par langage. |
| `harness` | `/design:harness` | Génère le harness HTML autonome (`setPage`/`setViewport`) piloté par l'oracle de fidélité et le fan-out `copycat`. |

## Enforcement hybride

`enforce` et `diffuse` fonctionnent en mode hybride :

1. **Baseline** — `lint-core.mjs` portable (Node.js, aucune dépendance), dérivé du contrat à l'exécution.
2. **Pivot** (si installé) — `sc-<langage>:design-bridge` réalise nativement les règles que le cœur portable ne peut pas lire. Le routage se fait sur le **type d'enforcement** de chaque règle, jamais sur le nom de la plateforme : `references/enforcement-registry.md`.

Aucun `sc-<langage>` installé → le cœur portable tourne seul, et les règles qui exigeaient un réceptacle sont déclarées **non réalisées** dans le rapport du gate. Le code de sortie est inchangé : une règle non réalisée n'est ni une violation ni une conformité.

Le runner oppose ensuite le **seuil de maturité** : sous `validated`, il sort en **4** (violations toujours listées, conformité non affirmée, chemin de remontée nommé). Le seuil a une seule source exécutable — la constante `THRESHOLD` de `status.py`, importée par `run-gates.py` — et une seule source humaine, `references/maturity-status.md`.

## copycat — réplication de maquette mesurée (1.1.0)

`copycat` industrialise la copie conforme d'une maquette arbitraire vers le contrat, **sans nouveau verbe** (l'entonnoir reste à 5). C'est :

- un **agent** (`agents/copycat.md`, `model: sonnet`) — opérateur **par page** : mesure les styles calculés, classe chaque écart à sa couche, propose des contributions tokens/composants. Trois frontières : il PROPOSE (n'arbitre/fige jamais), la mesure vit dans le **script déterministe**, et c'est une **feuille** (ne spawn aucun agent).
- un **oracle Python** (`adapters/measure/`) — `getComputedStyle` **par breakpoint** (Mode A extraction / Mode B diff), cross-OS, sans dépendance Node.
- deux **câblages** dans l'entonnoir :
  - `define/05-copycat-fanout` — fan-out parallèle (1 agent/page, `Agent`/`Workflow`) → table de correspondance agrégée au **checkpoint humain** (avant `adjust`) ; conflits inter-pages remontés, pas arbitrés.
  - `enforce/05-fidelity-gate` — **2ᵉ gate** : fidélité du rendu vs la maquette résolue (référence **externe**), en plus du lint vocabulaire (référence **interne**) ; les deux doivent être verts, chacun dans sa portée (`references/gate-natures.md`).

Responsive : règle **ask-or-derive** — mesurer chaque breakpoint si la maquette le fournit, sinon déduire du profil mobile-first et **flaguer** (le tablette est le cas « derive » canonique). Écarts tolérés déclarés dans **`deviations.json`** (source, lu par `measure.py --ledger-registry`) ; `ds-deviation-ledger.md` en est la **vue Markdown générée** par `tools/generate.py` (on édite le JSON, jamais la vue). Un écart n'est sanctionné que par une entrée `active` non expirée portant sa valeur `expected` (DRY/SOLID d'abord, pixel-identique sinon) ; sinon le verdict est `OPEN`.

## Artefacts produits dans le projet

```
design/
  release.json           # racine — versions, empreintes, provenance, statut, generated
  tokens.json            # valeurs — W3C DTCG, source unique
  components.json        # anatomie — nomenclature déclarée, base du linter
  policies.json          # mode, préfixes utilitaires, usage, liste d'émission
  oracle.json            # cibles de mesure de fidélité (optionnel)
  deviations.json        # registre des écarts tolérés — active sanctionne (optionnel)
  design-system.md       # entrée — charte prose, figée après adjust
  adapters/              # dérivés — produits par generate.py seul, jamais à la main
  lint/
    run-gates.py         # runner d'agrégation — seule commande du gate, aux trois sites d'appel
    lint-core.mjs        # linter portable dérivé du contrat, invoqué par le runner
    migrate-contract.py  # migration 1.x → 2.0, nommée par l'exit 3 du linter
    status.py            # statut de maturité — seule implémentation ; THRESHOLD importé par run-gates.py
    contrast.py          # oracle de contraste WCAG AA par thème, déterministe (au figeage)
    gates.config.json    # périmètre exécutable — contrat, cibles, rapports de pivot
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
