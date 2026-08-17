---
name: log-analysis
description: >-
author: François-Xavier Guillois
version: 0.5.2
vibe_version: ">=1.0.0"
permissions:
  - bash
  - files
tags:
  - backend
  - audit
  - rust
---

Read [host portability](../../references/host-portability.md) before resolving plugin files, invoking sibling skills, or persisting project guidance.

# Log Analysis

Inspects Rust application logs from any environment — local filesystem, Docker containers, or a remote server via SSH. Produces a raw tail, filtered error list, pattern search, or period summary. Handles tracing subscriber output, env_logger, actix-web/axum request logs, and panic backtraces.

## Available actions

| # | Action | Role | Input |
|---|--------|------|-------|
| 01 | `tail` | Display the last N lines from a log source | env, source, optional lines |
| 02 | `parse-errors` | Extract and group panics, ERROR-level events, and 5xx responses | env, source, optional since |
| 03 | `search` | Search for a pattern, span name, or HTTP status code | pattern, optional env, source |
| 04 | `summarize` | Period digest: error rate, top panics, span timing summary | optional env, optional since |

## Default flow

Non-sequential — dispatch based on user intent:

- "tail / show / last lines / recent logs / check logs" → `tail`
- "errors / panics / error list / backtraces" → `parse-errors`
- "find / search / grep / [specific pattern or span or status code]" → `search`
- "summary / digest / report / stats" → `summarize`
- Env not specified → ask: `local`, `docker`, or `prod`?
- No clear intent → `tail` on `app`, then offer `parse-errors`

## Transversal rules

- Never print or log SSH credentials, passwords, or key paths.
- Always show timestamps in output.
- Truncate individual log lines to 300 chars to avoid flooding context.
- When errors are found, always suggest a likely fix or next investigation step.
- Default `env` is `docker` when Docker is detected in the project; otherwise `local`.
- For `prod`: if no SSH host is configured, ask user for `user@host` before proceeding.
- Panic backtraces must be kept intact — never truncate mid-frame.
- JSON-format tracing output (from `tracing-subscriber` JSON layer): parse as NDJSON before displaying.

## References

- `references/environments.md` — env detection, standard log paths, SSH config pattern
- `references/log-formats.md` — tracing/env_logger/actix-web log formats and parsing patterns
