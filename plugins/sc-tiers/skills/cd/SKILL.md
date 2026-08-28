---
name: cd
description: Configures supported hosting prerequisites and thin delivery automation from an existing validated project contract. Use when the user wants local provider emulation, production provider setup, or automation for SSH, Railway, Heroku, GitHub, or GitLab. Not for deployment logic.
argument-hint: provider setup | production provider | automation target
---

# Provider CD

```mermaid
flowchart LR
  local_request([provider setup]) --> local --> local_outcome([adapter or not applicable])
  server_request([production provider]) --> contract_check{current contract}
  contract_check -->|no| stopped([stopped])
  contract_check -->|yes| server --> provider_ready([provider configured])
  automation_request([automation target]) --> automation_check{current contract}
  automation_check -->|no| stopped
  automation_check -->|yes| automata --> generated([thin envelope generated])
```

## Actions

Run the flow above. Read only the next action file.

| Action | Does |
| --- | --- |
| local | reconcile a supported local provider adapter |
| server | reconcile bounded prerequisites for one named server target |
| automata | generate a thin envelope for one named automata target |

## Transversal rules

- Read [host portability](../../references/host-portability.md), [the common contract](../../references/cd-contract.md), and [the project schema](../../references/cd-project-contract.schema.json) before acting.
- Require a current contract from the root application or static owner before any provider or automation write.
- Own provider configuration and envelopes only and never own or redetect the deployment procedure.
- Never create another environment, collect secret values, contact production during configuration, mask a failure, or invent an unsupported provider.
- Require an exact target id when a contract declares several targets. Read only that target's phase, mode, provider, invocation, lifecycle guard, lock, secrets, proof and recovery.
- Keep unsupported status isolated to the selected target. Never aggregate paths, data, media or credentials across targets, and refuse every target-to-target flow.
