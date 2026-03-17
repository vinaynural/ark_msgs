from ark_msgs.registry import msgs

# imu_pb2.py is generated from imu.proto
from .imu_pb2 import Imu

msgs.register_item(Imu)

__all__ = ["Imu"]
