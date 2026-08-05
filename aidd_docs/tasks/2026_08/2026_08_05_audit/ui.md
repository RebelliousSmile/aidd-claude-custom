# Codebase Audit: `design:harness` — ui

Le harness scaffoldé naît en violation de l'invariant de titrage qu'il prescrit lui-même, son sélecteur de page n'a pas de nom accessible, et il n'a pas d'état d'erreur : une fonction de page qui échoue laisse l'écran sur la page précédente et fait remonter l'exception jusqu'à l'oracle.

- **Date**: 2026-08-05
- **Scope**: le HTML produit par `plugins/design/adapters/harness/harness.py` (chrome `.preview-bar` + coquille de page), mesuré dans Chromium via Playwright
- **Health**: fair
- **Findings**: 2 critical, 2 warning, 2 minor

Périmètre : le **chrome généré** et la coquille. Le contenu des pages est écrit après coup par un agent — il n'est pas audité ici, mais les invariants que le fichier lui impose le sont.

## Findings

| Sev | Category | Location                                                     | Issue                                                                                                                                                                                          | Suggested fix                                                                                                                       | Effort |
| --- | -------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------ |
| 🔴  | ui       | `plugins/design/adapters/harness/harness.py:258` et `:279`    | Le scaffold **ne contient aucun `h1`** — mesuré `h1 count: 0`, `h2 count: 1`. Or le même fichier prescrit ligne `:200` « Un seul h1 par page ; hiérarchie de titres réelle » et `measure.py:444` scanne `h1, h2` pour la complétude structurelle. Le fichier fraîchement généré échoue le contrôle que le fichier lui-même déclare | `placeholder()` émet un `h1` (c'est le titre de la page), le repli « Page introuvable » aussi ; le commentaire `:200` devient une règle vérifiable au lieu d'être contredite par le scaffold | S      |
| 🔴  | ui       | `plugins/design/adapters/harness/harness.py:231`              | `<select class="page-select" id="page-select">` n'a **ni `<label>` ni `aria-label`** — mesuré `ariaLabel = None`, `labels = []`. Le seul contrôle de navigation du harness n'est pas nommé (WCAG 2.2 · 4.1.2 Name, Role, Value) | `aria-label="Page"` sur le `select`, aligné sur le `role="group" aria-label="Device"` déjà présent `:230`                             | S      |
| 🟡  | ui       | `plugins/design/adapters/harness/harness.py:277-281`          | **Aucun état d'erreur.** `render()` assigne `container.innerHTML = fn()` sans `try`/`catch` : si une fonction de page jette, l'affectation n'a jamais lieu, l'écran **reste sur la page précédente** sans rien signaler, et l'exception remonte à travers `render` → `setPage` → l'appelant. `measure.py:191` appelle `window.setPage(k)` sans garde : l'oracle plante ou mesure la mauvaise page | Envelopper `fn()` dans un `try`/`catch` rendant un bloc d'erreur visible (clé de page + message), à l'image du repli « Page introuvable » déjà écrit `:279` | S      |
| 🟡  | ui       | `plugins/design/adapters/harness/harness.py:235-237`          | Les trois `.viewport-btn` portent un état actif **purement visuel** (`classList.toggle('active')`, `:294`) sans `aria-pressed` ; les `<svg>` décoratifs n'ont pas `aria-hidden="true"`. Mesuré : 0 occurrence de `aria-pressed` ou `aria-hidden` dans la sortie | `aria-pressed` maintenu par `setViewport` en même temps que la classe ; `aria-hidden="true"` sur les trois `<svg>`                    | S      |
| 🟢  | ui       | `plugins/design/adapters/harness/harness.py:106`              | `<html lang="fr">` est codé en dur dans un générateur par ailleurs agnostique, dont `SKILL.md` est en anglais. Un harness pour un projet anglophone s'annonce français aux lecteurs d'écran et aux correcteurs | Paramètre `--lang` (défaut `en`, ou dérivé du contrat quand `--contract` est passé)                                                    | S      |
| 🟢  | ui       | `plugins/design/adapters/harness/harness.py:111-112`          | Deux `<link rel="preconnect">` vers `fonts.googleapis.com` / `fonts.gstatic.com` sont émis inconditionnellement, dans un fichier que `SKILL.md` vend comme « autonome ». Hors ligne, ce sont deux résolutions DNS mortes ; en ligne, deux connexions à un tiers qu'aucune `@font-face` n'utilise dans le scaffold | Ne les émettre que si une police distante est réellement déclarée (jamais dans le scaffold nu)                                        | S      |

### Reproduction

```python
# Chromium, viewport 1600×900, fichier généré par : harness.py --pages 'home:Accueil,contact:Contact'
select accessible name : None
h1 count               : 0
h2 count               : 1
apres cle inconnue     : 'Page introuvable'      # le repli existe, il est juste sans h1
erreurs JS             : []
```

Propagation de l'exception (mesurée en remplaçant `placeholder` par une fonction qui jette, puis en appelant `window.setPage('home')`) :

```
Error: boom
    at pageHome   (ref.html:159)
    at render     (ref.html:177)
    at setPage    (ref.html:185)
```

L'appelant reçoit l'exception ; c'est exactement la ligne que `measure.py:191` exécute.

### Ce qui a été vérifié et ne donne pas de finding

- **Contrastes du chrome**, calculés en composant les `rgba()` sur `#1F2A37` : `.preview-bar__brand small` **4.76**, `.viewport-btn` **6.50**, `.page-select` **10.69**, `.ph p` sur blanc **4.83**. Tous ≥ 4.5 (AA texte normal). Rien à signaler.
- **Bascule de viewport** : `setViewport('mobile')` amène le cadre de 1600 px à **390 px**, `tablet` à 834 px, `desktop` fluide — conformes aux échantillons déclarés dans `references/harness-contract.md`.
- **Aucune `@media`** dans la sortie : le modèle par classes tient, comme l'asserte `tools/harness-selftest.sh`.
- **Aucune erreur JS** au chargement ni pendant les bascules.

## Top actions

1. **Poser le `h1` dans le scaffold** (résout le 🔴 de titrage). Coût dérisoire, effet direct sur la seule chaîne outillée du plugin : le harness cesse d'échouer d'emblée le scan de complétude de `measure.py`. Handoff : `aidd-dev:03-act`.
2. **Nommer le sélecteur et exposer l'état des boutons** (résout le 🔴 a11y et le 🟡 `aria-pressed`) — trois attributs dans le template, une ligne dans `setViewport`.
3. **Donner un état d'erreur à `render()`** (résout le 🟡 d'état). Le harness est rempli par un agent : une fonction de page cassée est le mode d'échec attendu, pas l'exception. Aujourd'hui il n'affiche rien et contamine l'oracle en amont.

## Coverage

- **Scanned**: ui
- **Skipped**: architecture, security, dependencies, performance — voir `tests.md § Coverage`.
