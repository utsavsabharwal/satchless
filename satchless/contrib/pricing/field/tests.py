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


class VariantFieldGetterSimpleTest(FieldGetterTestBase):
    def setUp(self):
        super(VariantFieldGetterSimpleTest, self).setUp()
        self.pricing_queue = PricingQueue(VariantFieldGetter)

    def test_variant_price(self):
        price = self.pricing_queue.get_variant_price(
            self.almost_alive_parrot)
        self.assertEqual(price, Price(11))

        price = self.pricing_queue.get_variant_price(
            self.dead_but_pretty_parrot)
        self.assertEqual(price, Price(7))

    def test_variant_price_range(self):
        range = self.pricing_queue.get_product_price_range(self.dead_parrot)
        self.assertEqual(range, PriceRange(Price(7), Price(11)))


class VariantFieldGetterOtherFieldNameTest(VariantFieldGetterSimpleTest):
    def setUp(self):
        self.dead_parrot = ValuableDeadParrot.objects.create(value=Decimal(5))
        self.almost_alive_parrot = self.dead_parrot.variants.create(
            looks_alive=True, value=Decimal(11))
        self.dead_but_pretty_parrot = self.dead_parrot.variants.create(
            looks_alive=True, value=Decimal(7))
        self.pricing_queue = PricingQueue(
            VariantFieldGetter(field_name='value'))


class VariantFieldGetterManyHandlersTest(VariantFieldGetterSimpleTest):
    def setUp(self):
        super(VariantFieldGetterManyHandlersTest, self).setUp()
        self.pricing_queue = PricingQueue(
            VariantFieldGetter(field_name='value'), VariantFieldGetter)


class ProductFieldGetterSimpleTest(FieldGetterTestBase):
    def setUp(self):
        super(ProductFieldGetterSimpleTest, self).setUp()
        self.pricing_queue = PricingQueue(ProductFieldGetter)

    def test_product_price(self):
        price = self.pricing_queue.get_variant_price(
            self.almost_alive_parrot)
        self.assertEqual(price, Price(5))

        price = self.pricing_queue.get_variant_price(
            self.dead_but_pretty_parrot)
        self.assertEqual(price, Price(5))

    def test_product_price_range(self):
        range = self.pricing_queue.get_product_price_range(self.dead_parrot)
        self.assertEqual(range, PriceRange(Price(5), Price(5)))


class ProductThenVariantFieldGetterTest(FieldGetterTestBase):
    def setUp(self):
        super(ProductThenVariantFieldGetterTest, self).setUp()
        self.pricing_queue = PricingQueue(
            ProductFieldGetter, VariantFieldGetter)

    def test_price(self):
        price = self.pricing_queue.get_variant_price(
            self.almost_alive_parrot)
        self.assertEqual(price, Price(11))

        price = self.pricing_queue.get_variant_price(
            self.dead_but_pretty_parrot)
        self.assertEqual(price, Price(7))

    def test_price_range(self):
        range = self.pricing_queue.get_product_price_range(self.dead_parrot)
        self.assertEqual(range, PriceRange(Price(7), Price(11)))
