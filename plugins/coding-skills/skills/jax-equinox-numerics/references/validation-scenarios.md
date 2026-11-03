# Validation scenarios

## Experimental custom types

Use these open-ended prompts when revising HiType guidance. Evaluate API choices
and stated validation limits, not matching wording.

1. A user wants coupled compressed weights to remain one value in jaxprs, with
   dense gradients. Sketch the representation and transformation contracts, and
   explain what must be tested before calling it supported. They only need JIT
   and reverse AD initially; avoid requiring every available transform.
2. A proposed VJP reads `weights.payload` and returns a new registered container
   around traced arrays. Diagnose why eager success is insufficient and show
   where constructor/accessor operations belong.
3. A user wants to map and scan over custom values with no ordinary array
   inputs, then add distributed AD. Identify the additional interfaces and
   validation needed at each stage; do not infer distributed support from JIT.
4. A user proposes replacing every Equinox module with a HiType because it is
   newer. Assess the tradeoff without claiming established best practices or
   assuming array-based filtering recognizes all registered values.

## Primitive derivative scenarios

1. A multi-output primitive works when every output is used but fails when a
   loss selects one output. Inspect its handwritten backward rule and propose
   a regression test with an independent expected gradient.
2. A primitive takes mapped vectors and a shared scalar and emits both mapped
   and shared outputs. Specify which cotangents need batch reduction and test
   both a shared result and a result explicitly broadcast by `out_axes`.
3. A user wants to validate a surrogate gradient with numerical perturbations
   and to derive its JVP from a nonlinear clipped backward rule. Explain which
   mathematical contracts apply and choose validation against the intended rule.
4. A VJP-only primitive passes `grad` but fails inside checkpointing. Inspect
   the supported JAX version/configuration before choosing a repair; avoid a
   blanket global configuration change.

## Boundary conversion and failure policy

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
