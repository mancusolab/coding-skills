---
name: writing-good-tests
description: Use when designing, writing, or reviewing software tests - selects meaningful oracles, test scope, isolation, and dependency boundaries to verify observable contracts.
license: CC-BY-SA-4.0
---

# Writing good tests

Choose tests that would detect a plausible violation of the requested behavior.
Match effort to risk and repository conventions; do not require new tests for every
reversible documentation or low-impact change.

## Choose the evidence

- Identify the observable contract and failure mode before writing the assertion.
  For a bug, reproduce the failure before fixing when practical; otherwise explain
  the available evidence and verify the corrected behavior afterward.
- Prefer direct unit tests for pure rules and numerical algorithms, integration
  tests for component boundaries, and a few end-to-end tests for critical journeys.
  There is no universal unit/integration ratio.
- Choose expected values from specifications, hand-computable cases, independent
  references, or justified properties. Computing expected values with the same
  implementation can make a test pass while the behavior is wrong.
- Assert outputs, state changes, errors, and required interactions. Internal call
  ordering matters only when it is a contract, such as commit before notification.
  Avoid snapshots of incidental representation and assertions on mock existence.

## Choose dependency boundaries

Use real local components when they are fast, isolated, and informative. Use fakes
or mocks to control external services, rare failures, or expensive dependencies.
Ownership alone does not determine the choice. Never require live production
services or credentials merely to obtain realistic coverage.

A double must preserve the behavior and data contract relevant to the test.
Check assumptions against a real adapter or contract test when appropriate;
do not mock away the persistence or validation being tested. Introduce wrappers
when they clarify a real boundary, not merely to satisfy a universal mocking rule.

## Control isolation and timing

Use scoped temporary resources and restore changed environment/global state.
Account for parallel execution and clean up even after failure. For generated tests,
reset mutable state for each example, not just each test function.

For asynchronous behavior, use events or bounded condition waits with informative
failures. For timers, use a controlled clock where feasible; real timing tests need
explicit tolerances and an execution environment suitable for measuring them.
Fixed sleeps are not a reliable synchronization mechanism.

Keep fixtures small enough that the tested preconditions are visible. Prefer
parameterization for meaningful behavioral partitions; avoid duplicating tests
that exercise the same path without adding evidence.

## Verify and report

Run the relevant tests using repository commands and inspect failures. When useful,
check that a regression test fails on the original bug or a representative faulty
implementation. Distinguish tests actually run from proposed coverage and report
material gaps. Coverage percentages and passing mocks alone do not establish quality.

Use `property-based-testing` when generated cases add value, and
`functional-core-imperative-shell` when tangled effects obstruct meaningful tests.
A test-writing request does not authorize a broad architecture rewrite.

Attribution and adaptation licensing: [LICENSE](LICENSE).
