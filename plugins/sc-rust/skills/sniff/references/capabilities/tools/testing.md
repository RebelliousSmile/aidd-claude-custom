---
---

# Testing — pivot de gouvernance (cargo test)

Contenu factuel structuré — inventaire de l'outillage de test et des signaux que la stack rend lisibles — et non des patterns de revue de code, contrairement aux autres fichiers de ce dossier. C'est aussi pourquoi il ne porte pas de `paths:` : il ne s'applique pas à une famille de fichiers, il décrit une suite. Ce que ce fichier fournit est décrit ici ; qui le lit ne l'est pas. Applicable dès qu'un `Cargo.toml` est présent — la stack n'a qu'un seul harnais de test et il est fourni par la toolchain, il n'y a donc pas de dépendance de test à détecter.

**Titres de sections** — repris verbatim des noms de champs du contrat, en anglais. Aucune table de correspondance n'est due : rien ne diverge.

**Terrain de mesure** — `winfxstart` : crate binaire natif Win32 (`tao` 0.26, `windows` 0.52, `image` 0.25), 17 fichiers `src/**/*.rs`, 122 tests, toolchain `cargo 1.93.0` / `rustc 1.93.0`, lecture seule. Ce que ce terrain n'a pas — répertoire `tests/`, doctests, outil de couverture, `[dev-dependencies]`, code asynchrone — est signalé comme **non vérifié** là où il apparaît. Un crate applicatif diffère d'une bibliothèque publiée sur au moins deux de ces points.

## Test runner(s)

- **Unit / contrat** : `cargo test`. Une seule commande couvre trois populations que le contrat distingue ailleurs — tests unitaires intra-source, tests d'intégration de `tests/`, doctests — et les isoler demande un sélecteur : `--lib`, `--bins`, `--tests` (intégration seulement), `--doc` (doctests seulement).
- **Toute mesure exige une compilation complète** en profil `test`. Mesuré : 52 s à froid sur le terrain, pour 17 fichiers et une vingtaine de dépendances transitives. Il n'existe aucune inspection statique équivalente côté cargo — voir *Test-count command* pour ce que coûte de s'en passer.
- **`cargo nextest run`** — runner tiers, un processus par test, sortie machine-lisible. Prérequis non fourni par la toolchain (`cargo nextest --version` ; constaté absent sur le terrain).
- **E2E** : aucune commande standard. Rust n'a pas d'équivalent de `playwright test` — voir *Canonical E2E tool*.

## Test file glob

- `src/**/*.rs` — **les tests unitaires vivent dans le fichier source lui-même**, sous `#[cfg(test)] mod tests`.
- `tests/**/*.rs` — tests d'intégration, un binaire compilé par fichier. *Absent du terrain mesuré.*
- Doctests — dans les blocs ` ``` ` des commentaires `///`. Compilés et exécutés par `cargo test`, invisibles à tout glob de fichiers. *Absents du terrain mesuré.*

**Cette population n'est pas disjointe de `Source glob & exclusions`, et le cas courant est le recouvrement total.** Mesuré : 122 fonctions `#[test]`, réparties sur **12 des 17** fichiers source, **zéro fichier de test dédié**. Un glob de fichiers de test au sens JS ou Python rend ici *0 test et 17 fichiers de production non testés*, sur un crate qui en porte 122.

**L'unité réelle de séparation est le module annoté `#[cfg(test)]`, pas le fichier.** Deux conséquences mesurées :

- **L'attribut n'annote pas que des modules de tests.** Sur le terrain, 14 occurrences de `#[cfg(test)]` pour 12 modules de tests : les deux autres annotent des *helpers* compilés seulement en test — une fonction (`icons/decode.rs:104`) et un module utilitaire (`icons/resolve.rs:233`, un `TempDir` maison). Compter les attributs surcompte les suites.
- **Un fichier peut porter plusieurs blocs** ; deux fichiers du terrain en portent deux chacun.

## Test-count command

```
cargo test -- --list | grep -c ': test$'
```

Mesuré : **122**, cohérent avec le pied de sortie `122 tests, 0 benchmarks`. Le `grep` filtre le suffixe `: test`, la liste mêlant tests et benchmarks (`: benchmark`) que le pied compte séparément — un crate à benchmarks rendrait deux nombres là où un seul est attendu.

