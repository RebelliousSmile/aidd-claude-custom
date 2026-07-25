# Registre d'enforcement

Espace fermé des valeurs de `policies.json § usage.rules[].enforcement`. Chaque valeur nomme **la preuve** que la règle doit lire ; le réalisateur s'en déduit. Aucune valeur ne nomme une plateforme.

Lu par `tools/run-gates.py` (agrégation, sélection du réalisateur) et par `enforce/04-pivot.md` (émission du spec).

## Types

| `enforcement` | Preuve que la règle doit lire | Réalisateur | Cible |
|---|---|---|---|
| `markup` | un fichier de markup, en texte | `skills/enforce/adapters/lint-core.mjs` | le fichier passé au linter |
| `stylesheet` | les feuilles de style du projet, sélecteurs compris | pivot `sc-css:design-bridge` | les sources de style déclarées |
| `source-graph` | la source applicative parsée, plusieurs nœuds à la fois | pivot `sc-<langage source>:design-bridge` | les globs de source déclarés |
| `stored-content` | du contenu hors des fichiers source (base, CMS, API) | pivot `sc-<langage du runtime>:design-bridge` | le magasin de contenu du runtime |
| `platform-config` | le fichier de configuration de la plateforme | pivot `sc-<langage du runtime>:design-bridge` | ce fichier |
| `unrealized` | — | aucun | — |

`<langage source>` et `<langage du runtime>` sont lus dans le projet, jamais supposés. Le pivot absent ne change pas le type de la règle : il la laisse **non réalisée à l'exécution** (§ Marqueur non réalisé).

## Ce qui échappe au linter, et pourquoi

`lint-core.mjs` lit **un fichier de markup à la fois, en texte**. Quatre classes de règles sortent de cette portée par construction, et aucune ne peut y rentrer :

| Classe | Type | Hors de portée parce que |
|---|---|---|
| Sélecteurs de feuille de style | `stylesheet` | la classe fautive n'est pas dans le markup, elle est dans le style |
| Fichier de configuration de plateforme | `platform-config` | le fichier n'est pas du markup et a sa propre grammaire |
| Contenu stocké hors des fichiers source | `stored-content` | rien n'est sur le disque au moment du lint |
| Co-occurrence sémantique | `source-graph` | exige deux nœuds liés ; un scanner de chaînes ne les apparie pas sans faux positif |

## Contrôles a11y — qui réalise quoi

L'a11y est scindée par ce qui est **calculable et quand** (dec-002, côté WHAT/HOW). Deux volets sont calculés par le plugin au figeage et enregistrés dans `release.json § checks` ; le troisième est du markup et reste au pivot. Aucun n'est une prétention non tenue.

| Volet | Preuve lue | Réalisateur | Quand |
|---|---|---|---|
| Contraste texte/fond | valeurs de tokens résolues par thème | `adapters/a11y/contrast.py` (plugin) | au figeage, déterministe |
| Présence déclarative des états `disabled`/`error`/`focus` | `components.json § .states` | `tools/status.py` (plugin) | au figeage, sans markup |
| Rôles et attributs ARIA | `components.json § .a11y.role`/`.requires` opposés au markup rendu | pivot `sc-<langage>:design-bridge` (type `markup`) | à l'enforcement |

Le contraste et les états pèsent sur le statut de maturité (`maturity-status.md`) : ils sont **réalisés**, non déclarés non réalisés. Les rôles et attributs exigent le markup rendu qu'aucun figeage ne possède ; sans pivot installé, ils sont **non réalisés à l'exécution** (§ Marqueur non réalisé), jamais affirmés par le plugin.

## Règle de typage

- `enforcement` **absent** ⇒ contrat inutilisable, exit 2. Même doctrine que `mode` : l'outil refuse de deviner qui réalise une règle.
- Valeur **hors de ce registre** ⇒ exit 2, message nommant la règle et la valeur.
- `unrealized` est une valeur du registre : elle ne fait jamais sortir en 2.

## Marqueur non réalisé

Une règle est **non réalisée** dans deux cas, indistinguables dans le rapport :

1. `enforcement: "unrealized"` — aucun réalisateur n'existe pour cette règle.
2. Type réalisable, réalisateur absent du projet — pivot non installé.

Obligation, dans les deux cas :

- `run-gates.py` liste la règle dans son rapport, avec son `id`, son type et la raison.
- Le code de sortie est **inchangé** : une règle non réalisée n'est ni une violation ni une conformité. La déclarer est exactement ce qui empêche de la lire comme vérifiée.
- Aucun drapeau ne masque la liste.

## Valeurs retirées

| Retirée | Remplacée par |
|---|---|
| `baseline` | `markup` |
| `pivot-only` | le type qui nomme la preuve — `stylesheet`, `source-graph`, `stored-content` ou `platform-config` |

`pivot-only` ne disait pas quelle preuve la règle demandait : il ne désignait aucun réalisateur. `tools/migrate-contract.py` le traduit en `unrealized` et le signale — un contrat 1.x ne porte pas l'information manquante, et la deviner reviendrait à inventer un réalisateur. Le re-typage est un geste d'auteur.
