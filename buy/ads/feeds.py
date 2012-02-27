# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from buy.ads.models import Advert


class LatestAdvertsFeed(Feed):
    title = "Барахолка Физтеха"
    link = "/feed/"
    description = "Последние объявления Барахолки Физтеха."

    def items(self):
        return Advert.objects.filter(sell=True, is_selled=False).\
            order_by('-created')[:5]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.text

    def item_link(self, item):
        return '/item/%d' % item.id
