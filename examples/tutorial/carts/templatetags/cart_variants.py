# -*- coding: utf-8 -*-
from django.template import Library
from ..app import cart_app
register = Library()

@register.inclusion_tag('cart/_variants_forms.html')
def variants_to_cart_forms(variants, product):
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

@register.simple_tag
def cart_target():
    return cart_app.reverse('details')

@register.inclusion_tag('cart/_view.html', takes_context = True)
def cart(context):
    if 'request' not in context:
        return
    cart = cart_app.get_cart_for_request(context['request'])
    return {'items': cart.get_all_items()}