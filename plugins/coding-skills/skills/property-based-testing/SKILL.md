---
name: property-based-testing
description: Use when designing or reviewing tests for transformations, serialization, numerical contracts, or stateful operations that benefit from generated inputs and invariant checks.
license: CC-BY-SA-4.0
---

# Property-based testing

Use generated cases when they explore meaningful variation beyond a few examples.
Start with the contract and a falsifiable property, then choose a generator.
Do not add a property-testing dependency for a trivial assertion that examples cover.

## Choose an independent property

- Select roundtrip, invariant, idempotence, reference comparison, or state-machine
  properties that follow from the actual specification. See the
  [property catalog](references/property-catalog.md) for selection and pitfalls.
- Properties are complementary; there is no universal ranking that makes roundtrip
  stronger than every invariant. Two mutually incorrect converters can roundtrip.
- Keep the oracle independent of the implementation. Avoid reproducing the same
  algorithm in the assertion or checking only that a mocked result was returned.
- Separate valid-input properties from invalid-input rejection properties. Include
  domain boundaries and empty/degenerate cases when the contract permits them.

## Generate useful cases

Build constraints into generators where practical. Use dependent generators for
relationships such as aligned shapes or valid indices; excessive filtering can
make tests slow or vacuous. Keep invalid cases deliberate rather than accidentally
excluding every difficult input to satisfy the implementation.

Bound data sizes according to test cost. Preserve meaningful extremes and explicit
regression examples. For floats, specify treatment of NaN, infinities, signed zero,
conditioning, and tolerance; do not assume exact associativity or equality.
For stateful APIs, generate operation sequences against an independent small model
and check both state and externally observable results.

## Make failures actionable

Use the repository's framework where suitable: Hypothesis for Python, proptest for
Rust, or fast-check for JavaScript/TypeScript. Consult current official documentation
for syntax and settings instead of assuming identical behavior across libraries.

Allow shrinking and retain a minimal counterexample as a regression when useful.
Control external randomness and reset mutable fixtures per generated example;
a test runner fixture may live longer than one example. Preserve the framework's
reproduction information and follow repository policy for example databases.

Choose generation budgets from runtime and risk. A fixed sample count is not
exhaustive verification. Do not silently disable deadlines or health checks to hide
slow generators; investigate first and document justified exceptions.

Run the targeted test and report the property checked, relevant domain limits,
and any failure found. Do not claim proof over all inputs or improvement over
example tests without evidence. Use `writing-good-tests` for broader test design;
this skill does not require a new plan or a mandatory chain of other skills.

Attribution and adaptation licensing: [LICENSE](LICENSE).
