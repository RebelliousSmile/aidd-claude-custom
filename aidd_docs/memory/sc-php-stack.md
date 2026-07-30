# sc-php — état du plugin

| Champ | Valeur |
|---|---|
| Version courante | 0.10.0 |
| Dernière release | 2026-07-30 |

## Skills disponibles

sniff, audit, improve, legacy, teach, log-analysis, bruno, setup, design-bridge, builder-coverage

## Capability pivots (chargés à l'audit)

`php/solid.md` (toujours), `testing/bruno.md` (si Bruno), `wordpress/ssr.md` (v0.5.2+, si WordPress détecté — authoring de blocs SSR : attributs additifs, `wp_kses_post`, compteurs serveur, `blocks/` vs `build/`, nav SSR vs show/hide JS)

## Pivot `tools/testing.md` (v0.10.0+)

Fournisseur du champ `testing` de `overcode:control` — 10 sections, anglais. Voir [pivots-testing.md](pivots-testing.md) pour la règle transversale. Deux faits propres à PHP à ne pas réapprendre : **l'unité de mesure est le composant, pas le dépôt** (une commande lancée à la racine d'un projet multi-modules rend zéro test), et **la couverture sans driver Xdebug/PCOV sort 0 sans écrire de fichier** — un consommateur qui lit le code de retour croit avoir réussi.

## Pivots perf

WordPress, Laravel, Symfony, HTMX hybrid

## Pivots data

Eloquent, Doctrine

## Réceptacles pivot design

`design-bridge` (v0.5.0+) — réceptacle pour `design:enforce` + `design:diffuse` :
- `01-realize-lint` → génère `design/lint/check-classes.php` (checker PHP avec placeholders `__VALID_BASES__`/`__VALID_CLASSES__` + theme.json coherence)
- `02-render` → block pattern WP FSE (commentaires Gutenberg + classes design + theme.json palette)
