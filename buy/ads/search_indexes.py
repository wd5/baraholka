from haystack.indexes import *
from haystack import site
from ads.models import Advert

class AdvertIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    user = CharField(model_attr='user')
    category = MultiValueField(model_attr='category')
    price = CharField(model_attr='price')
    place = CharField(model_attr='place')


site.register(Advert, AdvertIndex)
