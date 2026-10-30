# HiJAX primitive selection and migration

Use this reference when adding a new primitive or replacing low-level primitive
registration. The [runnable example](../snippets/hijax_polynomial.py) and
[transformation tests](../snippets/test_hijax_polynomial.py) were verified with
JAX 0.12.0.1. HiJAX is exposed through `jax.experimental.hijax`; check the target
project's supported versions before adopting it. This example is not a minimum
version guarantee.

## Choose the appropriate level

| Need | Approach |
| --- | --- |
| Ordinary differentiable computation | Compose existing JAX operations |
| Function-level derivative override on mixed Equinox PyTrees | Public filtered custom JVP/VJP wrappers remain useful |
| New primitive with JAX-defined evaluation and custom transforms | Prefer HiJAX over new `eqxi.filter_primitive_*` scaffolding when experimental dependencies are acceptable |
| External compiled implementation | Use the JAX FFI contract; a HiJAX wrapper alone cannot lower arbitrary Python/native effects |
| Existing solver extension tied to internal utilities | Preserve it until equivalent behavior is demonstrated |

The benefit here is explicit, colocated transformation behavior and less manual
primitive plumbing. It does not establish a runtime or memory improvement.
Do not migrate nondifferentiable metadata guards, callbacks, or solver adjoints
merely because they also live in an internal module.

## Primitive contract

Declare `in_avals`, `out_aval`, and hashable static `params` before initializing
`HiPrim`. Build instances from `jax.typeof` at the wrapper boundary. Keep arrays
and traced data in inputs rather than static parameters. `expand` supplies a
JAX-traceable implementation for evaluation/lowering; keep it free of effects.

The example handles real floating-point arrays only. Its unary elementwise batch
rule preserves the mapped axis; do not reuse that rule for reductions, multiple
inputs, broadcasting, or shape-changing operations without deriving their contracts.

## Transformation coverage

- `jvp` implements forward mode; handle symbolic zero tangents where needed.
- Reverse mode needs a VJP rule or explicit derivation. The example uses
  `linearize_from_jvp` and `vjp_from_lin` to supply linearization and reverse mode.
- Handwritten VJPs use `vjp_fwd` plus either `vjp_bwd_retval` or the accumulator
  form `vjp_bwd`; choose one backward interface.
- `batch` handles `vmap`. Test axis placement and combinations with differentiation.

Test the required orders and compositions, not only individual transforms.
Our example checks analytic primal/derivative values, second derivatives,
linearization, nonleading batch axes, and batched gradients. Distributed sharding,
custom HiTypes, and gradient accumulators require their own examples and validation;
they are not covered by this snippet.

## Sources

- [JAX custom derivatives with HiJAX](https://docs.jax.dev/en/latest/301/custom-derivatives.html)
- [JAX primitive extension guidance](https://docs.jax.dev/en/latest/601/jax-primitives.html)

The installed `jax.experimental.hijax` exports and `HiPrim` method contracts were
also inspected when validating the example. Recheck them when changing versions.
