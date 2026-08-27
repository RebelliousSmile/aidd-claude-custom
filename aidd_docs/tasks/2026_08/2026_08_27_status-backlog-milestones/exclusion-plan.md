---
objective: "Permettre d'exclure des milestones spécifiques du backlog synchronisé par status backlog, pour qu'un projet tracé dans un markdown précis ne contienne pas les issues de certaines milestones."
status: pending
parent: "2026_08_27_status-backlog-milestones/plan.md"
depends_on: ["status backlog avec support des milestones"]
---

# Plan: Ajouter l'exclusion de milestones au backlog overcode status

## Compréhension du besoin

Actuellement, `status backlog <fichier.md>` permet de:
- Synchroniser la section `## Backlog` depuis les issues ouvertes GitHub/GitLab
- Filtrer par une milestone spécifique avec `--milestone <titre>` ou `--ml <titre>`
- Grouper les issues par milestone lorsque le projet en possède

**Nouveau besoin** : Pouvoir **exclure** des milestones spécifiques du backlog, pour qu'un projet tracé dans un markdown précis ne contienne pas les issues de certaines milestones.

## Analyse de l'existant

Cette feature s'appuie sur l'implémentation existante de `status backlog` avec support des milestones (voir `parent` ci-dessus).

### Fichiers clés à modifier
1. `plugins/overcode/skills/status/actions/04-backlog.md` - Implémentation principale
2. `plugins/overcode/skills/alias/actions/04-previously.md` - Alias qui chaîne backlog
3. `plugins/overcode/docs/workflow.md` - Documentation utilisateur
4. `plugins/overcode/docs/aliases.md` - Documentation de l'alias
5. `plugins/overcode/CHANGELOG.md` - Historique des changements
6. `plugins/overcode/skills/status/evals/backlog-scenarios.md` - Tests

### Comportement actuel (Step 3 - Fetch and validate)
- Filtre unique par milestone: si fourni, ne garde que les issues de cette milestone
- Sans filtre: garde toutes les issues ouvertes
- Validation: 0 correspondance = succès avec 0 issue, 1 correspondance = filtre appliqué, >1 correspondance = ambiguïté

## Solution proposée

### Nouvelle syntaxe
```text
status backlog <fichier.md> [--milestone <titre> | --ml <titre>] [--exclude-milestone <titre> | --em <titre>] [--exclude-milestone <titre2> | --em <titre2>]
```

### Règles de design
1. `--exclude-milestone` et `--em` sont des synonymes stricts (comme `--milestone`/`--ml`)
2. Peut être spécifié plusieurs fois pour exclure plusieurs milestones
3. Peut être combiné avec `--milestone` pour filtrer ET exclure
4. L'exclusion s'applique **après** le filtrage par milestone et est **prioritaire** en cas de conflit (ex: `--milestone M --exclude-milestone M` → résultat vide)
5. Correspondance exacte, sensible à la casse (comme le filtre actuel)
6. Si une milestone à exclure n'existe pas, c'est un succès (comportement silencieux, **non loggé**)
7. Les options peuvent apparaître dans n'importe quel ordre dans la commande
8. Chaque valeur d'exclusion doit être non vide (espaces périphériques retirés, valeur requise). **Erreur attendue** : `"--exclude-milestone: valeur vide interdite"`

### Comportement en cas d'erreur

