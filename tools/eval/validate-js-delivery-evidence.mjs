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

export function validateEvidenceFixture(fixture) {
  if (fixture?.kind !== 'transport-profile') return ['fixture kind must be transport-profile'];
  return validateTransportProfile(fixture.evidence);
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
