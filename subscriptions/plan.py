import attr

from .money import Money
from .customer import Customer


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

    def create_payment(self, customer: Customer):
        return customer.default_payment_method.create(
            amount=self.amount,
        )



