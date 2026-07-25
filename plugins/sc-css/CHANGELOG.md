# Changelog — sc-css

## [0.2.0] — 2026-07-24

### Reçu du pivot design (design 2.2.0)

- **`design-bridge/actions/03-realize-lint.md`** (nouveau) — réalisation native des règles de type `stylesheet` : celles dont la preuve est **les feuilles de style réellement chargées**, sélecteurs compris. Le cœur portable de `design:enforce` scanne du markup fichier par fichier ; il ne peut ni résoudre une cascade ni voir un second `:root` redéclarant une custom property du contrat — le cas le plus destructeur, puisque le markup reste littéralement conforme pendant que la valeur dérive. Le périmètre est déclaré (feuilles dérivées du contrat + feuilles applicatives de `Enforcement target`) : une feuille hors périmètre et un style injecté à l'exécution sortent en `unrealized`, jamais en `pass`.
- **Obligation de report** (`design-bridge/SKILL.md`) — toute règle reçue en `Declared rules` est rendue au gate, réalisée ou non, au format `plugins/design/references/gate-config-schema.md § Rapport de pivot`. Sans `status: "unrealized"` explicite, une règle hors de portée et une règle oubliée laissent la même trace — aucune — et le gate ne peut que les confondre.
- Le rapport se déclare dans `gates.config.json § pivotReports` avec un `command` : le runner relance la vérification avant de lire, ce qui rend un rapport périmé impossible.

## [0.1.0] — 2026-06-16

Initial release — **couche CSS technique du pipeline design**.

### Ajouté

- **`sniff`** : détection d'architecture CSS (BEM, utility-first, CSS Modules, ad-hoc), stack (préprocesseur, linter), maturité (custom properties, cascade layers). Émet un pivot manifeste JSON pour audit et improve.
- **`audit`** : audit multi-dimensionnel read-only — spécificité (guerres de cascade, `!important`, ID sélecteurs), code mort (sélecteurs inutilisés cross-référencés avec le HTML), magic numbers (valeurs hors tokens), a11y CSS (contrastes WCAG, focus, `prefers-reduced-motion`), opportunités modernes (`:has()`, container queries, nesting).
- **`improve`** : amélioration ciblée — extraction custom properties, organisation cascade layers, réduction spécificité, modernisation syntaxique. Propose plan lisible avant toute édition.
- **`legacy`** : migration legacy → standards modernes : `float` → `flex/grid`, `px` → `rem`, vendor prefixes → standard, variables Sass/Less → custom properties CSS natives. Scan d'abord, plan, puis migration fichier par fichier.
- **`teach`** : explications CSS contextuelles (spécificité, cascade layers, custom properties, sélecteurs modernes, container queries) ancrées dans le code du projet.
- **`design-bridge`** : réceptacle du pivot design — `tokens.json` → `design/css/tokens.css` (custom properties en `@layer design.tokens`), `components.json` → `design/css/<component>.css` (BEM structuré en `@layer design.components`). Signale les sélecteurs orphelins et les tokens manquants. Invoqué par `design:enforce/04-pivot` et `design:diffuse/03-pivot` quand la stack est CSS pure.
