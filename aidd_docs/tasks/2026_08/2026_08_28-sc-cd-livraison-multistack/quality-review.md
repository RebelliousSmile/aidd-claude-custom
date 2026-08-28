# Revue qualité — skills `cd`

Date : 2026-08-28

Périmètre : six routeurs `cd`, leurs dix-huit actions et les six suites Behave `delivery-safety-scenarios.md`. La fixture est peuplée et strictement en lecture seule ; aucune commande de production n'est exécutée.

## Couverture comportementale

| Suite | Comportements couverts | Miroir NO-GO | Contrôles | Frontières couvertes |
| --- | --- | --- | --- | --- |
| sc-css | local statique, façade unique, contrat, idempotence, contribution composite, délégation automata | sortie absente, propriété sc-js | positif et négatif | web-tiers absent, sortie inventée |
| sc-js | détection Nuxt/pnpm, façade unique, contrat, idempotence, IndexedDB, SQL, délégation | façade existante conflictuelle | positif et négatif | contrat périmé, web-tiers absent |
| sc-php | wp-env/Docker, façade Composer, contribution JS/CSS, synchro WordPress raisonnée | portée ou direction de sync absente | positif et négatif | sauvegarde/confirmation absentes, web-tiers absent |
| sc-python | uv et processus multiples, façade Python, contrat, idempotence, Alembic | migration forcée de gestionnaire | positif et négatif | entrypoint inconnu, web-tiers absent |
| sc-rust | workspace, alias/xtask, artefact immuable, migration, health-check, rollback | cross-build non prouvé | positif et négatif | dépendance globale refusée, web-tiers absent |
| web-tiers | local non applicable, SSH/PaaS, métadonnées non secrètes, enveloppe CI mince | contrat producteur absent | positif et négatif | primitive SSH absente, contrat périmé, propagation d'échec |

La couverture de routage `local/server/automata` reste portée par les six `scenarios.json`. Les nouvelles suites couvrent volontairement un seul aspect distinct : la sûreté des mutations et la propriété de la livraison.

## Qualité des scénarios

Barème Behave : ambiguïté, observabilité, minimalité, NO-GO, contrôlabilité, préconditions et N/A, chacun sur 2 ; maximum 14. Aucun anti-pattern A–F n'a été détecté.

| Suite | Scénario | Score | Axe perfectible | Anti-pattern |
| --- | --- | ---: | --- | --- |
| sc-css | S1 | 13/14 | minimalité | aucun |
| sc-css | S2 | 12/14 | minimalité | aucun |
| sc-css | S3 | 14/14 | — | aucun |
| sc-css | S4 | 14/14 | — | aucun |
| sc-css | S5 | 14/14 | — | aucun |
| sc-css | S6 | 14/14 | — | aucun |
| sc-css | S7 | 12/14 | minimalité | aucun |
| sc-css | S8 | 14/14 | — | aucun |
| sc-js | S1 | 13/14 | minimalité | aucun |
| sc-js | S2 | 12/14 | minimalité | aucun |
| sc-js | S3 | 14/14 | — | aucun |
| sc-js | S4 | 14/14 | — | aucun |
| sc-js | S5 | 14/14 | — | aucun |
| sc-js | S6 | 14/14 | — | aucun |
| sc-js | S7 | 12/14 | minimalité | aucun |
| sc-js | S8 | 14/14 | — | aucun |
| sc-js | S9 | 14/14 | — | aucun |
| sc-php | S1 | 13/14 | minimalité | aucun |
| sc-php | S2 | 12/14 | minimalité | aucun |
| sc-php | S3 | 13/14 | observabilité | aucun |
| sc-php | S4 | 14/14 | — | aucun |
| sc-php | S5 | 13/14 | minimalité | aucun |
| sc-php | S6 | 13/14 | observabilité | aucun |
| sc-php | S7 | 12/14 | minimalité | aucun |
| sc-php | S8 | 14/14 | — | aucun |
| sc-python | S1 | 13/14 | minimalité | aucun |
| sc-python | S2 | 12/14 | minimalité | aucun |
| sc-python | S3 | 14/14 | — | aucun |
| sc-python | S4 | 14/14 | — | aucun |
| sc-python | S5 | 13/14 | observabilité | aucun |
| sc-python | S6 | 13/14 | minimalité | aucun |
| sc-python | S7 | 12/14 | minimalité | aucun |
| sc-python | S8 | 14/14 | — | aucun |
| sc-python | S9 | 14/14 | — | aucun |
| sc-rust | S1 | 13/14 | minimalité | aucun |
| sc-rust | S2 | 12/14 | minimalité | aucun |
| sc-rust | S3 | 14/14 | — | aucun |
| sc-rust | S4 | 14/14 | — | aucun |
| sc-rust | S5 | 14/14 | — | aucun |
| sc-rust | S6 | 14/14 | — | aucun |
| sc-rust | S7 | 12/14 | minimalité | aucun |
| sc-rust | S8 | 14/14 | — | aucun |
| sc-rust | S9 | 14/14 | — | aucun |
| web-tiers | S1 | 14/14 | — | aucun |
| web-tiers | S2 | 14/14 | — | aucun |
| web-tiers | S3 | 13/14 | minimalité | aucun |
| web-tiers | S4 | 14/14 | — | aucun |
| web-tiers | S5 | 14/14 | — | aucun |
| web-tiers | S6 | 12/14 | minimalité | aucun |
| web-tiers | S7 | 13/14 | minimalité | aucun |
| web-tiers | S8 | 14/14 | — | aucun |

