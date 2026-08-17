#!/usr/bin/env node
// Explicit Docker/wp-env integration. This is intentionally not part of `pnpm test`.

import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';

const pnpm = process.platform === 'win32' ? 'pnpm.cmd' : 'pnpm';
const python = process.platform === 'win32' ? 'python' : 'python3';
const authAvailable = process.env.WP_EDITOR_STORAGE_STATE || process.env.WP_EDITOR_AUTH_HOOK
  || (process.env.WP_ENV_ADMIN_USER && process.env.WP_ENV_ADMIN_PASSWORD);
if (!authAvailable) {
  console.error('✗ fse-integration — fournir WP_EDITOR_STORAGE_STATE, WP_EDITOR_AUTH_HOOK ou WP_ENV_ADMIN_USER + WP_ENV_ADMIN_PASSWORD; aucun identifiant ne sera écrit dans le config');
  process.exit(2);
}
if (!process.env.WP_EDITOR_AUTH_HOOK && process.env.WP_ENV_ADMIN_USER) {
  const user = JSON.stringify(process.env.WP_ENV_ADMIN_USER);
  const password = JSON.stringify(process.env.WP_ENV_ADMIN_PASSWORD);
  process.env.WP_EDITOR_AUTH_HOOK = `document.querySelector('#user_login').value=${user};
document.querySelector('#user_pass').value=${password}; document.querySelector('#loginform').submit()`;
}
const docker = spawnSync('docker', ['info'], { encoding: 'utf8' });
if (docker.status !== 0) {
  console.error('✗ fse-integration — Docker indisponible; cette preuve ne peut pas être simulée');
  process.exit(2);
}

const root = mkdtempSync(join(tmpdir(), 'sc-php-fse-integration-'));
const theme = join(root, 'theme');
const design = join(theme, 'assets', 'css', 'design');
const patterns = join(theme, 'patterns');
const scripts = join(root, 'scripts');
for (const dir of [design, patterns, scripts, join(theme, 'templates')]) mkdirSync(dir, { recursive: true });
const put = (path, content) => writeFileSync(path, content, 'utf8');
const run = (command, args, options = {}) => {
  const result = spawnSync(command, args, { cwd: root, encoding: 'utf8',
    shell: process.platform === 'win32', ...options });
  if (result.stdout) process.stdout.write(result.stdout);
  if (result.stderr) process.stderr.write(result.stderr);
  if (result.status !== 0) throw new Error(`${command} ${args.join(' ')} (exit ${result.status}; ${result.error?.message ?? 'no spawn error'})`);
  return result.stdout.trim();
};

put(join(root, 'package.json'), JSON.stringify({ private: true, scripts: {
  'wp-env': 'wp-env', wp: 'node scripts/wp-cli.mjs'
}, devDependencies: { '@wordpress/env': 'latest' } }, null, 2));
put(join(root, '.wp-env.json'), JSON.stringify({ themes: ['./theme'], port: 8890,
  testsEnvironment: false }, null, 2));
put(join(scripts, 'wp-cli.mjs'), `import { spawnSync } from 'node:child_process';
const bin = process.platform === 'win32' ? 'pnpm.cmd' : 'pnpm';
const r = spawnSync(bin, ['wp-env', 'run', 'cli', 'wp', ...process.argv.slice(2)],
  {stdio:'inherit', shell: process.platform === 'win32'});
process.exit(r.status ?? 1);\n`);
put(join(theme, 'style.css'), '/*\nTheme Name: FSE Cascade Integration\nVersion: 1.0.0\n*/\n');
put(join(theme, 'theme.json'), JSON.stringify({ version: 3, settings: { color: { palette: [
  { slug: 'base', name: 'Base', color: '#ffffff' }, { slug: 'contrast', name: 'Contrast', color: '#142850' }
] } } }, null, 2));
put(join(theme, 'templates', 'index.html'), '<!-- wp:post-content /-->\n');
put(join(design, 'index.css'), '@import url("fse-bindings.css");\n');
put(join(design, 'fse-bindings.css'), `.btn-pinceau > .wp-block-button__link,
.wp-block-navigation .site-nav__lien .wp-block-navigation-item__content,
.wp-block-navigation .site-nav__lien.wp-block-navigation-item__content { color:#fff; background-color:#142850; }\n`);
put(join(theme, 'functions.php'), `<?php
add_action('after_setup_theme', function () { add_theme_support('editor-styles'); add_editor_style('assets/css/design/index.css'); });
$enqueue_design = static function () { wp_enqueue_style('fse-design', get_theme_file_uri('assets/css/design/index.css'), [], null); };
add_action('wp_enqueue_scripts', $enqueue_design);
add_action('enqueue_block_assets', $enqueue_design);\n`);
put(join(patterns, 'integration.php'), `<?php
/** Title: Integration blocks
 * Slug: fixture/integration-blocks
 * Categories: call-to-action
 * Inserter: yes
 */ ?>
<!-- wp:button {"className":"btn-pinceau"} --><div class="wp-block-button btn-pinceau"><a class="wp-block-button__link wp-element-button">Action</a></div><!-- /wp:button -->
<!-- wp:navigation {"overlayMenu":"never"} --><nav class="wp-block-navigation"><!-- wp:navigation-link {"label":"Accueil","url":"/","className":"site-nav__lien"} /--></nav><!-- /wp:navigation -->\n`);

