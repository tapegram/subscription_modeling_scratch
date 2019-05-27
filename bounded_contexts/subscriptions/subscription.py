import attr
import arrow

from .billing_period import (
    BillingPeriod,
)
from .customer import Customer
from .exceptions import (
    BillingPeriodAlreadyExists,
)
from .money import (
    Money,
)
from .plan import (
    Plan,
)



@attr.s(frozen=True)
class Subscription:
    current_billing_period: BillingPeriod = attr.ib()
    customer: Customer = attr.ib()
    plan: Plan = attr.ib()

    def bill(self):
        now = arrow.utcnow()

        if (
                self.current_billing_period
                and self.current_billing_period.includes(
                    now,
                )
        ):
            raise BillingPeriodAlreadyExists

        payment = self.plan.create_payment(
            self.customer,
        )

        payment.capture()

        return attr.evolve(
            self,
            current_billing_period=BillingPeriod(
                start=now,
                end=now.shift(months=+1),
                payment=payment,
            )
        )
