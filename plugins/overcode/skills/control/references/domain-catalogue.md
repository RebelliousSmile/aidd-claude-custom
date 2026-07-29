# Domain catalogue

A floor of detection, never an inventory. Each entry below is a **default proposal** - a name, a level, and the literal terms `06-align` matches against the codebase to suggest it - never a verdict on the project. The user confirms, overrides, renames, or discards every proposal before it is written to `<project>/aidd_docs/memory/testing-domains.md`. No domain here is universal: a project may have none of them, several besides, or the same behavior split across two of its own.

Resolution terms are **literal substrings, matched case-insensitively**, and **a domain's own name is one of its terms** - the column below lists what the name alone would miss, never a set that replaces it. They are matched **over paths and declared identifiers, never over an arbitrary occurrence in a file's body**: a file mentioning `Token` in an import or a log string does not thereby have its behaviour in the `auth` column, and counting such occurrences multiplies the resolved set several-fold for no gain in truth. No regex, no stemming, no synonym expansion - a term that does not appear verbatim (modulo case) does not match. This is deliberately a floor: it is expected to under-match rather than to guess, and whatever it misses is residue for the user to name by hand.

| Domain | Default level | Resolution terms | Typical paths |
|---|---|---|---|
| `auth` | critical | Login, Signin, Signup, Register, Session, Password, Token, Credential | `auth/**`, `session/**`, `login/**` |
| `authorization` | critical | Role, Permission, Guard, Policy, Acl, Access | `permissions/**`, `guards/**`, `policies/**` |
| `payment` | critical | Payment, Checkout, Invoice, Billing, Charge, Refund, Subscription, Stripe, Paypal | `payment/**`, `billing/**`, `checkout/**` |
| `checkout` | critical | Cart, Order, Checkout, Fulfillment | `cart/**`, `order/**`, `checkout/**` |
| `data-persistence` | critical | Migration, Delete, Purge, Bulk, Transaction, Rollback | `migrations/**`, `db/**` |
| `account` | structuring | Account, Profile, Settings | `account/**`, `profile/**`, `user/**` |
| `onboarding` | structuring | Onboarding, Welcome, Invite, Setup | `onboarding/**`, `setup/**` |
| `integrations` | structuring | Webhook, Sync, Connector, Import, Export | `integrations/**`, `webhooks/**` |
| `notifications` | ordinary | Notification, Email, Mailer, Push, Sms | `notifications/**`, `mail/**` |
| `search` | ordinary | Search, Query, Filter, Index | `search/**` |
| `upload` | ordinary | Upload, Media, Attachment, File | `upload/**`, `media/**` |
| `reporting` | ordinary | Report, Export, Dashboard, Analytics | `reporting/**`, `analytics/**` |

The **default level is a starting point, stated so `06-align` has something concrete to put in front of the user - not a claim about what any given project's failure actually costs.** A project may run `payment` at `structuring` because it only ever handles pre-authorized amounts elsewhere, or promote `search` to `critical` because it is the entire product. The catalogue proposes; what the user confirms is the **entry written to `testing-domains.md`**, and that written decision is what every other action reads.

**Outside that write, a catalogue hit is taken, not asked.** An action handed a `domain` argument the project has not frozen reads this table's default level, cites the catalogue as its source, and runs - the argument was already the user's declaration of the name, and the level is reported overridable like any other value rather than put as a question. A name matching nothing here is asked open, never guessed. Nothing so resolved is persisted; only `06-align` writes. The distinction is the whole use of a floor: a floor that stops the run to have itself confirmed is a floor nobody keeps.

A file matching no term in this catalogue is **residue**, not `hors-domaine`: residue is unclassified and gets rescanned on the next `06-align` pass; `hors-domaine` is a **confirmed, frozen answer** - the user has looked at a path and said it carries none of the project's declared domains. The two must never be conflated - one is pending work, the other a closed one.
