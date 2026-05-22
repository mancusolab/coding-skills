# Guideline Index

Use this index to select the smallest relevant guideline set. The original
Microsoft guideline IDs are retained for traceability.

## Universal

- `M-UPSTREAM-GUIDELINES`: follow the upstream Rust API Guidelines.
- `M-STATIC-VERIFICATION`: use compiler and clippy lints to catch issues statically.
- `M-LINT-OVERRIDE-EXPECT`: prefer `#[expect(..., reason = "...")]` for lint overrides.
- `M-PUBLIC-DEBUG`: public types implement `Debug`.
- `M-PUBLIC-DISPLAY`: public types meant for humans implement `Display`.
- `M-SMALLER-CRATES`: split crates when boundaries become unclear.
- `M-CONCISE-NAMES`: avoid vague filler words in names.
- `M-REGULAR-FN`: prefer regular functions over associated functions where that is clearer.
- `M-PANIC-IS-STOP`: treat panic as stopping the program.
- `M-PANIC-ON-BUG`: use panic for detected programming bugs, not recoverable errors.
- `M-DOCUMENTED-MAGIC`: document magic values, defaults, and surprising behavior.
- `M-LOG-STRUCTURED`: use structured logging and message templates.

## Library Interoperability

- `M-TYPES-SEND`: keep public types and futures `Send` where feasible.
- `M-ESCAPE-HATCHES`: provide native escape hatches when abstraction is not enough.
- `M-DONT-LEAK-TYPES`: avoid exposing dependency-owned types in public APIs.

## Library UX

- `M-SIMPLE-ABSTRACTIONS`: avoid visibly nested abstractions.
- `M-AVOID-WRAPPERS`: avoid smart pointers and wrappers in public APIs unless needed.
- `M-DI-HIERARCHY`: prefer concrete types, then generics, then `dyn Trait`.
- `M-ERRORS-CANONICAL-STRUCTS`: use canonical structured errors for library APIs.
- `M-INIT-BUILDER`: use builders for complex type construction.
- `M-INIT-CASCADED`: use cascaded initialization for complex hierarchies.
- `M-SERVICES-CLONE`: service handles should be cloneable.
- `M-IMPL-ASREF`: accept `impl AsRef<T>` where feasible.
- `M-IMPL-RANGEBOUNDS`: accept `impl RangeBounds<T>` where feasible.
- `M-IMPL-IO`: accept I/O traits where feasible and keep core logic runtime-neutral.
- `M-ESSENTIAL-FN-INHERENT`: expose essential functionality as inherent methods.

## Library Resilience

- `M-MOCKABLE-SYSCALLS`: make I/O and system calls mockable.
- `M-TEST-UTIL`: feature-gate test utilities.
- `M-STRONG-TYPES`: use the proper type family and strong domain types.
- `M-NO-GLOB-REEXPORTS`: do not glob re-export public items.
- `M-AVOID-STATICS`: avoid statics unless the global state is justified.

## Library Building

- `M-OOBE`: libraries should work out of the box.
- `M-SYS-CRATES`: native `-sys` crates should compile without unnecessary dependencies.
- `M-FEATURES-ADDITIVE`: cargo features should be additive.

## Applications

- `M-MIMALLOC-APPS`: applications may choose mimalloc deliberately.
  The source checklist also refers to this as `M-MIMALLOC-APP`; the guideline
  file and heading use `M-MIMALLOC-APPS`.
- `M-APP-ERROR`: applications may use `anyhow`, `eyre`, or similar top-level error crates.

## FFI

- `M-ISOLATE-DLL-STATE`: isolate DLL state between FFI libraries.

## Safety

- `M-UNSAFE`: unsafe needs a reason and should be avoided where practical.
- `M-UNSAFE-IMPLIES-UB`: unsafe contracts should identify undefined behavior.
- `M-UNSOUND`: all code must be sound.

## Performance

- `M-THROUGHPUT`: optimize for throughput and avoid empty cycles.
- `M-HOTPATH`: identify, profile, and optimize hot paths early.
- `M-YIELD-POINTS`: long-running tasks should have yield points.

## Documentation

- `M-FIRST-DOC-SENTENCE`: first doc sentence should be one line, roughly 15 words.
- `M-MODULE-DOCS`: modules should have comprehensive documentation.
- `M-CANONICAL-DOCS`: documentation should use canonical sections.
- `M-DOC-INLINE`: mark public re-exports with `#[doc(inline)]`.

## AI

- `M-DESIGN-FOR-AI`: design APIs and docs so AI tools can discover and use them correctly.
