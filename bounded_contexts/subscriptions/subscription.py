import attr
import arrow
import uuid

from .billing_period import (
    BillingPeriod,
)
from .customer_id import CustomerID
from .exceptions import (
    BillingPeriodAlreadyExists,
)
from .money import (
    Money,
)
from .plan import (
    Plan,
)

from events.event_stream import EventStream
from events.event import Event
from aggregate import Aggregate
from method_dispatch import method_dispatch


@attr.s(frozen=True)
class SubscriptionID:
    id: uuid.UUID = attr.ib()


@attr.s(frozen=True)
class SubscriptionEvent(Event):
    pass

@attr.s(frozen=True)
class SubscriptionCreated(SubscriptionEvent):
    customer_id: str = attr.ib()
    plan_interval: str = attr.ib()
    plan_amount: int = attr.ib()
    plan_currency: str = attr.ib()


@attr.s(frozen=False)
class Subscription(Aggregate):
    event_stream: EventStream = attr.ib()
    id: SubscriptionID = attr.ib(default=False)
    current_billing_period: BillingPeriod = attr.ib(default=False)
    customer_id: CustomerID = attr.ib(default=False)
    plan: Plan = attr.ib(default=False)
    expires_on: arrow.Arrow = attr.ib(default=False)

    @classmethod
    def create(
            cls,
            customer_id: CustomerID,
            plan: Plan,
    ):
        initial_event = SubscriptionCreated(
            customer_id=str(customer_id),
            plan_interval=str(plan.interval),
            plan_amount=int(plan.cents),
            plan_currency=str(plan.currency),
        )
        instance = cls(
            EventStream(
                events=[initial_event],
                version=0,
            )
        )
        instance._changes = [initial_event]
        return instance

    @method_dispatch
    def apply(self, event):
        raise ValueError('Unknown event!')

    @apply.register(SubscriptionCreated)
    def _(self, event: SubscriptionCreated):
        self.plan = Plan(
            amount=Money(
                cents=Cents(event.plan_amount),
                currency=USD(),
            ),
            interval=Monthly()
        )
        self.customer_id = CustomerID(event.customer_id)
