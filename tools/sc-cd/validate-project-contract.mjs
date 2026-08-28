#!/usr/bin/env node
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const secretKey = /(?:password|passwd|token|secret|private.?key|api.?key)/i;
const operationName = /^deploy:[a-z0-9:-]+$/;
const targetId = /^[a-z0-9][a-z0-9-]*$/;
const pluginName = /^sc-[a-z0-9-]+$/;
const secretName = /^[A-Z][A-Z0-9_]*$/;

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

function validateOperation(operation, failures) {
  const label = operation?.name || 'operation';
  if (!operation || typeof operation !== 'object' || Array.isArray(operation)) {
    failures.push('operations must contain objects');
    return;
  }
  if (!operationName.test(operation.name || '')) failures.push(`${label}: only deploy:* operation names are supported`);
  if (!['code', 'schema', 'data', 'media'].includes(operation.surface)) failures.push(`${label}: surface must be code, schema, data, or media`);
  if (!['local', 'target'].includes(operation.authority)) failures.push(`${label}: authority must be local or target`);
  if (!strings(operation.phases) || operation.phases.some((phase) => !['staging', 'production'].includes(phase))) {
    failures.push(`${label}: phases must contain staging or production`);
  }
  for (const field of ['preconditions', 'proof', 'recovery']) {
    if (!strings(operation[field])) failures.push(`${label}: ${field} is required`);
  }

  if (['code', 'schema'].includes(operation.surface) && operation.authority !== 'local') {
    failures.push(`${label}: ${operation.surface} must remain local-authoritative`);
  }
  if (['data', 'media'].includes(operation.surface)) {
    if (operation.authority !== 'local') failures.push(`${label}: target-authoritative ${operation.surface} cannot be a deploy operation`);
    if (operation.phases?.some((phase) => phase !== 'staging')) failures.push(`${label}: mutable ${operation.surface} deploy is staging-only`);
    if (!operation.sync || operation.sync.comparison !== 'content-hash' || operation.sync.resumable !== true) {
      failures.push(`${label}: mutable ${operation.surface} requires resumable content-hash sync`);
    }
    if (!['mirror', 'preserve', 'forbid'].includes(operation.sync?.deletions)) failures.push(`${label}: a deletion policy is required`);
  }
}

function validateTarget(target, contract, operations, failures, targetIds, lockKeys, observedGuards) {
  const id = target?.id || 'target';
  if (!target || typeof target !== 'object' || Array.isArray(target)) {
    failures.push('targets must contain objects');
    return;
  }
  if (!targetId.test(target.id || '')) failures.push(`${id}: invalid target id`);
  else if (targetIds.has(target.id)) failures.push(`${id}: target id is duplicated`);
  else targetIds.add(target.id);
  if (!['staging', 'production'].includes(target.phase)) failures.push(`${id}: phase must be staging or production`);
  if (!['server', 'automata'].includes(target.mode)) failures.push(`${id}: mode must be server or automata`);
  if (typeof target.provider !== 'string' || !target.provider.trim()) failures.push(`${id}: provider is required`);
  if (!['workspace', 'automation-checkout'].includes(target.executionContext)) failures.push(`${id}: executionContext is invalid`);
  if (!Number.isInteger(target.lifecycleRevision) || target.lifecycleRevision < 1) failures.push(`${id}: lifecycleRevision must be a positive integer`);
  if (!target.guard || !['file', 'provider-metadata'].includes(target.guard.kind) || typeof target.guard.reference !== 'string' || !target.guard.reference.trim()) {
    failures.push(`${id}: a non-secret lifecycle guard is required`);
  }
  if (!target.lock || typeof target.lock.key !== 'string' || !target.lock.key.trim() || !['wait', 'fail'].includes(target.lock.behavior)) {
    failures.push(`${id}: a target lock and behavior are required`);
  } else if (lockKeys.has(target.lock.key)) failures.push(`${id}: lock key ${target.lock.key} is shared by multiple targets`);
  else lockKeys.add(target.lock.key);

  if (target.secretNames !== undefined && (!Array.isArray(target.secretNames) || target.secretNames.some((name) => !secretName.test(name)))) {
    failures.push(`${id}: secretNames may contain names only`);
  }
  if (target.trigger !== undefined && !['manual', 'push'].includes(target.trigger)) failures.push(`${id}: trigger must be manual or push`);
  if (target.trigger === 'push' && target.mode !== 'automata') failures.push(`${id}: push requires automata mode`);
  if (target.mode === 'automata' && target.executionContext !== 'automation-checkout') failures.push(`${id}: automata requires an automation checkout`);
  if (target.mode === 'automata' && (!contract.source.clean || /^(?:working-tree|head)$/i.test(contract.source.ref || ''))) {
    failures.push(`${id}: automata requires a clean immutable source ref`);
  }

  const invocation = target.invocation;
  if (!invocation || typeof invocation.command !== 'string' || !invocation.command.trim()) failures.push(`${id}: invocation command is required`);
  else {
    if (!(invocation.command === contract.command || invocation.command.startsWith(`${contract.command} `))) failures.push(`${id}: invocation diverges from the root facade`);
    if (!invocation.command.includes(target.id)) failures.push(`${id}: invocation must select its target id explicitly`);
  }
  if (invocation?.workingDirectory !== contract.workingDirectory) failures.push(`${id}: invocation workingDirectory diverges from the root facade`);
  if (!strings(invocation?.operations)) failures.push(`${id}: invocation operations are required`);
  for (const name of invocation?.operations || []) {
    const operation = operations.get(name);
    if (!operation) failures.push(`${id}: invocation references unknown operation ${name}`);
    else {
      if (!operation.phases.includes(target.phase)) failures.push(`${id}: ${name} is not enabled for ${target.phase}`);
      if (target.phase === 'production' && ['data', 'media'].includes(operation.surface)) failures.push(`${id}: production cannot deploy mutable ${operation.surface}`);
    }
  }

  const destructiveMutable = (invocation?.operations || []).some((name) => {
    const operation = operations.get(name);
    return operation?.destructive && ['data', 'media'].includes(operation.surface);
  });
  if (target.phase === 'staging' && destructiveMutable) {
    if (!target.quiescence || !target.quiescence.strategy || !target.quiescence.enter || !target.quiescence.exit || !strings(target.quiescence.proof)) {
      failures.push(`${id}: destructive staging sync requires a proven quiescence strategy for promotion`);
    }
  }

  const observed = observedGuards?.[target.id];
  if (observed && (observed.phase !== target.phase || observed.lifecycleRevision !== target.lifecycleRevision)) {
    failures.push(`${id}: lifecycle guard is stale`);
  }
}

