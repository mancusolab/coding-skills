# Coding Skills

Codex skills for designing, planning, implementing, and reviewing software,
with domain guidance for Python, JAX/Equinox, Polars, and Rust.

## Contents

The repository is packaged as a local Codex plugin named `coding-skills`.
Each skill is user-invocable and can also be triggered conversationally by its
frontmatter description.

| Skill | What it does |
| --- | --- |
| `design-software` | Grounds design decisions in the repository and defines observable acceptance criteria. |
| `plan-implementation` | Turns agreed requirements into dependency-ordered tasks and verification steps. |
| `implement-plan` | Executes authorized work, tracks progress, verifies behavior, and handles review findings. |
| `review-code` | Reviews changes or existing code for actionable defects against requirements and repository contracts. |
| `functional-core-imperative-shell` | Separates domain computation from effects while preserving cohesive modules and transaction semantics. |
| `property-based-testing` | Designs generated tests with meaningful properties, constrained inputs, and reproducible failures. |
| `systematic-debugging` | Investigates failures with reproductions, discriminating experiments, and causal verification. |
| `writing-good-tests` | Chooses test oracles, scope, isolation, and dependency boundaries around observable contracts. |
| `jax-equinox-numerics` | Applies JAX and Equinox numerics rules: JIT boundaries, PyTrees, static/dynamic fields, dtype stability, solver/sampler contracts, AD, and batching tests. |
| `jax-project-engineering` | Covers project-level engineering for JAX/Equinox code: public APIs, CLI contracts, docs, packaging, serialization, type checks, and CI gates. |
| `polars-data-engineering` | Guides Polars `LazyFrame`/`DataFrame` workflows: lazy planning, materialization boundaries, joins, reconciliation, null policy, and `to_jax()` export. |
| `python-module-design` | Reviews Python package structure: file/module granularity, subpackage boundaries, passive type placement, helper organization, and over-fragmentation. |
| `python-rust-bridge` | Designs Python packages backed by Rust: product shape, PyO3 boundaries, conversion ownership, GIL policy, error mapping, maturin packaging, and bridge tests. |
| `pragmatic-rust-guidelines` | Applies pragmatic Rust review rules: API design, unsafe/FFI, PyO3 adapter hygiene, feature flags, lint policy, performance, and Rust documentation. |

See `plugins/coding-skills/docs/skill-boundaries.md` for the boundary between
overlapping skills, especially the Python/JAX/Polars/Python-Rust split.

## Use the workflows

Start at the stage you need. A small fix can go straight to implementation;
a review does not require a design or plan. For a larger change:

```text
Use $design-software to design resumable imports for this repository.
Use $plan-implementation to turn the agreed design into executable tasks.
Use $implement-plan to carry out that plan and verify the changes.
Use $review-code to review the working-tree changes against the requirements.
```

The workflows use the relevant domain skills from this bundle. They do not
require scientific-software-playbook, other home skills, custom agents, hooks,
MCP servers, or a fresh session between stages. Existing authorization carries
forward; design-only and review-only requests stay within their requested scope.
Delegation is optional and subject to the session's permissions.

## Install

### Plugin install

Use the plugin install when you want Codex to treat these skills as one bundle.
From the repository root:

```bash
codex plugin marketplace add .
codex plugin add coding-skills@coding-skills-local
```

Start a new Codex session. You can also install from the `Coding Skills Local`
marketplace in `/plugins`.

To refresh after pulling changes:

```bash
git pull
codex plugin add coding-skills@coding-skills-local
```

Then start a new session to load the refreshed skills. `marketplace upgrade`
refreshes configured Git marketplace snapshots; this setup uses a local checkout.

### Direct skill install

For local authoring without the plugin, copy the skills into Codex's user skill
directory:

```bash
mkdir -p "$HOME/.agents/skills"
rsync -a --exclude __pycache__ --exclude '*.pyc' \
  plugins/coding-skills/skills/ "$HOME/.agents/skills/"
```

Choose either plugin installation or direct installation to avoid duplicate
skill discovery. Direct installation includes:

- `design-software`
- `plan-implementation`
- `implement-plan`
- `review-code`
- `functional-core-imperative-shell`
- `property-based-testing`
- `writing-good-tests`
- `systematic-debugging`
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

## Licensing

The original six domain skills remain MIT-licensed. The four workflow skills and
four architecture, testing, and debugging skills are adapted from Scientific Software Playbook and distributed under CC BY-SA
4.0. See [the attribution and file-scope notice](plugins/coding-skills/NOTICE)
and the license files bundled with the plugin.
