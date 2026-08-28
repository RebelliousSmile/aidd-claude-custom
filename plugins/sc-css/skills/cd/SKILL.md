---
name: cd
description: Standardizes local preview and production delivery for pure static sites while keeping CSS bounded inside composite applications. Use when the user wants static setup, hosting configuration, or delivery automation. Not for owning an application runtime.
argument-hint: project setup | production host | automation target
---

# CSS CD

```mermaid
flowchart LR
  local_request([project setup]) --> local --> local_ready([local ready])
  server_request([production host]) --> local_check{local verified}
  local_check -->|no| local --> server
  local_check -->|yes| server --> server_ready([production configured])
  automation_request([automation target]) --> contract_check{current contract}
  contract_check -->|no| stopped([stopped])
  contract_check -->|yes| automata --> delegated([automation delegated])
```

## Actions

Run the flow above. Read only the next action file.

| Action | Does |
| --- | --- |
| local | reconcile a bounded static build and preview |
| server | reconcile one static production facade and contract |
| automata | validate and delegate the existing facade |

## Transversal rules

- Read [host portability](../../references/host-portability.md), [the common contract](../../references/cd-contract.md), and [the project schema](../../references/cd-project-contract.schema.json) before acting.
- Let sc-css own the root only for a pure static site with deterministic build, preview, and output evidence.
- Keep CSS as a bounded contributor when a language runtime owns the application.
- Never create another environment, contact production during configuration, or invent an unsupported output or provider.
