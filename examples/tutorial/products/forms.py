# -*- coding:utf-8 -*-
from django import forms
from satchless.product.forms import BaseVariantForm, registry
from . import models
from django.forms.formsets import formset_factory


class BookVariantForm(BaseVariantForm):
    stock = forms.DecimalField()

class TraditionalBookVariantForm(BookVariantForm):
    hard_cover = forms.BooleanField()
    ebook = forms.BooleanField()

class EBookVariantForm(BookVariantForm):
    ebook = forms.BooleanField()

#I can register only one variant per product...
#registry.register(models.TraditionalBookVariant, TraditionalBookVariantForm)
#registry.register(models.EBookVariant, EBookVariantForm)

models.TraditionalBookVariant.Form = TraditionalBookVariantForm
models.EBookVariant.Form = EBookVariantForm