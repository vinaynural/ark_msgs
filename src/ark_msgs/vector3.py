import numpy as np
from ark_msgs.registry import msgs

# vector3_pb2.py is generated from vector3.proto
from .vector3_pb2 import Vector3

@classmethod
def from_array(cls, array) -> Vector3:
    """
    Create a Vector3 from an array-like of shape (3,).
    """
    array = np.asarray(array, dtype=np.float32)
    if array.shape != (3,):
        raise ValueError(f"Expected shape (3,), got {array.shape}")
    return cls(x=float(array[0]), y=float(array[1]), z=float(array[2]))

def as_array(self: Vector3) -> np.ndarray:
    """
    Convert to a numpy.ndarray of shape (3,) with dtype float32.
    """
    return np.array([self.x, self.y, self.z], dtype=np.float32)

if not hasattr(Vector3, "from_array"):
    Vector3.from_array = from_array
if not hasattr(Vector3, "as_array"):
    Vector3.as_array = as_array

msgs.register_item(Vector3)

__all__ = ["Vector3"]
