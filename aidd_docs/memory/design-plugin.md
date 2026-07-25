# design — état du plugin

| Champ | Valeur |
|---|---|
| Version courante | 2.5.0 |
| Dernière release | 2026-07-25 |

## Architecture — verbe 0 + entonnoir 5 verbes

`detail (0) → define → destructure → adjust → enforce → diffuse`

| Verbe | Rôle |
|---|---|
| `detail` | **Verbe 0, lecture seule, aucun artefact** : `explain` (carte des verbes) + `route` (séquence exécutable pour une des 6 classes de cas). Voir `### Verbe 0 detail (Lot 6, 2.5.0)` |
| `define` | Extraction depuis référence/brief → tokens + inventaire composants + charte brouillon |
| `destructure` | Challenge multi-angles avant figeage |
| `adjust` | Arbitrage + figeage du contrat + **génération des dérivés** + **migration 1.x → 2.0** |
| `enforce` | Linter portable borné + runner d'agrégation + 4 gates + pivot par **langage** |
| `diffuse` | Éléments répétables sous gate lint |

## Contrat 2.0 — quatre artefacts, une racine (cristallise à `adjust`)

| Artefact | Contenu | Lecteur nommé |
|---|---|---|
| `design/release.json` | **racine** — versions par artefact, empreintes de source, provenance, statut de maturité, `generated` (enregistrement de dérive) | racine du contrat, `tools/generate.py` |
| `design/tokens.json` (W3C DTCG) | valeurs nommées, source unique | `lint-core.mjs`, adapters |
| `design/components.json` | anatomie seule | `lint-core.mjs` |
| `design/policies.json` | `mode`, `$utilityPrefixes`, `usage`, liste d'émission des adapters | `lint-core.mjs`, `tools/generate.py` |
| `design/oracle.json` | cibles de mesure de fidélité | `config-gen.py` |

`design/design-system.md` est une **entrée**, pas un artefact : `release.json § charter` constate sa présence et sa version.

**Invariant cardinal** : une donnée vit dans un seul artefact.

### Ruptures 2.0.0 (BREAKING)

- **`release.json` obligatoire.** Son absence = contrat 1.x → `lint-core.mjs` sort en **3** en imprimant la commande de migration. Aucun chemin de lecture 1.x ne subsiste.
- **`mode` déclaré, jamais déduit.** Fini l'inférence `utility-first` depuis un `components` vide (un vert sur rien). Absent → exit 2.
- **Parité de versions supprimée.** L'invariant 5 (`$version` ↔ `version:` de la charte) disparaît : versions par artefact, un écart est une donnée.
- **Migration outillée** : `python plugins/design/tools/migrate-contract.py --contract <dir> [--dry-run] [--mode bem|utility-first] [--now <ISO>]`. Sauvegarde en `.contract-1x/`, seconde exécution no-op, aucun champ perdu (clé inconnue transportée + signalée en anomalie). Action : `adjust/03-migrate`.
- **Statut de maturité** : `tools/status.py` détient seul l'échelle `extracted → normalized → validated → production-ready`. Écrit dans `release.json` ; **opposé au seuil `validated` depuis le Lot 5** (voir `### Maturité au figeage`).
- **Codes de sortie** `lint-core.mjs` : 0 ok · 1 violation · 2 invocation/environnement (dont une décision refusée) · 3 contrat 1.x.
- Décision : `aidd_docs/internal/decisions/005-design-2-0-contract-split.md`. Schéma : `plugins/design/references/contract-schema.md`.

## Portée réelle des gates (purge 1.17.0)

Le plugin documentait des règles de fond, a11y, concordance de couches et contraste WCAG comme comportements d'`enforce`. `lint-core.mjs` implémente **cinq règles** et aucune de celles-là. 1.17.0 les retire ou les requalifie et tague chaque champ du contrat *exécutable* (consommateur nommé) ou *informationnel*.

