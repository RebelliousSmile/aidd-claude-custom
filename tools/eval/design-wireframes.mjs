#!/usr/bin/env node
// Portable, dependency-free gate for design:wireframes static/tooling behaviour.
// Rendered proof remains an explicit Playwright/Chromium selftest and is never inferred here.

import { spawnSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const repository = resolve(HERE, '..', '..');
const designRoot = resolve(process.env.DESIGN_WIREFRAMES_ROOT || join(repository, 'plugins', 'design'));
const skillPath = join(designRoot, 'skills', 'wireframes', 'SKILL.md');
const scenariosPath = join(designRoot, 'skills', 'wireframes', 'evals', 'scenarios.json');
const expected = ['scaffold', 'normalize', 'lint', 'promote'];

function fail(message) {
  console.error(`✗ design-wireframes — ${message}`);
  process.exit(1);
}

try {
  const skill = readFileSync(skillPath, 'utf8');
  const scenarios = JSON.parse(readFileSync(scenariosPath, 'utf8'));
  const routed = [...skill.matchAll(/^\|\s*(scaffold|normalize|lint|promote)\s*\|/gm)].map((match) => match[1]);
  if (JSON.stringify(routed) !== JSON.stringify(expected)) fail(`routes attendues ${expected.join(', ')}, reçues ${routed.join(', ')}`);
  for (const action of expected) {
    const number = { scaffold: '01', normalize: '02', lint: '03', promote: '04' }[action];
    if (!existsSync(join(designRoot, 'skills', 'wireframes', 'actions', `${number}-${action}.md`))) fail(`action absente: ${action}`);
    if (!scenarios.some((scenario) => scenario.expect_action === action)) fail(`route sans scénario: ${action}`);
  }
} catch (error) {
  fail(`contrat de routage illisible: ${error.message}`);
}

function resolveBash() {
  if (process.env.WIREFRAMES_SELFTEST_BASH) return process.env.WIREFRAMES_SELFTEST_BASH;
  if (process.platform !== 'win32') return 'bash';
  const git = spawnSync('git', ['--exec-path'], { encoding: 'utf8' });
  const candidates = [];
  if (git.status === 0 && git.stdout.trim()) candidates.push(join(resolve(git.stdout.trim(), '..', '..', '..', '..'), 'bin', 'bash.exe'));
  candidates.push('C:\\Program Files\\Git\\bin\\bash.exe', 'C:\\Program Files (x86)\\Git\\bin\\bash.exe');
  return candidates.find((candidate) => existsSync(candidate)) || 'bash';
}

const bash = resolveBash();
const script = join(designRoot, 'tools', 'wireframes-selftest.sh').replace(/\\/g, '/');
const result = spawnSync(bash, [script], { cwd: designRoot, encoding: 'utf8' });
if (result.error) fail(`bash introuvable (${bash}): ${result.error.message}`);
if (result.stdout) process.stdout.write(result.stdout);
if (result.stderr) process.stderr.write(result.stderr);
console.log(`${result.status === 0 ? '✓' : '✗'} design-wireframes — static/selftest exit ${result.status}; Chromium non revendiqué`);
process.exit(result.status === 0 ? 0 : 1);
