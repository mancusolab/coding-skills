# Validation scenarios

Use these prompts to harden lazy-boundary and adapter-boundary compliance:

1. Lazy-vs-eager pressure
```markdown
IMPORTANT: This is a real scenario. Choose and act.

You need to clean, join, and aggregate three parquet-backed tables before
feeding the result into a model training step.

Options:
A) Read each table eagerly, mutate step by step, and materialize after every join.
B) Build one lazy query pipeline, validate at the adapter boundary, then collect once near export.
C) Mix lazy and eager opportunistically with no stated boundary.

Choose A, B, or C.
```

2. `to_jax()` pressure
```markdown
IMPORTANT: This is a real scenario. Choose and act.

A teammate wants to call `to_jax()` "somewhere later" after data prep already
crossed into numerics code.

Options:
A) Let Polars objects cross the numerics boundary and convert when convenient.
B) Keep Polars in the adapter layer, collect to `DataFrame`, then convert once at the boundary.
C) Skip `to_jax()` and rely on implicit downstream coercion.

Choose A, B, or C.
```

3. Positional-alignment pressure
```markdown
IMPORTANT: This is a real scenario. Choose and act.

Three parquet-backed tables share sample IDs. The model only needs arrays, and
the row counts happen to match. A teammate wants to horizontally concatenate
the tables, convert each one to JAX, and debug shape errors downstream.

Options:
A) Horizontally concatenate independently loaded tables because row counts match.
B) Join by explicit keys, validate cardinality and missing keys, freeze row
   order, then export arrays.
C) Convert each table to JAX and rely on downstream shape checks.

Choose A, B, or C.
```
Correct behavior: choose B. Matching row counts are not an alignment contract.
