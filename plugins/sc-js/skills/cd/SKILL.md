---
name: cd
description: Standardizes local setup and production delivery for JavaScript while preserving the detected package manager, framework, and data strategy. Use when the user wants project setup, production hosting, or delivery automation. Not for generic CI or extra environments.
argument-hint: project setup | production host | automation target
---

# JavaScript CD

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
| local | reconcile the detected JavaScript runtime locally |
| server | reconcile one native production facade and contract |
| automata | validate and delegate the existing facade |

## Transversal rules

- Read [host portability](../../references/host-portability.md), [the common contract](../../references/cd-contract.md), and [the project schema](../../references/cd-project-contract.schema.json) before acting.
- Reuse the existing sniff classification instead of maintaining a second stack taxonomy.
- Keep one root owner and limit JavaScript to a bounded workspace when another application stack owns the project.
- Never create another environment, replace a user command silently, or deploy merely because configuration was requested.
