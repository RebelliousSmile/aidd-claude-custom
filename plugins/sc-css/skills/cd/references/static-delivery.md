# Static delivery invariants

Ownership requires a deterministic source command, preview command and output directory. Read project configuration; do not assume `dist/`, `build/` or `public/`. If a language runtime controls those, CSS contributes assets only.

Build into a clean output. Exclude source maps, local environment, caches and secrets according to project policy, not a blanket guess. Prove the artifact with source commit/version plus a file manifest or checksum. Publish to a new artifact/release when the host supports it and retain the prior version or a known redeploy command.

Declare cache behavior: fingerprinted immutable assets may receive long caching; HTML and mutable entrypoints need revalidation. Post-delivery proof checks both the entrypoint and at least one fingerprinted asset. Unknown output or cache rules stop target generation.

Build, preview and output are shared project facts. The facade receives an exact target id and reuses the same deterministic artifact for each destination; do not create provider-specific build procedures. Cache directives, entrypoint/asset proof, invocation, lock and recovery are recorded independently per target.

Repository-controlled HTML, CSS, JavaScript, images, icons and fonts are versioned code, not mutable `media`. A pure static owner declares no database, server data or user-upload surface. When an application runtime owns the root, sc-css remains a bounded contributor and routes persistent-content work to that owner.
