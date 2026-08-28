# Python command facade

Preserve the detected manager in this order of evidence, not preference:

| Existing evidence | Facade pattern |
| --- | --- |
| `uv.lock` / uv project | a declared uv command such as `uv run scripts/deploy.py prod` |
| Poetry configuration | an existing Poetry script or `poetry run python scripts/deploy.py prod` |
| Pipenv configuration | an existing Pipenv script or `pipenv run python scripts/deploy.py prod` |
| requirements/venv only | the documented environment's Python invocation, after user agreement on how to expose it |

Do not add uv, Poetry, Pipenv, Make, Poe or another task runner only to mimic package scripts. Keep a versioned deployment module/script as the stable implementation and record its full invocation in `deploy/contract.json`. Existing divergent commands require arbitration, never silent replacement.

The facade accepts a declared target id and operation; provider-specific behavior belongs to target metadata, not to a second deployment implementation. Each target records its exact invocation, working directory, process order, migration command, health proof and restart procedure. Server and automata may therefore call the same facade through different envelopes without changing its semantics.

Acquire a lock scoped to the target id and lifecycle revision. A failure from update, migration, media delta, restart or health proof must be returned unchanged. Never fall back to another target, and never create target-to-target flows.
