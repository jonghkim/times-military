# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import restaurant, choice
import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

admin.site.register(restaurant)
admin.site.register(choice)
