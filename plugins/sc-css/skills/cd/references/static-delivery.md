# Static delivery invariants

Ownership requires a deterministic source command, preview command and output directory. Read project configuration; do not assume `dist/`, `build/` or `public/`. If a language runtime controls those, CSS contributes assets only.

Build into a clean output. Exclude source maps, local environment, caches and secrets according to project policy, not a blanket guess. Prove the artifact with source commit/version plus a file manifest or checksum. Publish to a new artifact/release when the host supports it and retain the prior version or a known redeploy command.

Declare cache behavior: fingerprinted immutable assets may receive long caching; HTML and mutable entrypoints need revalidation. Post-delivery proof checks both the entrypoint and at least one fingerprinted asset. Unknown output or cache rules stop target generation.
