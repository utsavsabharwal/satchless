# -*- coding:utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from satchless.category.models import CategorizedProductMixin
from satchless.contrib.pricing.simpleqty.models import (ProductPriceMixin,
    VariantPriceOffsetMixin)
from satchless.contrib.tax.flatgroups.models import TaxedProductMixin
from satchless.util.models import construct
import satchless.product.models

from categories.models import Category

from . import pricing

class Product(satchless.product.models.Product,
              ProductPriceMixin, TaxedProductMixin,
              construct(CategorizedProductMixin, category=Category)):

    name = models.CharField(_('name'), max_length=128)
    description = models.TextField(_('description'), blank=True)

class Variant(satchless.product.models.Variant, VariantPriceOffsetMixin):
    product = models.ForeignKey(Product)

    def __unicode__(self):
        return u'offset %s'%self.price_offset

    def get_price(self, quantity=1):
        return pricing.get_price(self, quantity)


class OnlineVariantMixin(models.Model):
    file = models.FileField(upload_to='tmp')
    file_format = models.CharField(max_length=4)

    class Meta:
        abstract = True

class OfflineVariantMixin(models.Model):
    stock = models.PositiveIntegerField()

    class Meta:
        abstract = True

class Book(Product):
    isbn = models.CharField(max_length=13)
    author = models.CharField(max_length=50)
    publication_date = models.DateField(blank=True, null=True)

class EBookVariant(Variant, OnlineVariantMixin):
    def __unicode__(self):
        return u"eBook (%s)" % self.file_format

class TraditionalBookVariant(Variant, OfflineVariantMixin):
    hard_cover = models.BooleanField(default=False)

    def __unicode__(self):
        return u"Book %(with)s hard cover" % {
            'with' : 'with' if self.hard_cover else 'without',
        }

class Movie(Product):
    director = models.CharField(max_length=50)
    premiere_date = models.DateField(blank=True, null=True)

class OnlineMovieVariant(Variant, OnlineVariantMixin):
    with_adverts = models.BooleanField(default=False)

class TraditionalMovieVariant(Variant, OfflineVariantMixin):
    CARRIERS = (
        ('vhs', 'VHS'),
        ('dvd', 'DVD'),
        ('br', 'BlueRay'),
    )
    carrier = models.CharField(choices=CARRIERS, max_length=5)

class Music(Product):
    author = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)

class MusicFileVariant(Variant, OnlineVariantMixin):
    duration = models.IntegerField()

class MusicAlbumVariant(Variant, OfflineVariantMixin):
    CARRIERS = (
        ('dvd', 'DVD'),
        ('br', 'BlueRay'),
        ('cd', 'Audio CD'))
    carrier = models.CharField(choices=CARRIERS, max_length=5)
