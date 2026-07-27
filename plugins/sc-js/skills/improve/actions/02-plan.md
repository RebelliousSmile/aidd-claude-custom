# Action 02 — plan

Produce a prioritized improvement plan from the findings emitted by `01-analyze`.

## Process

### Step 1 — Prioritize findings

Group by severity and effort:
- 🔴 Critical (likely bugs) — fix first
- 🟡 Maintainability — batch by file or pattern type
- 🟢 Style — batch as a single low-priority pass

Within each tier, order by frequency: patterns appearing in ≥3 files rank before isolated occurrences.

### Step 2 — Write improvement plan

For each group, produce:
- A descriptive task title
- Effort estimate (S = <30min, M = 30min–2h, L = >2h)
- The pattern to fix with a canonical before/after example
- The files affected (list or glob)
- The slash command to use for implementation: `/aidd-dev:02-implement`

### Step 3 — Emit plan

## Output

```
📝 sc-js improve — plan

Priority 1 — 🔴 Fix likely bugs (critical)
─────────────────────────────────────────
(réservé aux défauts prouvés au scan : `==` sur null, `var` capturé en boucle,
 `await` manquant sur une valeur ensuite déréférencée — pas les indécidables.)

Priority 2 — 🟡 Maintainability / à décider
─────────────────────────────────────────
Task: Revoir les promesses possiblement non gérées [S]
Pattern: appel async sans try/catch/.catch() visible
Note: NE PAS injecter await/.catch d'office — vérifier d'abord handler global
      ou fire-and-forget voulu ; l'await ajouté change l'ordre d'exécution.
Files: src/composables/useData.ts, src/composables/useAuth.ts

Task: Migrate 3 Options API components to Composition API [L]
Files: src/components/UserCard.vue, src/components/Header.vue, ...
Next: /aidd-dev:02-implement "Migrate Options API → Composition API"

Priority 3 — 🟢 Style cleanup
─────────────────────────────────────────
Task: Replace var with const/let across project [S]
Files: src/utils/ (7 files)
Next: /aidd-dev:02-implement "Replace var declarations"
```

## Test

Invoke after `01-analyze` with at least 3 findings; verify the plan groups findings by severity, includes effort estimates, and references specific files.
