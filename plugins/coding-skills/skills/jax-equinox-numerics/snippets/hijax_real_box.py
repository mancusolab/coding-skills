"""Teaching-only opaque real array; ordinary arrays need no wrapper.

Verified with JAX 0.12.0.1. Supports JIT, AD, leading-axis mapping and scan.
Distributed transformations and Equinox filtered transforms are not covered.
"""

from dataclasses import dataclass

import jax
import jax.numpy as jnp
from jax.experimental.hijax import (
    HiPrim,
    HiType,
    MappingSpec,
    ShapedArray,
    instantiate_zeros,
    linearize_from_jvp,
    register_hitype,
    vjp_from_lin,
)


@dataclass(frozen=True)
class RealBox:
    payload: jax.Array


@dataclass(frozen=True)
class Leading(MappingSpec):
    pass


@dataclass(frozen=True)
class RealBoxTy(HiType):
    array_type: ShapedArray

    def __post_init__(self):
        if not jnp.issubdtype(self.array_type.dtype, jnp.floating):
            raise TypeError("expected a real floating-point payload")

    def lo_ty(self):
        return [self.array_type]

    def lower_val(self, value):
        return [value.payload]

    def raise_val(self, payload):
        return RealBox(payload)

    def to_tangent_aval(self):
        return self.array_type.to_tangent_aval()

    def dec_rank(self, size, spec):
        if not isinstance(spec, Leading):
            raise TypeError("expected Leading mapping spec")
        if not self.array_type.shape or self.array_type.shape[0] != size:
            raise ValueError("mapped size must match leading dimension")
        return RealBoxTy(self.array_type.dec_rank(size, 0))

    def inc_rank(self, size, spec):
        if not isinstance(spec, Leading):
            raise TypeError("expected Leading mapping spec")
        return RealBoxTy(self.array_type.inc_rank(size, 0))

    def leading_axis_spec(self):
        return Leading()


register_hitype(RealBox, lambda value: RealBoxTy(jax.typeof(value.payload)))


class Pack(HiPrim):
    def __init__(self, aval):
        self.in_avals = (aval,)
        self.out_aval = RealBoxTy(aval)
        self.params = {}
        super().__init__()

    def expand(self, x):
        return RealBox(x)

    def jvp(self, primals, tangents):
        (x,), (dx,) = primals, tangents
        return self(x), instantiate_zeros(dx)

    lin, linearized = linearize_from_jvp
    vjp_fwd, vjp_bwd_retval = vjp_from_lin

    def batch(self, axis_data, args, dims):
        (x,), (axis,) = args, dims
        if axis is None:
            return pack(x), None
        return pack(jnp.moveaxis(x, axis, 0)), Leading()


class Unpack(HiPrim):
    def __init__(self, aval):
        if not isinstance(aval, RealBoxTy):
            raise TypeError("expected RealBox")
        self.in_avals = (aval,)
        self.out_aval = aval.array_type
        self.params = {}
        super().__init__()

    def expand(self, value):
        return value.payload

    def jvp(self, primals, tangents):
        (value,), (tangent,) = primals, tangents
        return self(value), instantiate_zeros(tangent)

    lin, linearized = linearize_from_jvp
    vjp_fwd, vjp_bwd_retval = vjp_from_lin

    def batch(self, axis_data, args, dims):
        (value,), (spec,) = args, dims
        if spec is None:
            return unpack(value), None
        if not isinstance(spec, Leading):
            raise TypeError("expected Leading mapping spec")
        return unpack(value), 0


def pack(x):
    x = jnp.asarray(x)
    return Pack(jax.typeof(x))(x)


def unpack(value):
    return Unpack(jax.typeof(value))(value)
