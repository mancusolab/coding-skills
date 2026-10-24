# Implementation plan outline

Prefer a single document unless the work benefits from separate milestones.

## Context

Record the target repository, requirements/design reference, scope, key
decisions, and authorization. Identify environment or external dependencies
that affect execution or verification.

## Tasks

For each task, record:

- State: pending, in progress, complete, or blocked with a concrete reason.
- Intended behavior and acceptance criteria covered.
- Files to inspect/change and why any new file is needed.
- Dependencies and relevant existing patterns.
- Verification command(s), working directory, and expected observable outcome.

## Coverage and handoff

Map acceptance criteria to tasks and checks. Capture incomplete coverage,
material risks, and any required release or migration work.

During execution, append actual verification outcomes and justified deviations.
On interruption, record the last completed task, current changes, next action,
and blockers. Preserve failed or unavailable checks rather than marking the
whole plan complete because some tests passed.
