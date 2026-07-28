# Write-material

Écrire la matière de design **malléable** depuis le token set dérivé (par `02-extract` ou `03-construct`) : `design/tokens.json` et `design/design-system.md` en **brouillon non figé**. Aucun manifeste, aucun artefact dérivé.

## Inputs

- Le token set finalisé + stratégie responsive + liste de composants candidats (de `02` ou `03`).
- Provenance : l'origine (URL/fichier de référence, ou résumé du brief), la date du jour, la version `0.1.0` pour un premier système.
- Le choix d'injection du profil optionnel (de `01-intake`).

## Process

Suivre la procédure partagée : `${CLAUDE_PLUGIN_ROOT}/references/write-system-procedure.md` — **avec ces surcharges propres à `define`** :

1. **Statut brouillon** — `design-system.md` porte explicitement la mention `status: brouillon / non figé` près de la ligne `version:`. `define` n'arbitre pas et ne canonise pas ; le figeage est le rôle de `adjust`.
2. **Jamais d'artefact du contrat** — n'écrire **aucun** `design/components.json`, `policies.json`, `oracle.json` ni `release.json`. Interdiction dure : les artefacts et leur racine sont produits par `adjust`.
3. **Inventaire en prose candidate** — la section "Component inventory" de `design-system.md` liste les composants en **prose, marqués candidats**. Cet inventaire prose est distinct du manifeste JSON figé : il sera *promu* (pas recopié) en manifeste par `adjust`. Le dire dans la section.

   Ses deux colonnes couleur — fonds et avant-plans — reportent les appariements relevés en `02-extract` ou décidés en `03-construct`. Ne pas les laisser vides pour un composant qui affiche du texte : c'est ici, et nulle part ailleurs, que l'usage transite jusqu'à `adjust`. Un token set complet accompagné d'un inventaire sans appariements produit un contrat que le contrôle de contraste ne peut pas lire, et que `adjust/02-freeze` refusera de figer.
4. **Provenance concrète** — nommer la source réelle : "Extrait du screenshot de landing fourni le {date}" / "Dérivé de `marketing-site/styles.css`" / "Construit depuis le brief {résumé}". Pour une extraction mono-viewport, dire en § Open questions que la stratégie responsive est partiellement inférée.
5. **Reporter les hypothèses** — chaque hypothèse signalée en `02`/`03` va en § Open questions ; ne pas les résoudre silencieusement.
6. **Profil optionnel** — si l'utilisateur l'a demandé en `01-intake`, injecter le contenu de `references/profile-mobile-first.md` dans le projet (`.claude/rules/08-design/`) ; sinon, ne rien installer et le mentionner comme disponible.

### Artefacts écrits (par la procédure partagée)

- `design/tokens.json` — W3C DTCG, source de vérité, alias `{group.name}` pour les liens sémantique→ramp.
- *(aucun adapter)* — un artefact dérivé n'est produit que par `${CLAUDE_PLUGIN_ROOT}/tools/generate.py`, au figeage. Ici on **détecte** les consommateurs présents dans le projet et on les consigne en § Provenance : `${CLAUDE_PLUGIN_ROOT}/references/write-system-procedure.md § Adapter emission rule`.
- `design/design-system.md` — sections requises du contrat : Provenance · Foundations · Responsive strategy · Component inventory (prose candidate) · Open questions.

## Atomicity

- `tokens.json` est écrit seul : aucun adapter n'existe encore, donc rien ne peut se désynchroniser de lui à ce stade.
- Si `design/tokens.json` existe déjà, differ : bumper la version selon le contrat et résumer ce qui change au lieu d'écraser silencieusement.

## Report

- Lister chaque chemin écrit/régénéré.
- Donner la version (`0.1.0`) et une provenance en une ligne, avec le statut **brouillon**.
- Faire remonter les Open questions non résolues.
- Suggérer l'étape suivante de l'entonnoir : **`/design:destructure`** (challenger la direction avant de figer) — et non plus `wireframe`/`component`.

## Test

`design/tokens.json` et `design/design-system.md` existent ; **rien n'a été écrit sous `design/adapters/`** ; § Provenance nomme chaque consommateur détecté et sa preuve ; `design-system.md` a les 5 sections requises, une ligne `version:`, le statut **brouillon**, et un inventaire de composants en **prose candidate** dont les colonnes fonds/avant-plans sont renseignées pour chaque composant affichant du texte ; **aucun** artefact du contrat (`components.json`, `policies.json`, `oracle.json`, `release.json`) n'a été écrit.
