from products.models import Variant
from products import pricing
from satchless.cart.models import Cart, CartItem
from satchless.util.models import construct


class Cart(Cart):
    pass


class CartItem(construct(CartItem, cart=Cart, variant=Variant)):
    @property
    def price(self, handler=pricing.pricing_handler):
        return handler.get_variant_price(self.variant, quantity=self.quantity)

