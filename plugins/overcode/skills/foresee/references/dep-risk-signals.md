# Prospective dependency signals — foresee

This catalogue intentionally excludes vulnerabilities, licences, outdated versions, compatibility, permissions, and transitive depth. Those belong to the preceding AIDD `dependencies` audit.

| Dimension | Signal | Observation method | Required source |
|---|---|---|---|
| Continuity | Active-maintainer concentration | Count distinct people who merged/released or reviewed accepted work in the latest representative six-month window; do not use a registry owner list alone | Upstream commits, releases, or accepted PRs with observation date |
| Continuity | Organization concentration | Identify whether active maintainers share one employer/organization when public evidence exists | Upstream profiles or governance document |
| Continuity | Activity trajectory | Compare the latest two equal six-month windows for accepted changes, releases, and maintainer participation | Upstream history with both window dates |
| Continuity | Succession path | Look for governance, transfer policy, co-maintainers, or an explicit unfilled maintainer request | Upstream governance/issues |
| Isolation | Direct usage surface | Count non-generated project files importing/configuring the dependency and group them by product domain | Repository search with excluded paths stated |
| Isolation | Boundary leakage | Check whether package-specific types, decorators, schemas, or lifecycle hooks cross the adapter/module boundary | Concrete repository locations |
| Isolation | Replacement seam | Verify that product code uses an adapter or standard interface exclusively | Adapter and consumer locations |
| Exit options | Maintained alternatives | Name alternatives only with current maintenance evidence and a compatible required feature set | Official repositories/docs with observation date |
| Exit options | Data/export portability | Identify standard export formats and irreversible vendor/package state | Official export/migration documentation |
| Exit options | Migration effort | Estimate touched domains and discrete migration steps from local usage; state assumptions rather than person-day precision | Repository evidence plus explicit assumptions |

## Unknown rule

If a source cannot be accessed or does not establish the signal, record `unknown — <reason>`. Do not infer maintainer employment, roadmap intent, alternative compatibility, or migration duration from popularity metrics.
