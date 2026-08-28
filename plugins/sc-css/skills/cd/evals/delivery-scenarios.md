# Static delivery scenarios

| Scenario | Expected behavior |
| --- | --- |
| Pure static site | sc-css owns one facade after build/output/preview are proven. |
| JS application with CSS | Register a bounded contributor and defer root delivery to sc-js. |
| WordPress theme | Register theme assets only and defer root delivery to sc-php. |
| Unknown output | Report a gap and write no target or contract. |
| Cache policy | Revalidate HTML and preserve immutable caching for fingerprinted assets. |
| Missing sc-tiers | Stop automata with no generated fallback. |
