# -*- coding:utf-8 -*-
from django.contrib import admin
from products import models

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

#Book model and variants
class TraditionalBookVariantInline(admin.TabularInline):
    model = models.TraditionalBookVariant

class EBookVariantInline(admin.TabularInline):
    model = models.EBookVariant

class BookAdmin(ProductAdmin):
    inlines = [TraditionalBookVariantInline, EBookVariantInline]

#Movie model and variants
class OnlineMovieVariantInline(admin.TabularInline):
    model = models.OnlineMovieVariant

class TraditionalMovieVariantInline(admin.TabularInline):
    model = models.TraditionalMovieVariant

class MovieAdmin(ProductAdmin):
    inlines = [OnlineMovieVariantInline, TraditionalMovieVariantInline]

#Music model and variant
class MusicFileVariantInline(admin.TabularInline):
    model = models.MusicFileVariant

class MusicAlbumVariantInline(admin.TabularInline):
    model = models.MusicAlbumVariant

class MusicAdmin(ProductAdmin):
    inlines = [MusicFileVariantInline, MusicAlbumVariantInline]

admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Movie, MovieAdmin)
admin.site.register(models.Music, MusicAdmin)
