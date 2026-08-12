#!/usr/bin/env node
// Cohérence des informations dupliquées — manifestes et numérotation des actions.
//
// Ce garde existe parce que `alias:bump-plugin` vérifie déjà les manifestes, mais
// depuis l'intérieur du chemin discipliné : un bump fait à la main l'évite entièrement.
// Il doit donc vivre sur un point de passage obligé (`pnpm test`, CI), jamais dans l'outil.
//
//   node tools/eval/consistency.mjs   → exit 0 si aucune incohérence
//
// Ce qui est vérifié :
//   M1  plugin.json ↔ marketplace.json — version et description identiques
//   M2  toute entrée de marketplace.json a un dossier plugin
//   M3  index.json — mêmes plugins, et aucun champ `version`/`description`
//       (aucun lecteur ne s'en sert ; les rétablir ferait revenir la dérive)
//   A1  toute ligne de table d'un SKILL.md résout vers un fichier d'action
//   A2  tout fichier d'action figure dans la table de son SKILL.md
//   A3  aucun préfixe numérique n'est porté par deux fichiers (les trous sont tolérés)
//   A4  aucun titre H1 d'action ne porte son numéro (le nom de fichier le porte)
//   M4  toute source déclarée en face d'une cible `.claude/rules/` existe sur disque
//   M5  toute ligne de `pivot-providers.md` s'appuie sur une cible réellement installable

