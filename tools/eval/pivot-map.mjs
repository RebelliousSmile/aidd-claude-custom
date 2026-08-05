#!/usr/bin/env node
// Garde d'appariement carte ↔ table de fournisseurs.
//
// Un pivot peut exister sur disque, être installé par un plugin, être listé dans
// `references/pivot-providers.md` — et rester inatteignable par la skill que son
// propre en-tête déclare comme consommateur, parce qu'aucun slug de la carte de
// détection ne s'y apparie. Ce défaut est muet : rien ne le signale.
//
//   Sens 1, FATAL      — tout pivot de la table a au moins un slug dans la carte
//                        de son consommateur. Un orphelin fait échouer le gate.
//   Sens 2, informatif — tout slug de carte sans ligne dans la table est listé
//                        `no provider`. Correct depuis #11, jamais fatal.
//   Unicité de la clé  — aucun pivot revendiqué par deux plugins. La table est
//                        une fonction : `pivot-providers.md` le dit sans le garder.
//
// Règle d'appariement — un slug s'apparie au pivot de MÊME NOM
// (`<famille>-pivots-<slug>.md`), sauf divergence déclarée dans la note ⚠ de la
// carte, sous la forme d'une ligne :
//
//     - `slug`[, `slug`] → `<famille>-pivots-x.md`[ + `<famille>-pivots-y.md`]
//
// La note est l'autorité : rien n'est deviné, aucune décomposition de
// `php-symfony` en `symfony` — une telle heuristique apparierait aussi
// `rust-vanilla` à `perf-pivots-vanilla.md`, que le texte déclare `no provider`.
// Une divergence non écrite est donc un orphelin, et c'est voulu : c'est ce qui
// rend l'appariement lisible par un humain au même endroit que par ce script.
// Un slug hybride atteint plusieurs pivots — `load every matching and concatenate`.
//
// Échec bruyant : ancre introuvable, zéro slug collecté, fichier absent → exit 1.
// Jamais un vert par parseur muet.
//
//   node tools/eval/pivot-map.mjs   → exit 0 si aucun orphelin, aucune collision

import { readFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
// Racine paramétrable — le selftest pointe des fixtures qui doivent rendre rouge.
const ROOT = process.argv[2] ?? join(HERE, '..', '..');
const OVERCODE = join(ROOT, 'plugins', 'overcode');
const TABLE = join(OVERCODE, 'references', 'pivot-providers.md');

// Quelle famille de pivots est consommée par quelle skill. En dur : une skill qui
// tourne dans un projet ne voit pas les autres, rien ne se dérive à l'exécution.
// `seo` est absent — aucun fournisseur, réceptacle que personne ne remplit.
const CONSUMERS = {
  perf: 'web-optimize',
  data: 'data-optimize',
  ap: 'ap-optimize',
};

// Deux formulations de l'ancre coexistent dans les skills. Les deux sont acceptées,
// aucune n'est réécrite pour l'occasion.
const ANCHORS = ['Map to one (or more) of:', 'Map to:'];

const errors = [];
const notes = [];
const fail = (msg) => errors.push(msg);

const read = (path, label) => {
  if (!existsSync(path)) { fail(`${label} introuvable : ${path}`); return null; }
  return readFileSync(path, 'utf8');
};

/** Identifiants entre backticks, dans l'ordre d'apparition. */
const ticked = (line) => [...line.matchAll(/`([^`\n]+)`/g)].map((m) => m[1]);

/**
 * Pivots déclarés par la table, par famille : { perf: Map<pivot, plugin[]> }.
 * Une ligne de table vaut `| `<famille>-pivots-<stack>.md` | `<plugin>` | … |`.
 */
function readTable(src) {
  const byFamily = {};
  for (const [, pivot, plugin] of src.matchAll(
    /^\|\s*`((?:perf|data|ap|seo)-pivots-[^`]+\.md)`\s*\|\s*`([^`]+)`/gm,
  )) {
    const family = pivot.split('-pivots-')[0];
    (byFamily[family] ??= new Map()).set(pivot, [
      ...(byFamily[family].get(pivot) ?? []),
      plugin,
    ]);
  }
  return byFamily;
}

/**
 * Carte de détection d'une skill : les slugs, et les divergences slug → pivot que
 * la note ⚠ déclare. Le bloc de slugs court de l'ancre jusqu'à la première ligne
 * qui n'est plus une énumération d'identifiants backtickés.
 */
function readMap(src, family, label) {
  const lines = src.split(/\r?\n/);
  const at = lines.findIndex((l) => ANCHORS.some((a) => l.includes(a)));
  if (at === -1) { fail(`${label} : ancre de carte introuvable (${ANCHORS.map((a) => `« ${a} »`).join(' / ')})`); return null; }

  // Bloc de carte : de l'ancre jusqu'au ⚠ quand la carte en porte un AVANT l'étape
  // suivante — c'est la seule borne fiable, car un paragraphe de prose (couches
  // additives) sépare des lignes de slugs par des lignes vides. Sans ⚠, on retombe
  // sur la première ligne vide ou l'étape numérotée suivante.
  // Seules les lignes qui ne portent QUE des identifiants backtickés séparés par des
  // virgules sont collectées — la prose intercalée (couches additives, parenthèse
  // `other`, paragraphe `rust-vanilla`) est ignorée sans interrompre la collecte,
  // sinon un slug placé après elle serait invisible.
  // La ligne d'ancre peut déjà porter des slugs (forme inline de `ap-optimize`).
  const nextStep = lines.findIndex((l, n) => n > at && /^\s*\d+\.\s/.test(l));
  const stop = nextStep === -1 ? lines.length : nextStep;
  const warn = lines.findIndex((l, n) => n > at && n < stop && l.includes('⚠'));
  const slugs = new Set(ticked(lines[at]));
  let i = at + 1;
  for (; i < (warn === -1 ? stop : warn); i++) {
    if (warn === -1 && lines[i].trim() === '') break;
    if (/^\s*(`[^`\n]+`\s*,?\s*)+$/.test(lines[i])) ticked(lines[i]).forEach((s) => slugs.add(s));
  }
  if (slugs.size === 0) { fail(`${label} : ancre trouvée mais aucun slug collecté`); return null; }

  // Note ⚠ — bornée au bloc : de la ligne portant le ⚠ jusqu'à la prochaine étape
  // numérotée ou la première ligne vide. Sans cette borne, un `<famille>-pivots-*.md`
  // cité plus bas dans le fichier rattacherait des slugs qui ne sont pas les siens.
  const overrides = new Map();
  const pivotRe = new RegExp(`^${family}-pivots-[^<>]+\\.md$`);
  const start = lines.findIndex((l, n) => n >= i && l.includes('⚠'));
  if (start !== -1) {
    for (let n = start; n < lines.length; n++) {
      if (n > start && (/^\s*\d+\.\s/.test(lines[n]) || lines[n].trim() === '')) break;
      const [left, right] = lines[n].split('→');
      if (right === undefined) continue;
      const targets = ticked(right).filter((t) => pivotRe.test(t));
      const declared = ticked(left).filter((s) => slugs.has(s));
      if (targets.length === 0 && declared.length > 0) {
        fail(`${label} : divergence déclarée sans pivot cible — « ${lines[n].trim()} »`);
        continue;
      }
      for (const s of declared) overrides.set(s, [...(overrides.get(s) ?? []), ...targets]);
    }
  }
  return { slugs, overrides };
}

