#!/usr/bin/env node
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const surfaces = new Set(['data', 'media']);
const phases = new Set(['staging', 'production']);
const deletionPolicies = new Set(['mirror', 'preserve', 'forbid']);

function normalizeManifest(manifest, label) {
  if (!manifest || manifest.version !== 1 || typeof manifest.algorithm !== 'string' || !manifest.algorithm.trim() || !Array.isArray(manifest.entries)) {
    throw new Error(`${label}: invalid manifest header`);
  }
  const entries = new Map();
  const folded = new Set();
  let previousPath = null;
  for (const entry of manifest.entries) {
    const path = entry?.path;
    if (typeof path !== 'string' || !path || path.includes('\\') || path.includes('\0') || path.startsWith('/') || /^[A-Za-z]:/.test(path)) {
      throw new Error(`${label}: unsafe path`);
    }
    const segments = path.split('/');
    if (segments.some((segment) => !segment || segment === '.' || segment === '..')) throw new Error(`${label}: unsafe path`);
    if (previousPath !== null && path.localeCompare(previousPath, 'en-US') < 0) throw new Error(`${label}: entries are not sorted`);
    if (!['file', 'directory'].includes(entry.type)) throw new Error(`${label}: unsupported type at ${path}`);
    if (!Number.isInteger(entry.size) || entry.size < 0 || (entry.type === 'directory' && entry.size !== 0)) throw new Error(`${label}: invalid size at ${path}`);
    if (entry.type === 'file' && (typeof entry.hash !== 'string' || !entry.hash.trim())) throw new Error(`${label}: missing hash at ${path}`);
    const foldedPath = path.toLocaleLowerCase('en-US');
    if (entries.has(path) || folded.has(foldedPath)) throw new Error(`${label}: duplicate path ${path}`);
    entries.set(path, { path, type: entry.type, size: entry.size, ...(entry.type === 'file' ? { hash: entry.hash } : {}) });
    folded.add(foldedPath);
    previousPath = path;
  }
  return { algorithm: manifest.algorithm, entries };
}

export function compareManifests(localManifest, targetManifest, options = {}) {
  const phase = options.phase || 'staging';
  const surface = options.surface || 'media';
  const deletions = options.deletions || 'preserve';
  if (!phases.has(phase)) throw new Error('phase must be staging or production');
  if (!surfaces.has(surface)) throw new Error('surface must be data or media');
  if (!deletionPolicies.has(deletions)) throw new Error('deletions must be mirror, preserve, or forbid');

  const local = normalizeManifest(localManifest, 'local');
  const target = normalizeManifest(targetManifest, 'target');
  if (local.algorithm !== target.algorithm) throw new Error('manifest algorithms differ');

  if (phase === 'production') {
    return {
      allowed: false,
      reason: `production ${surface} is target-authoritative`,
      phase,
      surface,
      deletions,
      totalLocalBytes: [...local.entries.values()].reduce((sum, entry) => sum + (entry.type === 'file' ? entry.size : 0), 0),
      transferableBytes: 0,
      changes: { added: [], modified: [], deleted: [], unchanged: [] },
    };
  }

  const changes = { added: [], modified: [], deleted: [], unchanged: [] };
  let transferableBytes = 0;
  let totalLocalBytes = 0;
  for (const path of [...new Set([...local.entries.keys(), ...target.entries.keys()])].sort()) {
    const source = local.entries.get(path);
    const destination = target.entries.get(path);
    if (source?.type === 'file') totalLocalBytes += source.size;
    if (!destination) {
      changes.added.push(path);
      if (source.type === 'file') transferableBytes += source.size;
    } else if (!source) {
      changes.deleted.push(path);
    } else if (source.type !== destination.type || source.size !== destination.size || source.hash !== destination.hash) {
      changes.modified.push(path);
      if (source.type === 'file') transferableBytes += source.size;
    } else changes.unchanged.push(path);
  }

  if (deletions === 'forbid' && changes.deleted.length) {
    return { allowed: false, reason: 'target-only entries require a deletion decision', phase, surface, deletions, totalLocalBytes, transferableBytes: 0, changes };
  }
  return {
    allowed: true,
    phase,
    surface,
    deletions,
    totalLocalBytes,
    transferableBytes,
    deletionCount: deletions === 'mirror' ? changes.deleted.length : 0,
    changes,
  };
}

function parseArgs(args) {
  const [localPath, targetPath, ...rest] = args;
  if (!localPath || !targetPath) throw new Error('usage: compare-manifests.mjs <local.json> <target.json> [--phase staging|production] [--surface data|media] [--deletions mirror|preserve|forbid]');
  const options = {};
  for (let index = 0; index < rest.length; index += 2) {
    const key = rest[index];
    const value = rest[index + 1];
    if (!key?.startsWith('--') || value === undefined) throw new Error('invalid option');
    options[key.slice(2)] = value;
  }
  return { localPath, targetPath, options };
}

function main() {
  try {
    const { localPath, targetPath, options } = parseArgs(process.argv.slice(2));
    const local = JSON.parse(readFileSync(resolve(localPath), 'utf8'));
    const target = JSON.parse(readFileSync(resolve(targetPath), 'utf8'));
    console.log(JSON.stringify(compareManifests(local, target, options), null, 2));
  } catch (error) {
    console.error(`SC-CD MANIFEST FAIL: ${error.message}`);
    process.exit(1);
  }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main();
