---
name: mail
description: Triages emails exported as Markdown — applies the rules of mail-config.yaml to a mailbox branch, sets aside what the configuration condemns into a dated archive, and reports what needs human arbitration. Runs as a deterministic script, no model call. Use when the user asks to sort, clean or triage a mail branch.
author: fxgui
version: 0.38.0
vibe_version: ">=1.0.0"
permissions:
  - bash
tags:
  - documentation
  - obsidian
  - notes
---

Read [host portability](../../references/host-portability.md) before resolving plugin files, invoking sibling skills, or persisting project guidance.

# Mail

Triages emails exported as Markdown. The scope is **a branch passed as argument** — never a hardcoded mailbox path.

The triage is a rules engine, not a judgement: `${OBS_PLUGIN_ROOT}/scripts/mail.py` reads `mail-config.yaml` and applies it. What the configuration does not settle stays where it is and goes to the report for the user to arbitrate. Reading an email to decide what it means, summarising a thread, drafting a reply — none of that is scripted and none of it lives here.

## Commands

| Command | Role | Invocation |
| --- | --- | --- |
| `triage` | Scan the branch, apply the rules, archive what is condemned, report | `python mail.py triage <branche> [--config <chemin>] [--reprocess] [--apply]` |
| `init-config` | Write a blank, commented `mail-config.yaml` at the branch root | `python mail.py init-config <branche> [--apply]` |

## Default flow

`obs:mail [branche]` → `triage`. If the branch has no `mail-config.yaml`, run `init-config` first, then let the user fill in the rules — an empty configuration decides nothing and sends every email to arbitration.

Always run `triage` without `--apply` first and show the plan.

## Configuration

`mail-config.yaml` lives at the branch root. Rule precedence: `exceptions` > `preserve` > `suppress` > `prune` > arbitration.

| Key | Effect |
| --- | --- |
| `preserve` | `senders` (`domain:` or `address:`) and `branches` kept untouched |
| `suppress` | `senders` and `branches` set aside |
| `exceptions` | `address:` + `action: preserve\|suppress`, overrides everything else |
| `prune` | `branch:` or `sender:` + `days:` — set aside past that age |
| `phishing_brands` | brand names to watch in display names |

## Ce que le script garantit

- **Nothing is deleted.** What the configuration condemns is *moved* into `.archive/AAAA-MM-JJ/`, relative path preserved; the archived copy is marked `processed: true`. Reverting is a move back.
- **Nothing without `--apply`.**
- **Scope exclusions.** `.archive/`, `_drafts/`, `mail-sessions.log.md`, and anything already `processed: true` are out of scope — `--reprocess` brings the last category back in.
- **Preliminary report.** Files under an `ATrier/` directory and files with no usable date are flagged before any decision; an age rule never bites an email whose date cannot be read.
- **Untouched means untouched.** An email matched by `preserve` gets no frontmatter edit at all.
- **Phishing is signalled, never acted on.** A known brand in the display name with a registrable domain that is not that brand is reported as a suspicion — the script moves nothing on that basis.

## External data

- `${OBS_PLUGIN_ROOT}/scripts/mail.py` — the implementation. `--help` on any subcommand.
- `<branche>/mail-config.yaml` — the rules, written by the user.
- `${OBS_PLUGIN_ROOT}/references/email-md-format.md` — naming and frontmatter convention of the converted emails the script reads.
