from . import models
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from examples.tutorial.products.models import Variant
from satchless.cart.app import MagicCartApp
from satchless.core.app import view
from products.app import products_app


class CartApp(MagicCartApp):
    Cart = models.Cart
    CartItem = models.CartItem

    @view(r'^add/$', name='add-item')
    @method_decorator(require_POST)
    def add_item_view(self, request):
        cart = self.get_cart_for_request(request)
        post = request.POST
        variant_id = int(post.get('variant_id'))
        try:
            quantity = int(post.get('quantity'))
        except ValueError:
            quantity = 1
        redirect_url = (
            post.get('redirect_url')
            or request.META.get('HTTP_REFERER')
            or '')  # TODO it would be smarter to get product url or cart url
        variant = Variant.objects.get(variant_id)
        variant = variant.get_subtype_instance()
        cart.add_item(variant, quantity)
        return redirect(redirect_url)


cart_app = CartApp(product_app=products_app)
