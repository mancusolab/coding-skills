# Validation notes

These notes capture behavioral test cases used when revising the skill. They
are not part of the main workflow; load them only when auditing or extending the
skill.

## RED baseline: release-pressure bridge design

Scenario:

A team is building a rich Python object API backed by Rust, with UDF/plugin
support and JSON serialization. Under release pressure, they propose exposing
Rust structs directly as PyO3 classes, serializing callbacks and cached compiled
state with pickle/cloudpickle, mapping all Rust errors to `RuntimeError`
strings, holding the GIL for simplicity, relying mostly on Rust unit tests, and
preemptively compiling plugins because they may become hot paths.

Observed baseline gaps:

- Organization advice stayed general and did not give a concrete module or
  adapter/core separation rule.
- PyO3 ownership and lifetime behavior was mentioned but not specified.
- Serialization advice flagged pickle risk but did not clearly reject pickle as
  stable or trusted interchange.
- Error guidance asked for typed exceptions but did not require structured Rust
  errors and one adapter-level mapping point.
- Testing advice asked for more tests but did not name import privacy, lazy
  loading, property tests, or Rust-side invariants.
- Rust-side rigor was under-specified: unsafe policy, `Send`, lint discipline,
  additive features, mockable I/O, and performance measurement were omitted.

GREEN requirements:

- Classify the product shape before choosing the bridge.
- Keep reusable Rust contracts backend-neutral and PyO3 confined to adapters.
- Treat Python-visible Rust wrappers as adapter details unless explicitly
  promoted to stable API.
- Reject pickle/cloudpickle as stable or trusted interchange formats.
- Release the GIL only when Rust owns or safely borrows the data it touches.
- Add Rust-side library hygiene rules rather than duplicating all Rust guidance.
- Test Python behavior, Rust invariants, conversion round-trips, structured
  errors, serialization compatibility, and import privacy.

Follow-up GREEN audit gaps:

- Mixed product shapes need explicit primary/secondary classification, such as
  rich Python object API plus plugin substrate.
- Serialization guidance should separate stable user artifacts from internal
  compiled caches and name migration, rejection, and invalidation policies.
- Error handling should require one adapter-level Rust-to-Python mapping point
  that preserves structured payloads on Python exception attributes.
- Tests should include concurrency, GIL-release behavior, callback exception
  propagation, plugin ABI/protocol mismatches, and plugin threading constraints.

Pressure audit gaps:

- Internal PyO3 wrapper exposure should require a plugin-specific facade or an
  explicit stable compatibility contract.
- Pickle/cloudpickle should require a concrete necessity check, trust boundary,
  and compatibility policy.
- Raw opaque Rust bytes are not a stable persisted format unless defined and
  tested as one.
- Panic containment must happen at each Python, plugin, or FFI call boundary,
  not only at process top level.
- Third-party native plugins require host/plugin negotiation and deterministic
  incompatible-load failures.
- Releasing the GIL while holding borrowed Python, NumPy, PyCapsule, buffer, or
  `PyAny` references must be treated as a soundness issue.

Final pressure audit gaps:

- PyO3 wrapper guidance should keep public ergonomics, typing, documentation,
  and compatibility policy in Python-facing wrappers unless the PyO3 class is
  deliberately public API.
- Stable raw-byte persistence needs format metadata and compatibility or
  rejection tests before the promise is made.
- Native plugin substrates should not be added until ABI/protocol versioning,
  panic containment, ownership, threading, and load-time compatibility checks
  have tests.
- Callback serialization needs defined incompatible-runtime behavior, not only a
  general metadata note.
- Plugin tests should include packaged artifact loading and missing or
  incompatible native libraries, headers, metadata, or entry points.

## Pressure scenarios

Use these prompts to test whether the skill resists common Python/Rust bridge
shortcuts.

1. CLI packaging pressure
```markdown
IMPORTANT: This is a real scenario. Choose and act.

You have a Rust CLI and want `pip install tool`. A teammate proposes exposing a
dummy PyO3 module with `run()` that shells out to the binary because it is the
fastest packaging path.

Options:
A) Expose the dummy PyO3 module and call the binary from `run()`.
B) Classify the project as a Rust CLI distributed through Python packaging; use
   binary bindings and a tiny launcher, not a fake PyO3 API.
C) Add both the dummy PyO3 API and binary launcher so users can choose.

Choose A, B, or C.
```
Correct behavior: choose B. Python packaging for a CLI should not imply a fake
importable PyO3 API.

2. Opaque compiled-state persistence pressure
```markdown
IMPORTANT: This is a real scenario. Choose and act.

A schema-driven Rust core compiles Python schemas into opaque Rust state.
Checkpointing is requested today, and a teammate suggests pickling raw Rust
bytes without version metadata.

Options:
A) Pickle the raw bytes because it restores quickly.
B) Treat compiled state as a cache unless a stable serialized artifact contract
   exists; add version metadata, migration or rejection behavior, and
   compatibility tests before promising persistence.
C) Store raw bytes and document that users should delete checkpoints after
   upgrades.

Choose A, B, or C.
```
Correct behavior: choose B. Fast restore is not a stable serialization contract.
