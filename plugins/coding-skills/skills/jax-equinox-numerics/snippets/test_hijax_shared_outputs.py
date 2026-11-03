"""Independent answers for handwritten structured-output derivative rules."""

import jax
import jax.numpy as jnp
import numpy as np
import pytest
from hijax_shared_outputs import shared_outputs


@pytest.mark.parametrize(
    "strong_x,strong_b", [(False, True), (True, False), (False, False)]
)
def test_declared_output_types_match_scalar_promotion(strong_x, strong_b):
    dtype = jnp.asarray(0.0).dtype
    x = jnp.array(1.0, dtype=dtype) if strong_x else 1.0
    b = jnp.array(2.0, dtype=dtype) if strong_b else 2.0
    expected = {
        "shifted": jnp.asarray(x) + jnp.asarray(b),
        "shared": jnp.asarray(b) ** 2,
    }
    declared = jax.jit(shared_outputs).trace(x, b).out_avals
    assert declared == jax.tree.map(jax.typeof, expected)


@pytest.mark.parametrize("output", ["shifted", "shared"])
def test_unused_output_symbolic_zero(output):
    x, b = jnp.array([1.0, 4.0, -2.0]), jnp.array(3.0)
    dx, db = jax.jit(
        jax.grad(lambda x, b: shared_outputs(x, b)[output].sum(), argnums=(0, 1))
    )(x, b)
    np.testing.assert_array_equal(
        dx, jnp.ones(3) if output == "shifted" else jnp.zeros(3)
    )
    np.testing.assert_allclose(db, 3.0 if output == "shifted" else 6.0)


def test_shared_output_is_counted_once_or_broadcast_as_requested():
    x = jnp.arange(6.0).reshape(2, 3)
    b = jnp.array(2.0)
    mapped = jax.vmap(
        shared_outputs, in_axes=(1, None), out_axes={"shifted": 1, "shared": None}
    )
    out = jax.jit(mapped)(x, b)
    np.testing.assert_array_equal(out["shifted"], x + 2)
    np.testing.assert_allclose(out["shared"], 4)

    def loss(b):
        out = mapped(x, b)
        return out["shifted"].sum() + out["shared"]

    # Six shifted entries plus a single b**2: 6 + 2*b.
    np.testing.assert_allclose(jax.jit(jax.grad(loss))(b), 10)
    np.testing.assert_allclose(jax.jit(jax.grad(jax.grad(loss)))(b), 2)
    np.testing.assert_allclose(jax.jit(jax.jacfwd(jax.grad(loss)))(b), 2)

    def broadcast_loss(b):
        out = jax.vmap(shared_outputs, in_axes=(1, None))(x, b)
        return out["shifted"].sum() + out["shared"].sum()

    # Default out_axes broadcasts the shared scalar to three copies.
    np.testing.assert_allclose(jax.jit(jax.grad(broadcast_loss))(b), 18)


def test_partial_jvp_and_linearization():
    x, b = jnp.array([1.0, -2.0]), jnp.array(3.0)
    # One primal is closed over, exercising a symbolically zero input tangent.
    _, tangent = jax.jit(lambda x: jax.jvp(lambda x: shared_outputs(x, b), (x,), (x,)))(
        x
    )
    np.testing.assert_array_equal(tangent["shifted"], x)
    np.testing.assert_allclose(tangent["shared"], 0)
    _, linear = jax.linearize(shared_outputs, x, b)
    out = jax.jit(linear)(jnp.ones_like(x), jnp.array(2.0))
    np.testing.assert_array_equal(out["shifted"], [3.0, 3.0])
    np.testing.assert_allclose(out["shared"], 12)


def test_checkpoint_gradient_and_unsupported_batching():
    x, b = jnp.array([1.0, -2.0]), jnp.array(3.0)

    def loss(b):
        out = jax.checkpoint(shared_outputs)(x, b)
        return out["shifted"].sum() + out["shared"]

    np.testing.assert_allclose(jax.jit(jax.grad(loss))(b), 8)
    with pytest.raises(NotImplementedError, match="maps x only"):
        jax.vmap(shared_outputs, in_axes=(None, 0))(x, jnp.ones(3))
