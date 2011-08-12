# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from ads.models import Advert

def main_page(request):
  ads_list = Advert.objects.all()
  return render_to_response('main.html', {'ads_list': ads_list})
