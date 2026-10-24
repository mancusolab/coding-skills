# Repository Instructions

Do not run `pytest` directly. Run `pytest -p no:capture`.

This repository contains Codex-only skill definitions. Do not add
runtime-compatibility blocks for other assistant runtimes.

## Layout

- Repo-local marketplace source lives at `.agents/plugins/marketplace.json`.
- Codex plugin source lives under `plugins/coding-skills/`.
- Skill source-of-truth directories live under
  `plugins/coding-skills/skills/<skill-name>/`.
- Skill boundary notes live in `plugins/coding-skills/docs/skill-boundaries.md`.
- Validation notes live in `plugins/coding-skills/docs/validation-notes.md`.
- Keep companion files with their owning skill directory.
- Workflow skills are `design-software`, `plan-implementation`, `implement-plan`,
  and `review-code`. Keep them independent of external home skills, playbook
  scripts, and runtime-specific agent registries.
- Treat the `scientific-software-playbook` symlink, when present, as a read-only
  source reference. Do not package it or edit its target as part of this plugin.
- Do not commit generated Python cache files such as `__pycache__/` or `*.pyc`.

## Editing Skills

- Preserve each skill's frontmatter `name` and `description` unless the edit is
  intentionally changing discovery behavior.
- Keep `SKILL.md` focused on trigger conditions, decision rules, workflows, and
  short examples.
- Put long examples, checklists, snippets, and reference material in companion
  files near the skill that owns them.
- Preserve the file-scoped licensing and provenance in `plugins/coding-skills/NOTICE`.
- Validate new skills with the available skill-creator validator, check relative
  references from an isolated plugin copy, and exercise realistic workflow
  scenarios. Distinguish static checks from behavioral validation in the notes.

## Documentation Audience

- `README.md` is user-facing. Keep it focused on what the plugin is, what skills
  it includes, how to install it, and how to verify usage.
- `AGENTS.md` is agent-facing. Put repository layout, editing policy, validation
  expectations, and maintenance rules here.
