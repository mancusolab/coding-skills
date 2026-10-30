"""Transformation contracts for the runnable HiJAX example."""

import jax
import jax.numpy as jnp
import numpy as np
import pytest
from hijax_polynomial import cubic_plus_linear


def test_primal_and_forward_mode():
    x = jnp.array([-2.0, 0.0, 3.0])
    y, dy = jax.jit(lambda x: jax.jvp(cubic_plus_linear, (x,), (jnp.ones_like(x),)))(x)
    np.testing.assert_allclose(y, [-10, 0, 30])
    np.testing.assert_allclose(dy, [13, 1, 28])


def test_reverse_and_second_derivative():
    derivative = jax.grad(cubic_plus_linear)
    np.testing.assert_allclose(jax.jit(derivative)(2.0), 13)
    np.testing.assert_allclose(jax.jit(jax.grad(derivative))(2.0), 12)
    np.testing.assert_allclose(jax.jacfwd(derivative)(2.0), 12)


def test_linearization():
    value, linear = jax.linearize(cubic_plus_linear, jnp.array(2.0))
    np.testing.assert_allclose(value, 10)
    np.testing.assert_allclose(jax.jit(linear)(jnp.array(3.0)), 39)


def test_batching_nonleading_axis_and_grad():
    x = jnp.array([[0.0, 1.0], [2.0, 3.0]])
    actual = jax.jit(jax.vmap(cubic_plus_linear, in_axes=1, out_axes=1))(x)
    np.testing.assert_allclose(actual, [[0, 2], [10, 30]])
    gradient = jax.jit(jax.grad(lambda x: jax.vmap(cubic_plus_linear)(x).sum()))(x)
    np.testing.assert_allclose(gradient, [[1, 4], [13, 28]])


def test_invalid_dtype():
    with pytest.raises(TypeError, match="real floating-point"):
        cubic_plus_linear(jnp.array([1, 2], dtype=jnp.int32))
