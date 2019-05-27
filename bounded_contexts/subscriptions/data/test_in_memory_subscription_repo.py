import arrow

from unittest import TestCase

from ..billing_period import (
    BillingPeriod,
)
from ..customer_id import (
    CustomerID,
)
from .in_memory_subscription_repo import InMemorySubscriptionRepo
from ..money import (
    Cents,
    Money,
    USD,
)
from ..plan import (
    Monthly,
    Plan,
)
from ..subscription import (
    SubscriptionID,
    Subscription,
    SubscriptionCreated,
)
from events.event_stream import EventStream


class TestAddAndGetSubscription(TestCase):

            # Subscription(
            #     id=SubscriptionID("123"),
            #     current_billing_period=BillingPeriod(
            #         start=start_billing_period,
            #         end=expires_on,
            #     ),
            #     customer_id=CustomerID("abc"),
            #     plan=Plan(
            #         amount=Money(
            #             Cents(3900),
            #             USD()
            #         ),
            #         interval=Monthly()
            #     ),
            #     expires_on=expires_on,
            #     event_stream=EventStream(
            #         [
            #             SubscriptionCreated(

            #             ),
            #         ]
            #     ),
            # )
    def test_add_and_get_subscription_from_repo(self):
        now = arrow.utcnow()
        expires_on = now.shift(weeks=+2)
        start_billing_period = expires_on.shift(months=-1)

        InMemorySubscriptionRepo.add(
            Subscription(
                event_stream=EventStream(
                    [
                        SubscriptionCreated(
                            id="123",
                            current_billing_period_start=start_billing_period.timestamp,
                            current_billing_period_end=expires_on.timestamp,
                            customer_id="456",
                            plan_id="789",
                            occurred_on=start_billing_period.timestamp,
                        ),
                    ],
                    version=1,
                ),
            )
        )

        subscription = InMemorySubscriptionRepo.get(
            SubscriptionID("123")
        )

        self.assertEqual(
            subscription,
            Subscription.create(
                event_stream=EventStream(
                    [
                        SubscriptionCreated(
                            id="123",
                            current_billing_period_start=start_billing_period.timestamp,
                            current_billing_period_end=expires_on.timestamp,
                            customer_id="456",
                            plan_id="789",
                            occurred_on=start_billing_period.timestamp,
                        ),
                    ],
                    version=1,
                ),
            )
        )


class TestUpdateSubscription(TestCase):

    def test_update(self):
        now = arrow.utcnow()
        expires_on = now.shift(weeks=+2)
        start_billing_period = expires_on.shift(months=-1)

        subscription = Subscription(
            event_stream=EventStream(
                [
                    SubscriptionCreated(
                        id="123",
                        current_billing_period_start=start_billing_period.timestamp,
                        current_billing_period_end=expires_on.timestamp,
                        customer_id="456",
                        plan_id="789",
                        occurred_on=start_billing_period.timestamp,
                    ),
                ],
                version=1,
            ),
        )

        InMemorySubscriptionRepo.add(
            subscription
        )
