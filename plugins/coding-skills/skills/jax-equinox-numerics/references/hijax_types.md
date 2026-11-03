# Experimental HiJAX types

Use this reference when a computation needs a custom JAX value type, not just a
new operation on arrays. HiJAX is experimental; this is a capability map and
working guidance, not an established set of best practices. Check the target
JAX version and implement only the transformations the application needs.

## Choosing the boundary

Keep ordinary aggregate state as a PyTree unless type-level semantics justify
an opaque value. Useful reasons include coupled representation invariants,
primitives that exploit compressed storage, or a tangent representation that
differs from the primal. A custom type is not automatically faster or smaller.
Document the public operations and supported transformations before adopting it.

The [JAX type guide](https://docs.jax.dev/en/latest/301/hijax-types.html)
explains the distinction from PyTrees. In particular, traced HiType values must
be constructed and inspected through primitives. Direct container access belongs
in `expand` or the type's lowering methods, not in traced callers or AD rules.
Eager attribute access does not establish that the same code works under JIT.

## Capability map

The following interface names were inspected in `jax.experimental.hijax` on
JAX 0.12.0.1. They are version-specific contracts, not minimum-version promises.

| Capability | Type-side interface | Additional work |
| --- | --- | --- |
| Registration and JIT | Hash/equality, `lo_ty`, `lower_val`, `raise_val`; `register_hitype` associates the value class | Primitive signatures use the new abstract type; `expand` implements operations on its lowered representation |
| AD | `to_tangent_aval`; `to_ct_aval` defaults to it | Primitive derivative rules; `vspace_zero`/`vspace_add` if a HiType is itself a tangent/cotangent type |
| `vmap` | `MappingSpec`, `dec_rank`, `inc_rank` | Primitive `batch` rules translating array axes, custom specs, and unmapped inputs |
| `scan` | `leading_axis_spec`, plus rank conversion | Stable carry types; specify `length` when it cannot be inferred |
| `shard_map` | `HiPspec.to_lo`, `shard`, `unshard` | Component partition specs in lowering order |
| AD through `shard_map` | `HiPspec.to_tangent_spec`, `to_ct_spec`, and `HiType.nospec` | Derivative rules and residual handling consistent with the chosen tangent representation |
| Resharding | `reshard` | Define and test the intended placement transition if needed |

For hi-only mapped inputs, supply `axis_size` when JAX cannot infer it. Mapping
specs need not be integer axes or describe identical axes for all components.
For explicit sharding, define component placements and propagate them through
primitive types. JAX does not cross-check a primitive's declared output sharding
against its expansion: test both. See the guide's
[batching](https://docs.jax.dev/en/latest/301/hijax-types.html#vmap-and-mapping-specs)
and [sharding](https://docs.jax.dev/en/latest/301/hijax-types.html#sharding-in-types-explicit-mode)
sections for worked examples.

## Working rules and limits

- Keep runtime arrays out of type metadata and static primitive parameters.
  Check that type equality distinguishes every semantic property your operations
  rely on, including component shapes, dtypes, and relevant placement.
- Make lowering/reconstruction agree on component order and abstract types.
  Validate representation invariants at construction and preserve them in every
  producing operation; registration alone is not validation.
- Specify what derivatives mean. A surrogate derivative is a modeling choice;
  finite differences of the primal are not its correctness oracle. Check the
  declared derivative directly. Do not assume compressed primals imply compressed
  gradients or a closed tangent space.
- Test mapped and unmapped operand combinations required by the application.
  Do not generalize a unary elementwise batch rule to reductions or contractions.
- Treat unsupported transformations as explicit limits, not evidence that a
  type is unusable. Conversely, passing JIT does not establish AD or sharding.
- Use `jax.jit` for registered dynamic HiType values. Before using Equinox
  filtering/partitioning, verify how the supported Equinox version classifies
  those values. An array predicate is not proof of support for every JAX type;
  do not silently classify runtime payloads as static configuration.

## Example and validation

The [real-box example](../snippets/hijax_real_box.py) deliberately wraps one
floating-point array: it isolates the type protocol without adding quantization
or a surrogate gradient. Production code would normally use the array directly.
Its [tests](../snippets/test_hijax_real_box.py) check lowering round trips,
rejection of integer payloads, JIT inputs/results, dense tangents, mapping, and
scan. It does not implement distributed transforms, custom tangent accumulation,
or Equinox filtered transforms; do not infer those capabilities from its success.

For a real application, extend the tests with its representation invariants,
numerical reference, and required transform compositions. Compare declared and
actual placements when adding sharding. Record the tested versions and explicit
omissions, rather than labeling the whole experimental API validated.
