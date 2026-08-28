# Provider delivery scenarios

| Scenario | Expected behavior |
| --- | --- |
| SSH | Require supported primitives and secret names, then call the project facade only. |
| Railway | Preserve project command and fail before write if CLI/project link is absent. |
| Heroku | Preserve chosen deployment strategy and keep the API key out of files/output. |
| GitHub without trigger | Generate `workflow_dispatch`, not push. |
| GitLab explicit push | Generate push rules only because the contract declares them. |
| Missing/stale contract | Write no automation and name the producer correction required. |
| Failing facade | Preserve the non-zero CI result and surface contract recovery. |