- **Exige la compilation préalable** (voir *Test runner(s)*). Il n'existe pas de comptage instantané.
- **Approximation sans compilation** : `grep -rc '#\[test\]' src`. A rendu 122 sur le terrain, soit la valeur exacte — coïncidence à ne pas généraliser : elle **sous-compte** les tests générés par macro (`rstest`, `test_case`, `proptest`) et **tous** les doctests, et **surcompte** ce qui est derrière un `cfg` inactif. Utilisable comme ordre de grandeur, jamais comme décompte.
- `--list` **inclut les tests `#[ignore]`**, qui ne s'exécutent pas. *Non vérifié : le terrain n'en porte aucun.*
- Avec nextest : `cargo nextest list` (prérequis, voir *Test runner(s)*).

## Coverage command

**Prérequis — c'est le point où cette stack diffère le plus.** `cargo test` ne produit **aucun** rapport de couverture, et la toolchain n'embarque aucun outil pour en produire : la couverture passe entièrement par un binaire tiers installé séparément. Constat avant lancement :

```
cargo llvm-cov --version     # error: no such command: `llvm-cov`  → absent
cargo tarpaulin --version
```

Constaté absent des deux sur le terrain, ainsi que de `cargo-nextest`. Une commande qui échoue sur `no such command` signale une machine sans outil, **jamais** un défaut du projet mesuré : le champ est absent pour ce run, et son repli s'applique (`pivot-contract.md` › *Prerequisites*).

**Commandes, une fois le prérequis satisfait** — *aucune n'a pu être exécutée ici, les deux outils étant absents ; elles sont documentaires et à revérifier au premier terrain outillé.*

- `cargo llvm-cov --json --output-path <chemin>` — instrumentation LLVM, par région ; `--branch` requiert une toolchain nightly selon les versions.
- `cargo tarpaulin --out Xml --output-dir <répertoire>` — Linux/x86_64 principalement.

**Le repli documenté du champ ne fonctionne pas sur cette stack.** Le contrat replie sur un mapping statique module source → fichier de test ; ici chaque module porte ses propres tests, donc chaque module se référencerait lui-même. Le mapping ne discrimine rien et ne doit pas être rendu comme un classement grossier — il n'est pas grossier, il est vide de sens. Ce qui reste mesurable sans couverture : la présence ou l'absence d'un `#[cfg(test)] mod tests` par fichier source (5 des 17 fichiers du terrain n'en portent aucun), qui est un signal de population, pas de couverture.

## Source glob & exclusions

Code de production classable :

- `src/**/*.rs`, `build.rs`, et pour un workspace `<member>/src/**/*.rs` — les membres se lisent dans `[workspace] members`, jamais dans l'arborescence, qui peut porter des répertoires hors workspace.

Jamais classable :

- `target/` — artefacts de build, y compris des sources générées. Ce répertoire est en principe ignoré par git (vérifié sur le terrain), mais **cargo y écrit sans le demander** : voir *Known tooling gotchas*.
- Code généré inclus par `include!(concat!(env!("OUT_DIR"), "…"))` — produit par `build.rs` à la compilation, absent du dépôt.
- `tests/`, `benches/`, `examples/` — ce ne sont pas des cibles de production.
- **Les modules `#[cfg(test)]` internes aux fichiers de `src/`** — c'est du code de test dans un fichier que ce glob prend. Une mesure de volume de production qui compte ces lignes compte ses propres tests ; sur le terrain, plusieurs de ces modules dépassent la moitié du fichier.

## Risk signals

Structurellement à conséquence, propre à la stack :

- **`unsafe`** — tout bloc, et plus encore `unsafe impl Send` / `unsafe impl Sync`, qui déplacent une garantie du compilateur vers une affirmation humaine. Détection : `grep -rn 'unsafe' src`.
- **FFI et appels système** — `extern "C"`, `windows`/`winapi`, `libc`, `nix`. La frontière du langage est aussi celle de ses garanties.
- **`unwrap()` / `expect()` / `panic!` / indexation directe en chemin de production** — dans un binaire, un panic est un arrêt ; les mêmes appels dans un `#[cfg(test)] mod tests` sont l'idiome normal et ne sont pas un signal. Le compte brut sans distinction du contexte est trompeur : sur le terrain, la majorité des `unwrap()` sont dans les modules de test.
- **Persistance et suppression** — `std::fs::remove_*`, écriture de fichiers de configuration, migrations SQLx/Diesel.
- **Registre, processus, privilèges** — `Win32_System_Registry`, `Command::new`, élévation. Mesuré sur le terrain : 6 usages de registre, 3 lancements de processus, 28 opérations de système de fichiers.

