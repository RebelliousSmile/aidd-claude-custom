#!/usr/bin/env node
// Deterministic pre-flight for the design behavioural suites.
// The markdown suites remain the durable judge specs; this guard rejects missing structure,
// lost skill coverage, and the machine-verifiable P0/P1/P2 boundary before a judge run.

import { existsSync, readFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';

const skills = ['detail', 'define', 'destructure', 'adjust', 'enforce', 'diffuse', 'harness'];
const failures = [];
const fail = (message) => failures.push(message);

for (const skill of skills) {
  const base = `plugins/design/skills/${skill}`;
  const suitePath = `${base}/evals/routing-autonomy-scenarios.md`;
  if (!existsSync(suitePath)) { fail(`${skill}: suite routing-autonomy absente`); continue; }
  const suite = readFileSync(suitePath, 'utf8');
  const spec = readFileSync(`${base}/SKILL.md`, 'utf8');
  const rows = suite.match(/^\| S\d+ \|/gm) ?? [];

  for (const heading of ['## Scenarios', '## How to run', '## Results log'])
    if (!suite.includes(heading)) fail(`${skill}: section absente ${heading}`);
  if (!suite.includes('Fixture / preconditions')) fail(`${skill}: fixture non nommée`);
  if (rows.length < 4) fail(`${skill}: ${rows.length} scénarios, minimum 4`);
  if (!suite.includes('Authority:') || !suite.includes('§'))
    fail(`${skill}: autorité fichier + section absente`);
  if (!/### 2026-08-12 — run \d+ \((initial|post-fix|regression|generality), dry-run,/.test(suite))
    fail(`${skill}: run Behave structuré absent`);
  if (!suite.includes('Do not activate') && !suite.includes('Do not activate this skill'))
    fail(`${skill}: aucun NO-GO de déclenchement`);
  if (!/\| Action \| Does \|/.test(spec)) fail(`${skill}: table d'actions Codex absente`);
  if (!spec.includes('## Routing')) fail(`${skill}: routage explicite absent`);
}

const runGate = (config) => spawnSync('python3', [
  'plugins/design/tools/run-gates.py', '--config',
  `plugins/design/skills/enforce/fixtures/${config}`,
], { encoding: 'utf8' });

const clean = runGate('gates.clean.config.json');
if (clean.status !== 0 || !clean.stdout.includes('WARNING P2'))
  fail('P2: le workflow manquant doit avertir sans bloquer');

const dirty = runGate('gates.dirty.config.json');
if (dirty.status !== 1 || !dirty.stdout.includes('VIOLATION'))
  fail('P1: une violation contractuelle doit bloquer');

const missing = runGate('gates.missing-evidence.config.json');
if (missing.status !== 1 || !missing.stdout.includes('MISSING EVIDENCE'))
  fail('P0/P1: une preuve requise absente doit bloquer');

const maturity = runGate('gates.below-threshold.config.json');
if (maturity.status !== 4)
  fail('maturité: le code public 4 doit rester stable');

const readme = readFileSync('README.md', 'utf8');
for (const plugin of ['aidd-context', 'aidd-dev', 'aidd-refine'])
  if (!readme.includes(`codex plugin add ${plugin}@aidd-framework`))
    fail(`prérequis Codex absent du README: ${plugin}`);
if (!readme.includes('codex plugin add design@my-marketplace'))
  fail('installation Codex du plugin design absente du README');

if (failures.length) {
  for (const failure of failures) console.error(`✗ design-behave — ${failure}`);
  process.exit(1);
}

console.log(`✓ design-behave — ${skills.length}/7 suites structurées, autonomie + P0/P1/P2 vérifiées`);
