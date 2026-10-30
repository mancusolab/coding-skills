---
name: python-rust-bridge
description: Use when designing, reviewing, or refactoring a Python package backed by Rust - classifies the product shape and applies bridge-specific rules for organization, Python/Rust data conversion, error handling, packaging, and tests
user-invocable: true
metadata:
  short-description: Python/Rust bridge design
---

# Python/Rust bridge

## Overview

Rust-backed Python projects need different designs depending on what Python is
supposed to expose. Start by classifying the product shape. Then choose the
bridge, packaging, serialization, error, and test patterns that fit that shape.

This skill is based on patterns observed in Polars, pydantic-core/Pydantic,
Ruff, and uv. For repo-specific evidence, read
`references/repo-patterns.md` only when useful.

This skill does not replace general Rust API discipline. When the design
involves public Rust crates, unsafe/FFI, performance claims, feature flags,
lint policy, or PyO3 adapter internals, also apply `pragmatic-rust-guidelines`.

## Product shapes

Choose one primary shape before giving design advice:

- **Rich Python object API**: Python users work with Python classes and methods
  backed by Rust state. Example shape: dataframes, arrays, model validators.
- **Rust core with Python orchestration**: Python owns the high-level domain
  model, typing surface, plugins, or compatibility layer; Rust owns hot
  validation, parsing, serialization, or kernels.
- **Rust CLI distributed through Python packaging**: Python package exists so
  `pip install tool` and `python -m tool` work; the user interface is the binary.
- **Plugin or extension substrate**: Python registers compiled Rust functions or
  third-party native extensions; the boundary itself is public.

Do not force a PyO3 object API onto a CLI tool. Do not treat a rich Python
library as a thin binary launcher.

If a project combines shapes, name the primary product shape and the secondary
surface explicitly. For example, a rich Python object API with a plugin
substrate should keep the user API organized by Python domains while isolating
plugin registration, ABI/version checks, and native extension contracts in a
separate boundary module.

## Organization rules

For a rich Python object API:

- Keep reusable Rust logic separate from the PyO3 adapter. PyO3 should translate
  arguments, call backend-neutral Rust code, wrap results, and map errors.
  Reusable Rust crates should not expose Python exceptions, PyO3 classes, or
  Python-owned lifetime assumptions in their public contracts.
- Keep Python user ergonomics in Python: type hints, overloads, docstrings,
  deprecations, optional dependencies, and familiar constructors.
- Use private Python-visible bridge objects or attributes for Rust state. Keep
  public methods Pythonic, and do not accidentally make adapter wrapper types a
  stable API surface. If native plugins need handles, design a plugin-specific
  facade or protocol instead of reusing internal PyO3 wrappers. Public
  ergonomics, typing, documentation, and compatibility policy should live in
  Python-facing wrappers unless the project deliberately defines a PyO3 class as
  public API.
- Centralize wrappers such as `wrap_df`, `wrap_series`, `wrap_expr`, or
  equivalent constructors. Avoid scattered private constructor calls.
- Split Python modules by user-facing domains once those domains repeat:
  `dataframe`, `series`, `expr`, `io`, `validation`, `serialization`, or similar.

For a Rust core with Python orchestration:

- Let Python build declarative schemas, configuration, public classes, and
  compatibility behavior.
- Let Rust compile and execute those schemas. Store the compiled Rust state in
  small Python-visible objects.
- Keep `.pyi` stubs or typed Python wrappers close to the extension. PyO3
  signatures alone are not enough for Python users or type checkers.
- Check core package versions at import time if Python and Rust are released as
  separate distributions.

For a Rust CLI distributed through Python packaging:

- Use `maturin` with `bindings = "bin"` or the equivalent binary packaging mode.
- Keep the Python package tiny: binary discovery, `python -m tool`, `__all__`,
  and package metadata.
- Use `os.exec*` on Unix to replace the Python process. Use `subprocess.run` on
  Windows to preserve expected console behavior.
- Raise a clear `FileNotFoundError` if the installed binary cannot be found, and
  list searched paths.

For a plugin substrate:

- Make the plugin boundary explicit and documented: registration, input types,
  keyword arguments, output schema/dtype, ownership, panic behavior, and version
  compatibility.
- Define ABI or protocol stability separately from normal Python API stability.
  Include feature/version negotiation, minimum supported host version, and clear
  failure behavior for incompatible plugins.
- Reject third-party native plugin designs that lack host/plugin version
  negotiation and deterministic incompatible-load failures.
