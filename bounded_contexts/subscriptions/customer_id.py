import attr
import uuid


@attr.s(frozen=True)
class CustomerID:
    id: uuid.UUID = attr.ib()
