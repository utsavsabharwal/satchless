from django.db import models

from products.models import Variant
from satchless.cart.models import Cart, CartItem
from satchless.util.models import construct


class Cart(Cart):
    pass


class CartItem(construct(CartItem, cart=Cart, variant=Variant)):
    pass
