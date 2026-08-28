# Reversible Rust releases

A release identity contains source commit/version, Cargo package, binary, features, profile, compilation target and artifact checksum. Cross-compilation is accepted only with a proven builder/toolchain for the server target; otherwise stop before producing a target.

Upload into a new immutable release directory. Verify checksum and configuration prerequisites, run reviewed migrations, then atomically update the current pointer and restart. Health proof follows the switch. On failed health, restore the previous pointer and service; on failed build, checksum or migration, never switch.

Retain at least the previous selectable release according to project policy. Secrets and environment-specific configuration remain outside the artifact.

Release root, immutable release directory, `current`/`previous` pointers, service identity, lock and rollback proof are namespaced by target id. A migration failure leaves that target's pointer untouched. A health failure restores only that target's previous pointer. Concurrent releases to different targets may proceed because their locks do not overlap; a failure never selects another target as fallback.
