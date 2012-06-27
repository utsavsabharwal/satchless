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
    #Category = models.Category

    @view(r'^$', name='products-index')
    def product_list(self, request, products = None):
        if not products:
            products = self.Product.objects.all()
        context = self.get_context_data(request, products=products)
        template = 'satchless/products/list.html'
        return TemplateResponse(request, template, context)

#product_app = CategorizedProductApp()
products_app = ProductsApp()