| Cas | Comportement |
|-----|--------------|
| Milestone à exclure inexistante | Succès silencieux (pas de log, pas d'erreur) |
| Valeur vide pour `--exclude-milestone` | Échec avec message : `"--exclude-milestone: valeur vide interdite"` |
| Ambiguïté sur `--milestone` (plusieurs correspondances) | Échec (comportement existant) |
| `--milestone M` + `--exclude-milestone M` | Résultat vide (logique, exclusion prioritaire) |

### Logique de filtrage
```
1. Collecter toutes les issues ouvertes valides
2. Si --milestone <M> fourni:
   - Garder seulement les issues avec milestone == M
   - Si ambiguïté (plusieurs milestones avec titre M) → échec
3. Si --exclude-milestone <E1>, <E2>, ... fournis:
   - Pour chaque issue restante, si sa milestone est dans {E1, E2, ...} → exclure
4. Résultat: issues filtrées et exclues
```

### Exemples
- `status backlog projet.md --exclude-milestone "Version 2"` → toutes les issues sauf celles de "Version 2"
- `status backlog projet.md --milestone "Version 1" --exclude-milestone "Version 1"` → résultat vide (logique, exclusion prioritaire)
- `status backlog projet.md --exclude-milestone "Inexistante"` → toutes les issues (succès, comportement silencieux)
- `status backlog projet.md --exclude-milestone "Version 2" --exclude-milestone "Version 3"` → toutes les issues sauf celles de "Version 2" et "Version 3"
- `status backlog projet.md --milestone "Version 1" --exclude-milestone "Version 2"` → seules les issues de "Version 1" (l'exclusion n'affecte pas le filtre)
- `status backlog projet.md --exclude-milestone "Version 2" --milestone "Version 1"` → mêmes résultats que ci-dessus (ordre des options indifférent)

## Implémentation détaillée

### 1. Mise à jour de la syntaxe (Context required)
- Ajouter `--exclude-milestone <titre>` et `--em <titre>` comme options
- Accepter plusieurs occurrences de `--exclude-milestone`/`--em` (0 à N)
- Valider que chaque valeur est non vide après retrait des espaces périphériques
- Accepter les options dans n'importe quel ordre (avant ou après `--milestone`/`--ml`)

### 2. Mise à jour du Step 3 (Fetch and validate)
- Après l'application du filtre `--milestone` (lignes 88-91)
- Ajouter une nouvelle étape pour l'exclusion:
  ```
  6. Si des exclusions sont fournies:
     - Pour chaque titre d'exclusion (dans l'ordre fourni, après retrait des espaces périphériques):
       - Chercher dans le catalogue la milestone avec titre brut égal au titre d'exclusion
       - Si trouvée (0 ou 1 correspondance dans le catalogue validé), retirer toutes les issues ayant cet identifiant de milestone
       - Si non trouvée: continuer sans erreur (comportement silencieux)
     - Note: l'exclusion s'applique sur le jeu d'issues déjà filtré par --milestone
  ```

### 3. Mise à jour du Step 6 (Rapport)
- Ajouter une ligne `Excluded milestones: <liste>` si des exclusions étaient présentes
- `<liste>` est la liste des titres bruts des milestones exclues, séparés par des virgules, dans l'ordre fourni

### 4. Mise à jour de l'alias `previously`
- Transmettre les options `--exclude-milestone`/`--em` à `status backlog`
- Mettre à jour la syntaxe dans `Context required`

### 5. Mise à jour de la documentation
- `docs/workflow.md`: ajouter la description des nouvelles options
- `docs/aliases.md`: mettre à jour la syntaxe de `previously`

### 6. Scénarios de test à ajouter
- Exclusion simple d'une milestone existante
- Exclusion de plusieurs milestones
- Exclusion d'une milestone inexistante
- Combinaison filtre + exclusion
- Exclusion de toutes les milestones (résultat = issues sans milestone)
- Exclusion d'une milestone qui n'a pas d'issues associées
- Ordre des options: `--exclude-milestone` avant `--milestone`
- Exclusion avec valeur vide (doit être rejetée en validation)

## Validation

### Critères d'acceptation
1. ✅ La syntaxe accepte `--exclude-milestone` et `--em` avec plusieurs valeurs
2. ✅ L'exclusion fonctionne correctement avec le catalogue de milestones
3. ✅ La combinaison filtre + exclusion produit le résultat attendu
4. ✅ Le rapport inclut la liste des milestones exclues
5. ✅ Les tests existants continuent de passer (non-régression)
6. ✅ La documentation est mise à jour

### Tests à exécuter
1. Tous les scénarios existants de `backlog-scenarios.md` doivent rester PASS (33/39 actuellement)
2. Nouveaux scénarios pour l'exclusion:
   - S45: Exclusion simple → issues de cette milestone absentes
   - S46: Exclusion multiple → toutes les milestones exclues sont absentes
   - S47: Exclusion de milestone inexistante → toutes les issues présentes
   - S48: Filtre + exclusion → intersection correcte
   - S49: Exclusion de toutes les milestones → seul "Sans milestone" reste
   - S50: Exclusion d'une milestone sans issues → comportement inchangé
   - S51: Ordre des options indifférent → mêmes résultats
   - S52: Valeur vide pour --exclude-milestone → rejet en validation

## Files to modify

| File | Type | Changes |
|------|------|---------|
| `plugins/overcode/skills/status/actions/04-backlog.md` | Implementation | Add `--exclude-milestone`/`--em` parsing, exclusion logic in Step 3, update report in Step 6 |
| `plugins/overcode/skills/alias/actions/04-previously.md` | Integration | Forward exclusion options to status backlog |
| `plugins/overcode/docs/workflow.md` | Documentation | Add exclusion options description |
| `plugins/overcode/docs/aliases.md` | Documentation | Update previously syntax with exclusion |
| `plugins/overcode/CHANGELOG.md` | Documentation | Add entry for exclusion feature |
| `plugins/overcode/skills/status/evals/backlog-scenarios.md` | Tests | Add new scenarios for exclusion (S45-S52) |

## Estimations

- **Implémentation**: 2-3 heures (modification de 04-backlog.md)
- **Intégration alias**: 1 heure (modification de 04-previously.md)
- **Documentation**: 1 heure (workflow.md, aliases.md, CHANGELOG.md)
- **Tests**: 2-3 heures (ajout de scénarios et validation)
- **Total**: 6-8 heures

## Risques et mitigations

1. **Risque**: Incompatibilité avec la logique existante de filtrage
   - **Mitigation**: Bien séparer les étapes (filtre d'abord, puis exclusion) - validé par les règles de design

2. **Risque**: Ambiguïté si une milestone à exclure a le même titre qu'une milestone existante
   - **Mitigation**: Utiliser le catalogue validé (pas d'ambiguïté possible après validation du Step 3)

3. **Risque**: Performance avec beaucoup d'exclusions
   - **Mitigation**: Le catalogue est déjà en mémoire, l'exclusion est O(n*m) où n=issues, m=exclusions, ce qui est acceptable

4. **Risque**: Oubli de valider les valeurs vides pour --exclude-milestone
   - **Mitigation**: Validation explicite dans le Context required (règle #8) + message d'erreur clair.

5. **Risque**: Incohérence si --milestone et --exclude-milestone pointent vers la même milestone
   - **Mitigation**: Cas valide documenté dans les exemples et la section "Comportement en cas d'erreur". Résultat attendu : vide.

6. **Risque**: Comportement silencieux pour milestone inexistante pourrait masquer des erreurs de configuration
   - **Mitigation**: Documenté dans "Comportement en cas d'erreur" comme choix délibéré pour éviter les faux positifs.

## Prochaines étapes

1. ✅ Plan validé et amélioré via analyse rechallenge + subagent explore
2. Implémenter dans l'ordre: 04-backlog.md → tests → 04-previously.md → documentation
3. Exécuter tous les scénarios de test (existants + nouveaux)
4. Mettre à jour le CHANGELOG

## Historique des révisions

- **v1**: Plan initial créé
- **v2**: Appliqué améliorations via analyse rechallenge:
  - Ajout des règles #7-8 (ordre des options, validation des valeurs vides)
  - Exemples étendus avec 6 cas concrets
  - Précision sur le comportement silencieux pour milestones inexistantes
  - Ajout de 3 nouveaux scénarios de test (S50-S52)
  - Ajout de 2 nouveaux risques avec mitigations
  - Précision sur le nombre actuel de tests PASS (33/39)
- **v3**: Appliqué corrections via subagent explore (simulation de aidd-refine:02-challenge):
  - Clarification de la règle #4 : exclusion prioritaire en cas de conflit
  - Ajout de la section "Comportement en cas d'erreur" avec tableau récapitulatif
  - Précision sur le message d'erreur attendu pour valeur vide
  - Ajout du risque #6 avec mitigation
  - Mise à jour des mitigations existantes pour référence croisée

## Statut d'implémentation

- ✅ **Implémentation terminée** : Tous les fichiers modifiés et poussés (commit fd2de9c et 37fa6c1)
- ✅ **Version bumpée** : overcode 5.0.1 → 5.1.0
- ✅ **Tests ajoutés** : 8 nouveaux scénarios (S45-S52) dans backlog-scenarios.md
- ✅ **Documentation mise à jour** : workflow.md, aliases.md, CHANGELOG.md
- ⏳ **À valider** : Exécuter les scénarios de test pour confirmer 0 régression
