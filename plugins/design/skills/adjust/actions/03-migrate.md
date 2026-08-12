# Migrate

## Rôle

Faire passer un contrat 1.x (monolithe `components.json`) aux artefacts 2.0 racinés par `release.json` — trois obligatoires, plus `oracle.json` si le contrat porte des cibles de mesure — sans changer le verdict rendu sur le code du projet.

La redistribution champ par champ est celle de `${DESIGN_PLUGIN_ROOT}/references/contract-schema.md § Redistribution depuis un contrat 1.x`. Elle est **implémentée par le script** — ne pas la rejouer à la main, ne pas la reproduire ici.

**Déclencheur** : `lint-core.mjs` sort en 3 en nommant la commande de migration, ou l'utilisateur demande explicitement le passage en 2.0.

## Entrées

| Entrée | Origine | Obligatoire |
|---|---|---|
| Répertoire du contrat | l'utilisateur, ou le message d'exit 3 du linter | oui |
| `mode` (`bem` \| `utility-first`) | le contrat s'il le déclare, sinon l'utilisateur | oui — le script refuse de le deviner |
| Jeu de fichiers de référence pour la non-régression | le glob déjà scanné par `02-freeze § Étape 2bis` | oui |

## Étape 1 — Verdict de référence, avant toute écriture

Relever le verdict actuel, contrat 1.x en place, sur les fichiers de référence. C'est le seul point de comparaison qui prouvera que la migration n'a rien changé ; il n'est plus reconstituable une fois le contrat réécrit.

```
node ${DESIGN_PLUGIN_ROOT}/skills/enforce/adapters/lint-core.mjs <fichier> --contract <dossier-du-contrat>
```

Consigner le code de sortie de chaque fichier. Si le linter installé est déjà en 2.0, il sort en 3 sur un contrat 1.x : dans ce cas le verdict de référence se relève avec la version du linter antérieure à la migration, ou se lit dans la dernière exécution de gate archivée. Sans verdict de référence, la migration reste possible mais l'Étape 5 ne prouve rien — le dire à l'utilisateur plutôt que de la sauter en silence.

## Étape 2 — Dry-run

```
python ${DESIGN_PLUGIN_ROOT}/tools/migrate-contract.py --contract <dossier> --dry-run
```

Le rapport donne : la table de correspondance champ source → champ cible, la table des adapters réellement présents avec leur consommateur, les anomalies, et le statut de maturité initial.

Le dry-run n'écrit rien.

### Le script sort en 2

| Message | Décision à prendre |
|---|---|
| mode non déclaré | choisir avec l'utilisateur, puis relancer avec `--mode bem` ou `--mode utility-first`. Ne jamais trancher seul : un mode faux rend les règles de vocabulaire inertes et transforme un run vert en verdict sur rien |
| conflit de mode | le contrat déclare un mode, `--mode` en dit un autre — corriger la source, pas l'invocation |
| `tokens.json` ou `components.json` absent | ce n'est pas un contrat 1.x ; vérifier le chemin |

## Étape 3 — Validation humaine du rapport

Soumettre le rapport et attendre l'accord explicite. Trois points à faire lire, jamais à valider à la place de l'utilisateur :

- **les anomalies** — une clé hors table de redistribution est transportée telle quelle, jamais perdue, mais son emplacement final n'engage que le script ; c'est à l'utilisateur de dire s'il convient ;
- **le statut initial** — il n'est opposable à rien à ce stade, mais il constate l'état réel du contrat ;
- **la table des adapters** — un consommateur `unknown` est à compléter à la main après écriture.

## Étape 4 — Écrire

```
python ${DESIGN_PLUGIN_ROOT}/tools/migrate-contract.py --contract <dossier>
```

Le script sauvegarde le contrat 1.x avant d'écrire, dans un répertoire préfixé d'un point — le linter ignore les répertoires pointés, la sauvegarde ne peut donc pas être confondue avec un second contrat. Le rapport final nomme le répertoire de sauvegarde et les fichiers écrits.

Une seconde exécution sur un contrat déjà migré est un no-op annoncé comme tel : la migration est rejouable sans précaution.

## Étape 5 — Non-régression

Rejouer le linter 2.0 sur les mêmes fichiers qu'à l'Étape 1, contre le contrat migré.

**Critère** : code de sortie identique, fichier par fichier. Un seul écart invalide la migration.

Un écart ne se corrige pas en ajustant le contrat migré à la main. Restaurer depuis la sauvegarde, identifier le champ mal placé dans le rapport de dry-run, corriger la source 1.x s'il s'agit d'une donnée manquante, puis rejouer.

## Sortie attendue

> Contrat migré en 2.0.
>
> - `release.json` — version {V}, statut {statut}, charte {présente|absente}
> - `components.json` — {M} composants
> - `policies.json` — mode {mode}, {N} adapters
> - `oracle.json` — {P} composants ciblés *(ligne omise si le contrat 1.x n'en portait aucun : le fichier n'est alors ni écrit ni déclaré)*
> - Sauvegarde du contrat 1.x : `{répertoire}`
> - Non-régression : {K}/{K} fichiers au même verdict qu'avant migration

## Test

- [ ] Le verdict de référence a été relevé **avant** l'écriture, ou son absence a été annoncée à l'utilisateur
- [ ] Le dry-run a été lu et validé explicitement par l'utilisateur avant l'écriture
- [ ] Le mode a été déclaré par le contrat ou choisi par l'utilisateur — jamais deviné
- [ ] `release.json` existe et `$format` vaut `2.0`
- [ ] La sauvegarde du contrat 1.x existe et contient l'ancien `components.json`
- [ ] Chaque fichier de référence rend le même code de sortie qu'à l'Étape 1
- [ ] Une seconde exécution du script est annoncée no-op et ne produit aucun diff
- [ ] Toute anomalie du rapport est soit corrigée, soit explicitement acceptée par l'utilisateur
