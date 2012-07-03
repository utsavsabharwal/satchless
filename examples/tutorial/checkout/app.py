from django.forms.models import modelform_factory
from tutorial_payments import PaymentsProvider
from satchless.contrib.delivery.simpledownload import DownloadDeliveryProvider
from satchless.contrib.delivery.simplepost import PostDeliveryProvider
from satchless.order import forms

from satchless.contrib.checkout.singlestep.app import SingleStepCheckoutApp

from carts.app import cart_app
from orders.app import order_app
from satchless.order.handler import DeliveryQueue, PaymentQueue


class CheckoutApp(SingleStepCheckoutApp):
    Order = order_app.Order

    BillingForm = modelform_factory(order_app.Order,
        forms.BillingForm)
    ShippingForm= modelform_factory(order_app.DeliveryGroup,
        form=forms.ShippingForm,
        fields=forms.ShippingForm._meta.fields)
    DeliveryMethodForm = modelform_factory(order_app.DeliveryGroup,
        form=forms.DeliveryMethodForm,
        fields=forms.DeliveryMethodForm._meta.fields)

checkout_app = CheckoutApp(
    cart_app,
    delivery_provider=DeliveryQueue(
        PostDeliveryProvider, DownloadDeliveryProvider),
    payment_provider=PaymentQueue(PaymentsProvider))