import { readdirSync, readFileSync, existsSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const findings = [];
const fail = (code, msg) => findings.push({ code, msg });
const readJson = (p) => JSON.parse(readFileSync(join(ROOT, p), 'utf8'));
const dirs = (p) => existsSync(join(ROOT, p))
  ? readdirSync(join(ROOT, p)).filter((n) => statSync(join(ROOT, p, n)).isDirectory())
  : [];

// ─── Manifestes ────────────────────────────────────────────────────────────────

const marketplace = readJson('.claude-plugin/marketplace.json');
const index = readJson('index.json');
const byName = new Map(marketplace.plugins.map((p) => [p.name, p]));
const plugins = dirs('plugins').filter((n) => existsSync(join(ROOT, 'plugins', n, '.claude-plugin/plugin.json')));

for (const name of plugins) {
  const manifest = readJson(`plugins/${name}/.claude-plugin/plugin.json`);
  const entry = byName.get(name);
  if (!entry) { fail('M1', `${name} — absent de marketplace.json`); continue; }
  if (entry.version !== manifest.version)
    fail('M1', `${name} — version : plugin.json ${manifest.version} ≠ marketplace.json ${entry.version}`);
  if (entry.description !== manifest.description)
    fail('M1', `${name} — description : plugin.json et marketplace.json divergent`);

  const codexPath = `plugins/${name}/.codex-plugin/plugin.json`;
  if (existsSync(join(ROOT, codexPath))) {
    const codex = readJson(codexPath);
    for (const key of ['name', 'version', 'description'])
      if (codex[key] !== manifest[key])
        fail('M1', `${name} — ${key} : manifeste Codex et manifeste Claude divergent`);
  }
}

for (const entry of marketplace.plugins)
  if (!plugins.includes(entry.name)) fail('M2', `${entry.name} — déclaré dans marketplace.json, sans dossier plugin`);

const indexed = new Set(index.plugins.map((p) => p.id));
for (const name of plugins) if (!indexed.has(name)) fail('M3', `${name} — absent d'index.json`);
for (const p of index.plugins) {
  if (!plugins.includes(p.id)) fail('M3', `${p.id} — déclaré dans index.json, sans dossier plugin`);
  for (const key of ['version', 'description'])
    if (key in p) fail('M3', `${p.id} — index.json porte un champ \`${key}\` : aucun lecteur ne s'en sert, il dérive en silence`);
}

// ─── Actions ───────────────────────────────────────────────────────────────────

// Une skill numérote son ordre dans la table de SKILL.md et, la plupart du temps,
// dans le nom du fichier. Les deux conventions coexistent volontairement :
//   `alias`  → table `| 01 | rechallenge |` + fichier `01-rechallenge.md`
//   `status` → table `| 01 | memory |`      + fichier `memory.md`
// La correspondance se lit donc toujours depuis la table, jamais entre fichiers.
// Un SKILL.md contient souvent plusieurs tables numérotées de la même forme
// (`sc-css/audit` en a une de *dimensions*), donc seule compte celle dont l'en-tête
// déclare une colonne `Action`. Et la cellule nomme l'action tantôt nue (`scan`),
// tantôt avec son préfixe (`01-scan`) : les deux se lisent, le nom nu fait foi.
const TABLE_HEAD = /^\|\s*(?:#\s*\|\s*)?Actions?\s*\|/i;
const TABLE_ROW = /^\|\s*`?(\d{2})`?\s*\|\s*`([^`]+)`/;
const CANONICAL_ACTION_ROW = /^\|\s*([a-z0-9][a-z0-9._-]*)\s*\|/i;
const ACTION_FILE = /^(?:(\d{2})-)?(.+)\.md$/;
const bare = (name) => name.replace(/^\d{2}-/, '');

function actionRows(skillMd) {
  if (!existsSync(skillMd)) return [];
  const rows = [];
  let inside = false;
  for (const line of readFileSync(skillMd, 'utf8').split('\n')) {
    if (TABLE_HEAD.test(line)) { inside = true; continue; }
    if (!inside) continue;
    if (!line.startsWith('|')) { inside = false; continue; }
    const m = line.match(TABLE_ROW);
    if (m) { rows.push({ num: Number(m[1]), name: bare(m[2]) }); continue; }
    const canonical = line.match(CANONICAL_ACTION_ROW);
    if (canonical && !/^[-:]+$/.test(canonical[1])) rows.push({ num: null, name: bare(canonical[1]) });
  }
  return rows;
}

/**
 * Politique de numérotation : un numéro **identifie**, il n'ordonne pas.
 *
 * Le doublon est une erreur — deux fichiers portant `06` rendent toute référence
 * ambiguë. Le trou est toléré : l'interdire rendrait bloquante la cascade de
 * renommages qui suit chaque suppression d'action, or c'est cette cascade non
 * faite qui a produit le trou d'`alias` en 3.1.1. Le strict n'aurait pas empêché
 * la dette, il l'aurait déplacée dans la CI.
 *
 * @param {number[]} numbers  préfixes trouvés sur disque, triés, ex. [1,2,3,5]
 * @param {string}   skill    chemin lisible, ex. `overcode/skills/alias`
 * @returns {{code: string, msg: string}[]}  vide si la suite est acceptable
 */
function numberingPolicy(numbers, skill) {
  const seen = new Set(), duplicates = new Set();
  for (const n of numbers) (seen.has(n) ? duplicates : seen).add(n);
  return [...duplicates].sort((a, b) => a - b).map((n) => ({
    code: 'A3',
    msg: `${skill} — le numéro ${String(n).padStart(2, '0')} est porté par plusieurs fichiers : toute référence à cette action est ambiguë`,
  }));
}

/**
 * Le titre H1 d'une action ne doit pas porter son numéro — le nom de fichier
 * et la table de SKILL.md le portent déjà, et un numéro écrit à trois endroits
 * ne se corrige qu'à un seul le jour d'un renommage.
 *
 * Trois formes coexistent aujourd'hui, dont deux à rejeter :
 *   `# Action 03 — bump-plugin`   (69 fichiers)  ✗
 *   `# 01-arbitrate` / `# 01 - intake`  (97)     ✗
 *   `# Scaffold` / `# Analyze-doc`      (12)     ✓
 *
 * Le rejet vise le *préfixe*, pas le chiffre : `Action` suivi d'un nombre est
 * toujours refusé, et un nombre en tête ne l'est que s'il est suivi d'une
 * ponctuation de séparation. Un titre qui commencerait par un nombre suivi d'un
 * simple espace (`# 3 raisons de…`) reste donc accepté — il n'en existe aucun
 * aujourd'hui, mais le rejeter demanderait de deviner l'intention, et un gate
 * qui devine produit des faux positifs que personne ne sait corriger.
 *
 * @param {string} h1  première ligne du fichier, déjà trimmée, ex. `# 01 - intake`
 * @returns {boolean}  true si le titre est acceptable en l'état
 */
