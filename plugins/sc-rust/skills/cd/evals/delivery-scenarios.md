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
| Two named targets | Use one xtask with distinct invocations, release roots, pointers and locks. |
| Server to automata | Preserve alias and arguments; change only the execution envelope. |
| Production data | Apply detected schema migration without copying local business data or persistent files. |
| Staging persistent files | Require a manifest delta and scoped recovery before mirror mutation. |
