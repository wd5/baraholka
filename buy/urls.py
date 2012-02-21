# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include
from buy.ads.views import ad_show, main, news_all_show, news_show, cat_list,\
                          ad_add, cabinet, my_ads_list, reg, ad_edit,\
                          ad_archive
from django.contrib.auth.views import login, logout
from django.views.generic.simple import redirect_to
from postman import urls as postman_urls

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^login/$', login),
    (r'^logout/$', logout),
    (r'^item/(?P<num>\d+)/$', ad_show),
    (r'^ads/(?P<num>\d+)/$', redirect_to, {'url': '/item/%(num)s/'}),
    (r'^edit/(?P<num>\d+)/$', ad_edit),
    (r'^archive/(?P<num>\d+)/$', ad_archive),
    (r'^$', main, {'p_num': '1'}),
    (r'^page/(?P<p_num>\d+)/$', main),
    (r'^news/$', news_all_show),
    (r'^news/(?P<num>\d+)/$', news_show),
    (r'^cat/(?P<num>\d+)/$', cat_list, {'p_num': '1'}),
    (r'^cat/(?P<num>\d+)/page/(?P<p_num>\d+)/$', cat_list),
    (r'^add/$', ad_add),
    (r'^cabinet/$', cabinet),
    (r'^cabinet/ads$', my_ads_list),
    #(r'^cabinet/msg$', msg_list),
    (r'^cabinet/msg/', include(postman_urls)),
    (r'^reg/$', reg),
    #(r'^search/$', search),
    (r'^search/', include('haystack.urls')),
)
