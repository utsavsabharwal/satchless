from django.conf.urls.defaults import patterns, include, url

from .products.app import AlchemyProductApp

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url('^products/', include(AlchemyProductApp().urls)),
    # Examples:
    # url(r'^$', 'sqlalchemy2.views.home', name='home'),
    # url(r'^sqlalchemy2/', include('sqlalchemy2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
