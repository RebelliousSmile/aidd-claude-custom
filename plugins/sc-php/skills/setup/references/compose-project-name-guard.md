# Garde-fou `COMPOSE_PROJECT_NAME` (générique — WordPress/Laravel/Symfony)

Contenu à écrire dans `scripts/start.ps1` et `scripts/stop.ps1` du projet scaffoldé. Ce garde-fou est partagé par les trois flows de scaffold (`scaffold-wordpress`, `scaffold-laravel`, `scaffold-symfony`) — copier-coller identique, seule la commande lancée en bas du script change (`wp-env start` vs `docker compose up -d`).

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

# {{START_COMMAND}}  — ex: pnpm dlx @wordpress/env start   |   docker compose up -d
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

# {{STOP_COMMAND}}  — ex: pnpm dlx @wordpress/env stop   |   docker compose down
```

## Wiring additionnel

Tout script Node.js du projet qui invoque Docker Compose en sous-main (scripts de déploiement, d'extraction, de lint) doit poser la même variable en tête de fichier, calculée par la même logique (dupliquer la fonction en JS si le script est en `.mjs`, ou lire `$env:COMPOSE_PROJECT_NAME` déjà posé par le shell appelant).
