import abc
from uuid import uuid4


class Aggregate(metaclass=abc.ABCMeta):

    def __init__(
            self,
            event_stream,
            uuid=None,
    ):
        self._uuid = uuid or uuid4()
        self._version = event_stream.version

        for event in event_stream.events:
            self.apply(event)

        self._changes = []

    @abc.abstractmethod
    def apply(self, event):
        pass

    @property
    def uuid(self):
        return self._uuid

    @property
    def version(self):
        return self._version

    @property
    def changes(self):
        return self._changes
