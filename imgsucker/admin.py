# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from imgsucker.models import Resolution, Wallpaper, Tag, User
# Register your models here.

admin.site.register(Resolution)
admin.site.register(Wallpaper)
admin.site.register(Tag)
admin.site.register(User)