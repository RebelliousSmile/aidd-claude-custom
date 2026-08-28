# Decision: la quittance d'un consommateur de pivot — quatre états, une ligne par stack

| Field   | Value |
|---------|-------|
| ID      | DEC-010 |
| Date    | 2026-08-03 |
| Feature | Consommation de pivot — obligation de sortie, transversale aux trois familles (`overcode:*-optimize`, `design:detail/02-route`, `overcode:control`) |
| Status  | Accepted |
| Antécédents | **DEC-004** — la consommation croisée de pivots est une interface publique ; la quittance en devient une clause, d'où le niveau de bump. **DEC-006** — la page porte la règle et son motif, la skill la procédure : la présente décision porte le rationnel, `docs/concepts.md` la règle, les `SKILL.md` la forme. **DEC-008** — le pivot suit le fichier ; une quittance rendue en valeur unique est donc fausse sur un dépôt polyglotte. **DEC-009 §2** — un prérequis constaté absent vaut champ absent pour ce run : même forme de raisonnement, appliquée ici au pivot entier plutôt qu'à un de ses champs |

## Context

La promesse est déjà écrite. `overcode/README.md:7` et `docs/concepts.md:25` portent, avant cette décision, *« Aucun pivot trouvé → un schéma générique s'applique, **et l'absence est énoncée** »*. Aucune des quatre skills `*-optimize` ne l'implémente : `provenance`, `stack-agnostic` et « name the source » sortent à **0 occurrence** sur l'ensemble de leurs fichiers, et leurs quatre critères de succès (`web:167`, `data:174`, `seo:149`, `ap:118`) se ferment tous sur *« a source is **loaded** »*. Le chargement est spécifié ; le rapport ne l'est pas.

Ce que le silence coûte se mesure en aval, pas en amont. Un audit générique et un audit spécialisé rendent la même forme de sortie ; rien n'y distingue *« aucun plugin ne couvre cette stack »* de *« un plugin la couvre, personne ne l'a installé ici »*. Le premier appelle une rédaction, le second une commande. Rendus identiques, les deux appellent la même chose : rien.

Le défaut est symétrique de celui que `design` a déjà nommé pour ses règles : *« sans rapport, une règle assignée et une règle oubliée produisent la même trace — aucune »* (`sc-pivot-contract.md:112`). La présente décision généralise cette phrase du réalisateur au **consommateur**.

## Decision

### 1. Tout consommateur de pivot rend, en sortie, ce qu'il a chargé et ce qu'il n'a pas pu charger

**Quatre** états à séparer, jamais deux :

| État | Terrain | Ce que la sortie doit permettre |
|---|---|---|
| `installed` | un pivot est chargé pour cette stack | nommer le fichier et sa stack — c'est la **provenance** |
| `no provider` | aucun plugin de la marketplace ne couvre cette stack | proposer d'en générer un ; il n'y a pas d'installeur à recommander |
| `not installed` | un plugin la couvre, rien n'est installé dans ce projet | nommer le plugin **et** sa commande, dans ce projet |
| `empty receptacle` | le réceptacle existe et ne porte **aucun fichier de règle** | même remède que `not installed`, diagnostic distinct |

**« Vide » se définit par les règles, pas par les fichiers.** Un `.gitkeep`, un `.gitignore` ou tout fichier de service ne peuplent pas un réceptacle ; une règle hors pivot le peuple. Le critère lu sur les fichiers ferait basculer en `not installed` un réceptacle créé exprès et laissé nu, ce qui est précisément l'état que le quatrième nomme.

**Aucun des quatre ne se confond avec *absent*.** Un réceptacle qui n'existe pas est `not installed` : rien n'a jamais été installé là.

`not installed` et `empty receptacle` appellent le **même remède** et ne partagent pas leur diagnostic — les fondre priverait le second de fondement et rendrait le premier faux là où le dossier existe.

**La quittance est par stack.** Sur un dépôt polyglotte, elle est **une ligne par stack applicable** : rendue en valeur unique, elle est fausse quelle qu'elle soit, puisque le pivot suit le fichier et non le dépôt (DEC-008). Un dépôt qui porte du Python couvert et du Rust non couvert n'a pas d'état global.

**La quittance est une obligation de sortie, pas de mécanisme.** Elle porte sur ce que le lecteur peut lire, jamais sur la façon dont le consommateur l'a établi. Un consommateur dont la lecture ne peut pas échouer — `control`, qui lit son pivot dans le plugin — la satisfait par sa seule ligne de provenance : il n'a rien à quitter.

### 2. Déléguer des règles oblige à une quittance ; déléguer un artefact non

Une règle non réalisée est **silencieuse** : assignée ou oubliée, même trace, aucune. Un artefact non produit est **auto-évident** : le fichier existe et passe le gate, ou il n'existe pas.

La quittance paie un silence. Là où il n'y a pas de silence, elle n'a rien à payer. C'est le motif de l'asymétrie que `design` porte déjà en position — `sc-pivot-contract.md:129-134` donne un contrat de retour à chaque sens et met la ligne *rapport* à `—` côté rendu — sans l'avoir jamais motivée.

