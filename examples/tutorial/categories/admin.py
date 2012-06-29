# -*- coding:utf-8 -*-
from django.contrib import admin
from categories.models import Category

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
