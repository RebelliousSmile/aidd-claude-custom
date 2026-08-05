#!/usr/bin/env node
// harness-runtime-check.mjs — execute the JS of a generated maquette, do not grep it.
//
// The selftest asserts on the TEXT of the generated file. A generator that emits a
// syntactically dead <script> still satisfies every one of those assertions: measured on a
// copy carrying an unbalanced brace in setViewport, the selftest printed ALL GREEN / exit 0
// while the produced file answered `typeof setPage === "undefined"` in a browser. This file
// closes that: the two control scripts are evaluated, and the contract the fidelity oracle
// calls (window.setPage / window.setViewport) is exercised.
//
// stdlib only — the repo has no node_modules and `pnpm test` has no dependency.
// Exit space 0 / 1, like the selftest that calls it. Never 2: that space belongs to
// harness.py (references/harness-contract.md).
//
// Usage: node harness-runtime-check.mjs <file.html> [--expect-pages home,contact]

import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const file = argv.find((a) => !a.startsWith('--'));
const expectIdx = argv.indexOf('--expect-pages');
const expectPages =
  expectIdx === -1 ? [] : String(argv[expectIdx + 1] || '').split(',').map((s) => s.trim()).filter(Boolean);

if (!file) {
  console.error('usage: harness-runtime-check.mjs <file.html> [--expect-pages a,b]');
  process.exit(1);
}

const fail = (msg) => {
  console.error(`FAIL runtime ${file}: ${msg}`);
  process.exit(1);
};

let html;
try {
  html = readFileSync(file, 'utf8');
} catch (e) {
  fail(`unreadable: ${e.message}`);
}

// ─── Extract the control scripts ─────────────────────────────────────────────
// Comments FIRST. The template's LLM framing block quotes `<script>` literally inside a
// <!-- … --> (harness.py, RESPONSIVE note): a naive match opens there and reports a
// SyntaxError on a perfectly healthy file.
const stripped = html.replace(/<!--[\s\S]*?-->/g, '');

// A <script> carrying attributes is a script this checker does not evaluate. Passing it
// silently would rebuild the very blind spot this file exists to close.
const attributed = stripped.match(/<script\s[^>]*>/i);
if (attributed) fail(`a <script> with attributes is not covered by this check: ${attributed[0]}`);

const bodies = [...stripped.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]);
if (bodies.length < 2) {
  fail(`${bodies.length} <script> body/bodies found, the harness declares 2`);
}

// ─── DOM stub ────────────────────────────────────────────────────────────────
// Exactly what the harness JS touches, and nothing more: an unstubbed API must throw so a
// future addition to the control scripts fails loudly instead of passing unmeasured.
const classList = () => {
  const set = new Set();
  return {
    _set: set,
    add: (...c) => c.forEach((x) => set.add(x)),
    remove: (...c) => c.forEach((x) => set.delete(x)),
    contains: (c) => set.has(c),
    toggle: (c, on) => (on === undefined ? (set.has(c) ? set.delete(c) : set.add(c)) : on ? set.add(c) : set.delete(c)),
  };
};
const el = (extra = {}) => ({
  innerHTML: '',
  scrollTop: 0,
  classList: classList(),
  attributes: {},
  setAttribute(n, v) { this.attributes[n] = v; },
  getAttribute(n) { return this.attributes[n]; },
  addEventListener() {},
  ...extra,
});

const container = el();
const frame = el();
const stage = el();
const select = el({ value: '' });
const buttons = ['desktop', 'tablet', 'mobile'].map((v) => el({ dataset: { viewport: v } }));

const document_ = {
  getElementById(id) {
    if (id === 'page-container') return container;
    if (id === 'preview-frame') return frame;
    if (id === 'page-select') return select;
    throw new Error(`unstubbed getElementById(${JSON.stringify(id)})`);
  },
  querySelector(sel) {
    if (sel === '.preview-stage') return stage;
    throw new Error(`unstubbed querySelector(${JSON.stringify(sel)})`);
  },
  querySelectorAll(sel) {
    if (sel === '.viewport-btn') return buttons;
    throw new Error(`unstubbed querySelectorAll(${JSON.stringify(sel)})`);
  },
};

const sandbox = {
  document: document_,
  location: { hash: '' },
  history: { replaceState() {} },
  console: { error() {}, warn() {}, log() {} },
  encodeURIComponent,
  decodeURIComponent,
  String, Object, Array, JSON, Error, RegExp, Math, Set, Map,
};
sandbox.window = sandbox;         // window === the sandbox global, as in a browser
sandbox.globalThis = sandbox;

const ctx = vm.createContext(sandbox);

bodies.forEach((body, i) => {
  try {
    vm.runInContext(body, ctx, { filename: `${file}#script${i + 1}` });
  } catch (e) {
    // An unbalanced brace reports at end of input, with no useful position — the script
    // index is the locator that actually helps.
    fail(`script ${i + 1} did not evaluate: ${e.name}: ${e.message}`);
  }
});

// ─── The contract the fidelity oracle calls ──────────────────────────────────
const check = (label, cond, detail = '') => {
  if (!cond) fail(`${label}${detail ? ` — ${detail}` : ''}`);
};

check('window.setPage is not a function', typeof sandbox.window.setPage === 'function');
check('window.setViewport is not a function', typeof sandbox.window.setViewport === 'function');
check('#page-container is empty after init()', container.innerHTML.length > 0);

try {
  sandbox.window.setViewport('mobile');
} catch (e) {
  fail(`setViewport('mobile') threw: ${e.name}: ${e.message}`);
}
check("setViewport('mobile') did not set the mobile class", frame.classList.contains('mobile'));
check(
  "setViewport('mobile') left an aria-pressed unset",
  buttons.every((b) => b.getAttribute('aria-pressed') !== undefined),
);
sandbox.window.setViewport('desktop');
check("setViewport('desktop') left the mobile class on the frame", !frame.classList.contains('mobile'));

// An unknown key renders a state, never propagates an exception: measure.py calls
// window.setPage(key) unguarded and must get a DOM back.
try {
  sandbox.window.setPage('a-key-no-page-declares');
} catch (e) {
  fail(`setPage(unknown) threw instead of rendering: ${e.name}: ${e.message}`);
}
check(
  'an unknown page key does not render the not-found state',
  container.innerHTML.includes('Page introuvable'),
  container.innerHTML.slice(0, 120),
);

for (const key of expectPages) {
  sandbox.window.setPage(key);
  check(`page "${key}" renders nothing`, container.innerHTML.length > 0);
  check(`page "${key}" did not sync the selector`, select.value === key, `select.value = ${select.value}`);
}

const pagesNote = expectPages.length ? `, pages ${expectPages.join('/')}` : '';
console.log(`ok   runtime: ${bodies.length} scripts, setPage/setViewport live${pagesNote}`);
process.exit(0);