let started = false;
try {
  run(pnpm, ['install', '--ignore-scripts']);
  run(pnpm, ['wp-env', 'start']);
  started = true;
  run(pnpm, ['wp', 'theme', 'activate', 'theme']);
  put(join(theme, 'navigation-content.html'),
    '<!-- wp:navigation-link {"label":"Accueil","url":"/","className":"site-nav__lien"} /-->');
  const navigationId = run(pnpm, ['wp', 'post', 'create',
    '/var/www/html/wp-content/themes/theme/navigation-content.html', '--post_type=wp_navigation',
    '--post_status=publish', '--post_title=Main-navigation', '--porcelain']).split(/\s+/).at(-1);
  put(join(theme, 'templates', 'index.html'), `<!-- wp:button {"className":"btn-pinceau"} --><div class="wp-block-button btn-pinceau"><a class="wp-block-button__link wp-element-button">Action</a></div><!-- /wp:button -->
<!-- wp:navigation {"ref":${navigationId},"overlayMenu":"never"} /-->
<!-- wp:post-content /-->\n`);
  const content = '<!-- wp:paragraph --><p>Integration fixture</p><!-- /wp:paragraph -->';
  put(join(theme, 'post-content.html'), content);
  const postId = run(pnpm, ['wp', 'post', 'create',
    '/var/www/html/wp-content/themes/theme/post-content.html', '--post_type=page',
    '--post_status=publish', '--post_title=Ownership', '--porcelain']).split(/\s+/).at(-1);
  const config = {
    reference_url: `http://localhost:8890/?page_id=${postId}`,
    implementation_url: `http://localhost:8890/?page_id=${postId}`,
    breakpoints: [{ name: 'desktop', width: 1280, height: 800 }],
    props: ['color', 'backgroundColor'],
    targets: [{ name: 'Button', mockup: '.wp-block-button__link', implementation: '.wp-block-button__link' }],
    coverage_ack: { sections: ['fixture has no headings'], reason: 'cascade-only integration fixture' },
    ownership: {
      surfaces: [
        { name: 'front', url: `http://localhost:8890/?page_id=${postId}` },
        { name: 'editor', url: 'http://localhost:8890/wp-admin/site-editor.php?postType=wp_template&postId=theme%2F%2Findex&canvas=edit',
          frame_selector: 'iframe[name=editor-canvas]', requires_auth: true,
          storage_state_env: 'WP_EDITOR_STORAGE_STATE', auth_hook_env: 'WP_EDITOR_AUTH_HOOK' }
      ],
      targets: [
        { name: 'Button', selector: '.btn-pinceau > .wp-block-button__link', class: 'btn-pinceau', prop: 'background-color', sources: ['fse-bindings.css'] },
        { name: 'Navigation', selector: '.site-nav__lien .wp-block-navigation-item__content, .site-nav__lien.wp-block-navigation-item__content', class: 'site-nav__lien', prop: 'color', sources: ['fse-bindings.css'], diagnostic_selector: '.wp-block-navigation-item__content, .wp-block-navigation-link' }
      ]
    }
  };
  put(join(root, 'measure.json'), JSON.stringify(config, null, 2));
  put(join(root, 'deviations.json'), JSON.stringify({ active: [] }));
  const measure = resolve('plugins/design/adapters/measure/measure.py');
  run(python, [measure, '--config', join(root, 'measure.json'), '--ledger-registry',
    join(root, 'deviations.json'), '--out', join(root, 'report.json')]);
  const report = JSON.parse(readFileSync(join(root, 'report.json'), 'utf8'));
  if (report.summary?.verdict !== 'CLOSED')
    throw new Error(`oracle verdict ${report.summary?.verdict}: ${(report.summary?.reasons || []).join('; ')}\n`
      + JSON.stringify(report.ownership, null, 2));
  console.log('✓ fse-integration — vrais blocs core mesurés sur front et canvas éditeur');
} catch (error) {
  console.error(`✗ fse-integration — ${error.message}`);
  process.exitCode = 1;
} finally {
  if (started) spawnSync(pnpm, ['wp-env', 'stop'], { cwd: root, stdio: 'inherit',
    shell: process.platform === 'win32' });
  const resolved = resolve(root);
  const temp = resolve(tmpdir());
  if (resolved.startsWith(temp + '\\') || resolved.startsWith(temp + '/'))
    rmSync(resolved, { recursive: true, force: true });
}
