from products.models import Variant
from products import pricing
from satchless.cart.models import Cart, CartItem
from satchless.pricing import Price
from satchless.util.models import construct


class Cart(Cart):
    def total(self, handler=pricing.pricing_handler):
        print 'aaaaaaaaaaaaaaaaaa'
        print ([item.price(handler) for item in self.get_all_items()])
        return sum(
            [item.price(handler) for item in self.get_all_items()],
            Price(0)
        )


class CartItem(construct(CartItem, cart=Cart, variant=Variant)):
    def price(self, handler=pricing.pricing_handler):
        return handler.get_variant_price(self.variant, quantity=self.quantity)
