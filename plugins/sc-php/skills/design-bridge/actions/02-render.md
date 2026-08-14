# Render (sc-php)

## Rôle

Rendre l'élément neutre en **block pattern WordPress FSE** idiomatique + mettre à jour `theme.json` si nécessaire. Dérive strictement du spec de rendu reçu de `design:diffuse/03-pivot`.

## Input attendu (spec de rendu)

```
## Design render spec
Source: design/tokens.json + design/components.json
Version: <semver>
Component: { name, base, elements, modifiers, backgrounds, a11y }
Variants to produce: [...]
Render target: { language: php-fse-block, output_dir: ... }
```

Vérifier que le spec est présent avant de continuer.

## Prérequis WP

Lire `${SC_PHP_PLUGIN_ROOT}/skills/design-bridge/references/wordpress-pitfalls.md` intégralement avant de produire quoi que ce soit. Points critiques :
- CLI conteneur obligatoire pour toute opération DB
- Classes appariées `has-*` → décider de les déclarer dans le manifeste ou les exclure du lint
- `wp eval-file` deprecated → utiliser `wp eval` avec `file_get_contents`
- Propagation block patterns : la source doit être réimportée après modification
- **Piège 8** : jamais de reset sur sélecteur descendant d'élément (`.wp-site-blocks a`) — il écrase
  toutes les classes simples du manifeste
- **Piège 9** : l'oracle de fidélité est relatif, il ne voit pas les défauts de la maquette → un gate
  absolu (contraste rendu) est obligatoire au-dessus
- **Piège 10** : le périmètre de l'oracle énumère *tous* les templates, `single*`/`archive*`/`404` compris

## Étape 1 — Produire le HTML du block pattern

Le block pattern WP est du HTML enrichi de commentaires Gutenberg (`<!-- wp:... -->`). Seules les classes du spec sont utilisées dans les balises HTML ; Gutenberg peut ajouter les siennes dans les commentaires (ex. `{"className":"card card--featured"}`).

Structure type :

```html
<!-- wp:group {"className":"<base> <modifier>","style":{}} -->
<div class="wp-block-group <base> <modifier>">

  <!-- wp:image {} -->
  <figure class="wp-block-image <base>__<element>">
    <img src="" alt=""/>
  </figure>
  <!-- /wp:image -->

  <!-- wp:group {} -->
  <div class="wp-block-group <base>__body">

    <!-- wp:heading {"level":2} -->
    <h2 class="wp-block-heading <base>__title">Titre</h2>
    <!-- /wp:heading -->

  </div>
  <!-- /wp:group -->

</div>
<!-- /wp:group -->
```

Règle : la classe design system (`card`, `card__body`, etc.) est sur l'élément HTML ; la classe WP (`wp-block-group`, etc.) est sur le même élément mais ne fait PAS partie du manifeste design — ne pas la linéter contre le manifeste.

## Étape 2 — Mettre à jour theme.json

Pour chaque fond autorisé (`.backgrounds`) du composant, vérifier que la couleur correspondante existe dans `theme.json § settings.color.palette` :

```json
{
  "settings": {
    "color": {
      "palette": [
        {
          "name": "Background",
          "slug": "semantic-background",
          "color": "#f7f8fa"
        }
      ]
    }
  }
}
```

- Si le slug existe déjà avec la bonne valeur → OK.
- Si le slug manque → ajouter l'entrée (valeur dérivée de `tokens.json` via le spec).
- Si la valeur diffère → signaler comme divergence (voir piège 7 de `wordpress-pitfalls.md`).

## Étape 3 — Enregistrer le block pattern

Créer le fichier du pattern dans l'output dir du spec (ex. `patterns/<canonical-name>.html`) avec une en-tête WordPress :

```php
<?php
/**
 * Title: <Nom du composant>
 * Slug: <plugin-ou-theme>/<canonical-name>
 * Categories: <categorie>
 * Viewport Width: 1200
 */
?>
<!-- Block pattern HTML ici -->
```

Si le projet utilise un répertoire `patterns/` dans le thème, placer le fichier à cet endroit.

## Étape 4 — Gate enforce

Linter le HTML du block pattern produit :

```bash
# Extraire le HTML (sans les commentaires wp:...) dans un fichier temporaire
# Puis linter contre le contrat
node design/lint/lint-core.mjs /tmp/pattern-<canonical-name>.html
```

Si exit 1 → corriger les classes non conformes, re-lint, ne pas livrer en exit 1.

### Étape 4b — Gates absolus (indépendants de la maquette)

Le lint de vocabulaire et l'oracle de fidélité sont tous deux **relatifs** (au manifeste, à la maquette).
Deux contrôles supplémentaires sont dus avant de livrer un rendu, parce qu'aucun des deux premiers ne
peut les produire (pièges 8 et 9) :

