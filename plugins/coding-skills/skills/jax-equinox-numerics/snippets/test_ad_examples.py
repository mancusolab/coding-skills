"""Exercise the runnable AD reference examples, not copies of their algorithms."""

from pathlib import Path

import equinox as eqx
import jax
import jax.numpy as jnp
import numpy as np
import pytest
from implicit_jvp import solve

REFERENCE = (
    Path(__file__).resolve().parents[1] / "references/ad_checkpointing_callbacks.md"
)


def reference_example(heading, namespace=None):
    section = REFERENCE.read_text().split(f"### Rule: {heading}\n", 1)[1]
    code = section.split("```python\n", 1)[1].split("```", 1)[0]
    namespace = {} if namespace is None else namespace
    # Execute only examples from this trusted repository, never external input.
    exec(compile(code, str(REFERENCE), "exec"), namespace)  # noqa: S102
    return namespace


@pytest.fixture
def stable_norm():
    return reference_example("Use custom JVP/VJP for implicit or iterative methods")[
        "stable_norm"
    ]


@pytest.mark.parametrize("values, expected", [([0.0, 0.0], 0.0), ([3.0, 4.0], 1.4)])
def test_norm_jvp(stable_norm, values, expected):
    x = jnp.array(values)
    value, tangent = eqx.filter_jit(
        lambda x: eqx.filter_jvp(stable_norm, (x,), (jnp.ones_like(x),))
    )(x)
    np.testing.assert_allclose(value, np.linalg.norm(values), rtol=1e-6)
    np.testing.assert_allclose(tangent, expected, rtol=1e-6)


@pytest.mark.parametrize(
    "values, expected", [([0.0, 0.0], [0.0, 0.0]), ([3.0, 4.0], [0.6, 0.8])]
)
def test_norm_reverse_derivative(stable_norm, values, expected):
    # At zero this checks the documented custom convention, not a derivative
    # of the ordinary Euclidean norm (which is undefined there).
    gradient = eqx.filter_jit(eqx.filter_grad(stable_norm))(jnp.array(values))
    np.testing.assert_allclose(gradient, expected, rtol=1e-6)


def test_implicit_solve_under_jit_and_batching():
    inputs = jnp.array([1.0, 4.0, 9.0])
    roots = jax.jit(jax.vmap(solve))(inputs)
    derivatives = jax.jit(jax.vmap(jax.grad(solve)))(inputs)
    np.testing.assert_allclose(roots, [1.0, 2.0, 3.0], rtol=1e-6)
    np.testing.assert_allclose(derivatives, [0.5, 0.25, 1 / 6], rtol=1e-6)


def test_reference_jitted_jvp_binding():
    namespace = reference_example(
        "Test JVP/VJP and batching under JIT with finite differences",
        {"f": lambda x: x * x, "x": jnp.array([2.0, 3.0]), "tx": jnp.array([1.0, 2.0])},
    )
    np.testing.assert_allclose(namespace["out"], [4.0, 9.0], rtol=1e-6)
    np.testing.assert_allclose(namespace["t_out"], [4.0, 12.0], rtol=1e-6)
