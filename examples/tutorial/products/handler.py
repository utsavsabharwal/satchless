from django.shortcuts import redirect

from models import Product, Variant
from . import forms

class VariantsHandler(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, instances=None, request=None, extra_context=None,
                 **kwargs):

        for product in instances:
            variants = [variant.get_subtype_instance() for variant in
                    self.app.Variant.objects.filter(product = product)]

            extra_context = {'variants': variants}

        return extra_context
