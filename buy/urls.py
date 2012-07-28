# -*- coding: utf-8 -*-
from subprocess import check_output
hostname = check_output('hostname').strip()
is_development = (hostname == 'Rocker' or hostname == 'rck-thinkpad')

if is_development:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf.urls.defaults import patterns, include
from buy.ads.views import ad_show, main, news_all_show, news_show, cat_list,\
                          ad_add, ad_edit, ad_archive, cabinet, my_ads_list,\
                          reg
from django.contrib.auth.views import login, logout
from postman import urls as postman_urls
from buy.ads.feeds import BaseFeed, VkontakteFeed
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^feed/', BaseFeed()),
    (r'^feed_vkontakte/', VkontakteFeed()),
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
    (r'^cabinet/item$', my_ads_list),
    #(r'^cabinet/msg$', msg_list),
    (r'^cabinet/msg/', include(postman_urls)),
    (r'^reg/$', reg),
    #(r'^search/$', search),
    (r'^search/', include('haystack.urls')),
)

if is_development:
    urlpatterns += staticfiles_urlpatterns()