## Rationale

**Pourquoi quatre états et pas deux.** Deux états — chargé / pas chargé — sont ce que le système rend aujourd'hui, et c'est exactement l'indistinction à lever. Trois ne suffisent pas non plus : le réceptacle nu est le seul état qui atteste qu'un installeur a été envisagé sans aboutir, et le fondre dans `not installed` fait disparaître la seule trace d'une installation entamée.

**Pourquoi la règle porte sur l'observable.** L'écrire sur le mécanisme — « le scan du réceptacle rend son résultat » — la rendrait inapplicable à `control`, dont la lecture in-plugin ne peut pas échouer, et à tout futur consommateur qui résoudrait ses pivots autrement. La sortie est ce que les trois familles ont en commun.

**Pourquoi ici et pas dans une skill.** Trois familles sont concernées et aucune ne fait autorité sur les deux autres. Écrite dans l'une, la règle ne lierait qu'elle ; répétée dans les trois, elle divergerait au premier amendement.

### Ce que la décision ne fait pas

Elle ne donne à **aucun** consommateur le pouvoir de décider ce qu'un pivot couvre, ni de tenir la carte des fournisseurs pour son compte. Le consommateur constate un état et le rend : c'est l'instrument qui mesure, et DEC-007 §2 lui refuse de trancher. La correspondance stack → plugin vit dans un fichier unique, référencé et non recopié.

Elle n'oblige personne à **installer** quoi que ce soit, ni à interrompre un run : les quatre états sortent tous un résultat, et l'absence de pivot n'est jamais une erreur. C'est la contrepartie du principe agnostique — un audit sans pivot reste un audit.

Elle ne touche pas au **contenu** des pivots, ni à qui les fournit : DEC-001 et DEC-008 tiennent inchangés.

## Compatibility

**Additive sur la sortie, contraignante sur la forme.**

- `overcode` — les quatre `*-optimize` gagnent une obligation de sortie et perdent trois énumérations de fournisseurs fausses. Aucun champ de pivot n'est renommé, aucun pivot existant ne devient illisible : DEC-004 §5 réserve le majeur à ce cas. D'où une **mineure**.
- `design` — `references/sc-pivot-contract.md` est lu par des plugins tiers, donc une **interface publique** au sens de DEC-004 §5. Le motif ajouté et les deux lignes de gate manquantes ne changent aucun comportement de `run-gates.py`, mais un lecteur du contrat voit deux sorties qu'il ne voyait pas. D'où une **mineure** également, pas un correctif.

Aucune rétroactivité : un pivot déjà installé se lit sans modification, et un consommateur non encore repris rend une sortie moins complète, jamais fausse.

## Consequences

Le lot qui instancie cette décision porte cinq parts et touche huit plugins plus le hors-plugin.

- **Part 1** — deux suites `behave` neuves, enregistrant l'état « avant » : `overcode/skills/web-optimize/evals/pivot-provenance-scenarios.md` (11 scénarios, run 1 : 0 PASS · 10 FAIL · 1 N/A) et `web-tiers/skills/setup/evals/pivot-install-scenarios.md` (7 scénarios, run 1 : 1 PASS · 6 FAIL).
- **Part 2** — la présente décision ; `overcode/docs/concepts.md` § *agnostique par défaut, spécialisé par pivot* (les quatre états, l'obligation de sortie, l'installeur nommé par famille, la quatrième ligne `seo-optimize`) ; `overcode/README.md:7` aligné ; `design/references/sc-pivot-contract.md` (motif de l'asymétrie, quatre chemins de skill normalisés, table des verdicts complétée) ; `design/skills/enforce/actions/04-pivot.md` (même table, à l'identique).
- **Part 3** — les quatre `*-optimize/SKILL.md` : règle de tête, échelle de repli, ligne de provenance, remède du garde-fou terminal, retrait des énumérations de fournisseurs fausses ; `overcode/references/pivot-providers.md`, table `<stack> → <plugin>, <commande>` créée.
- **Part 4** — assainissement des installeurs qui déclarent du vide (`web-tiers`, `sc-css`) ou figent leur sortie (`sc-python`, `sc-php`, `sc-rust`), un chemin non résolu dans `sc-js` ; gardes déclaré-vs-disque M4 et M5 dans `tools/eval/consistency.mjs` ; `CONTRIBUTING.md:24`/`:106` corrigé.
- **Part 5** — rejeu des deux suites, bumps et journaux : huit plugins, la version racine de `.claude-plugin/marketplace.json` et le `CHANGELOG.md` de racine. Un plugin, un bump, un commit — les parts 1 à 4 n'en posent aucun.

**Le cas d'école reste ouvert.** `seo-pivots-*` n'a, après cette décision, **aucun** fournisseur : le réceptacle est une interface publique sans réalisateur. C'est l'état `no provider` dans sa forme pure, et il est écrit comme tel plutôt que comme un oubli.

