# Modèle de contenu — block theme (FSE)

Réalisation de la phase *Établir le modèle de contenu* de `workflow-fse.md`. Aucun verbe design ne
produit de modèle de contenu : le contrat porte le vocabulaire visuel, pas les types de données. Sur une
plateforme qui distingue pages et types de contenu, quelqu'un doit le dériver — sur block theme, c'est ici.

Le scaffold amont (`sc-php:setup`) ne peut pas le faire : il s'exécute sur un dossier vide, avant que la
référence n'existe. Son squelette est un plancher navigable, jamais un modèle.

## Reconnaître un type dans une référence multipage

Une page de la référence n'est pas toujours une page du site. Trois signatures désignent un **type**, pas
une page :

| Signature dans la référence | Ce que c'est |
|---|---|
| Page titrée « Modèle / Template / Exemple / Fiche — `<nom au singulier>` » | un **spécimen** : une instance rendue d'un type |
| Page listant des cartes homogènes pointant vers ce spécimen | l'**archive** du type |
| Page de soumission alimentant ce type (« Annoncer un… », « Proposer un… ») | la **source d'alimentation** du type |

Indices secondaires : filtres ou onglets sur l'archive (catégorie, lieu, période) ⇒ **taxonomies** ; champs
du spécimen qui ne sont ni titre ni corps (date, lieu, tarif) ⇒ **métadonnées** ; renvoi du spécimen vers
un autre spécimen ⇒ **relation** entre deux types.

Règle de preuve : un type se prouve par **au moins deux vues** (spécimen + archive), ou par un spécimen
plus sa source d'alimentation. Une page unique sans répétition n'est jamais un type — c'est une page.

La sortie de cette lecture est un inventaire écrit, un type par ligne : nom, segment d'URL, taxonomies,
métadonnées, relations, et la ou les pages de la référence qui le prouvent. Un type sans page qui le
prouve est une invention ; une page-spécimen sans type est un trou.

## Où l'enregistrer

Dans le **plugin**, jamais dans le thème. Un type enregistré par le thème disparaît avec lui : le contenu
reste en base et devient inatteignable au changement de thème. C'est la même séparation que celle du
squelette de scaffold — le thème rend, le plugin porte.

```
plugins/<plugin>/includes/post-types.php
plugins/<plugin>/includes/taxonomies.php
```

Requis depuis le fichier principal, enregistrement sur `init`.

## Paramètres qui ne sont pas facultatifs en FSE

- `show_in_rest => true` — sans lui l'éditeur de blocs ne s'ouvre pas sur ce type : l'écran classique le
  remplace. Le type existe, il n'est pas éditable en FSE. Même exigence sur chaque taxonomie, faute de quoi
  elle n'apparaît dans aucun panneau.
- `has_archive => true` pour tout type qui a une archive dans la référence. Sans lui, `archive-<type>.html`
  n'est routé par rien : le fichier existe et n'est jamais servi.
- `supports` énuméré explicitement. Le défaut ne couvre que `title` et `editor` — pas de vignette, pas
  d'extrait. Une carte d'archive qui affiche une image sur la référence exige `thumbnail`.
- `rewrite['slug']` = le segment d'URL **de la référence**, pas le nom interne du type.
- `register_post_meta` pour chaque métadonnée relevée, avec `show_in_rest`, `type` et `single`. Sans
  enregistrement, le champ est invisible à l'éditeur et à l'API : les valeurs du spécimen n'ont nulle part
  où vivre.
- Régénération des règles de réécriture après enregistrement : les permaliens du nouveau type rendent 404
  tant qu'elle n'a pas eu lieu. Sur le hook d'activation du plugin, ou par la commande CLI en
  développement — jamais `flush_rewrite_rules()` sur `init`, qui réécrit à chaque requête.

## Templates dérivés

Pour chaque type : `templates/single-<type>.html` et, s'il a une archive, `templates/archive-<type>.html`.
Pour chaque taxonomie : `templates/taxonomy-<taxonomie>.html`.

Ces fichiers sont détectés par leur **nom** ; `theme.json` ne les déclare pas (`customTemplates` ne sert
qu'aux templates assignables à la main depuis l'éditeur).

Le mode de défaillance à connaître : sans `single-<type>.html`, la hiérarchie sert `single.html`. Le site
n'est pas cassé — il est **silencieusement générique**. Ni le code HTTP, ni la présence de `wp-site-blocks`,
ni l'absence d'erreur ne distinguent ce cas du cas nominal.

## Position dans le workflow

Avant le **rendu natif** et avant toute énumération du périmètre de mesure. Deux raisons, chacune
suffisante :

- `diffuse` pose des patterns dans des templates. Un template qui n'existe pas n'offre aucun point de pose,
  et le pattern atterrit dans le template générique le plus proche — où il ne sera jamais rejoué.
- Le périmètre de mesure énumère les templates du thème (`workflow-fse.md § Périmètre de mesure`).
  Énuméré avant, il rend une couverture **complète d'un thème incomplet** : tous les templates mesurés,
  tous verts, et les vues du modèle de contenu absentes du dénominateur. C'est le piège 10 déplacé d'un
  cran — non plus une vue non mesurée, mais une vue qui n'existe pas encore.

## Vérification

1. Chaque type de l'inventaire figure dans `wp post-type list --field=name` ; chaque taxonomie dans
   `wp taxonomy list --field=name`.
2. Créer une instance publiée, charger son permalien : HTTP 200 **et** le template servi est bien celui du
   type. Le prouver par un marqueur distinctif porté par `single-<type>.html` et cherché dans la réponse —
   un 200 seul ne distingue pas le template du type de son fallback générique.
3. Charger l'archive : l'instance y figure.
4. **Contre-épreuve obligatoire** : retirer `single-<type>.html`, rejouer. La réponse doit rester 200 et le
   marqueur doit disparaître. Sans cette bascule, l'étape 2 n'atteste que la disponibilité du site.
