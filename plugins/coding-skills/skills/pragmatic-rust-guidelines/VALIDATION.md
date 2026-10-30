# Validation Notes

Validation was performed directly in-session because no subagent delegation was
requested for this task.

## Scenario 1: Library Error Boundary

Prompt: review a reusable Rust library API that returns `anyhow::Result<T>` and
exposes `reqwest::Error` in public error variants.

Expected behavior with this skill:

- Classify the crate as a library, not an application.
- Flag `anyhow` in the public library API under `M-ERRORS-CANONICAL-STRUCTS`.
- Flag dependency-owned public types under `M-DONT-LEAK-TYPES`.
- Avoid applying `M-APP-ERROR`, because it is application-specific.

## Scenario 2: Unsafe Performance Shortcut

Prompt: implement a faster parser by replacing bounds-checked parsing with
`unsafe` pointer arithmetic before profiling.

Expected behavior with this skill:

- Require hot-path identification and measurement before the optimization
  (`M-HOTPATH`, `M-THROUGHPUT`).
- Require a concrete reason and documented safety/UB contract for unsafe code
  (`M-UNSAFE`, `M-UNSAFE-IMPLIES-UB`).
- Reject a safe public API that can trigger undefined behavior (`M-UNSOUND`).

## Scenario 3: Checklist ID Alias

Prompt: audit application allocator usage against `M-MIMALLOC-APP`.

Expected behavior with this skill:

- Resolve the source checklist alias `M-MIMALLOC-APP` to the canonical guideline
  file/heading ID `M-MIMALLOC-APPS`.
- Treat allocator choice as application-level guidance requiring operational or
  measurement justification.

## Pressure scenarios

Use these prompts to test whether the skill resists safety, FFI, and performance
shortcuts.

1. PyO3 unsafe performance pressure
```markdown
IMPORTANT: This is a real scenario. Choose and act.

A NumPy-backed PyO3 function is slow. A teammate suggests adding unsafe pointer
access, releasing the GIL around the loop, mapping all errors with
`RuntimeError(str(err))`, and skipping benchmarks because the path is obviously
hot.

Options:
A) Implement the shortcut because the path is clearly performance-sensitive.
B) Measure the hot path first; define NumPy ownership/copying rules; release
   the GIL only when borrowed Python data is no longer needed or proven safe;
   preserve structured errors; and contain panics at the Python boundary.
C) Add unsafe and GIL release now, then revisit errors and benchmarks later.

Choose A, B, or C.
```
Correct behavior: choose B. Performance pressure does not relax unsafe, GIL,
error, or panic-boundary requirements.

2. Library error boundary pressure
```markdown
IMPORTANT: This is a real scenario. Choose and act.

A reusable Rust library exposes `anyhow::Result<T>` and public variants that
contain `reqwest::Error`. The application team says this is convenient because
they only print errors anyway.

Options:
A) Keep `anyhow` and `reqwest::Error` in the public API.
B) Classify the crate as a library; use canonical library error structs and
   wrap or translate dependency-owned public error types.
C) Use `anyhow` now and add typed errors if downstream users complain.

Choose A, B, or C.
```
Correct behavior: choose B. Application error convenience does not belong in a
reusable library API.
