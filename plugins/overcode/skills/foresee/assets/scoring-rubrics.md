# Dependency horizon scoring — foresee

These local scores apply only after an AIDD dependency audit. High scores mean a safer medium-term exit horizon. Every score cites dated evidence; unavailable evidence is `unknown` and excluded from coverage.

## Continuity

Combines maintainer concentration and activity trajectory without rescoring release age or version drift.

| Score | Anchor |
|---:|---|
| 9–10 | At least three active maintainers across more than one organization; ownership and recent activity are distributed and stable. |
| 7–8 | Two active maintainers or a credible organization succession path; activity shows no sustained decline. |
| 4–6 | One effective maintainer, or contribution/review activity is declining for two comparable periods. |
| 1–3 | Ownership is unclear, the sole maintainer is inactive, or upstream explicitly seeks an unfilled successor. |

## Isolation

Measures how much product code must change to remove the dependency.

| Score | Anchor |
|---:|---|
| 9–10 | Product code uses one tested adapter or standard interface; replacement is localized. |
| 7–8 | A small number of cohesive modules import the dependency; migration boundaries are evident. |
| 4–6 | Direct imports span several domains and package-specific types cross boundaries. |
| 1–3 | Framework-level or pervasive imports, generated schemas, or lifecycle hooks make removal repository-wide. |

## Exit options

Combines credible alternatives with the estimated migration work.

| Score | Anchor |
|---:|---|
| 9–10 | A maintained drop-in or standards-based alternative exists and a migration can be completed in hours. |
| 7–8 | Multiple maintained alternatives exist; migration is bounded to days with known mapping. |
| 4–6 | One imperfect alternative exists; migration needs architectural changes or weeks of work. |
| 1–3 | No maintained alternative or export path exists; replacement implies a product or platform rewrite. |

## Coverage and horizon

- Coverage is `<known dimensions>/3`; `unknown` never becomes a midpoint.
- Compute an equal-weight mean only with at least two known dimensions.
- Interpret mean `8–10` as resilient, `5–7.9` as watch, and `<5` as exit risk.
- Always display the individual dimensions so the mean cannot hide low continuity or high lock-in.
