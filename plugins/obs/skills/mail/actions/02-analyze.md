# Analyze

Classify each email according to the two decision passes and produce the list of decisions.

## Inputs

- `file_list` — list of absolute paths of the `.md` files to analyze (from `01-scan`)
- `config` — parsed content of `mail-config.yaml`
- `prelim_report` — preliminary report from `01-scan` (ATrier/, epoch)

## Outputs

- `decisions` — structured list: for each file, `content_action` + `placement_action` + metadata
- `analyze_summary` — counters and anomalies for `05-report`

## Process

1. Display the `prelim_report` received from `01-scan` if non-empty (ATrier/ files, epoch).

2. **Delegate to a sub-agent (`model: sonnet`)** with the mission to:

   **Pre-processing:**
   - Read the YAML frontmatter of each file (from, to, date, subject, subject_hash)
   - Read the body if needed for the `summarize` taxonomy or phishing detection

   **Duplicate detection (before Pass A):**
   - Group by `(subject_hash, from, date)` → if N > 1 → exact duplicate
   - In each duplicate group: keep 1) the file with the oldest date; 2) on a tie → first alphabetically
   - Mark all other members of the group: `content_action: delete`, `duplicate: true`

   **Pass A — content decision** (decreasing priority, applied to non-duplicate files):
   1. `suppress` match (`from` address or branch contains a `suppress` rule) → `delete`
   2. `prune` match AND `date < (today - days)` → `delete`; `days: 0` = always delete
   3. `preserve` match (`from` address or branch, no contrary exception) → `intact`
   4. Thread: same `from` + `to` + normalized `subject` (without Re:/Fwd:/RE:/FW:, case ignored) shared with ≥1 other non-preserve file → `merge`
      - If `merge_by_domain: true` in config: normalize `from` to the root domain (last two segments, e.g. `mail.mondialrelay.com` → `mondialrelay.com`) before comparison; country TLDs kept (`.fr` ≠ `.com`)
   5. Otherwise → `summarize`

   **Pass B — placement decision** (independent of A):
   - File at direct root or in any `ATrier/` subfolder → `classify` toward proposed branch (level 3)
   - Already in a level-3 branch → `none`

   **Summarize taxonomy** (read body if needed):
   - `transactionnel`: livraison, commande, facture, paiement, ticket
   - `newsletter`: Kickstarter, Patreon, blog, newsletter, update
   - `notification`: login, sécurité, espace disque, alerte
   - `promotionnel`: offre, promo, réduction

   **Phishing detection**:
   - If the display name in `from` contains a known brand but the address domain does not match → `flag-phishing`
   - Default brands: google, paypal, amazon, apple, microsoft, netflix, impots, ameli, caf, pole-emploi
   - Complete with `config.phishing_brands` if present
   - Replaces the computed `content_action` with `flag-phishing`

   **Return** the list of decisions (without email content)

3. Receive the list of decisions from the sub-agent.

4. Check consistency:
   - The `merge` threads are correctly grouped (same `merge_group`)
   - No `preserve` file has `content_action: delete` (unless exact duplicate)

5. Return `decisions` and `analyze_summary` for handoff to `03-propose`.

## Decision output format

```yaml
decisions:
  - path: "C:/Users/fxgui/Public/Notes/Thunderbird/Internet/..."
    from: "expediteur@domaine.com"
    date: "2026-04-09"
    subject: "Sujet du mail"
    content_action: summarize    # delete | intact | merge | summarize | flag-phishing
    placement_action: none       # classify | none
    classify_target: null        # branche cible si placement_action=classify
    summary_type: newsletter     # transactionnel | newsletter | notification | promotionnel | null
    merge_group: null            # slug de groupe pour les threads
    duplicate: false             # true si doublon supprimé
```

## Test

- `decisions` contains one entry for each file in `file_list`.
- The `merge` threads share the same `merge_group`.
- No `preserve` file has `content_action: delete` (except `duplicate: true`).
- Duplicates have `content_action: delete` and `duplicate: true`.
- Phishing files have `content_action: flag-phishing`.
- `from`, `date`, `subject` are filled in for each decision.
- No email content appeared in the main chat.
