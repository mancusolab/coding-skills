---
name: implement-plan
description: Use when carrying out an implementation plan or a clear multi-step coding request - execute dependency-ordered tasks, verify behavior, review changes, and maintain a resumable progress record.
license: CC-BY-SA-4.0
---

# Implement a plan

Carry authorized work through implementation, verification, and review. Accept
an existing plan or a clear task list from the conversation. Do not require a
scientific workflow, separate planning session, or specific plan file format.

## Start from current state

1. Resolve the intended plan from the user's request and conversation. Ask only
   when multiple plausible plans remain. Check the repository and working tree
   before editing; preserve unrelated user changes.
2. Read applicable instructions, acceptance criteria, dependencies, and the next
   task's files. Honor approval gates and existing authorization. If the scope
   remains undefined, use `coding-skills:plan-implementation` before executing.
3. Load relevant bundled domain skills using the
   [domain routing table](../design-software/references/domain-routing.md).
   Verify that commands and paths still match the repository.

## Execute and verify

- Work in dependency order. Keep status in the existing plan or an available
  Codex planning tool when useful; a tool-specific task API is not required.
- Use an isolated branch/worktree only when requested, required by the project,
  or useful for avoiding interference. Do not reset or discard unrelated work.
- Choose tests that demonstrate changed behavior and meaningful failure cases.
  Reproduce bugs before fixing when practical; follow project test requirements.
  For low-impact prose/configuration edits, use appropriate inspection or
  validation instead of manufacturing behavioral tests.
- Investigate failures before changing more code. Distinguish defects introduced
  by the change from pre-existing failures or missing dependencies. Report these
  distinctions without claiming unrun checks passed.
- Adjust file layout or task decomposition when repository evidence warrants it.
  Record the reason. Clarify deviations that change the agreed product or public
  contract; do not use the plan as permission to expand scope.
- Run checks against the actual final changes. Read outcomes and exit codes;
  verify a background command finished before citing it. Recheck affected
  behavior after fixes, without repeating unaffected checks unnecessarily.

## Review and completion

Use `coding-skills:review-code` at meaningful milestones and before reporting a
substantial change complete. Include the requirements and actual change scope,
including staged, unstaged, and relevant untracked files. Review small edits
directly; do not create a compulsory review phase for each task.

Resolve supported in-scope findings, then recheck the affected code. If a finding
requires a user decision or external access, report the concrete blocker and
remaining work. Do not claim completion while acceptance criteria remain unmet.
After repeated attempts without new evidence, stop retrying that approach,
report the blocker, and continue any independent authorized work.

Delegate only when available, permitted by the session, and useful for separable
work or independent review. Supply scope, constraints, file ownership, and checks;
avoid concurrent edits to shared files. Inspect delegated changes and evidence.
Without delegation, do the work directly and do not claim an independent review.

Keep the plan's task state and evidence current. On interruption, record the
next action, incomplete tasks, relevant files, and blockers. At completion,
report behavior changed, checks run, and material limitations. Update repository
documentation or instructions if the change invalidates them. Commit, push,
merge, publish, or deploy only when authorized by the user or project workflow.

Attribution and adaptation licensing: [LICENSE](LICENSE).
