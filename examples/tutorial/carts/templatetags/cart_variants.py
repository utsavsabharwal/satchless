# -*- coding: utf-8 -*-
from django.template import Library
from ..app import cart_app
register = Library()

@register.inclusion_tag('cart/_variants_forms.html', takes_context = True)
def variants_to_cart_forms(context, variants, product):
    forms = {}
    for variant in variants:
        forms[variant.__class__]= variant.Form(product = product,
                                               variant=variant)
    return {'forms': forms.values()}

@register.inclusion_tag('cart/_variants_list.html')
def variants_to_list(variants, product):
    return {'variants':variants}

@register.simple_tag
def cart_form_target():
    return cart_app.reverse('add-item')