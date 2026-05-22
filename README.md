# Coding Skills

This repository stores useful Codex skills for scientific Python, Rust,
Python/Rust bridge design, and data-engineering workflows.


## Contents

The repository is packaged as a local Codex plugin named `coding-skills`.
Each skill is user-invocable and can also be triggered conversationally by its
frontmatter description.

| Skill | What it does |
| --- | --- |
| `jax-equinox-numerics` | Applies JAX and Equinox numerics rules: JIT boundaries, PyTrees, static/dynamic fields, dtype stability, solver/sampler contracts, AD, and batching tests. |
| `jax-project-engineering` | Covers project-level engineering for JAX/Equinox code: public APIs, CLI contracts, docs, packaging, serialization, type checks, and CI gates. |
| `polars-data-engineering` | Guides Polars `LazyFrame`/`DataFrame` workflows: lazy planning, materialization boundaries, joins, reconciliation, null policy, and `to_jax()` export. |
| `python-module-design` | Reviews Python package structure: file/module granularity, subpackage boundaries, passive type placement, helper organization, and over-fragmentation. |
| `python-rust-bridge` | Designs Python packages backed by Rust: product shape, PyO3 boundaries, conversion ownership, GIL policy, error mapping, maturin packaging, and bridge tests. |
| `pragmatic-rust-guidelines` | Applies pragmatic Rust review rules: API design, unsafe/FFI, PyO3 adapter hygiene, feature flags, lint policy, performance, and Rust documentation. |

See `plugins/coding-skills/docs/skill-boundaries.md` for the boundary between
overlapping skills, especially the Python/JAX/Polars/Python-Rust split.

## Install

### Plugin install

Use the plugin install when you want Codex to treat these skills as one bundle.
From the repository root:

```bash
codex plugin marketplace add .
```

Then restart Codex. In the plugin browser, select the `Coding Skills Local`
marketplace and install `coding-skills`.

To refresh after pulling changes:

```bash
git pull
codex plugin marketplace upgrade coding-skills-local
```

### Direct skill install

For local authoring without the plugin, copy the skills into Codex's user skill
directory:

```bash
mkdir -p "$HOME/.agents/skills"
rsync -a --exclude __pycache__ --exclude '*.pyc' \
  plugins/coding-skills/skills/ "$HOME/.agents/skills/"
```

This installs:

- `jax-equinox-numerics`
- `jax-project-engineering`
- `polars-data-engineering`
- `python-module-design`
- `python-rust-bridge`
- `pragmatic-rust-guidelines`

For repo-scoped installation, replace the destination with
`/path/to/repo/.agents/skills/`.

### Verify

Start a new Codex session and invoke a skill explicitly:

```text
Use $python-rust-bridge to review this package boundary.
```

For direct installs, you can also check the installed files:

```bash
find "$HOME/.agents/skills" -maxdepth 2 -name SKILL.md | sort
```