export function validateProjectContract(contract, runtime = {}) {
  if (!contract || typeof contract !== 'object' || Array.isArray(contract)) return ['contract must be an object'];
  const failures = scanSecrets(contract);
  if (contract.version === 1) {
    failures.push('version 1 contract requires explicit migration target id and phase');
    return failures;
  }
  if (contract.version !== 2) failures.push('version must be 2');
  if (!contract.owner || Array.isArray(contract.owner) || contract.owner.scope !== 'root' || !pluginName.test(contract.owner.plugin || '')) {
    failures.push('exactly one root owner is required');
  }
  for (const field of ['manager', 'command', 'workingDirectory']) {
    if (typeof contract[field] !== 'string' || !contract[field].trim()) failures.push(`${field} is required`);
  }
  if (!contract.source || !contract.source.repository || !contract.source.ref || typeof contract.source.clean !== 'boolean') {
    failures.push('source repository, ref, and clean state are required');
  } else if (!contract.source.clean && (!contract.source.manifest || !contract.source.dirtyPolicy)) {
    failures.push('dirty source requires a manifest and explicit policy');
  }

  const scopes = new Set();
  for (const contributor of contract.contributors || []) {
    if (!contributor || contributor.scope === 'root' || !contributor.scope || !pluginName.test(contributor.plugin || '')) failures.push('contributors require a bounded non-root scope');
    else if (scopes.has(contributor.scope)) failures.push(`contributor scope ${contributor.scope} is duplicated`);
    else scopes.add(contributor.scope);
  }

  if (!Array.isArray(contract.operations) || contract.operations.length === 0) failures.push('at least one operation is required');
  const operations = new Map();
  for (const operation of contract.operations || []) {
    validateOperation(operation, failures);
    if (operation?.name) {
      if (operations.has(operation.name)) failures.push(`${operation.name}: operation is duplicated`);
      else operations.set(operation.name, operation);
    }
  }

  if (!Array.isArray(contract.targets) || contract.targets.length === 0) failures.push('at least one target is required');
  const targetIds = new Set();
  const lockKeys = new Set();
  for (const target of contract.targets || []) validateTarget(target, contract, operations, failures, targetIds, lockKeys, runtime.guards);

  if (runtime.command !== undefined && runtime.command !== contract.command) failures.push('declared command is stale against the native facade');
  if (runtime.workingDirectory !== undefined && runtime.workingDirectory !== contract.workingDirectory) failures.push('declared workingDirectory is stale against the native facade');
  return failures;
}

export function validatePromotionTransition(before, after, observedGuard) {
  const failures = [];
  if (!before || !after || before.id !== after.id) failures.push('promotion must keep the same target id');
  if (before?.phase !== 'staging' || after?.phase !== 'production') failures.push('promotion must move staging to production');
  if (!Number.isInteger(before?.lifecycleRevision) || after?.lifecycleRevision !== before.lifecycleRevision + 1) {
    failures.push('promotion must increment lifecycleRevision exactly once');
  }
  if (!before?.quiescence?.strategy || !before.quiescence.enter || !before.quiescence.exit || !strings(before.quiescence.proof)) {
    failures.push('promotion requires proven application-write quiescence');
  }
  if (!observedGuard || observedGuard.phase !== after?.phase || observedGuard.lifecycleRevision !== after?.lifecycleRevision) {
    failures.push('promotion is not fail-closed until the remote guard matches production');
  }
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
  const targets = contract.targets.map(({ id }) => id).join(', ');
  console.log(`SC-CD CONTRACT PASS: ${path} (targets ${targets})`);
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main();
