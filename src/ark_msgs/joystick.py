from ark_msgs.registry import msgs

# joystick_pb2.py is generated from joystick.proto
from .joystick_pb2 import Joystick

def get_axis(self: Joystick, name: str) -> float:
    """
    Get axis value by name.
    Raises ValueError if name is not found, or IndexError if axis array is shorter than names.
    """
    try:
        idx = self.axis_name.index(name)
        return self.axis[idx]
    except (ValueError, IndexError) as e:
        raise KeyError(f"Axis '{name}' not available: {e}")

def get_button(self: Joystick, name: str) -> int:
    """
    Get button value by name.
    Raises ValueError if name is not found, or IndexError if button array is shorter than names.
    """
    try:
        idx = self.button_name.index(name)
        return self.button[idx]
    except (ValueError, IndexError) as e:
        raise KeyError(f"Button '{name}' not available: {e}")

if not hasattr(Joystick, "get_axis"):
    Joystick.get_axis = get_axis
if not hasattr(Joystick, "get_button"):
    Joystick.get_button = get_button

msgs.register_item(Joystick)

__all__ = ["Joystick"]
