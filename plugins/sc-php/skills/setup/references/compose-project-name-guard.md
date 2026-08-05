# Garde-fou `COMPOSE_PROJECT_NAME` (générique — WordPress/Laravel/Symfony)

Contenu à écrire dans `scripts/start.ps1` et `scripts/stop.ps1` du projet scaffoldé. Ce garde-fou est partagé par les trois flows de scaffold (`scaffold-wordpress`, `scaffold-laravel`, `scaffold-symfony`) — copier-coller identique, seule la commande lancée en bas du script change (`wp-env start` vs `docker compose up -d`).

**Deux choses sont dérivées, pas une.** Le nom de projet vient du dossier ; le **répertoire d'exécution** doit l'être aussi. wp-env comme Docker Compose résolvent le projet depuis le répertoire **courant**, jamais depuis l'emplacement du script : un script lancé par son chemin absolu depuis ailleurs pose le bon `COMPOSE_PROJECT_NAME` et cible quand même le vide. **Mesuré** : `& <racine>/scripts/stop.ps1` depuis un dossier tiers rend `Environment not initialized. Run wp-env start first.` avec les trois conteneurs up ; la même ligne depuis la racine du projet rend `Stopped WordPress.` — seule différence, le répertoire courant. Variante Compose, mesurée : `docker compose down` hors racine rend `no configuration file provided: not found`, exit 1. D'où le `Push-Location $ProjectRoot` de chacun des trois scripts, et le `finally` qui rend la main au répertoire de l'appelant (les scripts sont aussi lancés avec `&` depuis une session ouverte, pas seulement par `powershell -File`).

## `scripts/start.ps1`

```powershell
# Dérive un nom de projet Docker Compose valide et déterministe à partir du dossier courant.
# Docker Compose interdit certaines séquences (ex: "-_") dans un nom de projet — voir
# references/pitfalls.md #1. Ne jamais laisser Docker Compose deviner le nom seul.

function Get-SafeComposeProjectName {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ProjectRoot
    )

    # Nom du dossier projet uniquement (pas le chemin complet) => déterministe.
    $folderName = Split-Path -Leaf $ProjectRoot

    # Minuscules, puis tout caractère hors [a-z0-9-] (y compris "_") devient "-".
    # Un underscore adjacent à un tiret ("-_") devient donc "--", jamais la
    # séquence interdite d'origine — cf. references/pitfalls.md #1.
    $safeName = $folderName.ToLower() -replace '[^a-z0-9-]', '-'

    # Collapse les tirets consécutifs et retire les tirets de bord.
    $safeName = $safeName -replace '-{2,}', '-' -replace '^-+|-+$', ''

    return $safeName

    # Choix assumé : pas de hash anti-collision (peu de projets en parallèle).
    # Deux dossiers proches après assainissement (ex: "mon-projet" et
    # "mon_projet") produiront le même nom — accepté, pas un bug.
}

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$env:COMPOSE_PROJECT_NAME = Get-SafeComposeProjectName -ProjectRoot $ProjectRoot

Write-Host "COMPOSE_PROJECT_NAME=$env:COMPOSE_PROJECT_NAME"

# wp-env et docker compose résolvent le projet depuis le RÉPERTOIRE COURANT, pas depuis
# l'emplacement du script. Sans ce Push-Location, un lancement par chemin absolu depuis
# un autre dossier cible le vide, garde correctement posé. Le finally rend la main au
# répertoire de l'appelant, qui n'est pas toujours un processus jetable.
Push-Location $ProjectRoot
try {
    # {{START_COMMAND}}  — ex: pnpm dlx @wordpress/env start   |   docker compose up -d
}
finally {
    Pop-Location
}

exit $LASTEXITCODE
```

## `scripts/stop.ps1`

```powershell
function Get-SafeComposeProjectName {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ProjectRoot
    )

    # IDENTIQUE à la fonction dans start.ps1 — copier-coller exact,
    # sinon stop.ps1 cible un projet Docker Compose différent de celui démarré.
    $folderName = Split-Path -Leaf $ProjectRoot
    $safeName = $folderName.ToLower() -replace '[^a-z0-9-]', '-'
    $safeName = $safeName -replace '-{2,}', '-' -replace '^-+|-+$', ''
    return $safeName
}

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$env:COMPOSE_PROJECT_NAME = Get-SafeComposeProjectName -ProjectRoot $ProjectRoot

# IDENTIQUE à start.ps1 : le répertoire courant fait partie du garde. C'est ici que le
# manque coûte le plus — un arrêt qui échoue laisse les conteneurs et les volumes en place
# alors que le script a rendu la main. Mesuré : hors racine, `Environment not initialized`.
Push-Location $ProjectRoot
try {
    # {{STOP_COMMAND}}  — ex: pnpm dlx @wordpress/env stop   |   docker compose down
}
finally {
    Pop-Location
}

exit $LASTEXITCODE
```

## `scripts/wp.ps1` — le garde pour les commandes tapées à la main (WordPress)

`start.ps1` et `stop.ps1` ne couvrent que ce qu'ils lancent eux-mêmes. Toute commande wp-cli tapée directement — `pnpm dlx @wordpress/env run cli wp …` — s'exécute sans le garde et cible un projet Docker Compose qui n'existe pas. **Mesuré** : les six conteneurs up, et la commande rend `service "cli" is not running`. Seule différence entre l'échec et le succès : `$env:COMPOSE_PROJECT_NAME`.

```powershell
function Get-SafeComposeProjectName {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ProjectRoot
    )

    # IDENTIQUE aux fonctions de start.ps1 / stop.ps1.
    $folderName = Split-Path -Leaf $ProjectRoot
    $safeName = $folderName.ToLower() -replace '[^a-z0-9-]', '-'
    $safeName = $safeName -replace '-{2,}', '-' -replace '^-+|-+$', ''
    return $safeName
}

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$env:COMPOSE_PROJECT_NAME = Get-SafeComposeProjectName -ProjectRoot $ProjectRoot

# IDENTIQUE à start.ps1 / stop.ps1 : `pnpm wp` est tapé depuis n'importe où, c'est le cas
# nominal ici, pas l'exception.
Push-Location $ProjectRoot
try {
    pnpm dlx @wordpress/env run cli wp @args
}
finally {
    Pop-Location
}

exit $LASTEXITCODE
```

Câblé en `"wp": "powershell -File scripts/wp.ps1"` dans `package.json`, il donne `pnpm wp <commande>` — la seule forme que la skill prescrit. Un garde qui vit dans les scripts mais est absent des commandes documentées ne protège personne.

## Wiring additionnel

Tout script Node.js du projet qui invoque Docker Compose en sous-main (scripts de déploiement, d'extraction, de lint) doit poser la même variable en tête de fichier, calculée par la même logique (dupliquer la fonction en JS si le script est en `.mjs`, ou lire `$env:COMPOSE_PROJECT_NAME` déjà posé par le shell appelant) **et passer `cwd` = racine du projet à chaque `spawn`/`exec`** — poser la variable sans fixer le répertoire reproduit exactement le défaut corrigé dans les trois `.ps1`.
