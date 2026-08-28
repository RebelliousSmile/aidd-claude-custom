# PHP command facade

Prefer Composer's native scripts: `composer deploy:prod` invokes one versioned project-owned script or command. `deploy:db` and `deploy:sync` exist only for defined safe scopes. WordPress may continue to use `pnpm wp` internally because it is the established wp-env wrapper; it is not a root deployment facade.

Reconcile existing scripts before editing. An old `scripts/deploy.mjs` from `setup wire-deploy` is migrated behind Composer or retained as the owned implementation. Preserve targets and custom behavior. If old and new semantics conflict, show the difference and stop for arbitration rather than creating a second producer.

The project contract must match the Composer command and directory exactly. Preflight, exclusions, proof and recovery live behind the facade, never solely in CI.
