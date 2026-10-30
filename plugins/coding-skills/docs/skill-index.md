# Coding Skills Index

For overlap between the Python, JAX, Polars, and Python/Rust skills, see
`skill-boundaries.md`. For pressure-test notes, see `validation-notes.md`.

## Workflow skills

| Skill | Scope | Companion material |
| --- | --- | --- |
| `design-software` | Repository-grounded design, meaningful clarification, alternatives, acceptance criteria | `references/design-outline.md`, shared `references/domain-routing.md` |
| `plan-implementation` | Executable tasks, dependencies, verification coverage | `references/plan-outline.md` |
| `implement-plan` | Execution, progress, verification, review and fixes | None |
| `review-code` | Scoped findings, evidence, correction review | None |

These are Codex-only adaptations of the playbook workflows. They can be used
independently and do not require the original playbook installation. See `../NOTICE`
for provenance and licensing.

## Architecture, testing, and debugging

| Skill | Scope |
| --- | --- |
| `functional-core-imperative-shell` | Separates domain computation from effects while preserving cohesive modules and transaction semantics. |
| `property-based-testing` | Designs generated tests with meaningful properties, constrained inputs, and reproducible failures. |
| `systematic-debugging` | Investigates failures with reproductions, discriminating experiments, and causal verification. |
| `writing-good-tests` | Chooses test oracles, scope, isolation, and dependency boundaries around observable contracts. |

`property-based-testing` includes `references/property-catalog.md`. The other
three are self-contained. These four skills are CC BY-SA adaptations; see `../NOTICE`.

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
