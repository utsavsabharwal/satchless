# -*- coding:utf-8 -*-
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from orders.app import order_app

def thank_you_page(request, order_token):
    order = order_app.get_order(request, order_token)
    if not order.status in ('payment-failed', 'payment-complete', 'delivery'):
        return redirect(order_app.reverse('details',
            args=(order.token,)))
    if order.status == 'payment-failed':
        return redirect('payment-failed', order_token=order.token)

    return TemplateResponse(request, 'order/thank_you.html', {
        'order': order,
        })

def payment_failed(request, _order_token):
    return TemplateResponse(request, 'order/payment_failed.html')
