import attr
import arrow

from .payment import Payment


@attr.s(frozen=True)
class BillingPeriod:
    start: arrow.Arrow = attr.ib()
    end: arrow.Arrow = attr.ib()
    payment: Payment = attr.ib()

    def includes(self, time:arrow.Arrow):
        return self.start <= time <= self.end
