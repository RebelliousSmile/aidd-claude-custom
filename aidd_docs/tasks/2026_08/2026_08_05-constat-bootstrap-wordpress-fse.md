# Constat — bootstrap WordPress FSE de `sc-php:setup`, exécuté et mesuré

> **Résolu en `sc-php` 0.10.3** (même jour). Les sept défauts sont corrigés dans la source et le scaffold a été rejoué de bout en bout contre les références corrigées — voir le CHANGELOG du plugin pour les mesures d'après-correction. Ce document reste tel qu'il a été mesuré : c'est l'état d'avant.
>
> **Réemployé comme terrain de `design:harness`** (`design` 2.9.0, même jour). Le bootstrap corrigé a été rejoué sur une racine jetable, puis la chaîne `harness.py → HTML → remplissage → measure.py → verdict` a tourné contre ce site réel : verdict machine rendu sur les trois échantillons device, sans exception. Le point « la confrontation avec la maquette n'apporterait rien » ci-dessous garde sa valeur — il portait sur le **diagnostic du site blanc**, où la maquette était l'instrument ; ici c'est le site qui est le terrain de la chaîne, l'usage est inverse.
>
> **Constat, pas plan.** Rien n'est corrigé ici. Toutes les ancres `fichier:ligne` renvoient à la **source** (`plugins/sc-php/skills/setup/`), jamais au cache installé.

## Protocole

Le flow `01 → 02 → 06` a été exécuté **littéralement** : chaque fichier écrit avec le contenu exact des références, aucun ajout, aucun contenu inventé au-delà des placeholders. Racine jetable `_fse-bootstrap` — nom choisi pour exercer le piège d'origine (`pitfalls.md` #1 : dossier commençant par `_`). Environnement réel : Docker 29.6.1, pnpm 10.5.2, **WordPress 7.0.2** servi sur `localhost:8891`. Tout a été détruit après mesure (conteneurs, volumes, cache `~/.wp-env`) ; le projet Mauceri voisin est resté intact, vérifié.

**Ce qui marche** : le garde `COMPOSE_PROJECT_NAME` fait son travail — `_fse-bootstrap` → `fse-bootstrap`, images construites, aucune séquence `-_`. `stop.ps1` arrête le bon projet et ne touche pas le voisin. Le plugin custom est monté et **actif**. Le thème est monté, reconnu (`wp_get_theme()->exists() === true`, `errors()` vide), et `wp_is_block_theme()` rend `yes`.

---

## 1. Le site scaffoldé est blanc — défaut bloquant

`theme-plugin-skeleton.md:7-26` déclare cinq fichiers HTML (`templates/index.html`, `single.html`, `page.html`, `parts/header.html`, `parts/footer.html`) et **n'en spécifie le contenu nulle part**. `02-scaffold-wordpress.md:14` dit seulement « créer l'arborescence thème + plugin décrite » ; la note `theme-plugin-skeleton.md:90` les qualifie de « laissés minimaux ».

**Mesuré**, thème activé, HTTP 200 sur `/` :

- `document.body.className` = `home blog wp-embed-responsive wp-theme-fse-bootstrap` — le thème sert bien la page ;
- `document.body.innerText.trim().length` = **0** ;
- `document.querySelector('.wp-site-blocks')` = **null** ;
- les seuls enfants de `<body>` sont trois `<script>` injectés par le core.

**Contre-épreuve** : 67 octets de markup de bloc dans `templates/index.html` → `.wp-site-blocks` présent, texte rendu. La cause est isolée, c'est bien l'absence de contenu prescrit.

**Le plus lourd est ailleurs** : le *Test* déclaré par l'action, `02-scaffold-wordpress.md:35`, est « `wp core version` retourne une version WordPress ». Il **passe** sur ce site blanc — `7.0.2`. Le circuit de vérification de la skill ne peut pas distinguer un bootstrap réussi d'un site à zéro caractère. C'est le motif du chantier #14, transposé : une sortie verte qui n'atteste rien.

## 2. `tests.port: 8889` est codé en dur — deux projets de la skill ne coexistent pas

`wp-env-json.md:24`. Le port du site est paramétrable (`{{PORT}}`), celui de l'environnement de tests ne l'est pas.

**Mesuré** : `Bind for 0.0.0.0:8889 failed: port is already allocated`, l'occupant étant `code-tests-wordpress-1` — un autre projet wp-env de la même machine. **La cascade est le vrai défaut** : le conteneur `development` était pourtant `Started`, mais l'échec de `tests` fait échouer `wp-env start` en entier, et toute commande ultérieure rend `Environment not initialized. Run wp-env start first.` L'étape 2 de `06-verify` devient inatteignable **pour un port qui ne concerne pas le site**. Contre-épreuve : `8889` → `8892`, seule modification, démarrage complet.

