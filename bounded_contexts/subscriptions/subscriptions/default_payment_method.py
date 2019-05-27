import attr

from .money import Money
from .payment import Payment

@attr.s(frozen=True)
class DefaultPaymentMethod:
    """
    Would need to be able to generate new stripe/adyen payments
    """
    def create(self, amount: Money):
        return Payment(
            amount=amount,
        )
