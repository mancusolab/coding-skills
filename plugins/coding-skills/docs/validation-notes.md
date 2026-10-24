# Validation Notes

Validation targets the source-of-truth skills under
`plugins/coding-skills/skills/`. The historical testing skill named below is
not a runtime dependency of this plugin.

## 2026-10-24: Codex workflow port

Added `design-software`, `plan-implementation`, `implement-plan`, and
`review-code`. Each was validated with the installed skill-creator's
`quick_validate.py` using an isolated PyYAML environment. The six pre-existing
domain skill directories were unchanged.

Static checks:

- Plugin and marketplace JSON parse, source paths resolve, and the bundle
  contains ten skills.
- All workflow Markdown resource links resolve in an isolated plugin copy and
  in a skills-only direct-install copy. The domain routing reference was moved
  into the design skill after inspection exposed that plugin-level docs are
  absent from direct skill installs.
- Python snippet syntax and `git diff --check` pass. Snippet numerical behavior
  was not tested as part of this prose port.
- Adapted workflows include licensing in their own directories as well as the
  plugin's attribution notice, so direct copies retain their notices.

Independent forward tests used temporary fixtures outside this repository and
an isolated plugin copy, without the playbook or home workflow skills:

| Scenario | Observed result |
| --- | --- |
| Design and plan a dependency-free Node NDJSON-to-CSV CLI; planning only | Produced two documents, seven acceptance criteria and four pending tasks; chose routine details without a confirmation loop; created no implementation and claimed no behavioral test results. |
| Execute an authorized port-range validation fix without delegation | Reproduced four failing range subtests, implemented the fix, passed three unittest methods, preserved user notes, updated plan evidence, and made no commit. The parent independently reran the passing tests. |
| Review local staged/unstaged/untracked changes without editing | Inspected all three scopes, found the quantity-omission regression with a failing test, reported the trigger and line, and made no edits. |

A separate read-only review of the final workflow files, packaging, resources,
licensing, and scope/authorization instructions found no actionable issues.
These checks provide targeted evidence, not exhaustive validation of every
future workflow or domain combination.

## 2026-05-21

Using `testing-skills-with-subagents`, two independent explorer agents tested
pressure scenarios covering:

- Python/JAX file-list pressure and Equinox inheritance layout pressure
- JAX public API failure contracts versus traced execution semantics
- Polars positional-alignment shortcuts before `to_jax()`
- Rust CLI packaging pressure toward fake PyO3 APIs
- PyO3 unsafe/GIL performance shortcuts
- Rust library error-boundary leakage

Observed hardening needs:

- Add explicit validation scenarios to skills that had strong rules but no
  pressure prompts.
- Make the JAX runtime/API split explicit for public solver failure behavior.
- Make `pragmatic-rust-guidelines` mandatory for PyO3 adapter, GIL, panic,
  unsafe, feature-flag, and performance work in Rust-backed Python packages.

Edits made:

- `python-module-design/SKILL.md`: added file-list and Equinox inheritance
  validation scenarios.
- `polars-data-engineering/SKILL.md`: added positional-alignment validation
  scenario.
- `python-rust-bridge/SKILL.md`: added CLI-packaging and compiled-state
  persistence validation scenarios.
- `pragmatic-rust-guidelines/SKILL.md`: added PyO3 unsafe performance and
  library error-boundary validation scenarios.
- `docs/skill-boundaries.md`: strengthened cross-skill loading rules.
