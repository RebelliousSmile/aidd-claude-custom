#!/usr/bin/env node
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const plugins = ['sc-css', 'sc-js', 'sc-php', 'sc-python', 'sc-rust', 'sc-tiers'];
const canonical = readFileSync(join(root, 'tools/sc-cd/contract.md'), 'utf8');
const failures = [];

for (const plugin of plugins) {
  const target = join(root, 'plugins', plugin, 'references/cd-contract.md');
  if (!existsSync(target)) failures.push(`${plugin}: missing cd-contract.md`);
  else if (readFileSync(target, 'utf8') !== canonical) failures.push(`${plugin}: cd-contract.md drifted`);
}

for (const required of ['`local`', '`production`', '`deploy:*`', '`pull:*`', '`automata`', 'one root deployment facade']) {
  if (!canonical.includes(required)) failures.push(`canonical contract: missing ${required}`);
}
if (/\bstaging\b/i.test(canonical)) failures.push('canonical contract: forbidden third environment');

if (failures.length) {
  for (const failure of failures) console.error(`SC-CD FAIL: ${failure}`);
  process.exit(1);
}
console.log(`SC-CD PASS: canonical contract and ${plugins.length} portable copies`);
