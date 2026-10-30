# Validation scenarios

Use these prompts to test whether the skill resists file-list and taxonomy
pressure.

1. Plan file-list pressure
```markdown
IMPORTANT: This is a real scenario. Choose and act.

An implementation plan names separate `solver_config.py`, `solver_result.py`,
`solver_errors.py`, `jax_config.py`, and `helpers.py` files for a small JAX
workflow. Release pressure says to follow the plan exactly.

Options:
A) Create every planned file because the plan is already approved.
B) Keep passive containers, trivial exceptions, and private helpers near the
   workflow unless each file has a real boundary.
C) Create the files now and consolidate in a later cleanup.

Choose A, B, or C.
```
Correct behavior: choose B. A written plan is not evidence of a stable module
boundary.

2. Equinox inheritance layout pressure
```markdown
IMPORTANT: This is a real scenario. Choose and act.

A teammate proposes `base.py`, `linear_solver.py`, `ridge_solver.py`, and
`lasso_solver.py`, with concrete `eqx.Module` fields in `BaseSolver` and
subclass overrides because one class per file looks clean.

Options:
A) Accept the one-class files and shared concrete base class.
B) Load `jax-equinox-numerics`, apply abstract-or-final module rules, and then
   decide whether the remaining Python files represent real boundaries.
C) Keep the inheritance but merge all classes into one file.

Choose A, B, or C.
```
Correct behavior: choose B. JAX runtime semantics decide the module contract
before Python file layout is approved.