- State threading and `Send` requirements for native plugins, Python callbacks,
  and any shared Rust state.
- Do not add a native plugin substrate until ABI/protocol versioning, panic
  containment, ownership, threading, and load-time compatibility checks have
  tests.
- Prefer compiled plugins for measured or architecturally unavoidable hot paths
  instead of Python callbacks inside tight loops.
- Do not expose internal wrapper types as stable public API by default. Promoting
  them requires a deliberate compatibility contract, tests, and documentation.

## Python/Rust conversion rules

Write down the conversion contract before implementing the bridge:

- Which side owns the data after conversion?
- Is the path borrowed, copied, zero-copy, or lifetime-bound?
- Can Rust mutate the value?
- Does it require the GIL?
- Does it materialize lazy state?
- How are nulls, missing values, sentinels, and default values represented?
- How are Python objects serialized, and is the format versioned?

For typed tabular or array data, prefer standard interchange formats such as
Arrow C data/interface capsules, NumPy buffers, or PyCapsule protocols over ad
hoc Python lists.

For schema-driven validation or serialization, prefer a Python-declared schema
compiled into Rust state. Keep the schema reconstructable for pickle,
cloudpickle, or debugging if users need to serialize the compiled object. Treat
compiled state as a cache unless the project explicitly commits to a stable
serialized format.

Separate stable user artifacts from internal caches. Stable artifacts need a
format version, migration or rejection policy, compatibility tests, and clear
metadata for package/Rust/Python versions. Internal caches need invalidation keys
for versions, feature flags, platform, ABI/protocol version, and relevant source
or schema hashes. Raw opaque Rust bytes are not a stable format unless the
project defines format metadata and compatibility or rejection tests before
promising persistence.

For JSON, expose direct Rust JSON entry points when they avoid unnecessary
`json.loads` or Python object construction. Document differences between
`validate_json` and `validate_python`-style paths.

For Python callbacks, UDFs, or arbitrary Python objects:

- Serialize with `pickle` or `cloudpickle` only after a concrete necessity
  check: the feature really needs Python runtime object serialization, the
  trusted/untrusted input boundary is documented, and compatibility metadata is
  stored with defined incompatible-runtime behavior.
- Do not treat pickle as a stable, trusted, or language-neutral interchange
  format. Never deserialize untrusted pickle data.
- Store metadata such as Python version or serialization mode.
- Fail clearly when deserializing under an incompatible runtime.
- Treat callback execution as a GIL boundary, not normal Rust compute.

## GIL and execution rules

Release the GIL for long-running Rust work that does not touch Python objects.
Do not release it while Rust still depends on borrowed Python data whose
lifetime, aliasing, or mutation rules require the GIL, unless that data has
been copied or moved into Rust-owned storage. Treat borrowed NumPy arrays,
PyCapsules, buffers, or `PyAny` references under a released GIL as a soundness
question, not only a performance choice.

Centralize this policy behind a helper instead of repeating it in every method.
The helper should also handle interruption and error mapping. If Rust must call
back into Python, isolate that path and document that it reacquires the GIL.

Never let Rust panics cross Python, plugin, or FFI call boundaries as process
surprises. Contain panics at each boundary where untrusted or third-party code
can run. Convert expected failures into Python exceptions. Treat panics as bugs
unless the plugin or extension API has a documented panic translation contract.

## Rust-side implementation rules

Bridge design does not relax Rust library hygiene. When reusable Rust code sits
behind Python:

- Expose backend-neutral Rust contracts beneath the adapter. Keep PyO3, NumPy,
  Python exceptions, and Python runtime assumptions at the adapter boundary
  unless the crate is explicitly only a Python extension crate.
- Use structured Rust error types with useful `Debug`, `Display`, and source
  chains. Map those errors into Python exceptions in one adapter layer.
- Prefer builders for complex configuration and construction. Keep I/O and
  system calls mockable when tests need to cover failure behavior.
- Keep Cargo features additive, grouped by user-facing capability, and usable in
  out-of-the-box builds. Feature-gate test utilities instead of shipping them as
  normal API.
- Keep public Rust types `Send` where feasible, especially when Python calls may
  release the GIL or move work across threads.
- Require a concrete reason for unsafe or FFI. Document ownership, aliasing,
  lifetime, and undefined-behavior contracts, and keep safe public APIs sound.
- Measure hot paths before adding specialized native paths, non-default
  allocators, or plugin compilation. If a path is inherently hot, state that
  product assumption in the design.
