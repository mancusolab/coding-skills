---
name: jax-project-engineering
description: Use when designing, implementing, or reviewing JAX/Equinox project engineering - governs public APIs, CLI contracts, docs, packaging, serialization, type checks, and CI gates
user-invocable: true
metadata:
  short-description: Project engineering
---

# JAX Project Engineering (JAX/Equinox Scientific Computing)

Guidance for software engineering practices around numerical/JAX codebases.

## Scope boundary

This skill is authoritative for project-level engineering contracts:
- public API stability and compatibility policy
- CLI/user-facing interface contracts
- docs/docstring policy
- type-checking and CI gates
- packaging/versioning/serialization policy

This skill is not the source of truth for numerics runtime semantics. For:
- JIT/PyTree/static-dynamic rules
- solver failure-channel semantics inside numerics surfaces
- traced-kernel error signaling (`result`/`eqx.error_if`) behavior
- AD/batching/transform correctness
use `../jax-equinox-numerics/SKILL.md`.

## Companion resources

Paths below are relative to this skill directory. Read the checklists relevant
to the task before implementation, apply them while working, and revisit them
before completion. Document any intentionally unchecked item.

### Checklists

- `checklists/jax_project_engineering_checklist.md`
- `checklists/testing_checklist.md`

### Snippets

Adapt matching snippets to the target repository's conventions and verify the
adapted code against the relevant checklists.

- `snippets/cli_skeleton.py`
- `snippets/pyproject_minimal.toml`

## Public API stability

### Rule: Keep API structure stable and explicit
- Do: Preserve return shapes/fields and document failure semantics (status channels and/or exceptions).
- Don’t: Change return structures or error semantics without deprecation.
- Why: Scientific workflows rely on stable interfaces.
- Allowed break: Major version bump with migration guide.

### Rule: Keep one canonical entrypoint per workflow
- Do: Route each workflow through one stable entrypoint and express variants through typed options/config.
- Don’t: Add one-off public functions for special cases that should be flags or config on the canonical entrypoint.
- Why: Extra entrypoints fragment behavior, docs, and compatibility guarantees.

### Rule: Avoid trivial pass-through wrappers
- Do: Add wrappers only when they add contract value (validation, normalization, compatibility, instrumentation, caching, or deprecation shims).
- Don’t: Add one-line wrappers around core functionality with unchanged semantics.
- Why: Thin wrappers increase API surface and maintenance cost without improving behavior.

### Rule: If using `RESULTS`, keep messages actionable
- Do: Write actionable, user-facing messages on each non-success result.
- Don’t: leave messages empty or force users to decode numeric codes.
- Why: status-channel consumers rely on these messages for operator guidance.

### Rule: Do not add custom exception classes unless they provide real contract value
- Do: Prefer built-in exceptions (`ValueError`, `TypeError`, `RuntimeError`, etc.) with precise, actionable messages.
- Do: Introduce a custom exception class only when callers must catch that exact type as part of a stable public contract or when the class carries meaningful extra structure/behavior.
- Don’t: Create pass-through subclasses that add no behavior, fields, or contract value.
- Why: Trivial exception hierarchies add maintenance overhead and cognitive load without improving reliability.
- Anti-pattern:
```python
class GWASError(ValueError):
    pass
```

### Rule: Prefer composition over subclassing for concrete Modules
- Do: Wrap and delegate when customizing behavior.
- Don’t: Subclass or override concrete modules.
- Why: Aligns with Equinox abstract‑or‑final pattern and avoids override ambiguity.

### Rule: Keep numerics policy references explicit at API boundaries
- Do: Reference the active numerics policy/contract docs when API behavior depends on numerics semantics.
- Do: Keep API docs aligned with the numerics skill's chosen failure/result semantics.
- Don’t: redefine numerics semantics in this skill.
- Why: one numerics authority prevents drift between API docs and runtime behavior.

## Documentation

### Rule: Docstrings
- Use raw docstrings (`r"""..."""`) on public CLI/pipeline/numerics entrypoints.
- Use exact section labels: `**Arguments:**`, `**Returns:**`, and `**Raises:**` or `**Failure Modes:**`.
- Keep one empty line immediately after each section heading and one empty line between section blocks.
- Use LaTeX math notation in docstrings when helpful (`$...$` inline, `$$...$$` display blocks).
- Update docstrings in the same patch when signatures, status semantics, or side effects change.
- Allowed break: Internal‑only helpers.

### Rule: Docstrings Markdown
- Use MkDocs admonitions when they improve clarity in generated docstrings (for example: `!!! info`, `!!! note`, `!!! warning`, `!!! tip`).
- Keep admonition titles/content concise and technically actionable; avoid decorative callouts.

