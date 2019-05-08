import attr
import arrow


@attr.s(frozen=True)
class Subscription:
    current_billing_period = attr.ib()


    def bill(self):
        now = arrow.utcnow()
        return attr.evolve(
            self,
            current_billing_period=BillingPeriod(
                start=now,
                end=now.shift(months=+1),
            )
        )


@attr.s(frozen=True)
class BillingPeriod:
    start = attr.ib()
    end = attr.ib()

@attr.s(frozen=True)
class Payment:
    pass

@attr.s(frozen=True)
class Money:
    pass

@attr.s(frozen=True)
class Cents:
    pass

@attr.s(frozen=True)
class Currency:
    pass
