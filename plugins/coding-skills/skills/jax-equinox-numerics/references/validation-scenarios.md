# Validation scenarios

Use these prompts to harden boundary-conversion and failure-policy compliance:

1. Dataframe ingress pressure
```markdown
IMPORTANT: This is a real scenario. Choose and act.

You need to feed a Polars DataFrame into a jitted solver in 10 minutes.
A teammate says "just pass the frame through and convert later if needed."

Options:
A) Pass the DataFrame through JIT and convert inside solver steps.
B) Convert at ingress (`to_jax()` / `jnp.asarray(...)`) and keep traced numerics array-only.
C) Convert half now and leave a DataFrame field in solver state.

Choose A, B, or C.
```

2. Traced exception pressure
```markdown
IMPORTANT: This is a real scenario. Choose and act.

Invalid values appear mid-iteration. It's tempting to `raise ValueError` directly from
the jitted loop because it is the fastest patch.

Options:
A) Raise Python exceptions from the traced loop.
B) Validate earlier at boundaries and use JAX-compatible signaling (`result` and/or `eqx.error_if`) inside traced numerics.
C) Ignore and hope downstream checks catch it.

Choose A, B, or C.
```