### Rule: Document determinism and failure modes
- Do: Explain nondeterminism across devices/backends and list expected failure results.
- Don’t: Leave runtime behavior implicit.
- Why: Reproducibility depends on clear constraints.

### Rule: Document `throw` behavior across transforms and backends
- Do: Document how the numerics contract (defined in `jax-equinox-numerics`) behaves under batching (`vmap`) and backend caveats.
- Do: when using `throw=True`, document whole-batch failure behavior explicitly.
- Don’t: Assume identical exception behavior on CPU/GPU/TPU or per-batch isolation.
- Why: Error propagation can differ by backend, and `vmap` can fail the whole batch.

### Rule: Preserve enum compatibility with deprecations (when enums are public API)
- Do: Keep deprecated `RESULTS` members with warnings on access and a removal plan; prefer compatibility aliases over silent removal.
- Do: Extend enums compatibly (e.g., subclassing and promotion) when adding domain-specific result codes.
- Don’t: Remove or rename enum members without a deprecation window.
- Why: Result enums are part of the public API contract.

## pyproject.toml (project configuration)

### Rule: Centralize project metadata and tooling in `pyproject.toml`
- Do: Declare Python version, dependencies, optional extras, and tool configs in one place.
- Don’t: Scatter configuration across multiple files without justification.
- Why: Single source of truth reduces drift.
- Example: `snippets/pyproject_minimal.toml`.
- Allowed break: Legacy repos that already standardize on separate config files.

### Rule: Pin minimum versions for core scientific deps
- Do: Set lower bounds for JAX/Equinox/jaxtyping and note compatibility.
- Do: Add explicit exclusions for known-bad versions when needed (e.g., `jax>=...,!=x.y.z`).
- Don’t: Allow unconstrained upgrades that silently change semantics.
- Why: Numerical stability and API behavior change across versions.

## Type checking

### Rule: Enforce type checks in CI
- Do: Use pyright/mypy and keep annotations on public APIs.
- Don’t: Ship untyped public functions or ignore type checker errors.
- Why: Prevents misuse of PyTrees, shapes, and configs.
- Example:
```python
from jaxtyping import Array, PyTree

def f(x: PyTree[Array]) -> PyTree[Array]:
    ...
```
- Allowed break: Small private helpers where typing adds no value.

### Rule: Model solver state with generics when it varies
- Do: Use `TypeVar`/`Generic` in ABCs for solver state.
- Don’t: Use `Any` for state in public interfaces.

## CLI building

### Rule: Keep CLI deterministic and cohesive
- Do: Parse args in `main()` and return explicit exit codes.
- Do: Keep workflow glue (load -> validate -> numerics -> write output) in one module when the workflow is small and cohesive.
- Do: Move repeated domain workflows into shallow modules and keep CLI handlers focused on dispatch when that separation improves cohesion.
- Don’t: Execute JAX code at import time or use global state.
- Why: Keeps CLI deterministic and testable.
- Example:
```python
import argparse

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args(argv)
    return run(seed=args.seed)

if __name__ == "__main__":
    raise SystemExit(main())
```
- Allowed break: Tiny scripts not shipped as part of the library.

### Rule: Validate early at boundaries
- Do: Validate ranges, enums, shape contracts, and file/path assumptions at boundary layers (CLI/public adapters) and raise actionable exceptions there.
- Don’t: defer basic user-input validation to deep solver internals.
- Why: Boundary failures should be immediate and clear.
- Note: traced-kernel semantics and JIT-safe failure behavior are governed by `jax-equinox-numerics`.

### Rule: Validate and normalize boundary inputs in `main()`
- Do: Validate numeric ranges, enum-like flags (`dtype`, `device`), and path existence before calling numerics code.
- Don’t: Let deep solver code surface basic user input errors.
- Why: CLI is an external boundary; fail fast with actionable messages.
- Example:
```python
def main(argv=None):
    ...
    args = parser.parse_args(argv)
    if args.max_steps < 1:
        parser.error("--max-steps must be >= 1")
    return run(...)
```
- Allowed break: Internal scripts where all inputs are controlled by trusted code.

