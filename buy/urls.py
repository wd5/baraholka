# -*- coding: utf-8 -*-
from subprocess import check_output
hostname = check_output('hostname').strip()
is_development = (hostname == 'Rocker' or hostname == 'rck-thinkpad')

if is_development:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf.urls.defaults import patterns, include
from buy.ads.views import ad_show, news_all_show, news_show, \
                          ad_add, ad_edit, ad_archive, cabinet, my_ads_list,\
                          reg, adverts_list
from django.contrib.auth.views import login, logout
from postman import urls as postman_urls
from buy.ads.feeds import BaseFeed, VkontakteFeed
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', adverts_list, {'sell_page_num': '1', 'buy_page_num': '1', 
                           'cat_num': '0'}),
    (r'^list/(?P<sell_page_num>\d+)-(?P<buy_page_num>\d+)-(?P<cat_num>\d+)',
     adverts_list),
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
    (r'^news/$', news_all_show),
    (r'^news/(?P<num>\d+)/$', news_show),
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