const table = readTable(read(TABLE, 'table des fournisseurs') ?? '');

for (const [family, skill] of Object.entries(CONSUMERS)) {
  const pivots = table[family];
  if (!pivots || pivots.size === 0) { fail(`famille \`${family}\` : aucune ligne dans la table`); continue; }

  // Unicité de la clé — la table est une fonction, rien ne le vérifiait.
  for (const [pivot, plugins] of pivots) {
    const distinct = [...new Set(plugins)];
    if (distinct.length > 1) fail(`\`${pivot}\` revendiqué par ${distinct.length} plugins : ${distinct.map((p) => `\`${p}\``).join(', ')}`);
  }

  const path = join(OVERCODE, 'skills', skill, 'SKILL.md');
  const src = read(path, `carte de \`${skill}\``);
  if (!src) continue;
  const map = readMap(src, family, `\`${skill}\``);
  if (!map) continue;

  // Slug → pivot(s) : identité, sauf divergence déclarée. Un slug hybride en atteint
  // plusieurs — c'est la concaténation que les deux skills décrivent déjà.
  const reached = new Map();
  for (const slug of map.slugs) {
    for (const pivot of map.overrides.get(slug) ?? [`${family}-pivots-${slug}.md`]) {
      reached.set(pivot, [...(reached.get(pivot) ?? []), slug]);
    }
  }

  const orphans = [...pivots.keys()].filter((p) => !reached.has(p));
  const noProvider = [...reached].filter(([p]) => !pivots.has(p)).flatMap(([, s]) => s).sort();

  console.log(`\n${family} → ${skill} — ${pivots.size} pivot(s), ${map.slugs.size} slug(s), ${map.overrides.size} divergence(s) déclarée(s)`);
  for (const p of orphans) fail(`\`${p}\` (${[...new Set(pivots.get(p))].join(', ')}) : aucun slug de \`${skill}\` ne l'atteint — le pivot déclare ce consommateur et lui est inatteignable`);
  if (noProvider.length) notes.push(`${skill} — no provider (attendu) : ${noProvider.map((s) => `\`${s}\``).join(', ')}`);
  console.log(`  ${orphans.length ? '✗' : '✓'} ${pivots.size - orphans.length}/${pivots.size} pivot(s) atteint(s)`);
}

if (notes.length) { console.log('\nInformatif — slugs sans fournisseur :'); for (const n of notes) console.log(`  · ${n}`); }
if (errors.length) { console.log('\nOrphelins et collisions :'); for (const e of errors) console.log(`  ✗ ${e}`); }
console.log(`\n${errors.length ? '✗' : '✓'} pivot-map — ${errors.length} défaut(s) d'appariement`);
process.exit(errors.length ? 1 : 0);
