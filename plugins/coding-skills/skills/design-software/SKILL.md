---
name: design-software
description: Use when brainstorming a software idea or making design decisions before implementation - investigate the repository, resolve consequential uncertainties, compare approaches, and define observable acceptance criteria.
license: CC-BY-SA-4.0
---

# Design software

Turn a feature request or architectural problem into a grounded design. For a
small change with an established approach, state the approach briefly and move
to authorized implementation; do not manufacture a design process.

## Establish the contract

1. Read applicable repository instructions, the relevant implementation and
   tests, and any design or decisions already supplied in the conversation.
   Identify existing extension points before proposing new modules.
2. State the desired behavior, constraints, and what would demonstrate success.
   Separate verified facts from assumptions. Preserve prior user decisions.
3. Ask only about uncertainty that changes the product, public contract, scope,
   or substantial implementation cost. Investigate answers available in the
   repository first. Continue independent work while awaiting clarification.
4. When a decision depends on an external API or uncertain technical claim,
   verify it against primary sources and record the relevant version or date.
   Do not require external research for decisions already supported locally.

## Choose an approach

- Compare alternatives when there is a real tradeoff; recommend one and explain
  its consequences for callers, maintenance, failure behavior, and verification.
- Describe responsibilities, data flow, public contracts, and migration needs.
  Name files only after inspecting the repository; a new file needs a real
  responsibility, not merely a matching noun in the design.
- Load only the bundled domain skills relevant to the decision. Use the
  [domain routing table](references/domain-routing.md)
  when needed. Do not require Python or scientific guidance for unrelated work.
- Define observable acceptance criteria, including meaningful failure cases and
  compatibility requirements. Map each to a test, inspection, or demonstration.
- Present unresolved consequential choices before implementing work that depends
  on them. Honor explicit design approval requirements, but do not ask again for
  decisions already authorized. A request for design alone does not authorize
  implementation.

## Record and hand off

Brainstorming and small design discussions can stay in the conversation; do not
create a file merely because this skill is active. Write a document when the
user requests one or the design needs a durable record for substantial work.
When writing, use the project's established location, or
`.plans/designs/<descriptive-name>.md` in the target repository if none exists.
Derive the name from the task; no naming interview is needed.
Read [the design outline](references/design-outline.md) only when writing a
document. Update the relevant existing document instead of duplicating it.

Record the chosen approach, acceptance criteria, evidence, unresolved questions,
and whether implementation is authorized. Do not label a proposal approved
without supporting user or repository authorization.

Use `coding-skills:plan-implementation` when the accepted scope needs a task
breakdown. Continue in the same session when authorized; a fresh session,
commit, branch, or worktree is not a prerequisite. If stopping at design,
report the artifact and decisions still needed without starting implementation.

Attribution and adaptation licensing: [LICENSE](LICENSE).
