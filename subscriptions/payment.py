import attr

from .money import Money


@attr.s(frozen=True)
class Payment:
    """
    This would be a payment object from the existing Payments package
    """
    amount: Money = attr.ib()

    def capture(self):
        pass

