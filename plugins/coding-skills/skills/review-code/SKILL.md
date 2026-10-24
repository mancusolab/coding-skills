---
name: review-code
description: Use when reviewing a diff, pull request, implementation milestone, or existing code for actionable correctness and regression issues against requirements and repository contracts.
license: CC-BY-SA-4.0
---

# Review code

Produce evidence-backed findings about the requested scope. A review request
alone authorizes inspection and appropriate verification, not code changes.
When called during authorized implementation, fixes within that scope may proceed.

## Establish scope

1. Identify the requested change or code surface and its requirements. For a PR,
   inspect its actual base/head or merge base. Do not assume `HEAD~1` is the base.
   For local work, include staged and unstaged diffs and relevant untracked files.
   If the base or intended scope cannot be inferred safely, clarify it.
2. Read repository instructions, changed code, important callers, and relevant
   tests. Use surrounding context to evaluate behavior; a diff alone may omit
   the contract that makes a change correct or incorrect.
3. Apply only relevant bundled domain skills, using the
   [domain routing table](../design-software/references/domain-routing.md).
   No specialized reviewer installation or scientific plan is required.

## Evaluate the behavior

- Check requirements and compatibility, boundary validation, errors, state and
  resource lifetime, data integrity, concurrency, and security where affected.
- Inspect whether tests exercise the changed contract and plausible regressions.
  Run focused checks when feasible; report unavailable tests and assumptions.
  Passing tests alone do not establish that all requirements are met.
- Trace a suspected issue to a reachable condition and concrete consequence.
  Distinguish introduced regressions from pre-existing problems. For a diff
  review, flag existing defects only when the change exposes or worsens them.
- Prioritize actionable defects and violations of explicit repository contracts.
  Do not demand stylistic rewrites, speculative abstractions, or unrelated
  hardening. Separate optional suggestions from findings requiring correction.
- When independent review is useful and delegation is available and permitted,
  provide the reviewer with the requirements and exact scope. Do not prescribe
  its conclusions. Otherwise review directly and label the review accurately.

## Report and resolve

Lead with findings, ordered by severity. Each finding includes:

- A short title and severity based on concrete impact.
- A precise file/line location in the reviewed code.
- The triggering condition, consequence, and supporting evidence.
- A bounded correction or the contract that needs clarification.

If no actionable findings were found, say so and report the scope and testing
limits. Do not turn that statement into a guarantee of correctness.

For a review-only request, stop after reporting. For authorized implementation,
evaluate findings against the code, fix supported issues within scope, and
re-review the affected changes. Reject unsupported findings with evidence rather
than changing code to satisfy a reviewer mechanically. Do not enter an endless
zero-findings loop: if review repeats without new evidence, report the unresolved
disagreement or blocker. Track deferred issues and the user's explicit acceptance
where applicable; never silently drop them or report full completion with
unresolved required behavior.

Attribution and adaptation licensing: [LICENSE](LICENSE).
