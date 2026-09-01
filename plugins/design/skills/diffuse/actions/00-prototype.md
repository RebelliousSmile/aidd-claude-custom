# Prototype

## Input

- A component or ungoverned preview brief. A structured wireframe board with a manifest or pillars belongs to `design:wireframes`.
- An explicit output target and optional implementation language.

## Output

A scoped prototype plus a delivery note that states `governance: none`, `conformity: not assessed`, and the evidence that was not available without a frozen contract.

## Process

1. **Bound.** Extract only the requested component, variants, content slots, interaction states, and responsive expectations from the local brief.
2. **Render.** Produce the smallest preview or target-language artifact that demonstrates those requirements without creating design-system contract files.
3. **Check.** Verify semantic structure, keyboard and focus behavior, declared states, responsive behavior, and any measurable contrast available in the prototype.
4. **Label.** Deliver the artifact as ungoverned and state that no contract conformity or maturity was assessed.

## Test

| Case | Pass |
| --- | --- |
| `release.json` is absent | no contract artifact is created and no green gate is claimed |
| the brief requests one component | no unrelated design-system lifecycle capability is invoked |
| the prototype contains an interactive control | keyboard, focus, and disabled or error states are addressed or named as missing |
