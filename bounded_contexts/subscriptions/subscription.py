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


@attr.s(frozen=True)
class SubscriptionID:
    id: uuid.UUID = attr.ib()


@attr.s(frozen=True)
class Subscription:
    id: SubscriptionID = attr.ib()
    current_billing_period: BillingPeriod = attr.ib()
    customer_id: CustomerID = attr.ib()
    plan: Plan = attr.ib()
    expires_on: arrow.Arrow = attr.ib()
