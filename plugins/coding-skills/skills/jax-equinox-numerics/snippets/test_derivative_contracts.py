"""Analytic answers plus consistency identities, without step-size tuning."""

import jax
import jax.numpy as jnp
import numpy as np
from hijax_polynomial import cubic_plus_linear


def test_analytic_jvp_linearity_and_adjoint_identity():
    x = jnp.array([-2.0, 0.0, 3.0])
    u = jnp.array([1.0, -2.0, 0.5])
    v = jnp.array([-1.0, 3.0, 2.0])
    ct = jnp.array([2.0, 1.0, -3.0])

    @jax.jit
    def push(tangent):
        return jax.jvp(cubic_plus_linear, (x,), (tangent,))[1]

    # Independent known derivative values prevent mutually consistent wrong rules
    # from passing the identity checks alone.
    np.testing.assert_allclose(push(u), jnp.array([13.0, 1.0, 28.0]) * u)
    np.testing.assert_allclose(push(2 * u - v), 2 * push(u) - push(v))
    _, pull = jax.vjp(cubic_plus_linear, x)
    np.testing.assert_allclose(jnp.vdot(push(u), ct), jnp.vdot(u, pull(ct)[0]))
