# Validation Notes

Validation targets the source-of-truth skills under
`plugins/coding-skills/skills/`. The historical testing skill named below is
not a runtime dependency of this plugin.

## 2026-10-24: Architecture, testing, and debugging port (0.3.0)

Added `functional-core-imperative-shell`, `property-based-testing`,
`writing-good-tests`, and `systematic-debugging`. Simulation validation was
excluded. Source names are preserved; descriptions intentionally narrow discovery
to the revised responsibilities. Existing domain skill bodies are unchanged.

Static checks:

- All four new skills pass skill-creator `quick_validate.py` with PyYAML.
- Plugin and marketplace JSON parse and their source/skill paths resolve;
  the bundle now contains fourteen skills.
- Markdown links in the four new skills and four workflow skills resolve in
  isolated plugin and skills-only copies, including local license notices.
- `git diff --check` passes. Source playbook files were not edited or packaged.

Independent behavioral trial:

An independent agent read the new skill definitions and applied them to a small
SQLite inventory reservation service and a separate normalization regression.
Artifacts were isolated at `/private/tmp/skill-forward-reservation.33PJ21`.
The parent inspected the implementation/tests and independently reran:

```sh
uv run --with pytest --with hypothesis python -m pytest -p no:capture -q
```

Observed results:

- Kept a pure stock decision and an effectful reservation shell in one module;
  used an explicit `BEGIN IMMEDIATE` transaction with rollback and cleanup.
- Used known-answer tests, real SQLite integration, a trigger-induced write
  failure, and generated reservation sequences with conservation assertions.
  Each generated example received a fresh database.
- The duplicate-preserving sort regression failed before the fix, and Hypothesis
  reduced a failure to `[0, 0]`. Diagnosis isolated the `set` conversion; removing
  it preserved duplicates. Tests checked order, multiplicity, and input preservation.
- Final suite: ten tests passed; parent rerun also passed all ten.

This is a targeted behavioral trial, not an evaluation of model improvement.
No with/without-skill comparison, multi-process contention test, numerical
property trial, or exhaustive runtime/platform validation was performed.

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
