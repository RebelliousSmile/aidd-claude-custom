# Python delivery scenarios

| Scenario | Expected behavior |
| --- | --- |
| uv Django | Execute the versioned deployment script through uv and keep migrations distinct. |
| Poetry FastAPI | Preserve Poetry and the configured ASGI entrypoint. |
| Pipenv Flask | Preserve Pipenv and prove the script invocation. |
| requirements only | Ask before adding any runner or manager. |
| Celery worker | Declare process ordering and an independent health proof. |
| SQL data request | Require named scope, backup, confirmation and recovery. |
| Missing sc-tiers | Stop automata without files or fallback. |
