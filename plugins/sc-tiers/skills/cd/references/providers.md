# Supported provider primitives

| Provider | Required primitive | Contract/secret names | Failure boundary |
| --- | --- | --- | --- |
| Classic SSH | system `ssh` plus project-selected transfer/release commands | e.g. `DEPLOY_HOST`, `DEPLOY_USER`, key supplied by agent/CI | missing host/user/path or command stops before remote access |
| Railway | existing Railway project and supported CLI/API workflow | e.g. `RAILWAY_TOKEN`, project/service identifiers without secret values | missing CLI/project link stops configuration |
| Heroku | existing Heroku app and supported CLI/git/container workflow | e.g. `HEROKU_API_KEY`, app name | missing CLI/app/strategy stops configuration |

This is an allow-list. Unknown providers remain unsupported until a tested adapter is added. Provider files contain only identifiers safe to version and references to environment/secret-store names. The project facade continues to own build, migrations, deployment proof and recovery.

Local emulation is normally N/A for SSH, Railway and Heroku unless the project already uses an official supported local primitive. Do not simulate production semantics with an unrelated container.
