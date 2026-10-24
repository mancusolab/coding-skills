---
name: plan-implementation
description: Use when an agreed software change needs an actionable implementation plan - ground tasks in current code, identify dependencies, and map acceptance criteria to verification.
license: CC-BY-SA-4.0
---

# Plan implementation

Produce a plan that can be executed without reconstructing the conversation.
The input may be an existing design, an issue, or sufficiently clear requirements;
a formal design file is not required. For a small fix, a short task list suffices.

## Ground the work

1. Read the requested scope, prior decisions, repository instructions, relevant
   code, and test/build commands. Resolve the actual working directory and
   paths; do not invent file locations or commands from a design's examples.
2. Reconcile the design with current code. Handle routine implementation choices
   directly. Raise changes to public behavior, scope, or important tradeoffs
   before planning dependent work as settled.
3. Use `coding-skills:design-software` only if a consequential design choice is
   still unresolved. Do not restart design for a clear, authorized change.
4. Load bundled domain guidance where it affects the plan, using the
   [domain routing table](../design-software/references/domain-routing.md).
   Existing project boundaries take precedence over a template's file layout.

## Make tasks executable

- Group tasks by verifiable behavior or dependency, not one task per file.
  Distinguish independent tasks from work that must run in sequence.
- Each task states the intended change, existing files or justified new files,
  dependencies, relevant acceptance criteria, and how to verify the outcome.
- Use enough implementation detail to resolve ambiguity. Prefer contracts and
  existing examples over speculative full implementations that will go stale.
- Map every acceptance criterion to a check. Separate behavioral tests from
  build, type, lint, documentation, and manual checks; none substitutes for all
  the others. Explain criteria that cannot yet be verified.
- Follow repository testing requirements. For a bug, plan a reproduction or
  regression check when practical. Do not add tests that only mirror wording
  changes or require unavailable services without documenting the dependency.
- Record important rollout, data migration, compatibility, or rollback work
  when the change needs it. Do not impose unrelated release machinery.

## Save and hand off

Use the repository's plan location, or `.plans/implementations/<name>.md` in the
target repository. Use [the plan outline](references/plan-outline.md) when a
persistent plan is useful or requested. Split a large plan only when separate
milestones improve execution; there is no fixed phase count.

Record the target, scope, authorization, task state, and verification commands
with working directories. A plan is not evidence that tasks have been completed.

If the user requested planning only, finish with the plan. If implementation is
already authorized, continue with `coding-skills:implement-plan`; do not demand
another approval or a new session. Respect any explicit repository approval
gate. Do not create commits or publish artifacts merely to finish planning.

Attribution and adaptation licensing: [LICENSE](LICENSE).
