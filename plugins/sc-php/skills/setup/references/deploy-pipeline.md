# Pipeline de déploiement SSH (générique, cible type alwaysdata/Scriptami)

Deux fichiers Node : `scripts/deploy-targets.mjs` (config déclarative des cibles) et `scripts/deploy.mjs` (exécution). Le transfert de fichiers (rsync/SSH) est identique pour les trois frameworks ; seule l'étape base de données est framework-conditionnelle (WordPress a un export/import dédié via wp-cli, Laravel/Symfony n'exportent pas la base par défaut — migrations rejouées côté cible à la place).

## `scripts/deploy-targets.mjs`

```javascript
// Un projet peut avoir plusieurs cibles (ex: "ad" = staging alwaysdata, "prod" = prod réelle).
// Chaque cible est indépendante : pousser vers l'une n'affecte jamais les autres.

export const targets = {
  // ad: {
  //   host: 'ssh-XXXXXXX.alwaysdata.net',
  //   user: 'XXXXXXX',
  //   remotePath: '/home/XXXXXXX/www',
  //   url: 'https://mon-projet.scriptami.com',
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
import { resolveTarget } from './deploy-targets.mjs';

const [, , targetName, ...flags] = process.argv;
const skipDb = flags.includes('--no-db');

if (!targetName) {
  console.error('Usage: node scripts/deploy.mjs <target> [--no-db]');
  process.exit(1);
}

const target = resolveTarget(targetName);

function run(cmd) {
  console.log(`$ ${cmd}`);
  execSync(cmd, { stdio: 'inherit' });
}

// 1. Base de données (WordPress uniquement, et seulement si la cible le déclare et --no-db absent)
if (target.wpExportDb && !skipDb) {
  run('pnpm dlx @wordpress/env run cli wp search-replace "http://localhost" "' + target.url + '" --export=./dump.sql');
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
