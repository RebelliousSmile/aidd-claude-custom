#!/usr/bin/env node
// Aggregate static and runtime evidence for an existing HTML reference.
// Read-only: stdout is the report. Exit 0 means the input was analyzed, not that it is
// conformant. Exit 2 is reserved for invalid invocation or unreadable/empty input.

import { existsSync, readFileSync, statSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { basename, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const argv = process.argv.slice(2);
const valueAfter = (flag) => {
  const index = argv.indexOf(flag);
  return index === -1 ? null : argv[index + 1] || null;
};
const optionValues = new Set(['--input', '--baseline'].flatMap((flag) => {
  const index = argv.indexOf(flag);
  return index === -1 ? [] : [index + 1];
}));
const inputArg = valueAfter('--input') || argv.find((arg, index) => !arg.startsWith('--') && !optionValues.has(index));
const baselineArg = valueAfter('--baseline');

const die = (message) => {
  console.error(`Error: ${message}`);
  process.exit(2);
};

if (!inputArg) die('usage: harness-analyze.mjs <input.html>');

const input = resolve(inputArg);
let html;
try {
  html = readFileSync(input, 'utf8');
} catch (error) {
  die(`cannot read ${input}: ${error.message}`);
}
if (!html.trim()) die(`input is empty: ${input}`);

const stripped = html.replace(/<!--[\s\S]*?-->/g, '');
const head = stripped.match(/<head\b[^>]*>([\s\S]*?)<\/head\s*>/i)?.[1] || '';
const has = (pattern) => pattern.test(stripped);
const occurrences = (pattern) => [...stripped.matchAll(pattern)];
const unescapeHtml = (value) => value
  .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"')
  .replace(/&#x27;/g, "'").replace(/&#39;/g, "'").replace(/&amp;/g, '&');

const scripts = occurrences(/<script\b([^>]*)>([\s\S]*?)<\/script\s*>/gi)
  .map((match) => ({ attributes: match[1].trim(), body: match[2] }));
const externalScripts = scripts.flatMap((script) => {
  const match = script.attributes.match(/\bsrc\s*=\s*["']([^"']+)["']/i);
  return match ? [match[1]] : [];
});
const externalStylesheets = occurrences(/<link\b[^>]*\brel\s*=\s*["'][^"']*stylesheet[^"']*["'][^>]*>/gi)
  .flatMap((match) => {
    const href = match[0].match(/\bhref\s*=\s*["']([^"']+)["']/i);
    return href ? [href[1]] : [];
  });
const styleBlocks = [...head.matchAll(/<style\b([^>]*)>([\s\S]*?)<\/style\s*>/gi)];
const importedStylesheets = styleBlocks.flatMap((match) =>
  [...match[2].matchAll(/@import\s+(?:url\(\s*)?["']([^"']+)["']\s*\)?/gi)].map((item) => item[1]));
const stylesheetDependencies = [...new Set([...externalStylesheets, ...importedStylesheets])];
const pageSelect = stripped.match(/<select\b[^>]*\bid\s*=\s*["']page-select["'][^>]*>([\s\S]*?)<\/select\s*>/i);
const optionKeys = [...(pageSelect?.[1] || '').matchAll(/<option\b[^>]*\bvalue\s*=\s*["']([^"']*)["']/gi)]
  .map((match) => unescapeHtml(match[1]));
const mediaQueries = styleBlocks.flatMap((match) =>
  [...match[2].matchAll(/@media\s*([^\{]+)\{/gi)].map((item) => item[1].trim()));
const preferenceMediaQueries = mediaQueries.filter((condition) =>
  /\b(prefers-reduced-motion|prefers-contrast|forced-colors|prefers-color-scheme)\b/i.test(condition));
const viewportMediaQueries = mediaQueries.filter((condition) =>
  /\b(min-width|max-width|width|device-width|orientation|aspect-ratio)\b/i.test(condition));
const unsupportedMediaQueries = mediaQueries.filter((condition) =>
  !preferenceMediaQueries.includes(condition) && !viewportMediaQueries.includes(condition));

const sourcePaths = [...stripped.matchAll(/\bsource\s*:\s*("(?:\\.|[^"])*"|'(?:\\.|[^'])*')/g)]
  .flatMap((match) => {
    try {
      const literal = match[1];
      return [literal.startsWith('"') ? JSON.parse(literal) : literal.slice(1, -1)];
    } catch (_) {
      return [];
    }
  });
const isAbsolutePath = (value) => /^(?:[A-Za-z]:[\\/]|\/)/.test(value);
const unreadableAbsoluteSources = [...new Set(sourcePaths.filter((value) => isAbsolutePath(value) && !existsSync(value)))];

function objectKeys(name) {
  const block = stripped.match(new RegExp(`const\\s+${name}\\s*=\\s*\\{([\\s\\S]*?)\\n\\s*\\};`));
  if (!block) return [];
  return [...block[1].matchAll(/^\s*(?:"((?:\\.|[^"])*)"|'((?:\\.|[^'])*)')\s*:/gm)]
    .map((match) => match[1] ?? match[2]);
}

const registryKeys = objectKeys('pages');
const metadataKeys = objectKeys('pageMetadata');
const functionNames = occurrences(/^\s*function\s+(page[A-Za-z0-9_$]+)\s*\(/gm).map((match) => match[1]);
const viewportModes = occurrences(/data-viewport\s*=\s*["'](desktop|tablet|mobile)["']/gi)
  .map((match) => match[1].toLowerCase());
const unique = (values) => [...new Set(values)];
const sameSet = (left, right) => left.length === right.length && left.every((value) => right.includes(value));

const signals = {
  doctype: /^\s*<!doctype html>/i.test(html),
  html: has(/<html\b/i),
  head: has(/<head\b/i),
  body: has(/<body\b/i),
  previewBar: has(/class\s*=\s*["'][^"']*\bpreview-bar\b/i),
  previewFrame: has(/id\s*=\s*["']preview-frame["']/i),
  pageContainer: has(/id\s*=\s*["']page-container["']/i),
  pageSelect: has(/id\s*=\s*["']page-select["']/i),
  setPage: /window\.setPage\s*=/.test(stripped),
  setViewport: /window\.setViewport\s*=/.test(stripped),
  pagesRegistry: /const\s+pages\s*=\s*\{/.test(stripped),
  metadataRegistry: /const\s+pageMetadata\s*=\s*\{/.test(stripped),
  authorStyleStart: html.includes('/* ===== AUTHOR PAGE STYLES'),
  authorStyleEnd: html.includes('/* ===== END AUTHOR PAGE STYLES ===== */'),
};

const harnessSignalCount = [signals.previewBar, signals.previewFrame, signals.pageContainer,
  signals.pageSelect, signals.setPage, signals.setViewport, signals.pagesRegistry]
  .filter(Boolean).length;
const looksLikeHarness = harnessSignalCount >= 2;
const violations = [];
const add = (id, severity, message) => violations.push({ id, severity, message });

if (looksLikeHarness) {
  for (const [key, present] of Object.entries(signals)) {
    if (!present) add(`missing-${key}`, 'error', `canonical harness signal is absent: ${key}`);
  }
  if (scripts.length !== 2) add('control-script-count', 'error', `found ${scripts.length} script blocks; canonical harness declares 2`);
  if (scripts.some((script) => script.attributes)) add('attributed-script', 'error', 'script attributes are outside the runtime checker contract');
  if (!sameSet(unique(viewportModes), ['desktop', 'tablet', 'mobile']))
    add('viewport-set', 'error', `viewport controls are ${unique(viewportModes).join(', ') || 'absent'}`);
  if (!registryKeys.length) add('empty-pages-registry', 'error', 'the pages registry is absent or empty');
  if (!sameSet(registryKeys, optionKeys)) add('registry-option-drift', 'error', 'page registry and selector options differ');
  if (!sameSet(registryKeys, metadataKeys)) add('registry-metadata-drift', 'error', 'page registry and metadata keys differ');
  if (viewportMediaQueries.length)
    add('viewport-media-query', 'error', 'viewport-dependent rules must use preview-frame device classes');
  if (unsupportedMediaQueries.length)
    add('unsupported-media-query', 'error', 'only accessibility preference media queries are allowed in a harness');
} else {
  add('canonical-shell-missing', 'info', 'the source is author HTML, not a canonical harness shell');
}

if (externalScripts.length) add('external-scripts', 'warning', `${externalScripts.length} external script(s) require a migration decision`);
if (stylesheetDependencies.length)
  add('external-stylesheets', 'warning', `${stylesheetDependencies.length} external stylesheet dependency/dependencies require resolution`);
if (unreadableAbsoluteSources.length)
  add('unreadable-source-path', 'warning', `${unreadableAbsoluteSources.length} absolute source path(s) are unreadable on this machine`);
if (/Migrated token snapshot/i.test(html))
  add('unproven-token-snapshot', 'warning', 'an inlined token snapshot has no supplied frozen-contract provenance');
if (!looksLikeHarness && scripts.some((script) => !script.attributes && script.body.trim()))
  add('inline-application-script', 'warning', 'inline application JavaScript must not be copied into harness controls');

let runtime = { applicable: false, status: null, stdout: '', stderr: '' };
if (looksLikeHarness) {
  const checker = resolve(dirname(fileURLToPath(import.meta.url)), 'harness-runtime-check.mjs');
  const result = spawnSync(process.execPath, [checker, input], { encoding: 'utf8' });
  const runtimeFailed = Boolean(result.error) || result.status !== 0;
  runtime = {
    applicable: true,
    status: result.error ? null : result.status,
    stdout: (result.stdout || '').trim(),
    stderr: (result.stderr || result.error?.message || '').trim(),
  };
  if (runtimeFailed) add('runtime-invalid', 'error', runtime.stderr || `runtime checker exited ${result.status}`);
}

let sizeComparison = null;
if (baselineArg) {
  const baseline = resolve(baselineArg);
  try {
    const baselineBytes = statSync(baseline).size;
    const outputBytes = statSync(input).size;
    const ratio = baselineBytes === 0 ? null : outputBytes / baselineBytes;
    sizeComparison = { baseline, baselineBytes, outputBytes, ratio };
    if (ratio !== null && ratio > 2)
      add('size-growth', 'warning', `output is ${ratio.toFixed(2)}x the baseline; shared content must be deduplicated or explicitly accepted`);
  } catch (error) {
    die(`cannot compare baseline ${baseline}: ${error.message}`);
  }
}

const structuralErrors = violations.some((violation) =>
  violation.severity === 'error' && violation.id !== 'runtime-invalid');
let classification;
if (looksLikeHarness) classification = structuralErrors ? 'repairable-harness' : 'canonical-harness';
else if (signals.html && signals.head && signals.body) classification = 'html-document';
else classification = 'html-fragment';

const blockers = [];
if (!looksLikeHarness && externalScripts.length) blockers.push('external application scripts');
if (!looksLikeHarness && scripts.some((script) => !script.attributes && script.body.trim())) blockers.push('inline application scripts');
if (looksLikeHarness && scripts.length > 2) blockers.push('additional scripts require an interaction-by-interaction decision');
if (stylesheetDependencies.length) blockers.push('unresolved stylesheet dependencies');
if (unreadableAbsoluteSources.length) blockers.push('absolute source provenance is unreadable on this machine');
if (/Migrated token snapshot/i.test(html)) blockers.push('token snapshot has no frozen-contract provenance');
if (sizeComparison?.ratio > 2) blockers.push('output size exceeds 2x baseline without explicit acceptance');

const suggestedPageKey = basename(input).replace(/\.[^.]+$/, '').toLowerCase()
  .replace(/[^a-z0-9_-]+/g, '-').replace(/^-+|-+$/g, '') || 'home';
const report = {
  schemaVersion: 2,
  input,
  classification,
  conformant: classification === 'canonical-harness' && runtime.status === 0,
  outcome: {
    formatConformant: classification === 'canonical-harness',
    runtimeValid: runtime.applicable ? runtime.status === 0 : null,
    migrationComplete: null,
    visualFidelity: 'unmeasured',
  },
  evidence: {
    signals,
    scripts: { total: scripts.length, attributed: scripts.filter((script) => script.attributes).length, external: externalScripts },
    styles: {
      inlineHeadBlocks: styleBlocks.length,
      external: stylesheetDependencies,
      links: externalStylesheets,
      imports: importedStylesheets,
      mediaQueries,
      preferenceMediaQueries,
      viewportMediaQueries,
      unsupportedMediaQueries,
    },
    pages: { options: optionKeys, registry: registryKeys, metadata: metadataKeys, functions: functionNames },
    provenance: { sourcePaths: unique(sourcePaths), unreadableAbsoluteSources },
    sizeComparison,
    viewports: unique(viewportModes),
    runtime,
  },
  violations,
  migration: {
    suggestedPageKey,
    readyWithoutDecision: blockers.length === 0,
    blockers,
    preserves: ['page markup', 'page-owned CSS', 'explicit page metadata'],
    regenerates: ['preview chrome', 'page registries', 'viewport controls', 'control scripts'],
  },
};

process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
process.exit(0);
