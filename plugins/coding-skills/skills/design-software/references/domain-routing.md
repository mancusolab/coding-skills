# Workflow domain routing

Load a domain skill only when its subject affects the current task:

| Decision or changed surface | Bundled skill |
| --- | --- |
| Python module/file boundaries | `coding-skills:python-module-design` |
| JAX tracing, PyTrees, solvers, AD, or batching | `coding-skills:jax-equinox-numerics` |
| JAX project APIs, CLI, packaging, CI, or checkpoints | `coding-skills:jax-project-engineering` |
| Polars queries, joins, materialization, or array export | `coding-skills:polars-data-engineering` |
| Python/Rust product shape, conversion, or packaging | `coding-skills:python-rust-bridge` |
| Rust implementation, unsafe/FFI, or PyO3 internals | `coding-skills:pragmatic-rust-guidelines` |

For other stacks, use repository guidance and the available tools directly.
No domain skill is a universal prerequisite. When installed as standalone skills,
resolve these names without the `coding-skills:` plugin prefix.
