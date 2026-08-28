#!/usr/bin/env node
import { readFileSync, readdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const modePattern = /^[0-7]{3,4}$/;

function populated(value) {
  return typeof value === 'string' && value.trim().length > 0;
}

export function validateTransportProfile(evidence) {
  const errors = [];
  const filesystem = evidence?.filesystem;
  const transport = evidence?.transport;
  const proof = evidence?.postTransferProof;

  if (!filesystem || !['drvfs', 'linux-native'].includes(filesystem.provenance)) {
    errors.push('filesystem provenance must be drvfs or linux-native');
  } else if (filesystem.provenance === 'drvfs') {
    if (!populated(filesystem.resolvedPath) || !populated(filesystem.windowsPath)) {
      errors.push('drvfs provenance requires resolvedPath and windowsPath evidence');
    }
    if (!populated(filesystem.mountEvidence) && !populated(filesystem.filesystemEvidence)) {
      errors.push('drvfs provenance requires mount or filesystem evidence');
    }
  } else if (!populated(filesystem.resolvedPath) || !populated(filesystem.filesystemEvidence)) {
    errors.push('linux-native provenance requires resolvedPath and filesystem evidence');
  }

  if (!transport || typeof transport !== 'object') {
    errors.push('transport profile is required');
  } else {
    if (filesystem?.provenance === 'drvfs') {
      for (const field of ['preservePermissions', 'preserveOwner', 'preserveGroup']) {
        if (transport[field] !== false) errors.push(`drvfs transport must disable ${field}`);
      }
      if (!modePattern.test(transport.destinationModes?.directories ?? '')) {
        errors.push('drvfs transport requires an explicit directory destination mode');
      }
      if (!modePattern.test(transport.destinationModes?.files ?? '')) {
        errors.push('drvfs transport requires an explicit file destination mode');
      }
    }
    if (!Array.isArray(transport.executablePaths)) {
      errors.push('transport must declare executablePaths, including an empty list');
    }
  }

  if (proof?.execution !== 'delivery') {
    errors.push('post-transfer proof must execute during delivery');
  }
  for (const field of ['directories', 'newFiles', 'updatedFiles']) {
    if (!Array.isArray(proof?.[field]) || proof[field].length === 0 || !proof[field].every(populated)) {
      errors.push(`post-transfer proof requires ${field}`);
    }
  }

  return errors;
}

function eventMap(events, errors) {
  const byId = new Map();
  const orders = new Set();
  if (!Array.isArray(events) || events.length === 0) {
    errors.push('behavior trace requires ordered events');
    return byId;
  }
  for (const event of events) {
    if (!populated(event?.id) || byId.has(event.id)) errors.push('behavior trace event ids must be unique non-empty strings');
    else byId.set(event.id, event);
    if (!Number.isInteger(event?.order) || orders.has(event.order)) errors.push('behavior trace event orders must be unique integers');
    else orders.add(event.order);
    if (!['success', 'failure', 'all'].includes(event?.path)) errors.push(`event ${event?.id ?? '<unknown>'} has an invalid path`);
  }
  return byId;
}

function successEvent(byId, id) {
  const event = byId.get(id);
  return event && ['success', 'all'].includes(event.path) ? event : undefined;
}

export function validateBehaviorTrace(evidence) {
  const errors = [];
  if (!populated(evidence?.source?.path) || !evidence?.source?.digest?.startsWith('sha256:') || evidence?.source?.inspection !== 'full') {
    errors.push('behavior trace requires a fully inspected source path and sha256 digest');
  }

  const byId = eventMap(evidence?.events, errors);
  for (const proof of evidence?.proofs ?? []) {
    const event = successEvent(byId, proof.eventId);
    if (!event) {
      errors.push(`proof ${proof.name ?? '<unnamed>'} references a missing or unreachable event`);
      continue;
    }
    if (event.kind !== 'check' || !populated(event.observable) || event.onFailure !== 'propagate') {
      errors.push(`proof ${proof.name ?? '<unnamed>'} must bind to an observable check that propagates failure`);
    }
  }
  if (!Array.isArray(evidence?.proofs) || evidence.proofs.length === 0) errors.push('behavior trace requires at least one proof claim');

  for (const recovery of evidence?.recoveries ?? []) {
    const label = recovery.name ?? '<unnamed>';
    const created = successEvent(byId, recovery.createEventId);
    const through = successEvent(byId, recovery.availableThroughEventId);
    const removed = recovery.removeEventId ? successEvent(byId, recovery.removeEventId) : undefined;
    if (!populated(recovery.artifact)) errors.push(`recovery ${label} requires an artifact`);
    if (!created || created.kind !== 'mutation' || created.action !== 'create' || created.subject !== recovery.artifact) {
      errors.push(`recovery ${label} requires a matching reachable creation event`);
    }
    if (!through) errors.push(`recovery ${label} requires a reachable availability-window event`);
    if (created && through && created.order >= through.order) errors.push(`recovery ${label} is not created before its availability window`);
    if (recovery.removeEventId && (!removed || removed.kind !== 'cleanup' || removed.action !== 'remove' || removed.subject !== recovery.artifact)) {
      errors.push(`recovery ${label} has an invalid removal event`);
    }
    if (removed && through && removed.order <= through.order) {
      errors.push(`recovery ${label} is removed before its availability window ends`);
    }
  }
  if (!Array.isArray(evidence?.recoveries) || evidence.recoveries.length === 0) errors.push('behavior trace requires at least one recovery claim');

  return errors;
}

export function validateEvidenceFixture(fixture) {
  if (fixture?.kind === 'transport-profile') return validateTransportProfile(fixture.evidence);
  if (fixture?.kind === 'behavior-trace') return validateBehaviorTrace(fixture.evidence);
  return ['fixture kind must be transport-profile or behavior-trace'];
}

function runFixtureDirectory(directory) {
  const failures = [];
  const names = readdirSync(directory).filter((name) => name.endsWith('.json')).sort();
  for (const name of names) {
    const fixture = JSON.parse(readFileSync(join(directory, name), 'utf8'));
    const errors = validateEvidenceFixture(fixture);
    const valid = errors.length === 0;
    if (valid !== fixture.expected?.valid) {
      failures.push(`${name}: expected ${fixture.expected?.valid ? 'valid' : 'invalid'}, got ${valid ? 'valid' : errors.join('; ')}`);
    }
    for (const fragment of fixture.expected?.errorIncludes ?? []) {
      if (!errors.some((error) => error.includes(fragment))) failures.push(`${name}: missing expected error ${fragment}`);
    }
  }
  return { failures, count: names.length };
}

const isCli = process.argv[1] && resolve(process.argv[1]) === resolve(fileURLToPath(import.meta.url));
if (isCli) {
  const defaultDirectory = join(dirname(fileURLToPath(import.meta.url)), '../eval/fixtures-sc-cd/js-delivery-evidence');
  const { failures, count } = runFixtureDirectory(resolve(process.argv[2] ?? defaultDirectory));
  if (failures.length) {
    for (const failure of failures) console.error(`JS DELIVERY EVIDENCE FAIL: ${failure}`);
    process.exit(1);
  }
  console.log(`JS DELIVERY EVIDENCE PASS: ${count} fixtures`);
}
