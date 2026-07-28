#!/usr/bin/env node
/**
 * orphan-selectors — scan inverse de builder-coverage.
 *
 * `01-scan` part du contenu en base : il voit les classes utilisées sans pattern.
 * Ce script fait l'inverse : il liste les classes DÉCLARÉES en CSS qui n'ont aucun
 * consommateur dans le markup (templates, parts, patterns, rendus SSR, JS).
 *
 * Cas visé : une famille CSS portée depuis une maquette dont le markup n'a jamais
 * été écrit. Le CSS est complet, personne ne le voit, et rien ne le signale.
 *
 * Usage :
 *   node orphan-selectors.mjs --css <fichier|dossier> [...] \
 *                             --markup <dossier> [...] \
 *                             [--ignore <prefixe>[,<prefixe>]] \
 *                             [--json]
 *
 * Défaut d'ignorés : wp-, has-, is-, screen-reader, alignfull, alignwide, admin-bar
 * (classes de plateforme, hors manifeste projet).
 *
 * Sortie : liste plain-text + `ORPHANS: N`. Exit 1 si N > 0.
 *
 * Limite assumée : une classe assemblée à l'exécution ("prefix-" . $i) n'est pas
 * détectée comme consommée. Le script signale les fragments suspects pour que le
 * cas soit tranché à la main plutôt que masqué par une heuristique.
 */

import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, extname } from 'node:path';

const CSS_EXT = new Set(['.css']);
const MARKUP_EXT = new Set(['.html', '.php', '.js', '.jsx', '.json', '.mjs']);
const DEFAULT_IGNORE = ['wp-', 'has-', 'is-', 'screen-reader', 'alignfull', 'alignwide', 'admin-bar'];

function parseArgs(argv) {
  const out = { css: [], markup: [], ignore: [...DEFAULT_IGNORE], json: false };
  let key = null;
  for (const a of argv) {
    if (a === '--json') { out.json = true; continue; }
    if (a.startsWith('--')) { key = a.slice(2); continue; }
    if (key === 'ignore') out.ignore.push(...a.split(','));
    else if (key === 'css') out.css.push(a);
    else if (key === 'markup') out.markup.push(a);
  }
  return out;
}

function walk(target, exts, acc = []) {
  const st = statSync(target);
  if (st.isFile()) {
    if (exts.has(extname(target))) acc.push(target);
    return acc;
  }
  for (const entry of readdirSync(target)) {
    if (entry === 'node_modules' || entry === 'vendor' || entry.startsWith('.')) continue;
    walk(join(target, entry), exts, acc);
  }
  return acc;
}

/** Classes déclarées : on ne lit que les préludes de règles (avant `{`). */
function declaredClasses(css) {
  const clean = css.replace(/\/\*[\s\S]*?\*\//g, '');
  const found = new Map(); // classe -> Set(fichiers) rempli par l'appelant
  for (const segment of clean.split('}')) {
    const brace = segment.indexOf('{');
    if (brace === -1) continue;
    const prelude = segment.slice(0, brace);
    if (prelude.trimStart().startsWith('@')) continue; // at-rule : pas de sélecteur
    for (const m of prelude.matchAll(/\.(-?[_a-zA-Z][\w-]*)/g)) {
      found.set(m[1], true);
    }
  }
  return [...found.keys()];
}

const args = parseArgs(process.argv.slice(2));
if (!args.css.length || !args.markup.length) {
  console.error('usage: orphan-selectors.mjs --css <path...> --markup <path...> [--ignore p1,p2] [--json]');
  process.exit(2);
}

const cssFiles = args.css.flatMap((p) => walk(p, CSS_EXT));
const markupFiles = args.markup.flatMap((p) => walk(p, MARKUP_EXT));

const declared = new Map(); // classe -> fichier CSS d'origine
for (const f of cssFiles) {
  for (const cls of declaredClasses(readFileSync(f, 'utf8'))) {
    if (!declared.has(cls)) declared.set(cls, f);
  }
}

const haystack = markupFiles.map((f) => readFileSync(f, 'utf8')).join('\n');

const orphans = [];
for (const [cls, origin] of declared) {
  if (args.ignore.some((p) => cls.startsWith(p))) continue;
  // Bord de mot des deux côtés : `card` ne doit pas matcher `card__body`.
  if (new RegExp(`(?<![\\w-])${cls.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?![\\w-])`).test(haystack)) continue;
  // Fragment consommé par concaténation ? On le signale sans l'absoudre.
  const stem = cls.replace(/(--|__)[\w-]+$/, '');
  const suspect = stem !== cls && haystack.includes(stem);
  orphans.push({ class: cls, origin, suspect });
}

orphans.sort((a, b) => a.class.localeCompare(b.class));

if (args.json) {
  console.log(JSON.stringify({ orphans, cssFiles: cssFiles.length, markupFiles: markupFiles.length }, null, 2));
} else {
  console.log(`orphan-selectors — ${cssFiles.length} CSS, ${markupFiles.length} fichiers de markup`);
  if (!orphans.length) {
    console.log('   Aucune classe déclarée sans consommateur.');
  } else {
    for (const o of orphans) {
      console.log(`   - ${o.class.padEnd(32)} ${o.origin}${o.suspect ? '   [racine présente — concaténation possible]' : ''}`);
    }
  }
  console.log(`ORPHANS: ${orphans.length}`);
}

process.exit(orphans.length ? 1 : 0);
