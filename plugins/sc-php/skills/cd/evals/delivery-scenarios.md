# PHP delivery scenarios

| Scenario | Expected behavior |
| --- | --- |
| WordPress local | Reuse wp-env wrappers and never reset, destroy or import. |
| WordPress code release | Exclude uploads, database and secrets unless another explicit operation is selected. |
| Ambiguous sync | Ask for code/database/content/media scope and run no remote command. |
| Database push | Require backup, dry-run/review, confirmation, proof and recovery. |
| Legacy deploy.mjs | Preserve custom targets behind one Composer facade; create no concurrent script. |
| Laravel/Symfony | Use native migrations and keep them distinct from content copying. |
| Missing sc-tiers | Stop automata and write no fallback. |
