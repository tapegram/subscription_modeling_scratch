import arrow

from unittest import (
    mock,
    TestCase,
)
from .subscription import (
    BillingPeriod,
    DefaultPaymentMethod,
    Subscription,
    Money,
    Cents,
    Currency,
    Plan,
    Monthly,
    Customer,
)


class TestBillSubscription(TestCase):

    @mock.patch("subscriptions.subscription.Payment")
    def test_bill_a_new_sub_charges_payment_for_plan_amount(
            self,
            m_payment,
    ):
        m_payment = mock.MagicMock()

        subscription = Subscription(
            current_billing_period=None,
            customer=Customer(
                id="123",
                default_payment_method=DefaultPaymentMethod()
            ),
            plan=Plan(
                amount=Money(
                    cents=Cents(1945),
                    currency=Currency("USD")
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

        m_payment.capture.assert_called_once()

    def test_bill_a_new_sub_updates_billing_period(self):
        subscription = Subscription(
            current_billing_period=None,
            customer=Customer(
                id="123",
                default_payment_method=DefaultPaymentMethod()
            ),
            plan=Plan(
                amount=Money(
                    cents=Cents(1945),
                    currency=Currency("USD")
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
                ),
                customer=Customer(
                    id="123",
                    default_payment_method=DefaultPaymentMethod()
                ),
                plan=Plan(
                    amount=Money(
                        cents=Cents(1945),
                        currency=Currency("USD")
                    ),
                    interval=Monthly()
                ),
            )
        )
