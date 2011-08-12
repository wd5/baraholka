import sys
import os

path = '/var/www/djcode/'
if path not in sys.path:
  sys.path.append(path)

buy_path = '/var/www/djcode/buy/'
if buy_path not in sys.path:
  sys.path.append(buy_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'buy.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
