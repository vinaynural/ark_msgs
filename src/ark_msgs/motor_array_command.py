from ark_msgs.registry import msgs

# motor_array_command_pb2.py is generated from motor_array_command.proto
from .motor_array_command_pb2 import MotorArrayCommand

msgs.register_item(MotorArrayCommand)

__all__ = ["MotorArrayCommand"]
