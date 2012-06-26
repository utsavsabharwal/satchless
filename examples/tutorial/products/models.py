# -*- coding:utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from satchless.category.models import CategorizedProductMixin
from satchless.contrib.pricing.simpleqty.models import ProductPriceMixin,\
    VariantPriceOffsetMixin
from satchless.contrib.tax.flatgroups.models import TaxedProductMixin
from satchless.util.models import construct
import satchless.product.models

from ..categories.models import Category


class Product(ProductPriceMixin, TaxedProductMixin,
              construct(CategorizedProductMixin, category=Category)):

    name = models.CharField(_('name'), max_length=128)
    slug = models.SlugField(_('slug'), max_length=128)
    description = models.TextField(_('description'), blank=True)

class Book(Product):
    isbn = models.CharField(max_length=13)
    author = models.CharField(max_length=50)
    publication_date = models.DateField(blank=True)

class Movie(Product):
    director = models.CharField(max_length=50)
    premiere_date = models.DateField(blank=True)

class Music(Product):
    author = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)

