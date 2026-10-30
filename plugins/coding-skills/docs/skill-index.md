# Coding Skills Index

For overlap between the Python, JAX, Polars, and Python/Rust skills, see
`skill-boundaries.md`. For pressure-test notes, see `validation-notes.md`.

## `jax-equinox-numerics`

JAX and Equinox numerics guidance, including traced execution, PyTree/static
partitioning, dtype stability, solver semantics, AD, batching, and numerics test
patterns.

Companion material:
- `checklists/`
- `references/`
- `snippets/`

## `jax-project-engineering`

Project-level engineering guidance for JAX and Equinox codebases, including API
stability, docs, CLI conventions, packaging, CI, serialization, and testing.

Companion material:
- `checklists/`
- `references/`
- `snippets/`

## `polars-data-engineering`

Polars guidance for lazy-first data pipelines, explicit materialization
boundaries, deterministic joins, source/sink handling, and NumPy/JAX conversion.

Companion material:
- `checklists/`
- `references/`

## `python-module-design`

Python package and module-structure guidance for deciding when to create,
merge, or split modules and how to organize dataclasses, types, helpers, and
exceptions.

Companion material:
- `references/validation-scenarios.md`

## `python-rust-bridge`

Python packages backed by Rust, including product-shape classification, PyO3
adapter boundaries, packaging, error mapping, and cross-language tests.

Companion material:
- `references/`

## `pragmatic-rust-guidelines`

Rust design, implementation, and review guidance covering public APIs, unsafe
code, FFI, PyO3 adapters, performance-sensitive paths, lint policy, and
documentation.

Companion material:
- `references/`
- `VALIDATION.md`
