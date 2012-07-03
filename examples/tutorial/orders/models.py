from carts.models import Cart
from products.models import Variant
from satchless.order.models import Order, DeliveryGroup, OrderedItem
from satchless.util.models import construct


class Order(construct(Order, cart=Cart)):
    pass


class DeliveryGroup(construct(DeliveryGroup, order=Order)):
    pass


class OrderedItem(construct(OrderedItem,
                            delivery_group=DeliveryGroup,
                            variant=Variant)):
    pass

