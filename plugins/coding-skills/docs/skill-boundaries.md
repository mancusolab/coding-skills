# Skill Boundaries

These skills are intentionally overlapping at their edges. Use the primary
trigger to decide which skill owns the decision, then load adjacent skills only
when the task crosses that boundary.

## Primary Ownership

| Skill | Owns | Does not own |
| --- | --- | --- |
| `python-module-design` | Python package layout, file/module granularity, subpackage promotion, placement of passive types, helpers, and exceptions | JAX tracing semantics, Polars lazy/eager execution, Rust bridge ownership, project release policy |
| `jax-equinox-numerics` | JIT boundaries, PyTrees, static/dynamic fields, Equinox module semantics, dtype stability, solver/sampler contracts, AD and batching tests | Public API lifecycle, CLI shape, packaging, docs policy, broad Python module layout |
| `jax-project-engineering` | JAX/Equinox public API stability, CLI contracts, docs/docstrings, pyproject policy, type checking, CI, serialization/checkpoints | Traced execution internals, Polars query design, generic Python package granularity |
| `polars-data-engineering` | Polars `LazyFrame`/`DataFrame` boundaries, scan/read choice, joins, reconciliation, materialization, `to_jax()` export, pandas/Arrow interchange | JAX traced numerics internals, public API lifecycle, generic module-splitting decisions |
| `python-rust-bridge` | Python package shapes backed by Rust, PyO3 boundaries, conversion ownership, GIL policy, Rust/Python error mapping, maturin packaging, bridge tests | General Rust API review, non-Rust Python layout unless it affects the bridge |
| `pragmatic-rust-guidelines` | Rust API, unsafe/FFI, PyO3 adapter hygiene, feature flags, lint policy, performance review, Rust documentation | Python package ergonomics except where Rust adapter choices affect them |

## Python/JAX Overlap

`python-module-design` is the general Python layout authority. Use it when the
question is "should this be a file, module, or subpackage?" or when the codebase
is drifting toward many tiny files.

`jax-equinox-numerics` overrides generic Python layout instincts only when JAX
runtime semantics are the reason for the structure. Examples include keeping
static/dynamic PyTree state together, avoiding subclassed concrete
`eqx.Module`s, placing JIT boundaries, and deciding whether a result object is
an `eqx.Module` or a lightweight PyTree container.

`jax-project-engineering` owns the public-facing engineering surface around JAX
code. It should not restate PyTree or solver semantics; it should ensure that
the public API, CLI, docs, CI, type checks, and serialization contracts expose
those semantics clearly.

When a public API exposes solver failure behavior, load both skills:
`jax-equinox-numerics` decides the runtime failure channel, and
`jax-project-engineering` decides how that channel is documented, versioned,
and exposed.

## Polars/JAX Overlap

`polars-data-engineering` owns everything before array export: lazy query
construction, joins, null policy, row-order freeze, materialization, and
`DataFrame.to_jax()`.

`jax-equinox-numerics` owns everything after array export: canonical JAX arrays
and PyTrees, dtype policy inside numerics, traced execution, solver/sampler
failure signaling, AD, and batching.

The handoff rule is explicit: Polars objects stay in adapters, and JAX-traced
internals receive arrays or small typed containers.

## Python/Rust Overlap

`python-rust-bridge` owns the Python-facing product shape and the conversion
contract between Python and Rust.

`python-module-design` applies to Python wrapper layout once the bridge shape is
known. It should keep wrapper modules organized around user-facing domains
rather than mirroring Rust modules mechanically.

`pragmatic-rust-guidelines` applies to the Rust side and PyO3 adapter hygiene.
When the bridge exposes reusable Rust crates, Rust public API rules take
priority below the adapter boundary.

## Load Order

- Python layout question: start with `python-module-design`; add JAX, Polars,
  or Python/Rust skills only when those technologies determine the boundary.
- JAX numerics question: start with `jax-equinox-numerics`; add
  `jax-project-engineering` when public APIs, CLI, docs, CI, or serialization
  are affected.
- Tabular-to-JAX question: start with `polars-data-engineering`; add
  `jax-equinox-numerics` at the export boundary.
- Rust-backed Python question: start with `python-rust-bridge`; must add
  `pragmatic-rust-guidelines` when implementing or reviewing Rust API, unsafe,
  FFI, PyO3 adapter, GIL, panic, feature-flag, or performance behavior.
