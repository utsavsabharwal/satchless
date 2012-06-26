from django.test import TestCase
from ....pricing.handler import PricingQueue
from ....product.tests import DeadParrot
from ....contrib.pricing.field import ProductFieldGetter
from ....contrib.pricing.cache import PricingCacheHandler

from decimal import Decimal

class CacheTestHandler(ProductFieldGetter):
    def get_variant_price(self, variant, currency, quantity=1, **kwargs):
        price = super(CacheTestHandler, self).get_variant_price(variant,
                                                currency, quantity, **kwargs)        
        if not hasattr(price, '_cache'):
            price._cache = 0
        else:
            price._cache += 1
            
        return price

    def get_product_price_range(self, product, currency, **kwargs):
        price = super(CacheTestHandler, self).get_product_price_range(product,
                                                            currency, **kwargs)        
        if not hasattr(price, '_cache'):
            price._cache = 0
        else:
            price._cache += 1
        
        return price

class Cache(TestCase):
    def setUp(self):
        self.parrot = DeadParrot.objects.create(slug='parrot', species='Parrot')
        self.parrot_a = self.parrot.variants.create(color='white',
                                                    looks_alive=True)
        self.parrot.price = Decimal(10)
        self.parrot_a.price = Decimal(11)
        self.cockatoo = DeadParrot.objects.create(slug='cockatoo',
                                                  species='Cockatoo')
        self.cockatoo_a = self.cockatoo.variants.create(color='white',
                                                        looks_alive=True)
        self.cockatoo.price = Decimal(20)
        self.cockatoo_a.price = Decimal(21)
        self.pricing_cache_handler = PricingCacheHandler(CacheTestHandler)
        self.cached_queue = PricingQueue(self.pricing_cache_handler)
        self.non_cached_queue = PricingQueue(ProductFieldGetter)

    def test_variant_price_add_to_cache(self):
        p0 = self.non_cached_queue.get_variant_price(self.parrot_a, None)
        p1 = self.cached_queue.get_variant_price(self.parrot_a, None)
        self.assertEqual(p0, p1)

        p0 = self.non_cached_queue.get_variant_price(self.cockatoo_a, None)
        p1 = self.cached_queue.get_variant_price(self.cockatoo_a, None)
        self.assertEqual(p0, p1)

    def test_product_price_range_add_to_cache(self):
        p0 = self.non_cached_queue.get_product_price_range(self.parrot)
        p1 = self.cached_queue.get_product_price_range(self.parrot)
        self.assertEqual(p0, p1)
        
        p0 = self.non_cached_queue.get_product_price_range(self.cockatoo)         
        p1 = self.cached_queue.get_product_price_range(self.cockatoo)
        self.assertEqual(p0, p1)
        
    def test_variant_price_get_from_cache(self):
        p0 = self.non_cached_queue.get_variant_price(self.parrot_a, None)
        p1 = self.cached_queue.get_variant_price(self.parrot_a, None)
        
        self.assertEqual(p0, p1)
        self.assertEqual(p1._cache, 0)
        
        p0 = self.non_cached_queue.get_variant_price(self.cockatoo_a, None)
        p1 = self.cached_queue.get_variant_price(self.cockatoo_a, None)
        
        self.assertEqual(p0, p1)
        self.assertEqual(p1._cache, 0)

    def test_product_price_range_get_from_cache(self):
        p0 = self.non_cached_queue.get_product_price_range(self.parrot)
        p1 = self.cached_queue.get_product_price_range(self.parrot)
        
        self.assertEqual(p0, p1)
        self.assertEqual(p1._cache, 0)
        
        p0 = self.non_cached_queue.get_product_price_range(self.cockatoo)
        p1 = self.cached_queue.get_product_price_range(self.cockatoo)
        
        self.assertEqual(p0, p1)
        self.assertEqual(p1._cache, 0)
                
    def test_product_cache_key_generator(self):
        key = 'currency=None&product=%s'%self.parrot.id
        p = self.cached_queue.get_product_price_range(self.parrot)
        key_from_p = self.pricing_cache_handler._get_key(currency=None,
                                                         product=self.parrot)
        
        self.assertEqual(key, key_from_p)