const NUMBERED_TITLE = /^#\s+(?:actions?\s+\d+|\d{1,3}\s*[-–—.:)]\s*\S)/i;
const titleIsClean = (h1) => !NUMBERED_TITLE.test(h1);

/**
 * M4 — une action qui annonce écrire dans `.claude/rules/` doit pouvoir le faire.
 *
 * Le défaut visé n'est pas une faute de frappe : c'est un installeur qui **déclare
 * du vide**. `sc-tiers` annonçait quatre pivots data dont trois n'avaient aucune
 * source sur disque ; `sc-css` en annonçait six pour un plugin sans le moindre
 * `references/`. Le rapport de sortie, lui, affirmait le succès. D'où la garde :
 * une source citée en face d'une cible se relit sur disque, sinon rien n'est écrit
 * et l'annonce est fausse (DEC-009 §2 — un prérequis absent vaut champ absent).
 *
 * L'ancrage se fait sur la **forme**, jamais sur l'intitulé de colonne : `sc-tiers`
 * écrit `Reference file`, les quatre autres `Source (in plugin)`. Est donc examinée
 * toute ligne de table qui cite une cible `.claude/rules/…`, quelle que soit sa
 * colonne — `sc-python/01-scan.md` met source et cible dans la *même* cellule,
 * séparées d'une flèche, et doit être couverte comme les autres.
 *
 * Deux bases de résolution coexistent, et confondre les deux rendrait la garde
 * inopérante sur la moitié du parc :
 *   `${CLAUDE_PLUGIN_ROOT}/x`  → `plugins/<plugin>/x`             (les quatre `sc-*`)
 *   `references/x` (relatif)   → `plugins/<plugin>/skills/<skill>/x`  (`sc-tiers`)
 *
 * Couverture volontairement partielle, à ne pas confondre avec une garantie :
 *   — les listes de chemins en **bloc de code** (`sc-js/sniff/03-clean.md`) sont hors
 *     champ : ce ne sont pas des tables, et leur sens est historique (ce qu'une
 *     version passée a pu installer), pas déclaratif ;
 *   — une table **sans colonne source** échappe à la garde : il n'y a rien à
 *     résoudre. C'était le cas de `sc-css`, retiré en amont plutôt que toléré ;
 *   — le **sens inverse** n'est pas vérifié : une référence présente sur disque et
 *     citée hors table d'action (un `SKILL.md`, par exemple) n'est pas confrontée.
 *
 * @param {string} line    ligne de table brute, ex. `| \`refs/a.md\` | \`.claude/rules/x.md\` |`
 * @param {string} plugin  nom du plugin, pour la base `${CLAUDE_PLUGIN_ROOT}`
 * @param {string} skill   nom de la skill, pour la base relative
 * @returns {{sources: {raw: string, path: string, ok: boolean}[], targets: string[]}}
 */
