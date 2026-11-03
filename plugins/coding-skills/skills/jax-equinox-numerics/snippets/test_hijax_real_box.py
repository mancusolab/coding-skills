"""Observable contracts for the experimental opaque-value example."""

import jax
import jax.numpy as jnp
import numpy as np
import pytest
from hijax_real_box import Leading, pack, unpack


def test_lowering_roundtrip_and_jit_boundaries():
    x = jnp.arange(6.0).reshape(2, 3)
    value = jax.jit(pack)(x)
    ty = jax.typeof(value)
    assert ty == jax.typeof(pack(x + 1))
    assert hash(ty) == hash(jax.typeof(pack(x + 1)))
    assert ty != jax.typeof(pack(x.T))
    assert ty.lo_ty() == [jax.typeof(x)]
    restored = ty.raise_val(*ty.lower_val(value))
    np.testing.assert_array_equal(jax.jit(unpack)(restored), x)
    np.testing.assert_array_equal(jax.jit(lambda x: unpack(pack(x)))(x), x)


def test_dense_tangents_and_composed_derivatives():
    x = jnp.array([2.0, -3.0])
    value = pack(x)

    def loss(value):
        return jnp.sum(unpack(value) ** 2)

    np.testing.assert_allclose(jax.jit(jax.grad(loss))(value), 2 * x)
    primal, tangent = jax.jvp(unpack, (value,), (jnp.ones_like(x),))
    np.testing.assert_array_equal(primal, x)
    np.testing.assert_array_equal(tangent, jnp.ones_like(x))
    gradient = jax.grad(lambda x: loss(pack(x)))
    np.testing.assert_allclose(jax.jit(jax.jacfwd(gradient))(x), 2 * jnp.eye(2))


def test_mapping_axis_conversion_and_batched_gradients():
    x = jnp.arange(6.0).reshape(2, 3)
    values = jax.jit(jax.vmap(pack, in_axes=1, out_axes=Leading()))(x)
    result = jax.jit(jax.vmap(unpack, in_axes=Leading(), out_axes=1, axis_size=3))(
        values
    )
    np.testing.assert_array_equal(result, x)
    gradients = jax.vmap(
        jax.grad(lambda value: jnp.sum(unpack(value) ** 2)),
        in_axes=Leading(),
        axis_size=3,
    )(values)
    np.testing.assert_allclose(gradients, 2 * x.T)


def test_scan_hi_inputs_carry_and_outputs():
    x = jnp.arange(6.0).reshape(3, 2)

    def run(values):
        def step(carry, value):
            total = pack(unpack(carry) + unpack(value))
            return total, total

        return jax.lax.scan(step, pack(jnp.zeros(2)), values, length=3)

    total, history = jax.jit(run)(pack(x))
    np.testing.assert_array_equal(unpack(total), x.sum(axis=0))
    np.testing.assert_array_equal(unpack(history), jnp.cumsum(x, axis=0))


def test_reject_integer_payload_and_bad_mapping_size():
    with pytest.raises(TypeError, match="floating-point"):
        jax.jit(pack)(jnp.array([1, 2]))
    with pytest.raises(ValueError, match="leading dimension"):
        jax.vmap(unpack, in_axes=Leading(), axis_size=3)(pack(jnp.ones((2, 4))))
