# Rust Review Checklist

Use this as a review pass. Do not require every item for every crate; select by
scope and explain exceptions by guideline motivation.

## First Pass: Scope

- Is this a library, application, FFI boundary, unsafe abstraction, performance path, docs change, or mixed scope?
- Are public APIs stable enough that dependency exposure, type choices, and error shapes matter?
- Is the code user-facing, machine-facing, performance-sensitive, or safety-critical?

## Universal Checks

- Upstream Rust API Guidelines are followed before local preferences (`M-UPSTREAM-GUIDELINES`).
- Lints are configured for static verification (`M-STATIC-VERIFICATION`).
- Lint suppressions use `#[expect(..., reason = "...")]` rather than unexplained `allow` (`M-LINT-OVERRIDE-EXPECT`).
- Public types have useful `Debug`; human-readable types have `Display` (`M-PUBLIC-DEBUG`, `M-PUBLIC-DISPLAY`).
- Names avoid filler terms and encode domain meaning (`M-CONCISE-NAMES`).
- Panics are reserved for bugs or stop-the-program situations (`M-PANIC-IS-STOP`, `M-PANIC-ON-BUG`).
- Magic constants, defaults, and surprising behaviors are documented (`M-DOCUMENTED-MAGIC`).
- Logs are structured and avoid formatting data into opaque strings (`M-LOG-STRUCTURED`).

## Library API Checks

- Public APIs do not leak external dependency types unnecessarily (`M-DONT-LEAK-TYPES`).
- Public types and returned futures are `Send` where practical (`M-TYPES-SEND`).
- APIs expose escape hatches for native access when abstraction cannot cover all needs (`M-ESCAPE-HATCHES`).
- Essential operations are inherent methods, not hidden behind traits (`M-ESSENTIAL-FN-INHERENT`).
- The API avoids visible nesting, wrapper-heavy signatures, and unnecessary smart pointers (`M-SIMPLE-ABSTRACTIONS`, `M-AVOID-WRAPPERS`).
- Dependency injection follows concrete types first, generics second, dynamic traits last (`M-DI-HIERARCHY`).
- Library errors are structured, canonical, inspectable, and useful without `anyhow` (`M-ERRORS-CANONICAL-STRUCTS`).
- Complex construction uses builders; hierarchical construction cascades cleanly (`M-INIT-BUILDER`, `M-INIT-CASCADED`).
- Services are cheap and safe to clone (`M-SERVICES-CLONE`).
- Inputs accept `impl AsRef`, `impl RangeBounds`, or I/O traits where that improves ergonomics without ambiguity (`M-IMPL-ASREF`, `M-IMPL-RANGEBOUNDS`, `M-IMPL-IO`).

## Resilience And Build Checks

- I/O and system calls can be mocked for tests (`M-MOCKABLE-SYSCALLS`).
- Test utilities are behind an explicit feature (`M-TEST-UTIL`).
- Strong domain types prevent invalid states and unit confusion (`M-STRONG-TYPES`).
- Public re-exports are explicit, not globbed (`M-NO-GLOB-REEXPORTS`).
- Statics and global state are avoided or justified (`M-AVOID-STATICS`).
- The library builds and works out of the box (`M-OOBE`).
- Native `-sys` crates keep build dependencies minimal (`M-SYS-CRATES`).
- Cargo features are additive (`M-FEATURES-ADDITIVE`).

## Applications

- Top-level application errors may use `anyhow`, `eyre`, or derivatives (`M-APP-ERROR`).
- Allocator choices such as mimalloc are application-level decisions with measurement or operational justification (`M-MIMALLOC-APPS`; checklist alias `M-MIMALLOC-APP`).

## Unsafe, FFI, And Soundness

- Every unsafe block or API has a clear reason and a documented safety contract (`M-UNSAFE`).
- The contract names the behavior that would be undefined if callers violate it (`M-UNSAFE-IMPLIES-UB`).
- Safe public APIs cannot be used to cause undefined behavior (`M-UNSOUND`).
- FFI libraries isolate DLL state and do not assume shared process-global invariants across boundaries (`M-ISOLATE-DLL-STATE`).

## Performance

- Hot paths are identified and profiled before optimization (`M-HOTPATH`).
- Throughput improvements remove actual empty cycles or bottlenecks (`M-THROUGHPUT`).
- Long-running work yields cooperatively where needed (`M-YIELD-POINTS`).

## Documentation And AI Usability

- Public docs start with a concise first sentence (`M-FIRST-DOC-SENTENCE`).
- Modules explain purpose, usage, failure modes, and important invariants (`M-MODULE-DOCS`).
- Docs have canonical sections where useful: examples, errors, panics, safety, and related links (`M-CANONICAL-DOCS`).
- Re-exported public items use `#[doc(inline)]` (`M-DOC-INLINE`).
- APIs and docs are explicit enough for AI tools to select types, understand errors, and produce correct examples (`M-DESIGN-FOR-AI`).