function ruleInstallLine(line, plugin, skill) {
  const sources = [], targets = [];
  for (const token of line.match(/`[^`]+`/g) ?? []) {
    const raw = token.slice(1, -1).trim();
    if (!raw.endsWith('.md')) continue;
    if (raw.startsWith('.claude/rules/')) { targets.push(raw.split('/').pop()); continue; }
    const path = raw.startsWith('${CLAUDE_PLUGIN_ROOT}/')
      ? join('plugins', plugin, raw.slice('${CLAUDE_PLUGIN_ROOT}/'.length))
      : join('plugins', plugin, 'skills', skill, raw);
    sources.push({ raw, path, ok: existsSync(join(ROOT, path)) });
  }
  return { sources, targets };
}

// Cibles `.claude/rules/` qu'un plugin sait réellement écrire — clé `<plugin>::<fichier>`.
// N'y entre qu'une cible dont **toutes** les sources déclarées sur la même ligne résolvent :
// une ligne à source manquante ne promet rien, et une ligne sans source ne prouve rien.
const installable = new Set();

for (const plugin of plugins) {
  for (const skill of dirs(`plugins/${plugin}/skills`)) {
    const base = `plugins/${plugin}/skills/${skill}`;
    const label = `${plugin}/skills/${skill}`;
    const actionsDir = join(ROOT, base, 'actions');
    if (!existsSync(actionsDir)) continue;

    const files = readdirSync(actionsDir).filter((n) => n.endsWith('.md'));
    const byAction = new Map();
    for (const f of files) {
      const [, num, name] = f.match(ACTION_FILE);
      byAction.set(name, { file: f, num: num ? Number(num) : null });
    }

    const rows = actionRows(join(ROOT, base, 'SKILL.md'));

    const declared = new Set();
    for (const { num, name } of rows) {
      declared.add(name);
      const action = byAction.get(name);
      if (!action) { fail('A1', `${label} — table : \`${name}\` (${num}) ne résout vers aucun fichier`); continue; }
      if (num !== null && action.num !== null && action.num !== num)
        fail('A1', `${label} — \`${name}\` : table ${String(num).padStart(2, '0')}, fichier ${action.file}`);
    }
    for (const [name, { file }] of byAction)
      if (rows.length && !declared.has(name)) fail('A2', `${label} — ${file} absent de la table de SKILL.md`);

    const numbers = [...byAction.values()].map((a) => a.num).filter((n) => n !== null).sort((a, b) => a - b);
    for (const f of numberingPolicy(numbers, label)) fail(f.code, f.msg);

    for (const { file } of byAction.values()) {
      const text = readFileSync(join(actionsDir, file), 'utf8');
      const h1 = text.split('\n')[0].trim();
      if (!titleIsClean(h1))
        fail('A4', `${label}/${file} — le titre porte son numéro : « ${h1} »`);

      for (const line of text.split('\n')) {
        if (!line.startsWith('|') || !line.includes('.claude/rules/')) continue;
        const { sources, targets } = ruleInstallLine(line, plugin, skill);
        for (const s of sources.filter((s) => !s.ok))
          fail('M4', `${label}/${file} — source déclarée absente : \`${s.raw}\` (cherchée en ${s.path}) — la cible annoncée ne s'écrirait pas`);
        if (sources.length && sources.every((s) => s.ok))
          for (const t of targets) installable.add(`${plugin}::${t}`);
      }
    }
  }
}

// ─── Fournisseurs de pivots ────────────────────────────────────────────────────

/**
 * M5 — `pivot-providers.md` est la table que les quatre skills `*-optimize` citent
 * pour nommer le remède quand un pivot manque. Elle **dérive** des tables d'installeurs
 * (elle le dit elle-même, §Règle de dérivation), et une dérivation faite à la main
 * dérive tout court : une ligne y survivrait à la disparition de la source qu'elle
 * suppose, et la skill recommanderait alors une commande qui n'installe rien.
 *
 * La jointure porte sur le couple (cible, plugin) et sur lui seul — le nom du fichier
 * de pivot suffit à identifier la cible, le chemin `07-quality/` étant déjà imposé par
 * la borne de forme du document. Elle s'appuie sur `installable`, donc sur des sources
 * vérifiées : M5 ne peut pas passer sur un installeur que M4 vient de déclarer creux.
 * L'ordre entre les deux est ainsi sans effet sur le verdict.
 *
 * Non vérifié ici : le sens inverse (un pivot installable absent de la table) et
 * l'unicité de la clé (deux plugins revendiquant la même stack) — chaque ligne est
 * validée isolément.
 */
const PROVIDERS = 'plugins/overcode/references/pivot-providers.md';
const PROVIDER_ROW = /^\|\s*`((?:perf|data|ap|seo)-pivots-[^`]+\.md)`\s*\|\s*`([^`]+)`/;

if (existsSync(join(ROOT, PROVIDERS))) {
  for (const line of readFileSync(join(ROOT, PROVIDERS), 'utf8').split('\n')) {
    const m = line.match(PROVIDER_ROW);
    if (!m) continue;
    const [, pivot, provider] = m;
    if (!installable.has(`${provider}::${pivot}`))
      fail('M5', `pivot-providers — \`${pivot}\` attribué à \`${provider}\` : aucune action de ce plugin n'écrit cette cible depuis une source présente`);
  }
}

// ─── Verdict ───────────────────────────────────────────────────────────────────

for (const { code, msg } of findings) console.log(`✗ [${code}] ${msg}`);
console.log(findings.length
  ? `\n✗ consistency — ${findings.length} incohérence(s)`
  : `✓ consistency — ${plugins.length} plugins, manifestes et actions cohérents`);
process.exit(findings.length ? 1 : 0);
