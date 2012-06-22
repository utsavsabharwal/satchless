from decimal import Decimal
from . import VariantFieldGetter, ProductFieldGetter
from satchless.pricing.handler import PricingQueue
from django.test import TestCase
from ....pricing import Price, PriceRange
from django.db import models
from satchless.product.models import Variant, Product


class PriceMixin(models.Model):
    price = models.DecimalField(max_digits=12, decimal_places=4)


class ValueMixin(models.Model):
    value = models.DecimalField(max_digits=12, decimal_places=4)


class DeadParrot(Product, PriceMixin):
    pass


class DeadParrotVariant(Variant, PriceMixin):
    looks_alive = models.BooleanField()
    product = models.ForeignKey(DeadParrot, related_name='variants')


class ValuableDeadParrot(Product, ValueMixin):
    pass


class ValuableDeadParrotVariant(Variant, ValueMixin):
    looks_alive = models.BooleanField()
    product = models.ForeignKey(ValuableDeadParrot, related_name='variants')


class FieldGetterTestBase(TestCase):
    def setUp(self):
        self.dead_parrot = DeadParrot.objects.create(price=Decimal(5))
        self.almost_alive_parrot = self.dead_parrot.variants.create(
            looks_alive=True, price=Decimal(11))
        self.dead_but_pretty_parrot = self.dead_parrot.variants.create(
            looks_alive=True, price=Decimal(7))


class VariantFieldGetterTest(FieldGetterTestBase):
    def setUp(self):
        super(VariantFieldGetterTest, self).setUp()
        self.pricing_queue = PricingQueue(VariantFieldGetter)

    def test_variant_price(self):
        price = self.pricing_queue.get_variant_price(
            self.almost_alive_parrot)
        self.assertEqual(price, Price(11))

    def test_variant_price_with_previous_price(self):
        price = self.pricing_queue.get_variant_price(
            self.dead_but_pretty_parrot, price=Price(8))
        self.assertEqual(price, Price(7))

    def test_variant_price_with_curency_given(self):
        price = self.pricing_queue.get_variant_price(
            self.dead_but_pretty_parrot, currency='pln')
        self.assertEqual(price, Price(7, currency='pln'))

    def test_variant_price_with_curency_given_and_previous_price(self):
        price = self.pricing_queue.get_variant_price(
            self.dead_but_pretty_parrot, currency='pln', price=Price(8))
        self.assertEqual(price, Price(7, currency='pln'))

    def test_variant_price_from_args(self):
        self.pricing_queue = PricingQueue(VariantFieldGetter(currency='pln'))
        price = self.pricing_queue.get_variant_price(
            self.dead_but_pretty_parrot, price=Price(8))
        self.assertEqual(price, Price(8))

    def test_variant_usd_price_from_args(self):
        self.pricing_queue = PricingQueue(VariantFieldGetter(currency='pln'))
        price = self.pricing_queue.get_variant_price(
            self.dead_but_pretty_parrot, price=Price(8, currency='usd'))
        self.assertEqual(price, Price(8, currency='usd'))

    def test_variant_price_range(self):
        range = self.pricing_queue.get_product_price_range(self.dead_parrot)
        self.assertEqual(range, PriceRange(Price(7), Price(11)))


class VariantFieldGetterOtherFieldNameTest(VariantFieldGetterTest):
    def setUp(self):
        self.dead_parrot = ValuableDeadParrot.objects.create(value=Decimal(5))
        self.almost_alive_parrot = self.dead_parrot.variants.create(
            looks_alive=True, value=Decimal(11))
        self.dead_but_pretty_parrot = self.dead_parrot.variants.create(
            looks_alive=True, value=Decimal(7))
        self.pricing_queue = PricingQueue(
            VariantFieldGetter(field_name='value'))


class ProductFieldGetterTest(FieldGetterTestBase):
    def setUp(self):
        super(ProductFieldGetterTest, self).setUp()
        self.pricing_queue = PricingQueue(ProductFieldGetter)

    def test_product_price(self):
        price = self.pricing_queue.get_variant_price(
            self.almost_alive_parrot)
        self.assertEqual(price, Price(5))

    def test_product_price_with_previous_price(self):
        price = self.pricing_queue.get_variant_price(
            self.dead_but_pretty_parrot, price=Price(8))
        self.assertEqual(price, Price(5))

    def test_product_price_range(self):
        range = self.pricing_queue.get_product_price_range(self.dead_parrot)
        self.assertEqual(range, PriceRange(Price(5), Price(5)))

    def test_product_price_range_with_previous_range(self):
        range = self.pricing_queue.get_product_price_range(
            self.dead_parrot, price_range=PriceRange(Price(4), Price(6)))
        self.assertEqual(range, PriceRange(Price(5), Price(5)))

    def test_product_price_range_with_previous_range_and_currency(self):
        self.pricing_queue = PricingQueue(ProductFieldGetter(currency='pln'))
        range = self.pricing_queue.get_product_price_range(
            self.dead_parrot,
            price_range=PriceRange(Price(4), Price(6)), currency='usd')
        self.assertEqual(range, PriceRange(Price(4), Price(6)))
