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
- Do not commit generated Python cache files such as `__pycache__/` or `*.pyc`.

## Editing Skills

- Preserve each skill's frontmatter `name` and `description` unless the edit is
  intentionally changing discovery behavior.
- Keep `SKILL.md` focused on trigger conditions, decision rules, workflows, and
  short examples.
- Put long examples, checklists, snippets, and reference material in companion
  files near the skill that owns them.

## Documentation Audience

- `README.md` is user-facing. Keep it focused on what the plugin is, what skills
  it includes, how to install it, and how to verify usage.
- `AGENTS.md` is agent-facing. Put repository layout, editing policy, validation
  expectations, and maintenance rules here.