- **Vocabulaire ouvert par défaut** : une classe dont le bloc n'est pas déclaré est traitée comme utilitaire. Fermeture uniquement sous `--strict`, en `warning`, sur les classes de forme BEM hors `$utilityPrefixes`.
- `lint-core.mjs` scanne **un fichier de markup à la fois**, comme du texte. Hors périmètre par construction : CSS, liaisons dynamiques, contenu stocké, fichiers de thème de plateforme, cohérence inter-fichiers.
- **Gaps déclarés, non vérifiés** : contraste WCAG, rôles ARIA, fond réellement appliqué.
- Invariants 3, 4, 7 du manifeste sont réels mais tenus **au figeage** par `adjust/02-freeze.md`, jamais par le linter.
- Baseline des huit fixtures (ordre lexicographique) : `0 1 0 1 0 1 0 1` — pinnée par le plan Lot 0, à re-vérifier après toute modification du linter **et après toute migration de contrat** (c'est le contrôle de non-régression du Lot 1). Ne s'obtient qu'en fournissant le répertoire de contrat en `--contract`.
- Émission des adapters : règle canonique unique dans `references/write-system-procedure.md § Adapter emission rule` — **détection de rôles consommateurs**, pas écriture de fichiers.

## Génération déterministe (2.1.0, Lot 2)

`tools/generate.py` est le **seul producteur** d'un artefact dérivé. Aucun modèle, aucune procédure n'en écrit un.

- **Entrée** : `policies.json § adapters[]` — devenue **exécutable**. Un artefact émis par entrée déclarant un `consumer` ; entrée sans `consumer` (ou `unknown`) = déclarative, non émise, signalée une fois sur stderr.
- **Émetteurs indexés par rôle de consommateur, jamais par stack** — c'est ce qui tient DEC-002 (le générateur émet le QUOI ; le rendu propre à une stack reste aux pivots `sc-*`) et le critère d'agnosticité : `generate.py` ne contient aucune branche nommant une plateforme. `CSS_ROLES = ("stylesheet", "stylesheet source")` · `FLAT_ROLES = ("platform token file", "build configuration")`.
- **Résolution des alias dépendante du rôle** : rôles CSS → `var(--…)` (la cascade porte les thèmes) ; rôles plats → littéral résolu (pas de cascade). Thèmes : `dark` en classe, tout autre thème en attribut `[data-theme="…"]`, mêmes noms de variables dans chaque bloc.
- **Déterminisme** : ordre de source jamais retrié, LF, une déclaration par ligne, bannière nommant les sources. Deux exécutions ⇒ arbres identiques octet pour octet.
- **Enregistrement de dérive** : `release.json § generated` porte un `sha256` **par source lue** (pas un hash unique sur le jeu concaténé — le message doit nommer la source qui a bougé). Écrit au figeage par `adjust/02-freeze`, en préservant les fins de ligne du fichier (il est écrit à la main).
- **Gate** : `diffuse/02-render` **Étape 0** = `generate.py --check`. Exit ≠ 0 ⇒ pas de rendu. Retouche manuelle et source périmée sortent en **1**, et **aucun drapeau ne neutralise l'échec**.
- Exits (espace du plan maître, non réassignable) : `0` · `1` dérive · `2` invocation/artefact invalide · `3` contrat 1.x.
- Contrainte tenue : `define` **ne peut pas** appeler le générateur — il lui est interdit d'écrire `release.json` et `policies.json`, qui en sont les entrées requises. `define` écrit `tokens.json` + la charte et **détecte** les consommateurs ; les dérivés n'existent qu'à partir du figeage.

## Enforcement distribué (2.2.0, Lot 3)

**Une règle déclarée a un réalisateur nommé, ou est visiblement déclarée non réalisée.** Le linter portable n'est plus présenté comme le gate du système : il en est un réalisateur parmi d'autres.

- **Type d'enforcement = la preuve que la règle doit lire**, jamais le nom d'une plateforme. Registre : `references/enforcement-registry.md` — `markup` (lint-core.mjs) · `stylesheet` (sc-css) · `source-graph` (sc-js) · `stored-content` (sc-php) · `platform-config` (pivot du langage) · `unrealized` (marqueur). Retirés : `baseline` (→ `markup`) et `pivot-only` (→ re-typé par l'auteur).
- **Routage sur le langage de la preuve**, pas sur la plateforme ni le framework : le nommage `sc-<langage>` remplace partout l'ancien `sc-<techno>`. Un projet peut désigner deux réceptacles distincts (langage des feuilles ≠ langage du runtime).
- **Runner** `tools/run-gates.py` — **il route, il n'évalue jamais** : il ne lit que la configuration, `policies.json`, la sortie `lint-core.mjs --json` et les rapports de pivot. Une seule commande aux trois sites d'appel : `python design/lint/run-gates.py --config design/lint/gates.config.json` (local · pre-commit · CI). Exits : `0` · `1` violation · `2` invocation/environnement · `3` contrat 1.x.
- **Prérequis Python assumé** : le runner est Python, donc Python 3.10+ devient un prérequis de pre-commit **même sur un projet 100 % JavaScript** (Node 18+ reste requis pour le linter invoqué). Énoncé une fois dans `skills/enforce/references/gate-wiring.md`. Un runtime absent sort en **2**, jamais en 1 et jamais en traceback.
- **Configuration** `gates.config.json` + format du rapport de pivot : `references/gate-config-schema.md` (spécifiés là parce que c'est l'entrée du runner ; dupliqués nulle part). Une entrée `pivotReports` accepte `{ "path", "command" }` — avec `command`, le runner relance le réalisateur avant de lire, ce qui rend un rapport périmé impossible.
- **Obligation de report des pivots** (sc-css 0.2.0, sc-js 0.12.0, sc-php 0.6.0) : un rapport par règle assignée, réalisée ou non. Sans `status: "unrealized"` explicite, une règle hors de portée et une règle oubliée laissent la même trace — aucune.
- **Un `unrealized` ne change jamais le code de sortie** et aucun drapeau ne le masque. Ce n'est ni une violation ni une conformité : c'est le refus de certifier une surface que personne n'a ouverte.
- **Dégradation gracieuse** : aucun `sc-<langage>` installé → le cœur portable tourne seul, les règles qui exigeaient un réceptacle sont listées non réalisées, exit inchangé.

Gate `enforce` = **obligatoire** avant toute livraison via `diffuse` (refus absolu si lint exit 1) — dans la portée énoncée ci-dessus, jamais au-delà.

### Les plateformes quittent le cœur (Lot 3)

`references/wordpress-pitfalls.md` et `skills/enforce/adapters/wordpress.md` sont partis chez `sc-php` (`skills/design-bridge/references/`). Principe : **une contrainte de plateforme appartient au réceptacle qui la sert**.

Le routage de `enforce` ne se fait plus par nom de plateforme mais par **deux propriétés du terrain, indépendantes** : tout le markup vit-il dans des fichiers versionnés ? une référence visuelle externe existe-t-elle ? Les deux se combinent (contenu stocké sans maquette, ou l'inverse).

Dernière surface à nommer une plateforme sous `plugins/design/` : l'API de `adapters/measure/` (`--side wp|maq`, `*_in_wp`) et les citations de ces identifiants dans `agents/copycat.md` et `references/visual-diff-procedure.md` — **renommées au Lot 4** (voir `### Oracle obligatoire, registre structuré (Lot 4, 2.3.0)`). `adapters/measure/configs/mentions-legales.json` (config d'un projet réel commitée dans le plugin) supprimée au même Lot.

### Oracle obligatoire, registre structuré (Lot 4, 2.3.0)

La conformité n'est affirmée que par l'oracle **par propriété** ; tout écart toléré référence une entrée `active` de `deviations.json` portant sa `expected`. Changements :

- **`measure.py --ledger-registry` requis** : sans lui, exit **2** (invocation) en nommant l'argument, jamais de mesure. Une entrée `active` ne sanctionne qu'avec `expected` non vide et (si `expires` posé) non dépassée au clock du run ; sinon `OPEN`. `active[]` lu par la mesure ; `historical[]` = audit seul.
- **Renommage cassant, sans alias** : `--side maq|wp` → `mockup|implementation` ; clés config/rapport `maq`/`maquette`/`wp` → `mockup`/`implementation`, `*_in_wp` → `*_in_implementation`, `maq_count`/`wp_count` → `mockup_count`/`implementation_count`, `maq_viewport` → `mockup_viewport`. **Périme le 2.1.0 additif** (ligne du 2.1.0 ci-dessous : les alias sont retirés). Gate grep `\bwp\b|_in_wp|\bmaq\b` (-i) vert sur `measure.py`+`config-gen.py`.
- **Vue Markdown générée du registre** : `tools/generate.py` gagne le rôle `deviation ledger` (source = `deviations.json`, pas `tokens.json` — via `source_for(role)`). On édite le JSON, jamais la vue ; deux générations = octets identiques ; `--check` détecte la dérive. Template requalifié en **sortie générée** : `references/deviation-ledger-template.md`.
- **Refus d'affirmer la conformité** : référence externe présente mais oracle non câblé → `05-fidelity-gate` **refuse** et nomme l'étape (`config-gen.py` → config → `deviations.json` → `measure.py --ledger-registry`). Un diff pixel vert n'est jamais une preuve. Refus = état distinct du vert et du rouge.
- **Config d'exemple générique** : `configs/mentions-legales.json` supprimée ; `configs/example.json` la remplace (deux `localhost`, sélecteurs BEM neutres, aucun nom de projet).

### Maturité au figeage, conformité opposée au seuil (Lot 5, 2.4.0)

**Tout contrat porte un statut de maturité calculé qui conditionne l'invocation de la conformité, et tout écart connu plafonne ce statut au lieu d'être noté en prose.**

- **Échelle** : `tools/status.py` détient seul l'échelle `LADDER = extracted → normalized → validated → production-ready`. Première condition non tenue = fin de la montée ; un écart enregistré replafonne plus bas. `extracted` = artefacts présents · `normalized` = + charte · `validated` = + contrôles enregistrés · `production-ready` = + contraste vert & états complets. `python tools/status.py --contract <dir>` imprime le statut, un mot exact.
- **Seuil = `validated`** : la conformité ne s'affirme qu'au-dessus. **Une seule source exécutable** (constante `THRESHOLD` dans `status.py`, importée par `run-gates.py`) + **une seule source humaine** (`references/maturity-status.md`). Les routeurs (`enforce`/`diffuse`/`harness`) renvoient à `maturity-status.md`, ne re-citent jamais le littéral.
- **Exit 4 activé** (espace du plan maître, non réassignable) : `tools/run-gates.py` oppose le seuil **en dernier**, une fois toute violation déjà au rapport. Sous le seuil, la conformité ne peut être affirmée quel que soit le compte de violations → **exit 4 supersède le 1 d'une violation et le 0 d'un run propre**, et le rapport garde les violations. Imprime le statut, le chemin pour le relever, et renvoie à `maturity-status.md`.
- **Pas de grandfathering** : un contrat migré 1.x entre à `normalized` — la conformité est suspendue jusqu'à ce qu'il soit relevé (le gate continue de bloquer les vraies violations pendant ce temps).
- **Les écarts vivent dans l'artefact, pas en prose** : `release.json § gaps[]`, chaque entrée `{class, caps, detail}` plafonne le statut. Fini le « connu comme non vérifié » noté en commentaire.
- **Split a11y (DEC-002 QUOI/COMMENT)** — deux contrôles **calculés par le plugin au figeage**, déterministes, jamais par le linter de markup :
  - **contraste** : `adapters/a11y/contrast.py` calcule le ratio WCAG à partir des valeurs de tokens résolues **par thème**. `--json` déterministe : deux exécutions identiques octet pour octet, un pass/fail par paire de tokens et par thème (thèmes triés, fonds×surfaces triés, `sort_keys`).
  - **états déclaratifs** (`disabled`/`error`/`focus`) : `status.py --states` constate leur **présence déclarative** dans `components.json § .states` — pas leur rendu.
  - Les rôles/attributs ARIA restent du **markup → réalisé au pivot**.
- **Figeage non bloquant** : `adjust/02-freeze` calcule contraste + états, enregistre `checks` et les `gaps` correspondants dans `release.json`, mais **ne bloque jamais** sur un a11y non-vert — il laisse `status.py` plafonner. Le refus d'affirmer la conformité est porté par le seuil au gate, pas par un arrêt au figeage.
- **Fixtures de statut** : `skills/enforce/fixtures/status/` — `layer-3-absent` (charte absente → `extracted`), `no-contrast-run` (charte + contraste non couru → `normalized`, réutilise les artefacts sales pour reproduire les violations du Lot 3), `validated` (contrôles enregistrés → `validated`). L'`utility` reste `validated`, la racine `fixtures/` = `extracted`. Config gate `gates.below-threshold.config.json` (contrat = `no-contrast-run`, cibles sales) → exit 4 avec les mêmes violations que le Lot 3.

### Verbe 0 detail (Lot 6, 2.5.0)

**Un consommateur qui ne sait rien du plugin obtient, en une invocation, la carte des verbes et la séquence exécutable pour sa propre classe de cas, étendue par le workflow de plateforme quand le pivot correspondant est installé.**

- **7ᵉ skill `detail`, verbe 0, lecture seule, aucun artefact de sortie.** Deux actions : `explain` rend la carte des verbes, `route` rend ce qu'il faut exécuter. N'exécute jamais ce qu'il décrit, ne fige rien, ne corrige rien en silence.
- **Deux références autoritaires** : `skills/detail/references/funnel-map.md` (la carte — 8 colonnes, une ligne par verbe ; source unique lue par `01-explain`, jamais paraphrasée : le process reste chez le fichier autoritaire cité, dec-001) et `skills/detail/references/workflow-classes.md` (les six classes de cas).
- **Six classes de cas — closes, agnostiques de la stack** : contrat absent → `mockup-multipage` · `brief-only` · `codebase-inherited` ; contrat figé → `element-evolution` · `contract-drift` · `element-production`. Exhaustives sur signature d'entrée × état du contrat. `harness` n'est **pas** une classe — c'est la précondition de `mockup-multipage`.
- **Les workflows de plateforme quittent `design` pour les pivots (dec-002, prolonge le Lot 3)** : un workflow de plateforme est un COMMENT, il vit dans le pivot `sc-*`. Squelette **figé** dans `references/sc-pivot-contract.md § Workflow de plateforme` — chemin canonique `plugins/sc-<langage>/skills/design-bridge/references/workflow-<plateforme>.md`, **cinq titres imposés en anglais dans l'ordre** (`## Case classes covered` · `## Prerequisites (capabilities)` · `## Phases` · `## Gates` · `## Out of scope`), déclaration de phase input/output/verbe (ou `off-funnel`), prérequis en **capabilities jamais en vendors**, gates **instanciés jamais redéfinis**.
- **Règle de résolution (par `02-route`)** : pivot installé ET stack correspondante → classe agnostique étendue par le workflow de plateforme ; pivot absent OU stack non correspondante → classe agnostique seule + absence énoncée + recommandation conditionnelle d'installer `sc-<langage>`.
- **Trois premiers workflows livrés dans les pivots** : `sc-php:.../workflow-fse.md` (0.6.0 → 0.7.0), `sc-js:.../workflow-spa.md` (0.12.0 → 0.13.0), `sc-css:.../workflow-static.md` (0.2.0 → 0.3.0). Bumps MINOR — le plan part-8 listait les anciennes versions (le Lot 3 les avait déjà consommées) ; décision consignée en Amendement au plan.
- **Périmètre — subtilité vérifiée par le success_condition** : le vocabulaire de plateforme (wordpress, fse, vue, react, tailwind…) est **interdit sous `skills/detail/`** (grep exit 1) mais **autorisé dans les pivots** (c'est le sens de la relocalisation). Ce qui reste interdit partout dans les pivots : les noms de vendor/hébergeur (alwaysdata, netlify, vercel…) et de projet (mauceri, scriptami).

## Profil optionnel

`profile-mobile-first.md` — 7 conventions (mobile-first authoring, enrichissement progressif, UX mobile-only, tokens, variantes, a11y, iconographie). Proposé par `define/01-intake`, jamais imposé.

## copycat (1.1.0 → 1.2.0) — réplication de maquette mesurée

> **1.2.0 (enforcement structurel)** — les invariants en prose n'étaient pas suivis fiablement par l'agent (2 dry-runs ratés : tunnel vision hero-only, config non réconcilié, clôture auto-déclarée par grep). Déplacé dans la mécanique de `measure.py` : **verdict machine** `summary.verdict` (CLOSED ssi 0 diff non-ledgeré + 0 missing + aucune section manquante + couverture ok) que l'agent doit citer ; **scan de complétude** headings (guillemets normalisés) ; **garde de couverture** (under-coverage ⇒ OPEN sauf `coverage_ack`) ; **conscience ledger** (`ledger:[{target,prop,why}]` exclut un diff assumé du verdict). Re-run validé : 1 appel d'outil, verdict CLOSED cité, 0 édition.

> **1.1.2 (durcissement post dry-run réel)** — en mode dérive, l'agent avait *contourné* des règles existantes (DB-only sur page seedée, config désynchronisé, succès auto-déclaré, pivot court-circuité). Comblé : (1) « source authoritative » généralisée à tout contenu seedé/généré, pas que les patterns — DB-only = **P1** ; (2) couplage config↔markup : réconcilier les sélecteurs quand le markup change (`missing` masque le fix) ; (3) **invariants de clôture opposables** : delta clos seulement si source+pivot+config réconcilié+oracle à 0 diff ET 0 missing — clôture affirmée depuis l'oracle, jamais depuis l'édition ; (4) pivot non-skippable ; (5) **passe de complétude structurelle avant la mesure** (sections maquette ↔ cible) — une section absente est l'écart dominant, invisible au `getComputedStyle` scopé (le dry-run a « validé » un hero pendant que le corps de page manquait).

Réplication fidèle d'une maquette arbitraire vers le contrat, **sans nouveau verbe** (entonnoir toujours à 5). Composants :

- **Agent** `agents/copycat.md` (`model: sonnet`) — opérateur par page : mesure → classe l'écart à sa couche → propose tokens/composants. 4 frontières (1.1.1) : (1) jamais d'arbitrage cross-page — **bulk = propose-only ; dérive unité = boucle fermée** `enforce`→`adjust au besoin` (séquentiel, pas de course) · (2) mesure dans le script déterministe · (3) **feuille** (ne spawn aucun agent, mais appelle les skills design) · (4) **pivot** : possède le QUOI, délègue le COMMENT stack-spécifique à `sc-php`/`sc-js:design-bridge` (WP : patterns, `render.php`, `theme.json`, lint DB ; source + réimport). `tools` omis (= tous).
- **Oracle Python** `adapters/measure/` — `measure.py` (getComputedStyle, Mode A/B, **par breakpoint**) + `screenshot.py` + `pixeldiff.py`. Cross-OS, sans Node. OD-1 (spike) : Python validé (install propre, headless déterministe) ; fallback MCP documenté pour l'interactif, mais le gate CI reste Python. **2.1.0** : `config-gen.py` nomme deux rôles et non deux plateformes — `--reference-url` / `--implementation-url`, clés `reference_url` / `reference_page` / `implementation_url`. Renommage **additif** : anciens drapeaux acceptés en alias, anciennes clés lues en repli par `measure.py` et `screenshot.py` (un mineur ne casse pas une CLI). **⚠ Périmé au Lot 4 (2.3.0)** : ces alias `wp|maq` sont retirés, l'API n'accepte plus que `mockup|implementation` (voir la section Lot 4).
- **`define/05-copycat-fanout`** — fan-out parallèle (1 agent/page), agrège + remonte les conflits (sans arbitrer) → table de correspondance au **checkpoint P2** avant `adjust`. Modèle : Sonnet défaut, override par pré-signal (Haiku/Opus).
- **`enforce/05-fidelity-gate`** — **2ᵉ gate** : fidélité (référence externe = maquette résolue) en plus du lint vocabulaire (référence interne). Lit `ds-deviation-ledger`. Les deux verts.
- **Templates** `references/` : correspondence-table, deviation-ledger, copycat-checklist (résumable, mi-intégration). **Responsive** : ask-or-derive ; tablette = cas derive canonique.

> Invocation native `subagent_type: design:copycat` : **validée** (reload 1.1.0, smoke test OK). Oracle Python exécuté en réel sur `mentions-legales` (Mode B, headless) — OD-1 confirmé hors spike. ⚠ Après une édition de l'agent, réinstall + `/reload-plugins` requis pour que la session recharge le registry.

## Mode utility-first + thème/mode + adapter v3 (1.2.0 → 1.16.0, 2026-07-05)

Mode `utility-first` de 1ʳᵉ classe dans `lint-core.mjs` (vocabulaire fermé = namespaces d'usage de tokens, pas des noms de classe BEM), dimension thème/mode dans les tokens, adaptateur Tailwind v3, factorisation en deux tracks (BEM vs utility-first), réconciliation retrofit au figeage (`adjust/02-freeze`), persistance de la critique destructure, statut preview non intégrée de `diffuse`.

- **Fixtures par mode, pas un dossier unique** : `fixtures/` = contrat de base (`clean.html`/`dirty.html`, artefacts 2.0 + `release.json` directement dedans) ; `fixtures/themed/`, `fixtures/utility/`, `fixtures/retrofit/` = un contrat par mode ; `fixtures/migration/` = les quatre classes de cas d'entrée 1.x + la sortie attendue `nominal-2x`. `lint-core.mjs <file> <dir>` exige le bon dossier par paire de fixture — s'y tromper échoue bruyamment pour certaines paires et donne un résultat silencieusement faux pour d'autres (pas d'erreur visible).
- **Rule 4 (namespaces de couleur, mode utility-first) — trade-off assumé** : les préfixes Tailwind (`text`, `border`, `ring`...) sont à double usage (`text-lg`, `border-2`, `ring-offset-2` ne portent aucune couleur). La règle ne déclenche que sur la forme `<namespace>-<shade numérique 2-3 chiffres>` (ex. `bg-brand-500`) — seul signal fiable. Conséquence acceptée : un mot-clé de couleur nu sans shade (`bg-white`, `border-black`) hors contrat n'est plus détecté.
- Revue de code indépendante post-implémentation a trouvé 1 critique (le point Rule 4 ci-dessus, corrigé avant commit) + 2 mineurs (collision de libellé "Étape 2bis" dans `adjust/02-freeze.md` ; `$EXT_PATTERN` non assigné dans le snippet pre-commit de `sc-js/01-realize-lint.md`, corrigé avec garde-fou explicite).
