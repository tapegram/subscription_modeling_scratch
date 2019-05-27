import attr
import arrow


@attr.s(frozen=True)
class Event(object):
    occurred_on: arrow.Arrow = attr.ib()
