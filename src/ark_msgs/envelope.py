from .envelope_pb2 import Envelope
from ark_msgs.registry import msgs
from google.protobuf.message import Message


def _extract_message(msg: Envelope) -> Message | bytes:
    msg_cls = msgs.get(msg.msg_type)
    if msg_cls is bytes:
        return msg.payload
    inner_msg = msg_cls()
    inner_msg.ParseFromString(msg.payload)
    return inner_msg


def extract_message(self: Envelope) -> Message | bytes:
    return _extract_message(self)


def extract_request_message(self: Envelope) -> Message | bytes:
    return _extract_message(self.req_env)


def _one_way_latency(self: Envelope) -> int:
    if not self.sent_timestamp:
        raise ValueError("sent_timestamp is not set")
    if not self.recv_timestamp:
        raise ValueError("recv_timestamp is not set")
    return self.recv_timestamp - self.sent_timestamp


if not hasattr(Envelope, "extract_message"):
    Envelope.extract_message = extract_message
if not hasattr(Envelope, "extract_request_message"):
    Envelope.extract_request_message = extract_request_message
if not hasattr(Envelope, "one_way_latency"):
    Envelope.one_way_latency = property(_one_way_latency)

msgs.register_item(Envelope)

__all__ = ["Envelope"]
