import arrow

from unittest import TestCase

from .billing_period import (
    BillingPeriod,
)
from .customer_id import (
    CustomerID,
)
from .data.in_memory_subscription_repo import InMemorySubscriptionRepo
from .money import (
    Cents,
    Money,
    USD,
)
from .plan import (
    Monthly,
    Plan,
)
from .subscription import (
    SubscriptionID,
    Subscription,
)


class TestSubscription(TestCase):

    def test_add_and_get_subscription_from_repo(self):
        now = arrow.utcnow()
        expires_on = now.shift(weeks=+2)
        start_billing_period = expires_on.shift(months=-1)

        InMemorySubscriptionRepo.add(
            Subscription(
                id=SubscriptionID("123"),
                current_billing_period=BillingPeriod(
                    start=start_billing_period,
                    end=expires_on,
                ),
                customer_id=CustomerID("abc"),
                plan=Plan(
                    amount=Money(
                        Cents(3900),
                        USD()
                    ),
                    interval=Monthly()
                ),
                expires_on=expires_on,
            )
        )

        subscription = InMemorySubscriptionRepo.get(
            SubscriptionID("123")
        )

        self.assertEqual(
            subscription,
            Subscription(
                id=SubscriptionID("123"),
                current_billing_period=BillingPeriod(
                    start=start_billing_period,
                    end=expires_on,
                ),
                customer_id=CustomerID("abc"),
                plan=Plan(
                    amount=Money(
                        Cents(3900),
                        USD()
                    ),
                    interval=Monthly()
                ),
                expires_on=expires_on,
            )
        )
