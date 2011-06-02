# -*- coding:utf-8 -*-
try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.

from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.decorators import available_attrs
from django.views.decorators.http import require_POST

from ....cart.models import Cart
from ....order import handler
from ....order import models
from ....order import signals
from ....payment import PaymentFailure, ConfirmationFormNeeded

def require_order(status=None):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            order = None
            if 'order_token' in kwargs:
                try:
                    order = models.Order.objects.get(token=kwargs['order_token'],
                                                     status=status)
                except models.Order.DoesNotExist:
                    pass
            if not order:
                return redirect('satchless-cart-view')
            elif status is not None and status != order.status:
                if order.status == 'checkout':
                    return redirect('satchless-checkout',
                                    order_toke=order.token)
                elif order.status == 'payment-pending':
                    return redirect(confirmation)
                else:
                    return redirect('satchless-order-view',
                                    order_token=order.token)
            request.order = order
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

@require_POST
def prepare_order(request, typ):
    cart = Cart.objects.get_or_create_from_request(request, typ)
    order_pk = request.session.get('satchless_order')
    previous_orders = models.Order.objects.filter(pk=order_pk, cart=cart,
                                                  status='checkout')
    try:
        order = previous_orders.get()
    except models.Order.DoesNotExist:
        try:
            order = models.Order.objects.get_from_cart(cart)
        except models.EmptyCart:
            return redirect('satchless-cart-view', typ=typ)
    request.session['satchless_order'] = order.pk
    return redirect('satchless-checkout', order_token=order.token)

@require_POST
@require_order(status='payment-failed')
def reactivate_order(request, order_token):
    order = request.order
    order.set_status('checkout')
    return redirect('satchless-checkout', order_token=order.token)

@require_order(status='payment-pending')
def confirmation(request, order_token):
    """
    Checkout confirmation
    The final summary, where user is asked to review and confirm the order.
    Confirmation will redirect to the payment gateway.
    """
    order = request.order
    if not request.order:
        return redirect('satchless-checkout', order_token=order.token)
    signals.order_pre_confirm.send(sender=models.Order, instance=order,
                                   request=request)
    try:
        handler.confirm(order)
    except ConfirmationFormNeeded, e:
        return TemplateResponse(request, 'satchless/checkout/confirmation.html', {
            'formdata': e,
            'order': order,
        })
    except PaymentFailure:
        order.set_status('payment-failed')
    else:
        order.set_status('payment-complete')
    return redirect('satchless-order-view', order_token=order.token)
