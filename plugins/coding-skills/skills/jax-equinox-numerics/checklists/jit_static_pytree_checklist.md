# JIT / Static / PyTree Checklist

Use this before performance tuning or when encountering retracing.

## JIT boundaries
- [ ] JIT is applied once at the public API boundary.
- [ ] For multi-device sharding, prefer `eqx.filter_jit` + `eqx.filter_shard`; use `filter_pmap` only when pmap-specific semantics are required.
- [ ] No nested JITs inside inner loops or solver steps.
- [ ] Large subgraphs are staged explicitly if compile time dominates.

## Static vs dynamic
- [ ] All non-array config is static (fields or partitioned).
- [ ] Use `eqx.filter_jit` for mixed PyTrees/Modules with static leaves; `jax.jit` also supports registered HiTypes. Verify filtered-transform support before using Equinox with opaque HiType values.
- [ ] Dynamic inputs are JAX-supported values or PyTrees of them; arbitrary unregistered Python objects do not cross traced boundaries.
- [ ] Multi-source tabular inputs are reconciled by explicit key joins in adapters before conversion; positional row matching is not used.
- [ ] Table/dataframe objects (Polars/Pandas) are converted to arrays at ingress after reconciliation; traced functions receive JAX-supported values/PyTrees.
- [ ] `eqx.filter_closure_convert` is used for functions passed across JIT/AD boundaries.
- [ ] Closed-over JAX arrays are blocked at boundaries (`eqxi.nontraceable`) when closure conversion is not enough.

## PyTree stability
- [ ] State treedef and leaf shapes/dtypes are unchanged across iterations.
- [ ] Choose shape evaluation according to the supported value types; verify filtering behavior for custom HiTypes rather than assuming non-array means static.
- [ ] Structure checks avoid fabricated dummy arrays.
- [ ] `eqx.partition` + `eqx.combine` are used to keep static leaves fixed.

## Control flow
- [ ] No Python `if/for/while` branches depend on arrays inside JIT.
- [ ] `lax.cond` branches return identical PyTree structure.
- [ ] `lax.scan` carries only fixed-shape data.
