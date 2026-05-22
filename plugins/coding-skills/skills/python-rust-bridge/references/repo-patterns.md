# Repository patterns

Use this file as evidence when applying the `python-rust-bridge` skill. Do not
load it unless you need concrete examples.

## Polars

Shape: rich Python object API with a large Rust backend.

Patterns:

- Reusable Rust crates live under `crates/`; the PyO3 adapter is
  `crates/polars-python`; the Python package is `py-polars/src/polars`.
- Runtime packages such as `polars-runtime-32`, `polars-runtime-64`, and
  `polars-runtime-compat` select CPU-specific native modules at import time.
- `_plr.py` chooses a runtime, checks CPU feature flags, checks that Rust and
  Python package versions match, and raises clear import errors on mismatch.
- Python classes hold private Rust objects such as `_df`, `_s`, `_ldf`, and
  `_pyexpr`; helpers like `wrap_df`, `wrap_s`, `wrap_ldf`, and `wrap_expr`
  centralize conversion back to public Python objects.
- PyO3 wrapper types such as `PyDataFrame`, `PySeries`, and `PyLazyFrame` own
  Rust state behind transparent wrappers.
- `enter_polars` centralizes GIL release, timeout handling, keyboard interrupt
  handling, and Rust-to-Python error mapping for long-running compute.
- Rust errors map into a Python exception hierarchy in `polars.exceptions`, with
  I/O errors mapped to standard Python exceptions where possible.
- Interop code uses Arrow C schema/capsules, NumPy conversion modules, and
  centralized dtype/schema conversion rather than ad hoc Python containers.
- Serialization has explicit format choices: compact bincode, self-describing
  MessagePack, stack-safe DSL serialization, and Python-object pickle/cloudpickle
  paths with Python-version checks.
- Tests are mostly Python-facing for user behavior, with Rust tests kept focused
  on kernels and invariants. Public examples are doctested.

Use Polars as the model for large, stateful, data-heavy Python APIs backed by
Rust.

## pydantic-core and Pydantic

Shape: Rust validation/serialization core with Python orchestration.

Patterns:

- `pydantic-core` is a separate Maturin/PyO3 package with `python-source` and
  `module-name = "pydantic_core._pydantic_core"`.
- The Python package `pydantic` builds schemas, public model APIs, decorators,
  typing behavior, plugins, compatibility, and docs around `pydantic-core`.
- Pydantic checks the installed `pydantic-core` version at import time and
  raises a clear compatibility error outside editable development installs.
- Rust exposes small compiled objects such as `SchemaValidator` and
  `SchemaSerializer`. These own compiled validation/serialization state, retain
  Python schema/config references for pickling, and expose Python-callable
  methods.
- `.pyi` stubs document extension classes, method signatures, return types, and
  exceptions for type checkers and docs.
- Input has separate paths for Python objects, JSON bytes/strings, and strings.
  Direct JSON validation avoids building intermediate Python objects.
- Validation errors are structured. They carry type, location, message, input,
  context, and optional documentation URLs, and render readable error messages.
- User code exceptions can be attached as causes or notes where supported.
- Serializer APIs distinguish Python output from JSON bytes and expose fallback,
  warning, include/exclude, and round-trip controls.
- Tests cover validators, serializers, JSON, errors, recursion, pickling,
  garbage collection, typing, docstrings, property tests, and benchmarks.

Use pydantic-core as the model when Python owns the high-level schema/user API
and Rust owns compiled execution.

## Ruff

Shape: Rust CLI distributed as a Python package.

Patterns:

- The root `pyproject.toml` uses Maturin with `bindings = "bin"`,
  `manifest-path = "crates/ruff/Cargo.toml"`, `module-name = "ruff"`, and a
  tiny `python-source`.
- The Python package contains only `__init__.py`, `__main__.py`, and binary
  discovery helpers.
- `python -m ruff` finds the installed binary, then uses `os.execvp` on Unix or
  `subprocess.run` on Windows.
- Binary discovery checks script directories for the active interpreter, base
  interpreter, prefix installs, target installs, and user installs. Missing
  binaries raise a `FileNotFoundError` listing searched locations.
- Tests emphasize CLI behavior, snapshot outputs, formatter/linter fixtures,
  and integration tests.

Use Ruff as the model for a Rust tool whose Python package exists mainly for
installation and launch behavior.

## uv

Shape: Rust CLI distributed as a Python package, with Python packaging
awareness.

Patterns:

- The root `pyproject.toml` uses Maturin with `bindings = "bin"`,
  `manifest-path = "crates/uv/Cargo.toml"`, `module-name = "uv"`, and a small
  `python-source`.
- The Python package exposes `find_uv_bin`, `python -m uv`, and guards against
  accidentally importing build-backend functions from the wrong package.
- The launcher propagates virtual environment context and sets an internal
  parent-interpreter environment variable before executing the Rust binary.
- Wheel-content checks verify expected scripts and packaged binaries.
- Integration tests cover commands, generated files, lock files, ecosystem
  scenarios, snapshots, and platform-specific behavior.

Use uv as the model for a Rust CLI where Python packaging behavior is itself
part of the product contract.
