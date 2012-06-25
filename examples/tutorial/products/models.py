# -*- coding:utf-8 -*-
import os

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_images.models import Image
from mothertongue.models import MothertongueModelTranslate
from satchless.category.models import CategorizedProductMixin
from satchless.contrib.pricing.simpleqty.models import (ProductPriceMixin,
                                                        VariantPriceOffsetMixin)
from satchless.contrib.tax.flatgroups.models import TaxedProductMixin
from satchless.contrib.stock.singlestore.models import VariantStockLevelMixin
import satchless.product.models
from satchless.util.models import construct

from categories.models import Category
#from sale.models import DiscountedProductMixin

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
    
