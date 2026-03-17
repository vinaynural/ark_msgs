from ark_msgs.registry import msgs

# image_metadata_pb2.py is generated from image_metadata.proto
from .image_metadata_pb2 import ImageMetadata

msgs.register_item(ImageMetadata)

__all__ = ["ImageMetadata"]
