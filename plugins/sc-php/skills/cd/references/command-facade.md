# PHP command facade

Use the project's existing root package-manager facade. Detect it from versioned commands and operational documentation instead of inferring it from the implementation language:

- preserve `composer deploy:prod` when Composer already owns root project operations;
- preserve `pnpm deploy:*`, `npm run deploy:*`, or an equivalent native facade when that is the established owner, including WordPress projects whose delivery implementation is PowerShell, shell, or JavaScript;
- do not add `composer.json` solely to wrap an already coherent non-Composer facade;
- package-manager entries remain thin aliases to one versioned project-owned script or command.

`deploy:db` and `deploy:sync` exist only for defined safe scopes. A command name is not proof of scope: inspect the owning script. In particular, a `deploy:theme` alias that also transfers plugins or uploads must be renamed, split, or reported as a semantic conflict.

Reconcile existing scripts before editing. Preserve targets, host-specific workarounds, and custom behavior. If old and new semantics conflict, show the difference and stop for arbitration rather than creating a second producer.

The project contract must match the detected manager, command, and directory exactly. Preflight, exclusions, proof, and recovery live behind the facade, never solely in CI.
