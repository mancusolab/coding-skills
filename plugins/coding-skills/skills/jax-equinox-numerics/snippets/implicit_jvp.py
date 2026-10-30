import jax
import jax.numpy as jnp
import lineax as lx
import optimistix.internal as optxi

# Advanced solver-extension example using an internal Optimistix API.
# For ordinary solves, use optx.root_find(..., adjoint=optx.ImplicitAdjoint()).
# Keep these functions global: no closed-over JAX arrays.


def fn_primal(a):
    # Example: solve y^2 = a for y (pick positive branch)
    root = jnp.sqrt(a)
    residual = root * root - a
    return root, residual


def fn_rewrite(root, residual, a):
    # Rewrite whose Jacobian w.r.t. root is used by implicit JVP
    return root * root - a


def solve(a):
    root, _ = optxi.implicit_jvp(
        fn_primal,
        fn_rewrite,
        a,
        tags=frozenset(),
        linear_solver=lx.AutoLinearSolver(well_posed=True),
    )
    return root


a = jnp.array(4.0)
root, tangent = jax.jvp(solve, (a,), (jnp.ones_like(a),))
