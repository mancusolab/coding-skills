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
| Opaque values with representation or tangent semantics beyond PyTrees | Consider [experimental HiTypes](hijax_types.md) and primitives over those types |
| New primitive with JAX-defined evaluation and custom transforms | Prefer HiJAX over new `eqxi.filter_primitive_*` scaffolding when experimental dependencies are acceptable |
| External compiled implementation | Use the JAX FFI contract; a HiJAX wrapper alone cannot lower arbitrary Python/native effects |
| Existing solver extension tied to internal utilities | Preserve it until equivalent behavior is demonstrated |

The benefit here is explicit, colocated transformation behavior and less manual
primitive plumbing. It does not establish a runtime or memory improvement.
Do not migrate nondifferentiable metadata guards, callbacks, or solver adjoints
merely because they also live in an internal module.

## Primitive contract

Declare `in_avals`, `out_aval`, and a `params` dict of hashable static values
before initializing `HiPrim`. Build instances from `jax.typeof` at the wrapper boundary. Keep arrays
and traced data in inputs rather than static parameters. `expand` supplies a
JAX-traceable implementation for evaluation/lowering; keep it free of effects.
Ensure declared output types match the expansion, including weak typing after
scalar promotion; copying an input type is valid only if the operation preserves it.

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

### Derivative contracts

- Treat `in_avals` entries and `out_aval` as possible PyTrees of types. Match
  derivative output structures and return one input cotangent per positional
  argument. Map `jax.typeof` over ordinary PyTrees at the wrapper boundary.
- Compute forward-rule primals with `self(...)` to retain custom rules under
  higher derivatives. Calling `expand` directly can bypass that boundary.
- Handle `Zero` in backward cotangents as well as JVP tangents. An unused output
  is an important test case. For nested values, use tree-aware handling with
  `Zero` treated as a leaf; materialize only where arithmetic needs an array.
- `nzs_in` identifies differentiated inputs, not numerically nonzero data.
  It can guide residual retention. Optional `nzs_out` declares symbolic output
  activity; do not infer it from current numeric values.
- For mathematical derivatives and derived transposition, tangent outputs must
  be linear in tangent inputs. Avoid circular rule derivations. A deliberately
  nonlinear gradient modification needs a separately stated contract; do not
  assume it can be transposed into a consistent JVP.

These contracts and the examples of shared outputs are described in the
[official derivative guide](https://docs.jax.dev/en/latest/301/custom-derivatives.html).

### Choosing derived rules

The installed JAX 0.12.0.1 interface exposes these alternatives:

| Starting rule | Derivation | Tradeoff |
| --- | --- | --- |
| `jvp` | `lin, linearized = linearize_from_jvp`, then `vjp_fwd, vjp_bwd_retval = vjp_from_lin` | Save linearization residuals for reverse mode; used by the polynomial example |
| `jvp` | `vjp_fwd, vjp_bwd_retval = vjp_from_jvp` | Save primals and redo primal-dependent JVP work in backward; does not itself add `linearize` support |
| Handwritten `lin`/`linearized` | `jvp = jvp_from_lin`, optionally VJP via `vjp_from_lin` | Explicit control over the residuals and linear map |

Select based on the computation's storage/recomputation needs and measure if
performance matters. Higher-order support depends on the composed path: a
reverse-over-reverse test does not establish forward-over-reverse support.

### Batching and checkpointing

A batch rule defines a new program. Preserve the primitive boundary or explicitly
provide equivalent derivative semantics in that program. Check shared inputs and
outputs: reduction over a batch must not count a shared output's cotangent once
per example. Declare output mapping consistent with the intended tangent mapping,
including surrogate rules whose primal ignores an input.

The guide documents a version/configuration caveat: classic remat differentiates
through JVP rules, while `jax_remat3` uses VJP rules and supports their logs.
Check the target version and test `grad(checkpoint(f))`; do not prescribe a
global flag change or infer checkpoint compatibility from plain `grad` success.

### Optional advanced interfaces

Use these only when the application needs them; consult the linked guide and
installed API before implementing them.

- Accumulator backward rules receive `GradAccum` objects with an expected `aval`
  and `accum` operation. Support ordinary value accumulation (`ValAccum`) even
  if optimizing sparse updates through `RefAccum`; `NullAccum` means the input
  gradient is unwanted. Add contributions rather than overwriting prior ones.
- Under batching, preserving an input unchanged can matter for receiving the
  caller's gradient ref. Moving an axis may introduce an intermediate and force
  value accumulation. Test the fallback as well as repeated ref updates.
- Structured residuals use a fourth forward return slot and the accumulator
  backward interface, with an extra residual argument. Keep them separate from
  ordinary opaque residuals when caller inspection is part of the contract.
- Backward logs use a dict return from `vjp_bwd`, or
  `vjp_bwd_retval_logs` for value-returning rules. Log keys must be unique within
  the relevant backward scope; test repeated call sites and control flow.
- `transpose` is a separate interface for operations linear in some inputs;
  ordinary VJP coverage does not establish standalone transposition support.

## Validation without numerical perturbations

Use analytic derivatives, known-answer problems, or an independently implemented
reference as the primary oracle. Supplement with tangent linearity, JVP/VJP
adjoint identities, and eager/JIT/mapped consistency. Consistent but incorrect
rules can pass identities, so these do not replace an independent answer.
For surrogate or nonsmooth conventions, check the stated rule directly rather
than equating it with a derivative of the primal implementation.

The [structured-output example](../snippets/hijax_shared_outputs.py) and its
[tests](../snippets/test_hijax_shared_outputs.py) cover handwritten VJPs,
unused-output zeros, shared scalar inputs/outputs, and batch reductions.

Test the required orders and compositions, not only individual transforms.
The polynomial example checks analytic primal/derivative values, second derivatives,
linearization, nonleading batch axes, and batched gradients. Distributed sharding,
custom HiTypes, and gradient accumulators are not covered by that snippet.
For the type protocol and a separate runnable example, see
[HiJAX types](hijax_types.md); distributed transforms and gradient accumulators
still need application-specific validation.

## Sources

- [JAX custom derivatives with HiJAX](https://docs.jax.dev/en/latest/301/custom-derivatives.html)
- [JAX primitive extension guidance](https://docs.jax.dev/en/latest/601/jax-primitives.html)

The installed `jax.experimental.hijax` exports and `HiPrim` method contracts were
also inspected when validating the example. Recheck them when changing versions.
