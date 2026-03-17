import numpy as np
from typing import Iterable
from ark_msgs.translation import Translation
from ark_msgs.registry import msgs

# wrench_pb2.py is generated from wrench.proto
from .wrench_pb2 import Wrench

ProtoOrIterableWrench = Wrench | Iterable[float]

def _as_array(w: ProtoOrIterableWrench) -> np.ndarray:
    """Convert to numpy array of shape (6,)."""
    if isinstance(w, Wrench):
        return np.concatenate((w.force.as_array(), w.torque.as_array()))
    return np.asarray(w, dtype=np.float32).reshape(6)

def _as_proto(w: ProtoOrIterableWrench) -> Wrench:
    """Convert to ark_msgs.wrench.Wrench."""
    if isinstance(w, Wrench):
        return w
    arr = np.asarray(w, dtype=np.float32).reshape(6)
    return Wrench(
        force=Translation.from_array(arr[:3]),
        torque=Translation.from_array(arr[3:])
    )

@classmethod
def from_array(cls, array: Iterable[float]) -> Wrench:
    """
    Initialize from an array-like of 6 floats.
    [fx, fy, fz, tx, ty, tz]
    """
    return _as_proto(array)

def as_array(self: Wrench) -> np.ndarray:
    """
    Convert to a numpy array of shape (6,).
    Returns [fx, fy, fz, tx, ty, tz]
    """
    return _as_array(self)

if not hasattr(Wrench, "from_array"):
    Wrench.from_array = from_array
if not hasattr(Wrench, "as_array"):
    Wrench.as_array = as_array

msgs.register_item(Wrench)

__all__ = ["Wrench"]
