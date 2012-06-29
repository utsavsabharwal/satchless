from satchless.contrib.pricing.field import ProductFieldGetter
from satchless.contrib.tax.flatgroups import FlatGroupPricingHandler
from satchless.pricing import PricingHandler, Price
from satchless.pricing.handler import PricingQueue


class SimpleQtyPricingHandler(PricingHandler):
    def get_variant_price(self, variant, currency, quantity=1, price=None,
                          **kwargs):
        try:
            return price * quantity
        except TypeError:
            return price

    def get_product_price_range(self, product, currency,
                                price_range=None,
                                **kwargs):
        return price_range


class VariantOffsetHandler(PricingHandler):
    def get_variant_price(self, variant, currency, quantity=1, price=Price(0),
                          **kwargs):
        try:
            return price + Price(variant.price_offset)
        except TypeError, e:
            return price

    def get_product_price_range(self, product, currency,
                                price_range=None,
                                **kwargs):
        return price_range

pricing_handler = PricingQueue(ProductFieldGetter, VariantOffsetHandler,
    SimpleQtyPricingHandler, FlatGroupPricingHandler)
def get_price(variant, quantity=1):
    return pricing_handler.get_variant_price(variant, quantity=quantity)
