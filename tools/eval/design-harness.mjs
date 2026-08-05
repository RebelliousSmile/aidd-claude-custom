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
import { existsSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));

// Sous Windows, `bash` du PATH est celui de WSL (`C:\Windows\system32\bash.exe`) : il ne
// voit pas `C:/…` et ne partage ni le Python ni les chemins de l'hôte. Le selftest tourne
// sur des chemins Windows, donc il lui faut le bash de Git for Windows. On le résout
// explicitement plutôt que de dépendre du shell appelant — sinon la preuve passe depuis
// Git Bash et échoue depuis PowerShell, ce qui n'est pas une preuve.
function resolveBash() {
  if (process.env.HARNESS_SELFTEST_BASH) return process.env.HARNESS_SELFTEST_BASH;
  if (process.platform !== 'win32') return 'bash';
  const git = spawnSync('git', ['--exec-path'], { encoding: 'utf8' });
  const candidates = [];
  if (git.status === 0 && git.stdout.trim()) {
    // …/Git/mingw64/libexec/git-core → …/Git/bin/bash.exe
    candidates.push(join(resolve(git.stdout.trim(), '..', '..', '..', '..'), 'bin', 'bash.exe'));
  }
  candidates.push('C:\\Program Files\\Git\\bin\\bash.exe', 'C:\\Program Files (x86)\\Git\\bin\\bash.exe');
  return candidates.find((p) => existsSync(p)) || 'bash';
}
// Séparateurs POSIX : bash traite `\` comme échappement dans un argument, donc un chemin
// Windows natif lui arrive amputé de ses séparateurs (`C:UsersfxguiDocuments…`). `C:/…`
// est accepté tel quel par bash sous Windows, et `/` est déjà le séparateur ailleurs.
const script = join(HERE, '..', '..', 'plugins', 'design', 'tools', 'harness-selftest.sh').replace(/\\/g, '/');
const cwd = join(HERE, '..', '..', 'plugins', 'design');

const bash = resolveBash();
const r = spawnSync(bash, [script], { encoding: 'utf8', cwd });

if (r.error) {
  console.error(`✗ design-harness — bash introuvable (${bash}) : ${r.error.message}`);
  console.error('  Le selftest ne peut pas tourner. Ce n\'est pas un skip : installez bash (Git Bash, WSL).');
  process.exit(1);
}

if (r.stdout) process.stdout.write(r.stdout);
if (r.stderr) process.stderr.write(r.stderr);

console.log(`${r.status === 0 ? '✓' : '✗'} design-harness — harness-selftest.sh exit ${r.status}`);
process.exit(r.status === 0 ? 0 : 1);
