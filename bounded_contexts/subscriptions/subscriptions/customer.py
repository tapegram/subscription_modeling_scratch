import attr
import uuid

from .default_payment_method import DefaultPaymentMethod


@attr.s(frozen=True)
class Customer:
    id: uuid.UUID = attr.ib()
    default_payment_method: DefaultPaymentMethod = attr.ib()
