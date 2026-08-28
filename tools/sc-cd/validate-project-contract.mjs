#!/usr/bin/env node
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const secretKey = /(?:password|passwd|token|secret|private.?key|api.?key)/i;
const operationName = /^(deploy|pull):[a-z0-9:-]+$/;

function strings(value) {
  return Array.isArray(value) && value.length > 0 && value.every((item) => typeof item === 'string' && item.trim());
}

function scanSecrets(value, path = '$', failures = []) {
  if (!value || typeof value !== 'object') return failures;
  for (const [key, child] of Object.entries(value)) {
    const current = `${path}.${key}`;
    if (key !== 'secretNames' && secretKey.test(key)) failures.push(`${current}: secret values are forbidden`);
    if (key !== 'secretNames') scanSecrets(child, current, failures);
  }
  return failures;
}

export function validateProjectContract(contract, facade = {}) {
  const failures = scanSecrets(contract);
  if (!contract || typeof contract !== 'object' || Array.isArray(contract)) return ['contract must be an object'];
  if (contract.version !== 1) failures.push('version must be 1');
  if (!contract.owner || Array.isArray(contract.owner) || contract.owner.scope !== 'root' || !/^sc-[a-z0-9-]+$/.test(contract.owner.plugin || '')) {
    failures.push('exactly one root owner is required');
  }
  for (const field of ['manager', 'command', 'workingDirectory']) {
    if (typeof contract[field] !== 'string' || !contract[field].trim()) failures.push(`${field} is required`);
  }
  if (!contract.source || !contract.source.repository || !contract.source.ref) failures.push('source repository and ref are required');
  if (!contract.target || !['server', 'automata'].includes(contract.target.kind) || !contract.target.provider) failures.push('target kind and provider are required');
  if (contract.trigger !== undefined && !['manual', 'push'].includes(contract.trigger)) failures.push('trigger must be manual or explicit push');
  if (contract.secretNames !== undefined && (!Array.isArray(contract.secretNames) || contract.secretNames.some((name) => !/^[A-Z][A-Z0-9_]*$/.test(name)))) {
    failures.push('secretNames may contain names only');
  }
  const scopes = new Set();
  for (const contributor of contract.contributors || []) {
    if (!contributor || contributor.scope === 'root' || !contributor.scope || !/^sc-[a-z0-9-]+$/.test(contributor.plugin || '')) failures.push('contributors require a bounded non-root scope');
    else if (scopes.has(contributor.scope)) failures.push(`contributor scope ${contributor.scope} is duplicated`);
    else scopes.add(contributor.scope);
  }
  if (!Array.isArray(contract.operations) || contract.operations.length === 0) failures.push('at least one operation is required');
  for (const operation of contract.operations || []) {
    if (!operationName.test(operation.name || '')) failures.push('operation name must start with deploy: or pull:');
    const expectedDirection = operation.name?.startsWith('pull:') ? 'production-to-local' : 'local-to-production';
    if (operation.direction !== expectedDirection) failures.push(`${operation.name || 'operation'} has the wrong direction`);
    for (const field of ['preconditions', 'proof', 'recovery']) {
      if (!strings(operation[field])) failures.push(`${operation.name || 'operation'} requires ${field}`);
    }
  }
  if (contract.automata) {
    if (contract.automata.command !== contract.command) failures.push('automata command diverges from the root facade');
    if (contract.automata.workingDirectory !== contract.workingDirectory) failures.push('automata workingDirectory diverges from the root facade');
    const names = new Set((contract.operations || []).map(({ name }) => name));
    if (!strings(contract.automata.operations) || contract.automata.operations.some((name) => !names.has(name))) failures.push('automata operations diverge from the producer');
  }
  if (facade.command !== undefined && facade.command !== contract.command) failures.push('declared command is stale against the native facade');
  if (facade.workingDirectory !== undefined && facade.workingDirectory !== contract.workingDirectory) failures.push('declared workingDirectory is stale against the native facade');
  return failures;
}

function main() {
  const path = process.argv[2];
  if (!path) {
    console.error('usage: validate-project-contract.mjs <deploy/contract.json>');
    process.exit(2);
  }
  const contract = JSON.parse(readFileSync(resolve(path), 'utf8'));
  const failures = validateProjectContract(contract);
  if (failures.length) {
    for (const failure of failures) console.error(`SC-CD CONTRACT FAIL: ${failure}`);
    process.exit(1);
  }
  console.log(`SC-CD CONTRACT PASS: ${path} (trigger ${contract.trigger || 'manual'})`);
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main();
