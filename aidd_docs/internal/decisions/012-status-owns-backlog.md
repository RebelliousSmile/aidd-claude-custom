# Decision: `status` possède le backlog documentaire

| Field | Value |
|---|---|
| ID | DEC-012 |
| Date | 2026-08-27 |
| Feature | Backlog documentaire par milestone et intégration à `previously` |
| Status | Accepted |
| Antécédent | **DEC-011** — borne du bloc généré par motif |

## Context

Le backlog était une chaîne de la skill `alias`, alors qu'il synchronise un état durable du projet au même titre que les autres actions de `status`. Son intégration souhaitée à `previously` rendait cette confusion plus visible : une routine de reprise devait appeler un alias voisin et risquait de reproduire son rapport ou sa liste d'issues.

Les milestones ajoutent aussi une structure générée sous `## Backlog`. DEC-011 borne les lignes plates historiques, mais ne décide ni l'autorité de la capacité ni la reconnaissance de groupes titrés.

## Decision

### 1. `status` est l'unique autorité du backlog

La synchronisation devient l'action `status backlog`. L'ancien alias `backlog` est supprimé, sans redirection ni compatibilité de dispatch. `status backlog` possède la collecte, le filtre, le rendu, la reconnaissance et l'écriture atomique.

`previously --backlog <fichier.md>` ne réimplémente rien : il chaîne cette action comme précondition facultative, relaie son échec, puis ne conserve qu'une quittance compacte. Le rapport `status report` reste propriétaire du seul compte d'issues affiché dans le snapshot.

### 2. Les groupes ont l'identité du provider

Une milestone est rattachée et regroupée par son identifiant stable GitHub ou GitLab, jamais par son titre. Le titre brut sert au filtre exact et au tri ; une copie échappée sert seulement au rendu. Deux identifiants portant le même titre restent deux groupes distincts, et rendent un filtre par ce titre ambigu.

### 3. Le rendu reste adaptatif

Un catalogue milestone vide conserve le bloc plat de DEC-011, sans donnée milestone visible. Un catalogue non vide produit des sous-titres réservés `### Milestone: …` et `### Sans milestone`, triés par échéance, puis sans échéance, puis non assignés. Cette compatibilité évite de modifier les projets qui n'utilisent pas la notion de milestone.

### 4. DEC-011 est étendue, pas réécrite

Le bloc généré accepte désormais une forme groupée complète : chaque sous-titre réservé doit être immédiatement suivi d'au moins une ligne d'issue canonique du dépôt courant. Un groupe isolé ou suivi de prose est manuel ; tout autre sous-titre, notamment `### Notes historiques`, arrête la reconnaissance. Les anciens blocs plats et leur suffixe d'état toléré restent reconnus et migrent en une passe.

La limite nouvelle est explicite : un sous-titre manuel strictement conforme au motif réservé et immédiatement suivi d'une ligne d'issue canonique est indiscernable d'un groupe généré. Les limites de DEC-011 sur une ligne canonique manuelle et sur l'état vide restent valables.

## Rationale

La propriété suit la donnée durable plutôt que la commodité d'invocation. Cela donne une route publique unique, permet à d'autres routines de chaîner la capacité sans créer d'alias supplémentaire, et garde `previously` centré sur l'orchestration.

L'identité provider empêche une fusion silencieuse de milestones homonymes. Le maintien du format plat quand le catalogue est vide minimise le bruit documentaire et préserve les documents existants.

## Compatibility

- Rupture publique : `/overcode:alias backlog` disparaît ; utiliser `/overcode:status backlog`.
- Compatibilité documentaire : les blocs plats déjà générés restent reconnus et remplacés sans duplication.
- Compatibilité des projets sans milestone : leur rendu reste plat.
- `previously` sans `--backlog` conserve son flux historique.

## Consequences

- La rupture est distribuée sous `overcode` 5.0.0.
- Les descriptions publiques comptent dix alias et présentent la synchronisation comme une action de `status`.
- Les harnais de routage et de comportement vivent sous `status`; les journaux historiques mentionnant `alias backlog` restent inchangés.
