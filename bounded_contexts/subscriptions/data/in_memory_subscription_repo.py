import attr
import arrow

from ..billing_period import (
    BillingPeriod,
)
from ..customer_id import (
    CustomerID,
)
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
)


@attr.s(frozen=True)
class InMemorySubscriptionRepo:

    _subscriptions = {}

    @classmethod
    def add(cls, subscription: Subscription):
        cls._subscriptions[subscription.id] = subscription

    @classmethod
    def get(cls, id: SubscriptionID):
        return cls._subscriptions.get(id)
