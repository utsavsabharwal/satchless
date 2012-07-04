from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.shortcuts import redirect

from ..core.app import SatchlessApp, view
from ..util import JSONResponse

from . import models
from ..cart import forms

class ProductApp(SatchlessApp):

    app_name = 'product'
    namespace = 'product'
    Product = None
    Variant = None
    product_view_handlers_queue = None

    def __init__(self, *args, **kwargs):
        super(ProductApp, self).__init__(*args, **kwargs)
        self.product_view_handlers_queue = set()
        assert self.Product, ('You need to subclass ProductApp and provide'
                              ' Product')
        assert self.Variant, ('You need to subclass ProductApp and provide'
                              ' Variant')

    def get_product(self, request, product_pk, product_slug):
        product = get_object_or_404(self.Product, pk=product_pk,
                                    slug=product_slug)
        return product.get_subtype_instance()

    def get_product_details_templates(self, product):
        return ['satchless/product/view.html']

    @view(r'^\+(?P<product_pk>[0-9]+)-(?P<product_slug>[a-z0-9_-]+)/$',
          name='details')
    def product_details(self, request, extra_context={}, product=None, **kwargs):
        if not product:
            try:
                product = self.get_product(request, **kwargs)
            except ObjectDoesNotExist:
                return HttpResponseNotFound()
            
        context = dict(extra_context)
        context['variants'] = [variant.get_subtype_instance() for variant in
                self.Variant.objects.filter(product = product)]
        context['product'] = product
        context = self.get_context_data(request, **context)
        templates = self.get_product_details_templates(product)
        return TemplateResponse(request, templates, context)

    def register_product_view_handler(self, handler):
        self.product_view_handlers_queue.add(handler)


class ProductAppWithFormCart(ProductApp):
    def __init__(self, addtocart_formclass=forms.AddToCartForm, *args, **kwargs):
        super(ProductAppWithFormCart, self).__init__(*args, **kwargs)
        self.addtocart_formclass = addtocart_formclass
        
    @view(r'^\+(?P<product_pk>[0-9]+)-(?P<product_slug>[a-z0-9_-]+)/$',
          name='details')
    def product_details(self, request, **kwargs):
        try:
            product = self.get_product(request, **kwargs)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        Form = forms.add_to_cart_variant_form_for_product(product,
                    addtocart_formclass=self.addtocart_formclass)
        # TODO: remove hardcoded type
        form = Form(initial=request.POST, product=product, typ='cart')
        if form.is_valid():
            form_result = form.save()
            self.cart_item_added(form_result)
            if request.is_ajax():
                # FIXME: add cart details like number of items and new total
                return JSONResponse({})
            return redirect(self.reverse('details',
               kwargs = {'product_pk':product.id, 'product_slug':product.slug}))
        elif request.is_ajax() and form.errors:
            data = dict(form.errors)
            return JSONResponse(data, status=400)

        return super(ProductAppWithFormCart, self).product_details(request,
                  extra_context={'cart_form':form}, product=product, **kwargs)
        
    def cart_item_added(self, form_result):
        pass

class MagicProductApp(ProductApp):

    def __init__(self, **kwargs):
        self.Product = (self.Product or
                        self.construct_product_class())
        self.Variant = (self.Variant or
                        self.construct_variant_class(self.Product))
        super(MagicProductApp, self).__init__(**kwargs)

    def construct_product_class(self):
        class Product(models.Product):
            pass
        return Product

    def construct_variant_class(self, product_class):
        class Variant(models.Variant):
            pass
        return Variant