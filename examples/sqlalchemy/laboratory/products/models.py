import sqlalchemy
from sqlalchemy.orm import relationship, backref

from satchless.product.models import BaseProduct

from ..database import Base


class Product(Base, BaseProduct):

    __tablename__ = 'products'
    pk = sqlalchemy.Column(sqlalchemy.Integer,
                           sqlalchemy.Sequence('product_pk_seq'),
                           primary_key=True)
    slug = sqlalchemy.Column(sqlalchemy.String(250), index=True)
    title = sqlalchemy.Column(sqlalchemy.String(250))

    def __init__(self, slug, title):
        self.slug = slug
        self.title = title


class Variant(Base):

    __tablename__ = 'variants'
    pk = sqlalchemy.Column(sqlalchemy.Integer,
                           sqlalchemy.Sequence('variant_pk_seq'),
                           primary_key=True)
    product_pk = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey(Product.pk))
    product = relationship(Product,
                           backref=backref('variants', order_by=pk))