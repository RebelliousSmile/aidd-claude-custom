# Rust command facade

Choose from existing, versioned project mechanisms:

1. Existing task runner or project binary, if already configured and proven.
2. Workspace `xtask` binary for non-trivial release logic.
3. A `.cargo/config.toml` alias such as `deploy-prod = "run --package xtask -- deploy prod"` when the repository owns an xtask.

Do not claim Cargo natively supports colon scripts, install a global tool, or hide the full procedure in an alias. The alias is a memorable facade; the versioned project code owns arguments, exit propagation, preflight, proof and recovery. Record the exact executable command (for example `cargo deploy-prod`) in the contract and preserve an existing divergent alias until arbitration.
