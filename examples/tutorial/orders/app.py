from carts.app import cart_app
from satchless.order.app import MagicOrderApp

from . import models


class OrderApp(MagicOrderApp):
    Order = models.Order
    DeliveryGroup = models.DeliveryGroup
    OrderedItem = models.OrderedItem


order_app = OrderApp(cart_app=cart_app)
