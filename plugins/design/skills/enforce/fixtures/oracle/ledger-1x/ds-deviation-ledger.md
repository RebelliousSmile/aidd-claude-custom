# Deviation ledger — 1.x fixture (migration input)

> Markdown ledger a 1.x project keeps by hand. `migrate-contract.py --ledger` converts it to
> `deviations.json`. Three blocks exercise the mapping: a complete entry, one with an expiry,
> and one whose contract value is unparseable — reported as an anomaly, never dropped.

## Entries

### DEV-001 — Card title adopts the shared fluid type scale

- date:          2026-06-15
- component:     c.card-title
- selector(s):   .mock-card__title ↔ .card__title
- breakpoint:    mobile
- mockup value:  fontSize = 16px
- contract value:fontSize = 17px (clamp from the shared body scale)
- justification: the mockup hand-tuned 16px on mobile only; adopting the single fluid body
                 token removes a one-off breakpoint override and keeps every title on one
                 scale. +1px at 375 is below the perceptual threshold.
- gate evidence: fidelity gate, mobile, title fontSize delta +1px, no other prop affected.
- approver:      FX

### DEV-002 — Section lede keeps the token line-height, provisionally

- date:          2026-06-18
- component:     c.section-lede
- selector(s):   .mock-section__lede ↔ .section__lede
- breakpoint:    all
- mockup value:  lineHeight = 1.4
- contract value:lineHeight = 1.5 (the shared body token)
- justification: aligning on the single body line-height token drops a per-section override.
                 Provisional: revisit once the lede token is split from body.
- expires:       2026-12-31
- gate evidence: fidelity gate, all breakpoints, lede lineHeight delta +0.1, isolated.
- approver:      FX

### DEV-003 — Footer note colour, decision pending

- date:          2026-06-20
- component:     c.footer-note
- selector(s):   .mock-footer__note ↔ .footer__note
- breakpoint:    desktop
- mockup value:  color = #6b7280
- justification: the mockup grey is off the token ramp; the replacement token is not chosen
                 yet, so no contract value is recorded. The entry sanctions nothing until it is.
- approver:      FX

## Index (optional quick scan)

| id | component | breakpoint | prop | mockup → contract | approver |
|----|-----------|------------|------|--------------------|----------|
| DEV-001 | c.card-title | mobile | fontSize | 16 → 17px | FX |
| DEV-002 | c.section-lede | all | lineHeight | 1.4 → 1.5 | FX |
| DEV-003 | c.footer-note | desktop | color | pending | FX |
