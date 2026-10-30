"""Minimal real-array HiJAX primitive; verified with JAX 0.12.0.1.

This polynomial needs no custom rule in production. It makes the primitive and
transformation contracts easy to check against independent analytic answers.
"""

import jax
import jax.numpy as jnp
from jax.experimental.hijax import (
    HiPrim,
    instantiate_zeros,
    linearize_from_jvp,
    vjp_from_lin,
)


class CubicPlusLinear(HiPrim):
    def __init__(self, aval):
        if not jnp.issubdtype(aval.dtype, jnp.floating):
            raise TypeError("expected a real floating-point array")
        self.in_avals = (aval,)
        self.out_aval = aval
        self.params = {}
        super().__init__()

    def expand(self, x):
        return x * x * x + x

    def jvp(self, primals, tangents):
        (x,), (dx,) = primals, tangents
        return self(x), (3 * x * x + 1) * instantiate_zeros(dx)

    # Forward mode alone does not automatically supply these transformations.
    lin, linearized = linearize_from_jvp
    vjp_fwd, vjp_bwd_retval = vjp_from_lin

    def batch(self, axis_data, args, dims):
        (x,), (axis,) = args, dims
        # Elementwise unary operation: preserve any mapped axis unchanged.
        return cubic_plus_linear(x), axis


def cubic_plus_linear(x):
    x = jnp.asarray(x)
    return CubicPlusLinear(jax.typeof(x))(x)
