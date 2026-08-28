#!/usr/bin/env node
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { validateProjectContract } from '../sc-cd/validate-project-contract.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const plugins = ['sc-css', 'sc-js', 'sc-php', 'sc-python', 'sc-rust', 'sc-tiers'];
const canonical = readFileSync(join(root, 'tools/sc-cd/contract.md'), 'utf8');
const schema = readFileSync(join(root, 'tools/sc-cd/project-contract.schema.json'), 'utf8');
const failures = [];

for (const plugin of plugins) {
  const target = join(root, 'plugins', plugin, 'references/cd-contract.md');
  if (!existsSync(target)) failures.push(`${plugin}: missing cd-contract.md`);
  else if (readFileSync(target, 'utf8') !== canonical) failures.push(`${plugin}: cd-contract.md drifted`);
  const schemaTarget = join(root, 'plugins', plugin, 'references/cd-project-contract.schema.json');
  if (!existsSync(schemaTarget)) failures.push(`${plugin}: missing cd-project-contract.schema.json`);
  else if (readFileSync(schemaTarget, 'utf8') !== schema) failures.push(`${plugin}: project contract schema drifted`);

  const skillRoot = join(root, 'plugins', plugin, 'skills/cd');
  const skill = join(skillRoot, 'SKILL.md');
  if (!existsSync(skill)) failures.push(`${plugin}: missing cd skill`);
  else {
    const router = readFileSync(skill, 'utf8');
    for (const [index, action] of ['local', 'server', 'automata'].entries()) {
      const actionPath = join(skillRoot, 'actions', `0${index + 1}-${action}.md`);
      if (!existsSync(actionPath)) failures.push(`${plugin}: missing ${action} action`);
      const routedAction = new RegExp(`^\\|\\s*${action}\\s*\\|`, 'm');
      if (!routedAction.test(router)) failures.push(`${plugin}: ${action} is not routed`);
    }
  }
  const scenariosPath = join(skillRoot, 'evals/scenarios.json');
  if (!existsSync(scenariosPath)) failures.push(`${plugin}: missing cd routing scenarios`);
  else {
    const scenarios = JSON.parse(readFileSync(scenariosPath, 'utf8'));
    const routed = new Set(scenarios.map(({ expect_action: action }) => action));
    for (const action of ['local', 'server', 'automata', null]) {
      if (!routed.has(action)) failures.push(`${plugin}: scenarios do not cover ${action ?? 'a negative neighbor'}`);
    }
    const staging = scenarios.filter(({ prompt }) => /\bstaging\b/i.test(prompt));
    if (staging.some(({ expect_action: action }) => action !== null)) failures.push(`${plugin}: staging routes to a delivery action`);
  }
}

for (const required of ['`local`', '`production`', '`deploy:*`', '`pull:*`', '`automata`', 'one root deployment facade']) {
  if (!canonical.includes(required)) failures.push(`canonical contract: missing ${required}`);
}
if (/\bstaging\b/i.test(canonical)) failures.push('canonical contract: forbidden third environment');

const fixtures = join(root, 'tools/eval/fixtures-sc-cd');
const cases = [
  ['valid-language-owner', true],
  ['valid-composite', true],
  ['valid-automata', true],
  ['invalid-two-owners', false],
  ['invalid-secret', false],
];
for (const [name, expected] of cases) {
  const contract = JSON.parse(readFileSync(join(fixtures, name, 'deploy/contract.json'), 'utf8'));
  const result = validateProjectContract(contract);
  if ((result.length === 0) !== expected) failures.push(`${name}: expected ${expected ? 'valid' : 'invalid'} contract`);
  if (name === 'invalid-secret' && result.join('\n').includes('must-never-appear')) failures.push('invalid-secret: validator leaked a secret value');
}

const producer = JSON.parse(readFileSync(join(fixtures, 'valid-automata/deploy/contract.json'), 'utf8'));
if (validateProjectContract(producer, { command: producer.command, workingDirectory: producer.workingDirectory }).length) {
  failures.push('automata: exact producer facade rejected');
}
if (!validateProjectContract(producer, { command: 'cargo run deploy', workingDirectory: producer.workingDirectory }).some((message) => message.includes('stale'))) {
  failures.push('automata: divergent facade accepted');
}
if ((producer.trigger || 'manual') !== 'push') failures.push('automata: explicit push trigger was not preserved');
const manualDefault = JSON.parse(readFileSync(join(fixtures, 'valid-language-owner/deploy/contract.json'), 'utf8'));
if ((manualDefault.trigger || 'manual') !== 'manual') failures.push('language owner: trigger does not default to manual');
const composite = JSON.parse(readFileSync(join(fixtures, 'valid-composite/deploy/contract.json'), 'utf8'));
if (composite.owner.scope !== 'root' || composite.contributors.some(({ scope }) => scope === 'root')) failures.push('composite: contributor escaped its bounded scope');

if (failures.length) {
  for (const failure of failures) console.error(`SC-CD FAIL: ${failure}`);
  process.exit(1);
}
console.log(`SC-CD PASS: canonical contract, schema, ${plugins.length} portable copies and ${cases.length} project fixtures`);
