import numpy as np
from typing import Iterable
from scipy.spatial.transform import Rotation as Rot
from ark_msgs.registry import msgs

# rotation_pb2.py is generated from rotation.proto
from .rotation_pb2 import Rotation

ProtoOrScipyRotation = Rotation | Rot


def _as_scipy(r: ProtoOrScipyRotation) -> Rot:
    """Convert to scipy.spatial.transform.Rotation."""
    if isinstance(r, Rotation):
        return Rot.from_quat([r.x, r.y, r.z, r.w])
    return r


def _as_proto(r: ProtoOrScipyRotation) -> Rotation:
    """Convert to ark_msgs.rotation.Rotation."""
    x, y, z, w = r.as_quat().reshape(4).astype(np.float32)
    return Rotation(x=x, y=y, z=z, w=w)


@classmethod
def from_quat(cls, quat: Iterable[float], *, scalar_first: bool = False) -> Rotation:
    """
    Initialize from quaternions.

    Parameters match SciPy's Rotation.from_quat with scalar_first support.
    """
    quat = np.asarray(quat, dtype=np.float32).reshape(4)
    x, y, z, w = Rot.from_quat(quat, scalar_first=scalar_first).as_quat()
    return cls(x=x, y=y, z=z, w=w)


@classmethod
def from_matrix(cls, matrix: Iterable[Iterable[float]]) -> Rotation:
    """Initialize from rotation matrix."""
    matrix = np.asarray(matrix, dtype=np.float32).reshape(3, 3)
    return _as_proto(Rot.from_matrix(matrix))


@classmethod
def from_rotvec(cls, rotvec: Iterable[float], degrees: bool = False) -> Rotation:
    """Initialize from rotation vectors."""
    rotvec = np.asarray(rotvec, dtype=np.float32).reshape(3)
    return _as_proto(Rot.from_rotvec(rotvec, degrees=degrees))


@classmethod
def from_mrp(cls, mrp: Iterable[float]) -> Rotation:
    """Initialize from Modified Rodrigues Parameters (MRPs)."""
    mrp = np.asarray(mrp, dtype=np.float32).reshape(3)
    return _as_proto(Rot.from_mrp(mrp))


@classmethod
def from_euler(
    cls, seq: str, angles: Iterable[float], degrees: bool = False
) -> Rotation:
    """Initialize from Euler angles."""
    return _as_proto(Rot.from_euler(seq, angles, degrees=degrees))


@classmethod
def from_davenport(
    cls,
    axes: Iterable[int] | int,
    order: str,
    angles: Iterable[float] | float,
    degrees: bool = False,
) -> Rotation:
    """Initialize from Davenport angles."""
    return _as_proto(Rot.from_davenport(axes, order, angles, degrees=degrees))


def as_quat(
    self: Rotation, canonical: bool = False, *, scalar_first: bool = False
) -> np.ndarray:
    """Represent as quaternions."""
    return _as_scipy(self).as_quat(canonical=canonical, scalar_first=scalar_first)


def as_matrix(self: Rotation) -> np.ndarray:
    """Represent as rotation matrix."""
    return _as_scipy(self).as_matrix()


def as_rotvec(self: Rotation, degrees: bool = False) -> np.ndarray:
    """Represent as rotation vectors."""
    return _as_scipy(self).as_rotvec(degrees=degrees)


def as_mrp(self: Rotation) -> np.ndarray:
    """Represent as Modified Rodrigues Parameters (MRPs)."""
    return _as_scipy(self).as_mrp()


def as_euler(
    self: Rotation, seq: str, degrees: bool = False, *, suppress_warnings: bool = False
) -> np.ndarray:
    """Represent as Euler angles."""
    return _as_scipy(self).as_euler(
        seq, degrees=degrees, suppress_warnings=suppress_warnings
    )


def as_davenport(
    self: Rotation,
    axes: Iterable[int] | int,
    order: str,
    degrees: bool = False,
    *,
    suppress_warnings: bool = False,
) -> np.ndarray:
    """Represent as Davenport angles."""
    return _as_scipy(self).as_davenport(
        axes, order, degrees=degrees, suppress_warnings=suppress_warnings
    )


def inv(self: Rotation) -> Rotation:
    """Invert this rotation."""
    return _as_proto(_as_scipy(self).inv())


def magnitude(self: Rotation) -> float:
    """Get the magnitude of the rotation (in radians)."""
    return float(_as_scipy(self).magnitude())


@classmethod
def identity(cls) -> Rotation:
    """Get identity rotation."""
    return _as_proto(Rot.identity())


@classmethod
def random(cls, rng: np.random.Generator | int | None = None) -> Rotation:
    """Generate uniformly distributed rotations."""
    return _as_proto(Rot.random(random_state=rng))


def __mul__(self: Rotation, other: ProtoOrScipyRotation) -> Rotation:
    """
    Compose rotations (SciPy semantics).

    r = r1 * r2 means: apply r2, then apply r1.
    """
    return _as_proto(_as_scipy(self) * _as_scipy(other))


def __rmul__(self: Rotation, other: ProtoOrScipyRotation) -> Rotation:
    """
    Compose rotations (SciPy semantics), reversed operands.
    r = r2 * r1 means: apply r1, then apply r2.
    """
    # Handles cases where the left operand doesn't know how to multiply.
    return _as_proto(_as_scipy(other) * _as_scipy(self))


# Monkeypatch onto the generated protobuf class (only if missing)
if not hasattr(Rotation, "from_quat"):
    Rotation.from_quat = from_quat
if not hasattr(Rotation, "from_matrix"):
    Rotation.from_matrix = from_matrix
if not hasattr(Rotation, "from_rotvec"):
    Rotation.from_rotvec = from_rotvec
if not hasattr(Rotation, "from_mrp"):
    Rotation.from_mrp = from_mrp
if not hasattr(Rotation, "from_euler"):
    Rotation.from_euler = from_euler
if not hasattr(Rotation, "from_davenport"):
    Rotation.from_davenport = from_davenport

if not hasattr(Rotation, "as_quat"):
    Rotation.as_quat = as_quat
if not hasattr(Rotation, "as_matrix"):
    Rotation.as_matrix = as_matrix
if not hasattr(Rotation, "as_rotvec"):
    Rotation.as_rotvec = as_rotvec
if not hasattr(Rotation, "as_mrp"):
    Rotation.as_mrp = as_mrp
if not hasattr(Rotation, "as_euler"):
    Rotation.as_euler = as_euler
if not hasattr(Rotation, "as_davenport"):
    Rotation.as_davenport = as_davenport

if not hasattr(Rotation, "inv"):
    Rotation.inv = inv
if not hasattr(Rotation, "magnitude"):
    Rotation.magnitude = magnitude

if not hasattr(Rotation, "identity"):
    Rotation.identity = identity
if not hasattr(Rotation, "random"):
    Rotation.random = random

if not hasattr(Rotation, "__mul__"):
    Rotation.__mul__ = __mul__
if not hasattr(Rotation, "__rmul__"):
    Rotation.__rmul__ = __rmul__

msgs.register_item(Rotation)

__all__ = ["Rotation"]
