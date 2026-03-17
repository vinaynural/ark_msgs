import numpy as np
from ark_msgs.registry import msgs

# image_pb2.py is generated from image.proto
from .image_pb2 import Image

# PixelFormat to PIL mode mapping
_PIXEL_FORMAT_TO_PIL_MODE = {
    Image.GRAY: "L",
    Image.RGB: "RGB",
    Image.RGBA: "RGBA",
    Image.BGR: "BGR",
    Image.BGRA: "BGRA",
}

# Optional PIL support
try:
    from PIL import Image as PILImage
    _HAS_PIL = True
except ImportError:
    _HAS_PIL = False

@classmethod
def from_array(cls, array: np.ndarray, pixel_format: Image.PixelFormat | None = None) -> Image:
    """
    Initialize from a numpy array (e.g. from OpenCV).
    Assumes pixel_format matches array shape/type.
    """
    array = np.asarray(array)
    height, width = array.shape[:2]
    row_stride = array.strides[0]
    data = array.tobytes()

    obj = cls(
        height=height,
        width=width,
        row_stride=row_stride,
        size=len(data),
        data=data
    )
    if pixel_format is not None:
        obj.pixel_format = pixel_format
    
    return obj

def as_array(self: Image) -> np.ndarray:
    """
    Convert to a numpy array.
    """
    shape = (self.height, self.width, -1)
    
    # Handle Mono/Gray special case for shape
    if (self.pixel_format == Image.GRAY or 
        self.pixel_format == Image.BE_GRAY16 or
        self.pixel_format == Image.LE_GRAY16):
         shape = (self.height, self.width)
    
    return np.frombuffer(self.data, dtype=np.uint8).reshape(shape)



def no_pil(*args, **kwargs):
    raise RuntimeError("pillow is not installed. Install with: pip install -e .[pil] from the top level of ark_msgs.")

@classmethod
def from_pil(cls, pil_image: "PIL.Image.Image", pixel_format: Image.PixelFormat | None = None) -> Image:
    """
    Initialize from a PIL Image.
    Converts PIL Image to numpy array and uses from_array.
    Requires pillow to be installed.
    """
    if not _HAS_PIL:
        no_pil()
    
    # Convert PIL image to numpy array
    array = np.array(pil_image)
    
    # Determine encoding from PIL mode if not provided
    if pixel_format is None:
        mode_to_format = {
            "RGB": Image.RGB,
            "RGBA": Image.RGBA,
            "L": Image.GRAY,
            "BGR": Image.BGR,
        }
        pixel_format = mode_to_format.get(pil_image.mode, Image.RGB)
    
    return cls.from_array(array, pixel_format=pixel_format)

def as_pil(self: Image):
    """
    Convert to a PIL Image.
    Converts to numpy array first, then to PIL Image.
    Requires pillow to be installed.
    """
    if not _HAS_PIL:
        no_pil()
    
    # Convert to numpy array
    array = self.as_array()
    
    # Determine PIL mode from pixel format
    mode = _PIXEL_FORMAT_TO_PIL_MODE.get(self.pixel_format, "RGB")
    
    if mode == "BGR":
        # PIL doesn't have BGR mode, convert to RGB
        array = array[:, :, ::-1]
        mode = "RGB"
    elif mode == "BGRA":
        # Convert BGRA to RGBA
        array = array[:, :, [2, 1, 0, 3]]
        mode = "RGBA"
        
    return PILImage.fromarray(array, mode=mode)



if not hasattr(Image, "from_array"):
    Image.from_array = from_array
if not hasattr(Image, "as_array"):
    Image.as_array = as_array

if _HAS_PIL:
    Image.from_pil = from_pil
    Image.as_pil = as_pil
else:
    Image.from_pil = no_pil
    Image.as_pil = no_pil


# Constants are now automatically available via the generated protobuf code
# e.g. Image.RGB, Image.GRAY, etc.

msgs.register_item(Image)

__all__ = ["Image"]
