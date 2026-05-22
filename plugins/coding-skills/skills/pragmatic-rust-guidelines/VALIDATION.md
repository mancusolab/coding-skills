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
