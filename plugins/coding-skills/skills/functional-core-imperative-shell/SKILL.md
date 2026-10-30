---
name: functional-core-imperative-shell
description: Use when designing, implementing, or reviewing boundaries between computation and side effects - isolates domain decisions from I/O while preserving cohesive modules and operational correctness.
license: CC-BY-SA-4.0
---

# Functional core, imperative shell

Separate domain decisions and transformations from interactions with external state.
Apply this to the requested change; do not turn a small fix into an architecture rewrite.

## Choose the boundary

- The core receives values and returns values, decisions, or explicit effect descriptions.
  It does not read files, query databases, access environment variables, or mutate
  caller-owned state. Injecting a database client does not make its queries pure.
- The shell obtains inputs, invokes the core, and performs effects. Keep business
  rules in the core; keep resource lifetime, transactions, retries, cancellation,
  and external error handling at the effect boundary.
- Pass configuration, timestamps, and random inputs explicitly. A mutable random
  generator is still stateful; use explicit keys/state transitions where supported.
- Logging is an effect. Prefer returning diagnostic information for the shell to
  emit; when framework instrumentation remains inside computation, describe that
  exception accurately rather than promising purity.

## Preserve the real execution contract

A gather → compute → persist sequence is useful when inputs fit that model.
Streaming and interactive algorithms may alternate computation and effects;
use a pure transition such as `(state, event) -> (next_state, commands)` when useful.
Do not force all inputs into memory to obtain a pure-looking interface.

Moving reads away from writes can introduce stale decisions. Preserve transaction
boundaries, atomic operations, concurrency checks, and retry/idempotency semantics.
For example, a pure eligibility decision does not make a later database write safe
without the original transactional or conditional-write guarantee.

Keep performance-sensitive buffers, framework callbacks, and traced execution
constraints explicit. Local mutation of privately owned data can remain an
implementation detail; avoid exposing aliases that let it change external state.
Choose practical boundaries based on the actual contract and available evidence.

## Keep organization proportional

Functions with different effect responsibilities can live in one cohesive module.
Do not require classification comments, a file per layer, or generic dependency
injection interfaces. Extract a boundary where it makes decisions independently
testable or clarifies ownership. Use `python-module-design` when Python file
layout is the question, and the relevant bundled domain skill for runtime constraints.

## Verify the separation

Test core decisions directly using values and observable results. Test shell wiring
and failure behavior with isolated resources or appropriate doubles, including
transaction rollback or cleanup when those guarantees are affected. A core test
alone does not verify persistence, serialization, or delivery.

For a design or review request, describe the proposed boundary and its tradeoffs;
make edits only when requested. Use the existing workflow's plan and progress
record if present; this skill does not require a separate document.

Attribution and adaptation licensing: [LICENSE](LICENSE).
