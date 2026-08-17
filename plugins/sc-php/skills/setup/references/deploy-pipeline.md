# Pipeline de déploiement SSH (générique, cible type hébergement mutualisé)

Deux fichiers Node : `scripts/deploy-targets.mjs` (config déclarative des cibles) et `scripts/deploy.mjs` (exécution). Le transfert de fichiers (rsync/SSH) est identique pour les trois frameworks ; seule l'étape base de données est framework-conditionnelle (WordPress a un export/import dédié via wp-cli, Laravel/Symfony n'exportent pas la base par défaut — migrations rejouées côté cible à la place).

## `scripts/deploy-targets.mjs`

```javascript
// Un projet peut avoir plusieurs cibles (ex: "staging", "prod" = prod réelle).
// Chaque cible est indépendante : pousser vers l'une n'affecte jamais les autres.

export const targets = {
  // staging: {
  //   host: 'ssh-XXXXXXX.hebergeur.tld',
  //   user: 'XXXXXXX',
  //   remotePath: '/home/XXXXXXX/www',
  //   url: 'https://staging.mon-projet.tld',
  //   // Optionnel — uniquement pertinent pour le flow WordPress :
  //   wpExportDb: true,
  // },
};

export function resolveTarget(name) {
  const target = targets[name];
  if (!target) {
    const available = Object.keys(targets).join(', ') || '(aucune cible configurée)';
    throw new Error(`Cible de déploiement inconnue: "${name}". Cibles disponibles: ${available}`);
  }
  return target;
}
```

## `scripts/deploy.mjs`

```javascript
#!/usr/bin/env node
import { execSync } from 'node:child_process';
import path from 'node:path';
import { resolveTarget } from './deploy-targets.mjs';

// Garde COMPOSE_PROJECT_NAME — MÊME logique que scripts/start.ps1 (cf. compose-project-name-guard.md).
// Sans lui, l'appel wp-env ci-dessous cible un projet Docker Compose inexistant
// et rend `service "cli" is not running` alors que les conteneurs tournent.
const projectRoot = path.resolve(import.meta.dirname, '..');
process.env.COMPOSE_PROJECT_NAME = path
  .basename(projectRoot)
  .toLowerCase()
  .replace(/[^a-z0-9-]/g, '-')
  .replace(/-{2,}/g, '-')
  .replace(/^-+|-+$/g, '');

const [, , targetName, ...flags] = process.argv;
const skipDb = flags.includes('--no-db');

if (!targetName) {
  console.error('Usage: node scripts/deploy.mjs <target> [--no-db]');
  process.exit(1);
}

const target = resolveTarget(targetName);

function run(cmd) {
  console.log(`$ ${cmd}`);
  // cwd explicite : wp-env et docker compose résolvent le projet depuis le répertoire
  // courant, et les chemins relatifs ci-dessous (./dump.sql) en dépendent aussi. Poser
  // COMPOSE_PROJECT_NAME sans fixer le cwd laisse `node scripts/deploy.mjs` lancé
  // d'ailleurs échouer sur un projet vide, garde correctement posé.
  execSync(cmd, { stdio: 'inherit', cwd: projectRoot });
}

// 1. Base de données (WordPress uniquement, et seulement si la cible le déclare et --no-db absent)
if (target.wpExportDb && !skipDb) {
  run('pnpm wp search-replace "http://localhost" "' + target.url + '" --export=./dump.sql');
  run(`scp ./dump.sql ${target.user}@${target.host}:${target.remotePath}/dump.sql`);
  // L'import côté cible reste une étape manuelle documentée dans le README du projet —
  // ne jamais lancer une commande destructive (import qui écrase la prod) sans confirmation explicite.
}

// 2. Fichiers applicatifs (thème+plugin pour WordPress, ou dossier applicatif pour Laravel/Symfony)
run(
  `rsync -avz --delete ` +
  `--exclude .git --exclude node_modules --exclude .env ` +
  `./ ${target.user}@${target.host}:${target.remotePath}/`
);

console.log(`Déploiement vers "${targetName}" terminé.`);
```

## Notes

- `--no-db` doit toujours être supporté et documenté — un déploiement de code seul (sans toucher à la base distante) est le cas d'usage le plus fréquent une fois le projet en cours de vie.
- L'import du dump WordPress côté serveur distant n'est jamais automatisé par ce script : une commande qui écraserait une base de production doit rester un geste manuel et volontaire.
- `deploy-targets.mjs` ne doit jamais contenir de secrets en clair (mot de passe SSH, clé privée) — authentification par clé SSH uniquement, gérée par l'agent SSH de la machine, pas par ce fichier.