Moyenne : **13,3/14**. Minimum : **12/14**. Statut : **vert** ; aucun scénario ne passe sous le seuil de 8/14.

## Validation `aidd-context:04-skill-generate`

Les routeurs ont été raccourcis vers le routage et les règles transversales. Chaque action déclare désormais son entrée, sa sortie, une procédure numérotée et des tests observables. Les titres d'action ont été corrigés après détection par le contrôle de cohérence.

| Fichier écrit | Règles contrôlées | Correction / résultat |
| --- | --- | --- |
| `plugins/sc-css/skills/cd/SKILL.md` | R1–R10, lignes 1–35 | description discriminante, hint, Mermaid, table Action/Does |
| `plugins/sc-css/skills/cd/actions/01-local.md` | R11–R13, lignes 1–27 | titre sans numéro, Input/Output/Process/Test |
| `plugins/sc-css/skills/cd/actions/02-server.md` | R11–R13 | Input/Output/Process/Test et garde de façade |
| `plugins/sc-css/skills/cd/actions/03-automata.md` | R11–R13 | délégation exacte et arrêt sans web-tiers |
| `plugins/sc-js/skills/cd/SKILL.md` | R1–R10 | description discriminante, hint, Mermaid, table Action/Does |
| `plugins/sc-js/skills/cd/actions/01-local.md` | R11–R13 | titre sans numéro, Input/Output/Process/Test |
| `plugins/sc-js/skills/cd/actions/02-server.md` | R11–R13 | façade unique, conflit explicite, tests |
| `plugins/sc-js/skills/cd/actions/03-automata.md` | R11–R13 | contrat courant et délégation exacte |
| `plugins/sc-php/skills/cd/SKILL.md` | R1–R10 | description discriminante, hint, Mermaid, table Action/Does |
| `plugins/sc-php/skills/cd/actions/01-local.md` | R11–R13 | titre sans numéro, wp-env borné, tests |
| `plugins/sc-php/skills/cd/actions/02-server.md` | R11–R13 | portée/direction et barrières de données |
| `plugins/sc-php/skills/cd/actions/03-automata.md` | R11–R13 | données risquées manuelles, délégation exacte |
| `plugins/sc-python/skills/cd/SKILL.md` | R1–R10 | description discriminante, hint, Mermaid, table Action/Does |
| `plugins/sc-python/skills/cd/actions/01-local.md` | R11–R13 | titre sans numéro, gestionnaire conservé, tests |
| `plugins/sc-python/skills/cd/actions/02-server.md` | R11–R13 | façade native et barrières SQL |
| `plugins/sc-python/skills/cd/actions/03-automata.md` | R11–R13 | contrat courant et web-tiers requis |
| `plugins/sc-rust/skills/cd/SKILL.md` | R1–R10 | description discriminante, hint, Mermaid, table Action/Does |
| `plugins/sc-rust/skills/cd/actions/01-local.md` | R11–R13 | titre sans numéro, toolchain/workspace conservés |
| `plugins/sc-rust/skills/cd/actions/02-server.md` | R11–R13 | artefact identifiable, migration et rollback |
| `plugins/sc-rust/skills/cd/actions/03-automata.md` | R11–R13 | alias exact, échecs propagés, web-tiers requis |
| `plugins/web-tiers/skills/cd/SKILL.md` | R1–R10 | description discriminante, hint, Mermaid, table Action/Does |
| `plugins/web-tiers/skills/cd/actions/01-local.md` | R11–R13 | titre sans numéro, frontière distante explicite |
| `plugins/web-tiers/skills/cd/actions/02-server.md` | R11–R13 | stratégie prouvée et secrets hors dépôt |
| `plugins/web-tiers/skills/cd/actions/03-automata.md` | R11–R13 | enveloppe mince, manuel par défaut, statut propagé |

Les références existantes ont été relues au titre de R14–R15 : elles restent atteignables depuis les actions concernées et aucune duplication supplémentaire n'a été introduite.

## Compatibilité des validateurs

- Le validateur de distribution des plugins accepte les six skills et leur `argument-hint`.
- Le validateur AIDD est satisfait : les six routeurs portent le `argument-hint` requis par R4.
- Le `quick_validate.py` générique du skill système Codex refuse actuellement `argument-hint`, qu'il ne connaît pas parmi ses clés de frontmatter. Ce conflit de schéma est documenté et la clé est conservée, car elle est exigée par la skill explicitement demandée et acceptée par le validateur du format de ce dépôt.

## Conclusion

**GO.** Les suites sont actionnables, contrôlables, sans accès production et distinctes des tests de routage. Les six plugins passent les validateurs du dépôt ; les contrôles `sc-cd`, couverture, cohérence et `git diff --check` passent également.
