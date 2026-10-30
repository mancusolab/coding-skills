# Selecting properties

| Property | Useful contract | Pitfall to address |
| --- | --- | --- |
| Roundtrip | Decode an encoded supported value | Define canonicalization and loss; paired bugs can cancel out |
| Idempotence | Normalization reaches a fixed point | A function returning a constant also satisfies it |
| Invariant | Preserve mass, ordering, lengths, or identities | A no-op may preserve the invariant without doing the required work |
| Reference comparison | Optimized code agrees with a simpler implementation | Shared algorithms or helpers can share the same bug |
| Metamorphic relation | A specified input change predicts an output relation | Derive the relation from the domain; scaling and permutation are not always valid |
| Stateful model | Sequences of API operations agree with a small model | Reset state between examples and exercise failed operations too |
| Rejection | Invalid input produces the documented error without partial effects | Generate genuinely invalid inputs and inspect state after failure |

Combine properties with known-answer examples where each leaves a blind spot.
For serialization, test a known representation as well as roundtrip. For sorting,
check ordering and element preservation; idempotence alone is insufficient.

For floating-point algorithms, justify absolute/relative tolerances and handle
near-zero values, nonfinite inputs, and ill-conditioned cases according to the
contract. Avoid treating floating-point arithmetic as exact algebra.

For Python/Rust bridges, include shape, dtype, ownership, and error mapping when
those are public contracts. A value-only roundtrip will not detect an aliasing bug.

Official framework references for implementation details:
- [Hypothesis](https://hypothesis.readthedocs.io/)
- [proptest](https://proptest-rs.github.io/proptest/)
- [fast-check](https://fast-check.dev/)