1. **Contraste sur page rendue.** Pour chaque paire texte/fond du composant, lire `color` et
   `background-color` **calculés** (`getComputedStyle`) sur une instance réellement rendue, pas les
   valeurs déclarées dans le CSS. Une paire déclarée conforme peut rendre 1,06:1 si un reset descendant
   l'écrase. Seuil : WCAG AA (4,5:1 texte courant, 3:1 texte large et éléments d'interface).
2. **Spécificité.** Pour chaque propriété que le composant déclare sur un `<a>`, `<p>`, `<button>` ou
   `<li>`, vérifier qu'aucune règle descendante d'élément du CSS global ne la domine. Voir piège 8,
   règle 3, pour la forme exécutable du contrôle.

Un échec ici n'est **jamais** absorbable par le registre de déviations : le ledger sert à acter un écart
*au contrat*, pas un défaut d'accessibilité. Si la maquette est la source du défaut, corriger des deux
côtés (piège 9).

## Étape 5 — Poser le pattern

Un pattern enregistré n'est **rendu nulle part**. Il entre dans l'inserteur de l'éditeur, et c'est tout :
aucune page ne le contient tant qu'il n'a pas été posé. Le gate de vocabulaire linte le fichier du pattern
et sort vert ; le gate de fidélité mesure des templates qui ne le contiennent pas et sort vert. Deux verts,
site inchangé — le rendu est livré et invisible.

Le spec de rendu ne porte pas cette information : son `Render target` nomme un langage et un répertoire de
sortie, jamais un point d'insertion, et le contrat interdit à `03-pivot` de transporter des contraintes de
plateforme. Le placement appartient donc à ce réceptacle.

Trois destinations, une seule à choisir, **écrite** :

| Destination | Forme | Quand |
|---|---|---|
| Template du thème | `<!-- wp:pattern {"slug":"<prefix>/<canonical-name>"} /-->` dans `templates/*.html` ou `parts/*.html` | la section appartient à une vue, pas à une page |
| Contenu en base | markup du pattern copié dans `post_content` | la section appartient à une page éditée |
| Aucune, assumée | — | brique d'auteur destinée à l'insertion manuelle |

La troisième est un **statut déclaré**, jamais un silence : `posé: non — brique d'auteur`. Sans elle, un
pattern oublié et un pattern délibérément non posé laissent la même trace, et le bilan ne peut que les
confondre.

Deux conséquences à connaître avant de choisir :

- L'insertion par `wp:pattern` dans un **fichier** de thème est résolue au rendu : le contenu suit la
  source. L'insertion par copie ne suit rien (piège 2).
- Dès qu'un template est sauvegardé depuis l'éditeur de site, WordPress en écrit une copie en base qui
  **prend le pas sur le fichier du thème**, pattern aplati compris. Le fichier corrigé ensuite ne change
  plus rien à l'écran. C'est le piège 2 appliqué aux templates.

Vérification : charger la vue qui doit porter le pattern et y trouver un marqueur du markup produit. Un
`patterns/` peuplé n'est pas une preuve de pose.

## Étape 6 — Propagation (si pattern existant mis à jour)

Si le pattern existait déjà en DB, relancer le script d'import du projet pour propager :

```bash
pnpm dlx @wordpress/env run cli wp eval \
  '$c = file_get_contents("/var/www/html/tools/import/<script>.php"); eval($c);'
```

Puis relancer `design:enforce/03-lint-instances` pour vérifier les instances en DB.

## Sortie attendue

> Block pattern WP produit : `patterns/<canonical-name>.html`
> Variantes : <liste>
> theme.json : <mis à jour / aucune modification>
> Posé dans : <template ou page, et le marqueur qui le prouve> · ou `non — brique d'auteur`
> Gate enforce : vert (exit 0)
> Gates absolus : contraste <ratio min> · spécificité <0 conflit / N conflits>
> Couverture : mesuré = <liste> · non mesuré = <liste + raison>
>
> Retour à design:diffuse — rendu WP livré.

**Aucune sortie ne conclut avec un gate `OPEN`.** Si un gate reste rouge, la sortie porte le verdict
rouge, le commit d'origine de la régression (`git log -S"<chaîne>" -- <fichier>` — c'est la commande qui
transforme « on ne sait pas d'où ça vient » en attribution) et un propriétaire nommé. « Préexistant »,
« hors périmètre de cette part » et « sans rapport avec ce travail » ne sont pas des statuts : ce sont
des formulations qui font traverser un gate rouge à plusieurs itérations sans que personne n'en hérite.
