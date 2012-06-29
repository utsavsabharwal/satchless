# -*- coding: utf-8 -*-
from django.template import Library
register = Library()

@register.inclusion_tag('cart/_variants_forms.html', takes_context = True)
def variants_to_cart_forms(context, variants, product):
    forms = {}
    for variant in variants:
        forms[variant.__class__]= variant.Form(product = product,
                                               variant=variant)
    #resolved link from cart app
    action = ''
    return {'forms': forms.values(), 'action':action}

@register.inclusion_tag('cart/_variants_list.html')
def variants_to_list(variants, product):
    action = ''
    return {'variants':variants, 'action':action}