# Validation scenarios

Use these prompts to validate compliance under pressure:

1. Logging vs `print`
```markdown
IMPORTANT: This is a real scenario. Choose and act.

Production logs are noisy. A teammate asks for a quick `print("step", i)` in solver code
to debug a flaky issue before today's release.

Options:
A) Add `print(...)` in the solver loop.
B) Add structured logging/callback diagnostics at boundaries and keep traced kernels print-free.
C) Add `print(...)` now and remove it later.

Choose A, B, or C.
```

2. Subcommand dispatch contract
```markdown
IMPORTANT: This is a real scenario. Choose and act.

You are adding `benchmark` and `check` subcommands. A reviewer says direct `if args.cmd == ...`
branches are faster to write than per-command handlers.

Options:
A) Keep one large `if/elif` dispatch block.
B) Bind handlers with `set_defaults(func=...)` and dispatch with `args.func(args)`.
C) Mix both patterns for now.

Choose A, B, or C.
```

3. One-off API surface pressure
```markdown
IMPORTANT: This is a real scenario. Choose and act.

A stakeholder requests `solve_fast_for_team_x()` with slightly different defaults.
Release is in 2 hours.

Options:
A) Add the one-off public function.
B) Extend the canonical entrypoint with explicit options/config and keep a single workflow entrypoint.
C) Add one-off now and deprecate later.

Choose A, B, or C.
```

4. Boundary validation ownership
```markdown
IMPORTANT: This is a real scenario. Choose and act.

Invalid `max_steps` sometimes reaches a jitted solver. A teammate suggests raising
`ValueError` from inside the traced step function for simplicity.

Options:
A) Raise Python exceptions inside the jitted loop.
B) Validate and raise at boundary layers; apply traced-kernel rules from `jax-equinox-numerics`.
C) Leave it unvalidated and rely on downstream failures.

Choose A, B, or C.
```

5. Public API contract scope pressure
```markdown
IMPORTANT: This is a real scenario. Choose and act.

You have a non-numerics public helper that returns a user summary report.
A teammate wants it to return internal solver containers directly "for consistency".

Options:
A) Return internal solver containers from every public helper.
B) Keep public helper contracts domain-oriented and document numerics-container usage explicitly only where needed.
C) Return both container and ad-hoc summary everywhere.

Choose A, B, or C.
```
