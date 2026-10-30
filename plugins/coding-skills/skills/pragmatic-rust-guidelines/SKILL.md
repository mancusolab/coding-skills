---
name: pragmatic-rust-guidelines
description: Use when designing, implementing, reviewing, or documenting Rust crates, PyO3 adapters, APIs, unsafe code, FFI, performance-sensitive paths, or library/application boundaries - applies Microsoft's pragmatic Rust guidelines plus Python/Rust adapter checks as code-change and review criteria
user-invocable: true
---

# Pragmatic Rust Guidelines

## Overview

Apply pragmatic Rust guidance with the spirit of the rule in mind: improve
safety, performance, maintainability, and usability without forcing mechanical
compliance when a guideline's motivation does not apply.

The original Microsoft guideline IDs are preserved. Use them in review findings
and design notes when they make the concern easier to trace.

## When to Use

Use this skill for Rust work involving:

- public API design, type naming, builders, traits, errors, or documentation
- library/application boundary decisions, feature flags, `-sys` crates, or test utilities
- unsafe Rust, soundness, FFI, global state, or external type exposure
- PyO3 adapter crate structure, Python-to-Rust error mapping, panic containment, or GIL boundaries
- NumPy/Arrow/data ownership and copying rules across Python/Rust boundaries
- maturin build/install/test workflows or lazy/private Python import behavior for Rust extensions
- Send/future compatibility, async runtime neutrality, I/O abstraction, or dependency injection
- logging, panic/error boundaries, static verification, lints, or clippy policy
- performance work involving hot paths, throughput, allocators, or cooperative yield points

## Workflow

1. Classify the target as a library, application, FFI layer, unsafe abstraction, performance path, documentation change, or mixed scope.
2. Apply universal checks first: upstream Rust API Guidelines, static verification, lint override discipline, `Debug`/`Display`, concise naming, panic boundaries, documented magic behavior, and structured logging.
3. For libraries, prioritize API resilience: do not leak external types, keep types `Send` where feasible, avoid nested abstractions, avoid wrapper-heavy public APIs, use strong types, and expose escape hatches where appropriate.
4. For PyO3 adapter crates, keep PyO3 confined to the adapter layer, translate reusable Rust errors into Python exceptions deliberately, define NumPy/Arrow ownership and copying behavior, release the GIL around long Rust compute with `Python::allow_threads` where safe, contain panics before crossing into Python, and test lazy/private import behavior from Python.
5. For construction and dependencies, prefer builders for complex construction, cascaded initialization for hierarchies, cloneable service handles, mockable I/O/system calls, feature-gated test utilities, additive features, out-of-the-box builds, and explicit `maturin` build/install/test commands for Python extension workflows.
6. For unsafe and FFI, require a concrete reason, define the undefined-behavior contract, preserve soundness, isolate DLL state, and avoid public APIs that force consumers to inherit hidden unsafety.
7. For performance, identify and measure hot paths before optimizing, remove empty cycles, choose application allocators deliberately, and add yield points to long-running async or cooperative work.
8. For documentation and AI usability, make the first doc sentence concise, document modules comprehensively, use canonical docs sections, inline re-export docs, and include examples, failure modes, links, and precise type names.
9. Report guideline conflicts explicitly. If you do not follow a guideline, state the reason in terms of the guideline's motivation.

## Reference Loading

Load only the references needed for the task:

- `references/guideline-index.md` for topic-to-guideline lookup.
- `references/review-checklist.md` for code review and PR audit passes.

For full explanations, consult Microsoft's [Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/)
for the specific guideline IDs in scope.

## Output Contract

When reviewing code, lead with actionable findings. Include guideline IDs such
as `M-UNSAFE` or `M-DONT-LEAK-TYPES` when a finding maps cleanly.

When writing code, make the guideline-driven choice directly. Avoid long
explanations unless the choice is non-obvious or trades off against another
guideline.

When designing APIs, separate library advice from application advice. Do not
apply application-only guidance such as `anyhow`-style errors to reusable
library APIs. For PyO3 work, distinguish reusable Rust crate contracts from
Python adapter contracts; PyO3, NumPy, Python exceptions, and maturin-specific
behavior belong at the adapter boundary unless the crate is explicitly a
Python extension crate.

## Skill validation

Read [VALIDATION.md](VALIDATION.md) when testing or revising this skill.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Treating every guideline as mandatory in every crate | Classify the crate and apply the relevant topic set |
| Optimizing before measuring | Identify and profile the hot path first |
| Adding unsafe for convenience | Require a concrete reason and document the UB boundary |
| Using application error handling in libraries | Use canonical library error structs for public APIs |
| Hiding dependencies behind public external types | Wrap or translate public API types to avoid leaking dependencies |
| Letting PyO3 leak into reusable Rust crates | Keep PyO3 in the adapter crate and expose backend-neutral Rust contracts beneath it |
| Mapping Rust errors to Python with generic strings | Preserve actionable context and choose deliberate Python exception types |
| Holding the GIL during long Rust computation | Use `Python::allow_threads` when Rust code does not touch Python-owned objects |
| Leaving NumPy/Arrow ownership implicit | Document and test whether data is borrowed, copied, zero-copy, or lifetime-bound |
| Allowing panics to cross Python calls | Catch/translate panics or prove the boundary cannot panic |
| Treating maturin commands as tribal knowledge | Document build/install/test commands and verify them in CI or developer tests |
| Forgetting Python import privacy tests | Add tests proving Rust extensions are lazily imported and private when that is the contract |
| Letting test helpers ship as normal API | Feature-gate test utilities |
| Adding lint allows casually | Prefer `#[expect(..., reason = "...")]` |