Structurellement sans conséquence : `impl Display`/`Debug`, `#[derive]`, conversions `From`/`Into` triviales, ré-exports de `mod.rs`, glue générée par macro.

**Frontières externes, lues dans `Cargo.toml`** — `reqwest`, `hyper`, `tonic` (clients sortants) ; `sqlx`, `diesel`, `redis`, `mongodb` (persistance externe) ; `aws-sdk-*`, `stripe`, `sentry`, `opentelemetry` (SaaS) ; `windows`, `winapi`, `libc`, `nix` (frontière système d'exploitation — c'est une frontière externe au même titre, souvent oubliée parce qu'elle n'a pas d'URL). Les dépendances sont déclarées dans `[dependencies]`, les dépendances de test dans `[dev-dependencies]`, et une frontière n'apparaissant que dans la seconde n'est pas une frontière du produit.

**Un `Cargo.toml` sans `[dev-dependencies]` ne signale pas un crate sans tests.** Mesuré : le terrain n'a pas la section du tout, et porte 122 tests — la bibliothèque standard suffit à en écrire.

## Anchor boundary

Positionne la frontière dans les termes de cette stack. **Ne dit jamais quelle preuve un cas mérite** — cela se décide ailleurs, et rien ici ne le modifie.

**Ancre** — franchit la frontière publique réelle du produit :

- **Invoquer le binaire compilé** comme le ferait un utilisateur : `target/<profil>/<nom>` avec ses arguments, son environnement, son code de sortie. C'est l'équivalent Rust le plus proche d'un parcours réel.
- **Un appel réel sur un socket ouvert** par le service lancé en processus séparé.
- **L'API publique d'une bibliothèque consommée depuis l'extérieur du crate** — c'est-à-dire depuis `tests/`, qui compile un binaire distinct et ne voit que ce qui est `pub`. La différence avec un test intra-source n'est pas de style : un `#[cfg(test)] mod tests` accède au privé via `use super::*`, un test d'intégration ne le peut pas.
- Le **vrai registre**, le **vrai système de fichiers**, un **vrai processus lancé**, quand ils sont la frontière que le produit expose.

**N'ancre pas, malgré l'apparence** :

- **`#[cfg(test)] mod tests`, quelle que soit la lourdeur du test.** Il est compilé *dans* le crate testé, voit ses internes, et ne franchit rien. C'est le piège dominant de la stack : les tests les plus complets d'un crate Rust sont ordinairement ceux qui ancrent le moins.
- **`#[tokio::test]`** — monte un runtime asynchrone dédié au test, dans le processus de test. Un runtime n'est pas une frontière. *Non vérifié sur le terrain : aucun code asynchrone.*
- **Un serveur monté in-process** (`axum::Router` appelé via `tower::ServiceExt::oneshot`, `actix_web::test::init_service`) — le routeur est exercé sans qu'aucun socket ne s'ouvre.
- **Un `TempDir`** — écrire dans un vrai répertoire temporaire est un effet de bord réel, pas une frontière produit. Mesuré : les tests du terrain écrivent bel et bien dans le système de fichiers réel via `std::env::temp_dir()`, sans crate tierce. **Réel et ancré ne sont pas synonymes** : ce qui compte est de franchir la frontière que le produit expose, pas de toucher du matériel.
- **Un doctest** — compilé comme un crate consommateur, ce qui le rapproche du test d'intégration, mais exécuté par le harnais de `cargo test` sans que rien du produit ne soit lancé.

## Known tooling gotchas

- **`cargo test` écrit `target/` dans le dépôt mesuré.** *Détection* : la compilation crée `<racine du crate>/target/`, plusieurs centaines de Mo, quel que soit le sous-commande. *Fix* : `CARGO_TARGET_DIR=<chemin hors dépôt>` — appliqué pour toutes les mesures de ce pivot, l'arbre du terrain étant resté strictement propre (`git status --porcelain` vide avant et après). Le fait que `/target/` soit dans `.gitignore` ne rend pas l'écriture inoffensive sur un dépôt à ne pas modifier.
- **Aucun décompte sans compilation complète.** *Détection* : `cargo test -- --list` compile avant de lister (52 s à froid, mesuré). *Fix* : aucun côté cargo ; budgéter la compilation, ou assumer l'approximation par `grep` et la déclarer comme telle (voir *Test-count command*).
- **`cargo test` capture `stdout`** des tests qui passent. *Détection* : aucun `println!` dans la sortie d'un run vert. *Fix* : `cargo test -- --nocapture`.
- **Les tests s'exécutent en parallèle par défaut**, un thread par test dans un même processus. *Détection* : échecs intermittents sur des tests partageant un chemin fixe, une variable d'environnement ou un état global. *Fix* : `cargo test -- --test-threads=1` pour confirmer la cause ; la correction est d'isoler l'état, pas de figer le parallélisme. *Non observé sur le terrain — les 122 tests passent en parallèle.*
- **Compter les `#[cfg(test)]` surcompte les suites de tests.** *Détection* : l'attribut annote aussi des fonctions et modules utilitaires compilés seulement en test (mesuré : 14 attributs, 12 modules de tests). *Fix* : compter les `mod tests` ou, mieux, `cargo test -- --list`.
- **`cargo test --all-features` et `cargo test` ne testent pas la même chose.** *Détection* : `[features]` non vide dans `Cargo.toml`, et du code sous `#[cfg(feature = "…")]`. Un test derrière une feature désactivée n'est ni exécuté ni signalé. *Fix* : nommer explicitement le jeu de features mesuré. *Non vérifié : le terrain n'a pas de section `[features]`.*

## Domain resolution

**Comment retrouver ici un domaine déjà nommé, jamais lesquels existent.** Ce champ complète une résolution ; il ne prime jamais sur ce qui est énoncé à propos du code du projet.

### Par les répertoires et modules

- **Le module est l'unité de découpe** — `src/<domaine>/mod.rs` avec ses fichiers frères, ou `src/<domaine>.rs`. Les deux formes coexistent ; la seconde est la forme moderne, la première reste très répandue.
- **`[workspace] members` est plus fiable que l'arborescence** sur un workspace : il énumère les crates réellement construites et exclut d'office les répertoires morts. Le champ `[package] name` d'un membre peut différer du nom de son dossier, et c'est le `name` qui circule dans les chemins d'import.
- **`[[bin]]` / `[lib]`** — plusieurs binaires dans un même crate signalent ordinairement plusieurs points d'entrée d'un même domaine, pas plusieurs domaines.

### La couche ne porte pas le domaine

`ui/`, `windows/`, `platform/`, `sys/`, `api/`, `handlers/`, `models/`, `schema.rs`, `error.rs` sont des couches ou des adaptateurs, à l'intérieur ou en travers des domaines. Mesuré sur le terrain : `src/` porte `icons`, `storage`, `ui`, `windows` — les deux premiers sont des domaines, les deux suivants une couche de présentation et un adaptateur système. Un arbre dont le premier niveau est entièrement fait de couches n'expose aucun domaine, qui se lit alors dans les identifiants.

### Par les identifiants

- Préfixes et suffixes de types (`IconResolver`, `StorageError`, `CategoryStore`), chemins d'import (`crate::<domaine>::…`), et les variantes d'un enum d'erreur central, qui énumèrent souvent les domaines plus fidèlement que l'arborescence.

## Canonical E2E tool

**Aucun.** Rust n'a pas d'outil E2E standard, et l'écosystème n'en désigne pas un — c'est une différence de nature avec les stacks qui en ont un. Selon la forme du produit :

- **Binaire CLI** — `assert_cmd` + `predicates`, qui lancent l'exécutable compilé et vérifient sortie et code de retour.
- **Service HTTP** — le binaire lancé en processus séparé, interrogé par `reqwest` depuis un test d'intégration.
- **Application graphique** — pilotage par l'outillage d'accessibilité du système hôte, hors écosystème Rust.

Informationnel : rien ne lit ce champ comme une licence à proposer un remplacement. *Aucune de ces trois formes n'a été vérifiée sur le terrain, qui ne porte aucun harnais E2E.*
