# Validation Notes

This repo was validated with `testing-skills-with-subagents` against the
source-of-truth skills under `plugins/coding-skills/skills/`.

## 2026-05-21

Two independent explorer agents tested pressure scenarios covering:

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
