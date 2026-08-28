# Rust delivery scenarios

| Scenario | Expected behavior |
| --- | --- |
| Single binary | Identify binary, source and checksum, then retain the previous release. |
| Workspace xtask | Use the versioned xtask through a Cargo alias and relay arguments/exits. |
| Cross target unknown | Stop and request a proven builder; produce no artifact target. |
| SQLx or Diesel | Use only detected migration configuration before pointer switch. |
| rusqlite only | Require a project-owned migration mechanism. |
| Migration fails | Do not switch or restart; preserve the current release. |
| Health fails | Restore the previous pointer and report recovery proof. |
