from satchless.product.app import ProductApp

from . import models

class AlchemyProductApp(ProductApp):
    Product = models.Product
    Variant = models.Variant

    def get_product(self, request, product_pk, product_slug):
        Product = self.Product
        session = request.db_session
        return (session.query(Product)
                       .filter(Product.pk==product_pk,
                               Product.slug==product_slug)).one()