import numpy as np
from typing import Iterable
from ark_msgs.translation import Translation
from ark_msgs.registry import msgs

# twist_pb2.py is generated from twist.proto
from .twist_pb2 import Twist

ProtoOrIterableTwist = Twist | Iterable[float]

def _as_array(t: ProtoOrIterableTwist) -> np.ndarray:
    """Convert to numpy array of shape (6,)."""
    if isinstance(t, Twist):
        return np.concatenate((t.linear.as_array(), t.angular.as_array()))
    return np.asarray(t, dtype=np.float32).reshape(6)

def _as_proto(t: ProtoOrIterableTwist) -> Twist:
    """Convert to ark_msgs.twist.Twist."""
    if isinstance(t, Twist):
        return t
    arr = np.asarray(t, dtype=np.float32).reshape(6)
    return Twist(
        linear=Translation.from_array(arr[:3]),
        angular=Translation.from_array(arr[3:])
    )

@classmethod
def from_array(cls, array: Iterable[float]) -> Twist:
    """
    Initialize from an array-like of 6 floats.
    [vx, vy, vz, wx, wy, wz]
    """
    return _as_proto(array)

def as_array(self: Twist) -> np.ndarray:
    """
    Convert to a numpy array of shape (6,).
    Returns [vx, vy, vz, wx, wy, wz]
    """
    return _as_array(self)

if not hasattr(Twist, "from_array"):
    Twist.from_array = from_array
if not hasattr(Twist, "as_array"):
    Twist.as_array = as_array

msgs.register_item(Twist)

__all__ = ["Twist"]
