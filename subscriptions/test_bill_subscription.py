import arrow

from unittest import (
    mock,
    TestCase,
)

from .billing_period import (
    BillingPeriod,
)
from .customer import Customer
from .default_payment_method import (
    DefaultPaymentMethod,
)
from .exceptions import (
    BillingPeriodAlreadyExists,
)
from .money import (
    Cents,
    Money,
    USD,
)
from .payment import Payment
from .plan import (
    Plan,
    Monthly,
)
from .subscription import (
    Subscription,
)


class TestBillSubscription(TestCase):

    @mock.patch("subscriptions.payment.Payment.capture")
    def test_bill_a_new_sub_charges_payment_for_plan_amount(
            self,
            m_payment_capture,
    ):
        subscription = Subscription(
            current_billing_period=None,
            customer=Customer(
                id="123",
                default_payment_method=DefaultPaymentMethod()
            ),
            plan=Plan(
                amount=Money(
                    cents=Cents(1945),
                    currency=USD
                ),
                interval=Monthly()
            )
        )

        now = arrow.utcnow()
        with mock.patch(
                "subscriptions.subscription.arrow.utcnow",
                return_value=now
        ):
            subscription = subscription.bill()

        m_payment_capture.assert_called_once_with()

    def test_bill_a_new_sub_updates_billing_period_with_payment(self):
        subscription = Subscription(
            current_billing_period=None,
            customer=Customer(
                id="123",
                default_payment_method=DefaultPaymentMethod()
            ),
            plan=Plan(
                amount=Money(
                    cents=Cents(1945),
                    currency=USD
                ),
                interval=Monthly()
            )
        )

        now = arrow.utcnow()
        with mock.patch(
                "subscriptions.subscription.arrow.utcnow",
                return_value=now
        ):
            subscription = subscription.bill()

        self.assertEqual(
            subscription,
            Subscription(
                current_billing_period=BillingPeriod(
                    start=now,
                    end=now.shift(months=+1),
                    payment=Payment(
                        amount=Money(
                            cents=Cents(1945),
                            currency=USD
                        ),
                    )
                ),
                customer=Customer(
                    id="123",
                    default_payment_method=DefaultPaymentMethod()
                ),
                plan=Plan(
                    amount=Money(
                        cents=Cents(1945),
                        currency=USD
                    ),
                    interval=Monthly()
                ),
            )
        )

    def test_dont_bill_if_we_are_within_existing_billing_period(self):
        now = arrow.utcnow()
        a_week_ago = now.shift(weeks=-1)

        subscription = Subscription(
            current_billing_period=BillingPeriod(
                start=a_week_ago,
                end=a_week_ago.shift(months=+1),
                payment=Payment(
                    amount=Money(
                        cents=Cents(1945),
                        currency=USD
                    ),
                )
            ),
            customer=Customer(
                id="123",
                default_payment_method=DefaultPaymentMethod()
            ),
            plan=Plan(
                amount=Money(
                    cents=Cents(1945),
                    currency=USD
                ),
                interval=Monthly()
            ),
        )

        with self.assertRaises(BillingPeriodAlreadyExists):
            subscription = subscription.bill()
