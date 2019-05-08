import attr
import arrow
import uuid


@attr.s(frozen=True)
class Cents:
    value: int = attr.ib()


@attr.s(frozen=True)
class Currency:
    value: str = attr.ib()


@attr.s(frozen=True)
class BillingPeriod:
    start: arrow.Arrow = attr.ib()
    end: arrow.Arrow = attr.ib()


@attr.s(frozen=True)
class Money:
    cents: Cents = attr.ib()
    currency: Currency = attr.ib()


@attr.s(frozen=True)
class Payment:
    amount: Money = attr.ib()

    def capture(self):
        pass


@attr.s(frozen=True)
class Interval:
    pass


@attr.s(frozen=True)
class Monthly(Interval):
    pass


@attr.s(frozen=True)
class DefaultPaymentMethod:
    """
    Would need to be able to generate new stripe/adyen payments
    """
    def create(self, amount: Money):
        return Payment(
            amount=amount,
        )


@attr.s(frozen=True)
class Customer:
    id: uuid.UUID = attr.ib()
    default_payment_method: DefaultPaymentMethod = attr.ib()


@attr.s(frozen=True)
class Plan:
    amount: Money = attr.ib()
    interval: Interval = attr.ib()

    def create_payment(self, customer: Customer):
        return customer.default_payment_method.create(
            amount=self.amount,
        )


@attr.s(frozen=True)
class Subscription:
    current_billing_period: BillingPeriod = attr.ib()
    customer: Customer = attr.ib()
    plan: Plan = attr.ib()


    def bill(self):
        now = arrow.utcnow()

        payment = self.plan.create_payment(
            self.customer,
        )

        payment.capture()

        return attr.evolve(
            self,
            current_billing_period=BillingPeriod(
                start=now,
                end=now.shift(months=+1),
            )
        )
