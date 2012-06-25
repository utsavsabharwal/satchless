# -*- coding:utf-8 -*-
from django import forms
from django.contrib import admin
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms.models import modelform_factory
from django.utils.translation import ugettext_lazy as _, ugettext
import django.db.models

from categories.models import Category

#from categories.app import product_app
#import pricing.models
#from . import widgets
#from . import models

#from categories.admin.fields import CategoryMultipleChoiceField

class CategoryAdmin(admin.ModelAdmin):
    model = admin.ModelAdmin
    
admin.site.register(Category, CategoryAdmin)