# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from buy.ads.models import Advert
from buy.ads.templatetags import bbcode


class LatestAdvertsFeed(Feed):
    title = "Барахолка Физтеха"
    link = "/feed/"
    description = "Последние объявления Барахолки Физтеха."

    def items(self):
        items = Advert.objects.filter(sell=True, is_selled=False).\
            order_by('-created')[:5]
        items.reverse()
        return items

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return bbcode.strip_bbcode(item.text)

    def item_link(self, item):
        return '/item/%d' % item.id
    
    def item_pubdate(self, item):
        return item.created