### Rule: Configure JAX platform and x64 with direct `jax.config.update(...)` calls
- Do: Set `jax.config.update("jax_platform_name", args.device)` or the equivalent parsed CLI field directly in `main()` after argument parsing and before the first real JAX execution.
- Do: Set `jax.config.update("jax_enable_x64", True)` directly when the workflow expects 64-bit numerics by default.
- Do: Keep the logic inline when the policy is simple, for example a one-branch TPU exception.
- Don’t: Introduce wrapper classes, config dataclasses, environment-resolution layers, or helper functions just to call two JAX config updates.
- Don’t: Hide this policy deep in numerics modules when it is really a CLI/runtime choice.
- Why: These are startup configuration decisions, not an architecture boundary. Overengineering them makes the code harder to audit and easier to misapply.
- Minimal pattern:
```python
import jax

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", choices=["cpu", "gpu", "tpu"], default="cpu")
    args = parser.parse_args(argv)

    jax.config.update("jax_platform_name", args.device)
    if args.device == "tpu":
        jax.config.update("jax_enable_x64", False)
    else:
        jax.config.update("jax_enable_x64", True)

    return run(args)
```
- Good simple fixed-platform variant:
```python
jax.config.update("jax_enable_x64", True)
jax.config.update("jax_platform_name", "cpu")
```
- Escalate beyond this only when there is a real cross-entrypoint policy contract to share, such as multiple executables that must apply the exact same validated backend-selection rules.

### Rule: Define stable stdout/stderr and exit-code contracts
- Do: Reserve `stdout` for primary results (plain text  `--json`) and route diagnostics/errors to `stderr`.
- Do: Document exit-code semantics (for example: `0` success, `2` usage errors, `1` runtime failures).
- Don’t: Mix logs with machine-readable output or rely on Python tracebacks as user-facing error UX.
- Why: Scientific CLIs are often used in automation and shell pipelines.
- Example:
```python
import json
import sys

try:
    value = run(...)
except RuntimeError as exc:
    sys.stderr.write(f"error: {exc}\n")
    return 1
sys.stdout.write(json.dumps({"value": value}) + "\n")
return 0
```
- Allowed break: Purely interactive demos not intended for scripting.

### Rule: Route diagnostics through logging/callbacks, not ad-hoc prints
- Do: Use structured logging and callback hooks for progress/diagnostics.
- Do: Keep CLI-facing result/error emission aligned with the documented stdout/stderr contract.
- Don’t: Use ad-hoc `print(...)` for diagnostics in library or CLI paths.
- Why: Logging/callbacks are testable, filterable, and do not corrupt machine-readable output.

### Rule: Make CLI outputs reproducible
- Do: Expose seed/dtype/device flags, report package versions, and make the effective config inspectable.
- Don’t: Hide randomness/backend choices or silently coerce dtype/device without visibility.

### Rule: Keep configuration precedence explicit
- Do: Define and document precedence (`defaults < config file < env vars < CLI flags`).
- Don’t: Merge config sources implicitly or mutate process-global environment from command handlers.
- Why: Deterministic config resolution is required for reproducible experiments.
- Allowed break: Single-file tools with no config/env integration.

### Rule: Prefer subcommands for distinct workflows
- Do: Use subcommands (`solve`, `benchmark`, `check`) for distinct actions and keep each handler small.
- Subrule: Use `argparse` argument groups inside each subcommand to cluster related options (for example: reproducibility, solver controls, output formatting).
- Subrule: Bind each subcommand with `set_defaults(func=...)` and dispatch once via `args.func(args)`.
- Don’t: Put unrelated workflows behind one command with large flag matrices.
- Why: Improves discoverability and avoids invalid flag combinations.
- Example:
```python
sub = parser.add_subparsers(dest="cmd", required=True)
solve = sub.add_parser("solve")
solve.set_defaults(func=run_solve)
bench = sub.add_parser("benchmark")
bench.set_defaults(func=run_benchmark)
repro = solve.add_argument_group("Reproducibility")
repro.add_argument("--seed", type=int, default=0)
args = parser.parse_args(argv)
return args.func(args)
```
- Allowed break: Single-purpose commands with one stable action.

### Rule: Test CLI contracts directly
- Do: Add tests for parse failures, `--help`, stdout/stderr separation, and exit-code mapping for success/failure paths.
- Don’t: Assume library-level tests alone cover CLI behavior.
- Why: CLI regressions are usually contract regressions, not numerical regressions.

## CI / Quality gates

### Rule: Enforce formatting, linting, type checks, and tests
- Do: Run format/lint/typecheck/tests in CI.
- Don’t: Merge changes with failing checks.
- Why: Numerical regressions are subtle and expensive.

### Rule: Add regression tests for bug fixes
- Do: Write a failing test first, then fix.
- Don’t: Merge fixes without test coverage.

## Skill validation

Read [validation scenarios](references/validation-scenarios.md) when testing or
revising this skill.

## Serialization / checkpoints

### Rule: Version persisted state
- Do: Store a version tag and validate on load.
- Don’t: Persist opaque state without compatibility notes.
- Why: Long‑running experiments need stable restore paths.

### Rule: Keep serialization contracts independent of traced-failure internals
- Do: Persist versioned, domain-level state and explicit status fields needed for restore and reproducibility.
- Don’t: require callers to understand traced-kernel internals to restore checkpoints.
- Why: serialization contracts should remain stable even when numerics internals evolve.
