# Decision document protocol

## Detection

Treat a document as a decision record when its first 20 lines contain a decision/status field, an explicit `GO`, `NO-GO`, `ACCEPTED`, `REJECTED`, or `DEFERRED` verdict, or a Spike/ADR/Decision Record heading. Extract the decision value, its subject, explicit re-evaluation conditions, and subject-linked issue references.

## Subject-matched evidence

`Superseded` means events replaced the decision, not merely that time passed. Require all of the following:

1. Weighted local score is at least 80%.
2. No critical local claim is obsolete.
3. The replacement evidence names or implements the same decision subject.
4. One of these complete conditions holds:
   - a rejected/NO-GO feature now has a concrete implementation artifact in the repository;
   - a replacement decision or artifact is implemented and its relationship to the old subject is explicit;
   - every issue explicitly governing re-evaluation is closed with a resolution that satisfies the named condition;
   - every explicit re-evaluation condition is demonstrably met by primary repository or subject-linked tracker evidence.

A closed issue, release asset, or keyword match unrelated to the decision subject is never sufficient. If only some conditions are met, retain the weighted Current/Partial/Obsolete result and report `re-evaluation: partial`.

Apply `Superseded` before `Current` once all requirements hold. Suggested action is `archive` with the replacement evidence. Do not emit the former undocumented `Archived` sub-verdict.

## Output

```yaml
decision: <value>
subject: <normalized subject>
re_evaluation: met | partial | unmet | n/a
matched_evidence:
  - <primary source and relationship>
unmatched_signals:
  - <signal rejected as unrelated or incomplete>
```
