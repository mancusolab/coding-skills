# Validation Notes

Validation records for the skills under `plugins/coding-skills/skills/`.

## 2026-10-29

Fixed four executable-example defects in `jax-equinox-numerics`:

- The implicit JVP example now imports `optimistix.internal.implicit_jvp`,
  identifies it as an advanced internal API, and demonstrates differentiation
  through the positive square root. Ordinary solver users are directed to
  `root_find` with `ImplicitAdjoint`.
- The reference norm JVP guards the denominator before division so reverse
  differentiation at zero follows the example's zero-tangent convention.
- The jitted JVP reference binds the function with `functools.partial` before
  passing it to `filter_jit`.
- The finite-difference helper chooses its default step from the input dtype's
  machine epsilon rather than assuming float64 precision.

[test_ad_examples.py](../skills/jax-equinox-numerics/snippets/test_ad_examples.py)
exercises the reference code blocks and implicit solve under JIT, checking
analytic derivatives at zero and nonzero inputs. The
existing finite-difference test checks the dtype-sensitive comparison. These
tests reproduced the failures before the fixes.

Run the numerical example tests from the repository root:

```bash
uv run --with jax --with equinox --with lineax --with optimistix --with pytest \
  pytest -p no:capture -p no:cacheprovider \
  plugins/coding-skills/skills/jax-equinox-numerics/snippets
```

Repeat with `JAX_ENABLE_X64=1` to check float64 behavior. The environment used
JAX 0.12.0.1, Equinox 0.13.8, Lineax 0.1.1, and Optimistix 0.1.0 on CPU.

Results: seven tests passed in each precision mode, all ten non-test Python
snippets executed, and the modified Python files passed Ruff formatting and
lint checks. Syntax, companion references, unchanged frontmatter, and preserved
validation prompts were also checked.

The Codex-only cleanup also:

- Consolidated repeated relative-path, checklist, and snippet instructions.
- Removed plugin-maintenance instructions from the project-engineering skill,
  a missing temporary-checkout reference, and undefined CLI profile labels.
- Replaced the assumed Microsoft book checkout path with its official website.
- Moved validation prompts from all six entrypoints into linked companion
  files, preserving the prompts. Load these only when testing or revising the
  skill.
- Preserved every skill's frontmatter name and description.

No Claude/Codex compatibility blocks or preprocessing markers were present in
the skill sources. Remaining ellipses in short domain examples represent
omitted user code, rather than unexpanded preprocessing placeholders.

## 2026-05-21

This pass used `testing-skills-with-subagents` against the source skills.

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