- Prefer `#[expect(..., reason = "...")]` over casual lint allows, and make
  formatting, linting, type checks, and Rust test commands explicit in project
  tooling.

## Error handling rules

Design errors in Python terms.

- Use specific Python exception types for user-actionable categories.
- Preserve structured details for programmatic callers: error type, location,
  context, input, and documentation URL when appropriate.
- Map reusable Rust errors to Python exceptions in one adapter layer. Preserve
  source chains and structured payloads on exception attributes instead of only
  formatting them into strings.
- Map I/O failures to standard Python exceptions such as `FileNotFoundError`,
  `PermissionError`, and `FileExistsError`.
- Convert validation failures into a first-class `ValidationError` or domain
  equivalent, not a generic `RuntimeError`.
- Keep internal errors distinct from user input errors.
- Test string rendering and structured error payloads.

For CLIs, the public error contract is exit code, stderr/stdout, diagnostics, and
machine-readable output formats. Snapshot those outputs.

## Testing rules

Test at the boundary users call.

For PyO3 object APIs:

- Python tests should cover public API behavior, conversion paths, exceptions,
  warnings, pickling, lazy/private import behavior, and missing optional
  dependencies.
- Rust tests should cover pure kernels, parsers, algorithms, and invariants.
- Add property tests for round-trips, parsing, serialization, null/missing
  handling, recursive schemas, and dtype/schema conversions.
- Add concurrency tests for GIL-release paths, callback exception propagation,
  and cancellation or interruption behavior when the project supports it.
- Add doctests or documentation-example tests for public examples.
- Fail on unexpected warnings.

For schema-driven cores:

- Test both Python-object input and JSON/string input paths.
- Test structured errors, location paths, custom errors, recursion, and
  serialization warnings.
- Test version compatibility between the Python layer and Rust core.
- Test cache invalidation and stable serialized artifact migration or rejection
  behavior when persistence is part of the contract.

For plugin substrates:

- Test plugin registration, ABI/protocol version mismatches, unsupported
  features, panic translation, Python callback failures, ownership rules, and
  threading constraints.
- Test plugin loading from the packaged artifact, including missing or
  incompatible native libraries, headers, metadata, or entry points when those
  are part of distribution.
- Test both the slow Python callback path and any compiled/native fast path when
  both are supported.

For binary packages:

- Test `python -m package`, binary discovery, missing-binary failure messages,
  Windows and Unix launch behavior, and wheel contents.
- Use CLI integration tests with stable snapshots for stdout, stderr, exit code,
  and generated files.
- Add ecosystem or fixture tests when the tool transforms user projects.

## Packaging rules

Use `maturin` or a similarly explicit native build tool. Put the development
build command in project tooling so contributors do not invent incompatible
commands.

For extension modules:

- Set `python-source` and `module-name` deliberately.
- Use `abi3` only when the API can support it.
- Keep feature flags grouped by user-facing capability.
- Keep runtime/build metadata in sync with Python package metadata.

For binary packages:

- Use binary bindings, not a fake PyO3 API.
- Package only the small Python launcher and the Rust binary.
- Include wheel-content checks if the package relies on scripts or extra
  binaries.

## Workflow

1. Classify the product shape.
2. Identify the public Python contract and the private Rust contract.
3. Draw the bridge boundary: objects, functions, schemas, buffers, callbacks,
   and errors crossing it.
4. Specify conversion ownership and serialization behavior.
5. Choose error types and structured payloads before implementation.
6. Decide where tests must live: Rust unit, Python unit, boundary, property,
   doctest, CLI snapshot, or packaging.
7. Check that packaging metadata, runtime loading, and version compatibility
   match the chosen shape.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Treating every Rust-backed project as a PyO3 class library | Classify the product shape first. |
| Letting PyO3 types leak into reusable Rust crates | Keep PyO3 in the adapter unless Python is the domain. |
| Mirroring Rust APIs mechanically in Python | Put Python ergonomics in the Python layer. |
| Serializing Python objects without version or mode metadata | Store enough metadata to reject incompatible deserialization. |
| Mapping all Rust errors to `RuntimeError` | Build a Python exception hierarchy or structured CLI diagnostics. |
| Holding the GIL during long Rust compute | Centralize GIL release and interruption handling. |
| Testing only Rust internals | Test the Python surface and conversion edge cases. |
| Treating binary distribution as an importable API | Keep CLI Python packages as launchers unless a real Python API exists. |

## Skill validation

Read [validation notes](references/validation-notes.md) when testing or revising
this skill.