## 3. Le garde `COMPOSE_PROJECT_NAME` ne couvre pas les commandes que la skill prescrit de taper

`06-verify.md:14` et `02-scaffold-wordpress.md:19` donnent `pnpm dlx @wordpress/env run cli wp …` **nu**. Or `compose-project-name-guard.md:69` ne couvre que « tout script Node.js du projet qui invoque Docker Compose en sous-main » — une commande tapée à la main n'est pas un script du projet.

**Mesuré** : les six conteneurs `fse-bootstrap-*` up, et la commande rend `service "cli" is not running`. Seule différence entre l'échec et le succès : `$env:COMPOSE_PROJECT_NAME`. Le garde vit dans `start.ps1`/`stop.ps1` ; il est absent d'exactement les deux endroits où la skill demande de le contourner.

## 4. `WP_DEFAULT_THEME` n'active pas le thème

`wp-env-json.md:28` pose `config.WP_DEFAULT_THEME`. **Mesuré** : `DEF=fse-bootstrap | STYLESHEET=twentytwentyfive`, et `wp theme status fse-bootstrap` → `Status: Inactive`. La constante est correctement posée dans l'installation, elle n'active rien sur un WordPress déjà installé.

Aucune étape de `02-scaffold-wordpress.md` ni de `06-verify.md` ne prescrit `wp theme activate`. Sans elle, le site scaffoldé sert le thème par défaut de WordPress — donc, ironie, un site **non blanc**, ce qui masque le défaut n° 1 tant qu'on ne regarde que le rendu.

## 5. `theme.json` v3 contre `Requires at least: 6.5` — contradiction interne

Même référence, même étape d'écriture : `theme-plugin-skeleton.md:37` déclare `Requires at least: 6.5`, `theme-plugin-skeleton.md:47` déclare `"version": 3`.

La dev-note officielle : *« Updating to version 3 is recommended when your minimum supported WordPress version reaches 6.6. »* (`make.wordpress.org/core/2024/06/19/theme-json-version-3/`). Non reproduit sur le terrain — wp-env sert 7.0.2 ; le constat est documentaire et adossé à sa source.

## 6. Deux placeholders déclarés que l'action ne collecte pas

`theme-plugin-skeleton.md:3` déclare quatre placeholders : `{{THEME_SLUG}}`, `{{THEME_NAME}}`, `{{PLUGIN_SLUG}}`, `{{PLUGIN_NAME}}`. Les *Inputs* de `02-scaffold-wordpress.md:8` n'en collectent que deux — « slug du thème et du plugin custom ». Un agent qui exécute l'étape 2 doit inventer `THEME_NAME` et `PLUGIN_NAME`, ou les dériver sans règle. Même classe de défaut que les pivots orphelins de #14 : un fournisseur déclare plus que ce que le consommateur sait atteindre.

## 7. Le template scaffolde une configuration dépréciée

wp-env l'annonce à chaque démarrage : *« The "env", "testsPort", and "testsEnvironment" options are also deprecated. Use the --config option with a separate config file for test environments instead. »* Le bloc `env` de `wp-env-json.md:16-26` est exactement cette forme. Non daté ici : la version de `@wordpress/env` n'a pas été relevée, elle est résolue par `pnpm dlx` à l'exécution.

---

## Ce que ce constat ne dit pas

- **Les flows Laravel et Symfony n'ont pas été exécutés.** Les défauts 2, 3 et 7 sont spécifiques à WordPress ; le défaut 3 pourrait toucher `03`/`04` par le même mécanisme (commande Docker tapée hors script), non vérifié.
- **`05-wire-deploy` n'a pas été exercé** — il demande des identifiants réels.
- **La confrontation avec la maquette n'apporterait rien.** Le harness `design:harness` rempli est mesuré vert par ailleurs (5 pages, `setPage`/`setViewport` fonctionnels, largeurs 390 / 834 / desktop fluide conformes). Le passer par `measure.py` contre cette implémentation ne ferait que rhabiller le défaut n° 1, déjà mesuré directement et plus proprement.

## Estimation

L'unité coûteuse est le contenu FSE : cinq fichiers de markup de bloc à écrire, plus les entrées `templateParts` correspondantes dans `theme.json`, plus un *Test* d'action qui mesure le rendu et non la version du core. **1 session** pour les défauts 1 et 4 (les deux qui produisent un site inutilisable), **1 session de plus** pour les défauts 2, 3, 5, 6, 7, qui sont des corrections ponctuelles de référence sans dépendance entre elles.
