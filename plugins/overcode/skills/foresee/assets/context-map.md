# Dependency horizon context — foresee

Document and code context selection belongs to their delegated AIDD skills. Load this reference only for `analyze-dep` after the AIDD dependency audit has produced its report.

| Target | Required local context | Budget |
|---|---|---:|
| Named package | Project manifest and lockfile entry; files importing or configuring the package; architectural memory/rules that name it; upstream repository metadata needed by the horizon signals | 10 local files plus sourced upstream metadata |
| Manifest | AIDD dependency report; manifest and lockfile; local usage search for the dependencies selected from that report | 5 dependencies by default |

Exclude `node_modules`, vendored source, build output, and generated files from local-usage counts. A wrapper counts as isolation only if product code depends on the wrapper rather than also importing the package directly.

Do not reload or recompute the baseline audit's vulnerability, licence, outdated-version, transitive-depth, or compatibility evidence.
