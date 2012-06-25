# -*- coding:utf-8 -*-
from django import forms
from django.contrib import admin
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms.models import modelform_factory
from django.utils.translation import ugettext_lazy as _, ugettext
import django.db.models

from products.models import Book, Movie, Music

class BookAdmin(admin.ModelAdmin):
    pass

class MovieAdmin(admin.ModelAdmin):
    pass

class MusicAdmin(admin.ModelAdmin):
    pass

admin.site.register(Book, BookAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Music, MusicAdmin)