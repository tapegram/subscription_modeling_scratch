import attr
from .event import Event


@attr.s(frozen=True)
class EventStream(object):
    events: [Event] = attr.ib()
    version: int = attr.ib()
