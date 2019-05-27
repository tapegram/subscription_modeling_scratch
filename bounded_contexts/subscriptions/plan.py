import attr

from .money import Money


@attr.s(frozen=True)
class Interval:
    pass


@attr.s(frozen=True)
class Monthly(Interval):
    pass


@attr.s(frozen=True)
class Plan:
    amount: Money = attr.ib()
    interval: Interval = attr.ib()



