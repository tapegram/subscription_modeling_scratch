import attr


@attr.s(frozen=True)
class Cents:
    value: int = attr.ib()


@attr.s(frozen=True)
class Currency:
    pass

@attr.s(frozen=True)
class USD(Currency):

    def __str__(self):
        return "USD"

@attr.s(frozen=True)
class Money:
    cents: Cents = attr.ib()
    currency: Currency = attr.ib()

