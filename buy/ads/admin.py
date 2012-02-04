# -*- coding: utf-8 -*-
from django.contrib import admin
from buy.ads.models import Advert, Comment, PrivateMessage, News, Category, UserProfile

admin.site.register(Advert)
admin.site.register(Comment)
admin.site.register(PrivateMessage)
admin.site.register(News)
admin.site.register(Category)
admin.site.register(UserProfile)