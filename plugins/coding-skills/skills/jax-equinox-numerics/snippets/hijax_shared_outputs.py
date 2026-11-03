"""Teaching example: structured outputs and a scalar shared across a batch.

Verified with JAX 0.12.0.1. Only x may be mapped; b remains scalar.
No distributed or ref-accumulator support is claimed.
"""

import jax
import jax.numpy as jnp
from jax.experimental.hijax import (
    HiPrim,
    Zero,
    instantiate_zeros,
    linearize_from_jvp,
)


class SharedOutputs(HiPrim):
    def __init__(self, x_aval, b_aval):
        if (
            b_aval.shape != ()
            or x_aval.dtype != b_aval.dtype
            or not jnp.issubdtype(x_aval.dtype, jnp.floating)
        ):
            raise TypeError("expected real x and scalar b with matching dtypes")
        self.in_avals = (x_aval, b_aval)
        # Addition is weakly typed only when both operands are weakly typed.
        shifted_aval = x_aval.update(weak_type=x_aval.weak_type and b_aval.weak_type)
        self.out_aval = {"shifted": shifted_aval, "shared": b_aval}
        self.params = {}
        super().__init__()

    def expand(self, x, b):
        return {"shifted": x + b, "shared": b * b}

    def vjp_fwd(self, nzs_in, x, b):
        # Only b is needed backward; retain the primitive for higher derivatives.
        return self(x, b), b

    def vjp_bwd_retval(self, b, cotangents):
        ct = jax.tree.map(
            instantiate_zeros, cotangents, is_leaf=lambda v: isinstance(v, Zero)
        )
        # shifted has x's shape; shared is a single scalar, counted only once.
        return ct["shifted"], ct["shifted"].sum() + 2 * b * ct["shared"]

    def jvp(self, primals, tangents):
        x, b = primals
        dx, db = map(instantiate_zeros, tangents)
        return self(x, b), {"shifted": dx + db, "shared": 2 * b * db}

    lin, linearized = linearize_from_jvp

    def batch(self, axis_data, args, dims):
        x, b = args
        x_dim, b_dim = dims
        if b_dim is not None:
            raise NotImplementedError("this example maps x only")
        if x_dim is None:
            return shared_outputs(x, b), {"shifted": None, "shared": None}
        x = jnp.moveaxis(x, x_dim, 0)
        return shared_outputs(x, b), {"shifted": 0, "shared": None}


def shared_outputs(x, b):
    x, b = jnp.asarray(x), jnp.asarray(b)
    return SharedOutputs(jax.typeof(x), jax.typeof(b))(x, b)
