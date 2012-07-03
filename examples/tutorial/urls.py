from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
import orders.views

admin.autodiscover()

from products.app import products_app
from carts.app import cart_app
from orders.app import order_app
from checkout.app import checkout_app

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(products_app.urls)),
    url(r'^cart/', include(cart_app.urls)),
    url(r'^order/', include(order_app.urls)),
    url(r'^checkout/', include(checkout_app.urls)),
    url(r'^payment-gateways/django-payments/', include('payments.urls')),
    url(r'^thankyou/(?P<order_token>\w+)/$', orders.views.thank_you_page, name='thank-you'),
    url(r'^failed/(?P<order_token>\w+)/$', orders.views.payment_failed, name='payment-failed'),

)
