#!/usr/bin/env node
// Rejoue le selftest du générateur design:harness — l'espace de codes 0/2/3 (jamais 1)
// sur le chemin contrat comme sur le chemin pages, et la forme du HTML produit.
//
// ⚠ Homonymie : `tools/eval/harness.mjs` est le harnais d'évaluation du marketplace et
// n'a AUCUN rapport avec le générateur de maquette de design:harness. D'où ce nom.
//
// Une preuve écrite une fois et jamais rejouée n'est pas une preuve : bash introuvable
// est un ÉCHEC, jamais un skip silencieux — c'est exactement le défaut corrigé ici.
//
//   node tools/eval/design-harness.mjs   → exit 0 si le selftest rend 0

import { spawnSync } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const script = join(HERE, '..', '..', 'plugins', 'design', 'tools', 'harness-selftest.sh');

const r = spawnSync('bash', [script], { encoding: 'utf8', cwd: join(HERE, '..', '..', 'plugins', 'design') });

if (r.error) {
  console.error(`✗ design-harness — bash introuvable : ${r.error.message}`);
  console.error('  Le selftest ne peut pas tourner. Ce n\'est pas un skip : installez bash (Git Bash, WSL).');
  process.exit(1);
}

if (r.stdout) process.stdout.write(r.stdout);
if (r.stderr) process.stderr.write(r.stderr);

console.log(`${r.status === 0 ? '✓' : '✗'} design-harness — harness-selftest.sh exit ${r.status}`);
process.exit(r.status === 0 ? 0 : 1);
