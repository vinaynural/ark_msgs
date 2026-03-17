from ark.registry import Registry
from google.protobuf.message import Message


class ArkMsgsRegistry(Registry):

    def __init__(self):
        super().__init__()

        # enable user to pass bytes directly
        super().register_item("__bytes__", bytes)

    def register_item(self, item: type[Message]):
        name = item.DESCRIPTOR.full_name
        return super().register_item(name, item)


msgs = ArkMsgsRegistry()
