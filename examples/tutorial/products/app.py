import satchless.category.app
from satchless.pricing.app import ProductAppPricingMixin
from satchless.product.app import ProductApp
from satchless.core.app import view

from . import models
from products.models import Product, Variant

from django.template.response import TemplateResponse

class ProductsApp(ProductApp):
    Product = Product
    Variant = Variant

    @view(r'^$', name='products-index')
    def product_list(self, request, products = None):
        if not products:
            products = self.Product.objects.all()
        context = self.get_context_data(request, products=products)
        template = 'product/list.html'
        
        return TemplateResponse(request, template, context)

    @view(r'^\+(?P<product_pk>[0-9]+)-(?P<product_slug>[a-z0-9_-]+)/$',
          name='details')
    def product_details(self, request, **kwargs):
        tmpl_resp = super(ProductsApp, self).product_details(request, **kwargs)
        
        product = tmpl_resp.context_data['product']
        variants = [variant.get_subtype_instance() for variant in
                    self.Variant.objects.filter(product = product)]

        tmpl_resp.context_data['variants'] = variants
        tmpl_resp.template_name = 'product/%s.html'%product._meta.module_name

        return tmpl_resp

products_app = ProductsApp()