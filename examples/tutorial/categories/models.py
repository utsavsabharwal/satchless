# -*- coding:utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_images.models import Image
import satchless.category.models

from localeurl.models import reverse

class Category(satchless.category.models.Category):
    pass