# Registre des écarts — gabarit de la vue générée

Cette vue Markdown est un **artefact généré** par `tools/generate.py` à partir de `deviations.json` (rôle-consommateur `deviation ledger`). On n'édite jamais la vue : une retouche à la main est une dérive que `generate.py --check` signale. On édite `deviations.json` ; la vue suit.

La source, les champs et les cas de verdict `OPEN` : `references/deviations-schema.md`. Ce gabarit ne décrit que la **forme rendue**.

## Forme rendue

Une bannière, puis les écarts **actifs** puis **historiques**, chacun dans l'ordre source. Une entrée est un bloc `### <id> · <target>` suivi de ses champs. `expire` n'apparaît que si l'entrée le porte ; un champ requis absent est rendu `—` pour montrer le trou de la source plutôt que le masquer.

```markdown
<!-- GENERATED from deviations.json - do not edit by hand. Regenerate via tools/generate.py. -->
# Registre des écarts

## Actifs

### DEV-001 · Hero · lede
- statut : active
- propriété : fontSize
- attendu : 17px
- date : 2026-06-15
- expire : 2026-12-31
- raison : adopte le token fluide de corps unique ; +1px sous le seuil perceptif

## Historiques

### DEV-000 · Hero · title
- statut : superseded
- propriété : letterSpacing
- attendu : -0.02em
- date : 2026-05-02
- décidé : 2026-06-10
- raison : remplacé par DEV-004 après refonte de l'échelle typographique
```

## Correspondance champ → ligne

| Champ `deviations.json` | Rendu | Section |
|---|---|---|
| `id`, `target` | titre `### <id> · <target>` | les deux |
| `status` | `- statut :` | les deux |
| `prop` | `- propriété :` | les deux |
| `expected` | `- attendu :` (`—` si absent) | les deux |
| `date` | `- date :` | les deux |
| `expires` | `- expire :` — omis si absent | actifs |
| `decidedAt` | `- décidé :` | historiques |
| `reason` | `- raison :` | les deux |
