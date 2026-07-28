# Scan

Auditer la couverture builder : quels composants des pages n'ont **pas** de pattern
éditable enregistrée.

## Process

### Step 1 — Vérifier l'environnement

Confirmer que wp-env tourne et que le thème actif est un thème bloc avec
`patterns/*.php`. Utiliser exclusivement `pnpm dlx @wordpress/env run cli wp`.

### Step 2 — Lancer le gate

```bash
pnpm dlx @wordpress/env run cli wp eval-file <chemin>/builder-coverage.php
```

Surcharges optionnelles (sinon auto) :
- `BC_PREFIX=mau-` — préfixe des classes composant (auto-détecté par défaut).
- `BC_POST_TYPES=page,post,sc_service` — post types audités (publics par défaut).

Copier le script depuis `actions/scripts/builder-coverage.php` (le poser dans un
dossier accessible au conteneur, ex. `tools/qa/`).

### Step 3 — Lire le verdict

La sortie donne `COUVERTS`, `NON COUVERTS` (avec pages exemples) et une ligne
finale `GAPS: N`.

- `GAPS: 0` → couverture complète, rien à faire.
- `GAPS: N` → passer à `02-close-gaps` avec la liste.

### Step 4 — Écarter les faux positifs

Avant de traiter un gap, vérifier que ce n'est pas :
- une **variante** (`x--modifier`) dont la base est déjà couverte — le script
  normalise, mais recouper si doute ;
- un composant du **cache périmé** — relancer après `wp_clean_themes_cache()`.

### Step 5 — Sortir chaque gap survivant en ticket (obligatoire)

Un gap qui n'est pas fermé dans la foulée **ne reste pas une ligne de rapport**. Il
sort du scan sous forme de ticket : fichier de tâche du projet **et** issue, avec le
composant, les pages exemples, et la raison du report.

Pourquoi c'est une règle et pas une bonne pratique : un gap consigné en prose n'a ni
propriétaire, ni échéance, ni gate. Il se fait re-déclarer « hors périmètre » par
chaque tâche suivante — qui pointe vers la déclaration précédente comme
justification — jusqu'à ce qu'une reformulation lui retire son statut de manque
(« dette de contenu à suivre, pas un fix manqué »). Le défaut est alors livré, et
plus personne n'en répond. Ce mécanisme a été observé en production, sur trois
tâches successives, sur des gaps qui étaient la colonne latérale d'un article.

**Règle des deux occurrences** : un gap ne peut être re-déclaré hors périmètre
qu'**une seule fois**. À la seconde, un arbitrage est dû, et il n'a que trois
issues valides :

| Issue | Ce qu'elle exige |
|---|---|
| Fermer | passer à `02-close-gaps` |
| Planifier | ticket avec échéance et propriétaire nommés |
| Refuser | inscription au registre des non-réalisés, avec la raison |

« On verra plus tard » n'en fait pas partie.

### Step 6 — Scan inverse : les sélecteurs orphelins

`01-scan` part du **contenu réel** : il ne voit que les classes présentes en base.
Il est donc structurellement aveugle au cas symétrique — une famille CSS portée
depuis la référence dont le markup n'a jamais été écrit. Le CSS est là, complet,
sans un seul consommateur : personne ne le voit, et c'est pourtant la trace
matérielle d'un travail commencé puis abandonné.

```bash
# 1. Dumper le contenu stocké : une part du markup vit en base, pas dans les sources.
pnpm dlx @wordpress/env run cli wp post list \
  --post_type=page,post,<cpt> --post_status=any --field=post_content > /tmp/db-content.html

# 2. Scanner, en incluant ce dump dans le markup
node <chemin>/orphan-selectors.mjs \
  --css <theme>/assets/css \
  --markup <theme>/templates <theme>/parts <theme>/patterns <plugin>/ /tmp/db-content.html
```

Le script liste les classes déclarées en CSS sans occurrence dans le markup. Chaque
orpheline est **soit** un gap de markup (le composant reste à écrire : traiter comme
un gap de Step 5), **soit** du CSS mort (à supprimer). Les deux demandent une
action ; aucune ne se laisse en l'état.

**Oublier le dump DB (étape 1) produit des faux positifs**, et pas des moindres :
tout composant dont le markup vit en `post_content` remonterait comme orphelin. Les
deux scans sont complémentaires par construction — `01-scan` regarde la base et rate
le CSS sans consommateur, `orphan-selectors` regarde le CSS et rate ce qui n'est
qu'en base. Aucun des deux seul ne prouve la couverture.

Les entrées marquées `[racine présente — concaténation possible]` signalent un
modificateur dont la base existe dans le markup : soit la variante est assemblée à
l'exécution (faux positif), soit elle n'est réellement jamais émise — et c'est alors
souvent une divergence de branche SSR (Step 7).

### Step 7 — Parité des branches conditionnelles (SSR)

Un rendu SSR (`render.php` d'un bloc dynamique) contient des branches que les
données présentes en base n'activent pas forcément. Une branche jamais rendue n'est
jamais capturée, donc jamais comparée : aucune mesure ne peut la couvrir.

Pour chaque bloc SSR dont la référence a un équivalent, lire les deux côte à côte et
comparer la **structure conditionnelle**, pas le rendu :

- la référence produit-elle des éléments que le SSR ne produit dans aucun cas ?
  (piège classique : la référence rend deux boutons quand deux champs sont
  renseignés, le SSR fait `if / elseif` et n'en rend jamais qu'un) ;
- une branche du SSR est-elle inatteignable avec les données du modèle ?

Sortie : liste des divergences de branche, traitées comme des gaps.

## Output

Format plain-text, jamais de tableau markdown :

```
✅ builder-coverage — préfixe «mau-», 52 pages auditées
   Couverts   : 85
   Non couverts : 3
     - mau-contact-card        5 page(s)   ex: 180,181,159
     - mau-hero-stats          1 page(s)   ex: 141
     - mau-team-grid           1 page(s)   ex: 180
   → GAPS: 3 — lancer 02-close-gaps
```

Si `GAPS: 0` :

```
✅ builder-coverage — GAPS: 0, couverture complète
```
