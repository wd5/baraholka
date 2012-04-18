# -*- coding: utf-8 -*-
# Django settings for buy project.
from subprocess import check_output
hostname = check_output('hostname').strip()
is_development = (hostname == 'Rocker')

if is_development:
    from django.conf.global_settings import STATIC_URL

if is_development:
    DEBUG = True
else:
    DEBUG = False

DEFAULT_FROM_EMAIL = "noreply@buy.fizteh.ru"

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
    ('Vasiliy Korchagin', 'vasiliy.korchagin@gmail.com'),
)

MANAGERS = ADMINS

dev_db = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'buydb',
    'USER': 'buy',
    'PASSWORD': 'baraholka'
}
release_db = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'shop',
    'USER': 'vkorchagin',
    'PASSWORD': 'rSmjQL8YJbCTczaL'
}

DATABASES = {
    'default': dev_db if is_development else release_db
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    }
}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
# MEDIA_ROOT = '/var/www/djcode/buy/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
# MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
# ADMIN_MEDIA_PREFIX = '/media/'
ADMIN_MEDIA_PREFIX="/static/admin/"

# Make this unique, and don't share it with anybody.
SECRET_KEY = 't^*#g9u+!u1rv)9jejr+wwzy)s$fs^@uila&q8v_0_9)#10hsi'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

AUTH_PROFILE_MODULE = 'ads.UserProfile'

# --- Start of the postman settings ---
POSTMAN_DISALLOW_ANONYMOUS=True
POSTMAN_DISALLOW_MULTIRECIPIENTS=True
POSTMAN_DISALLOW_COPIES_ON_REPLY=True
POSTMAN_AUTO_MODERATE_AS=True
# --- End of the postman settings  ---

# --- Start of the haystack settings ---
HAYSTACK_SITECONF = 'buy.search_sites'
HAYSTACK_SEARCH_ENGINE = 'simple'
# --- End of the haystack settings   ---

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "postman.context_processors.inbox",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

#ROOT_URLCONF = 'buy.urls'
ROOT_URLCONF = 'urls'
FORCE_SCRIPT_NAME = ''

dev_template_dirs = ('/home/rocker/djcode/baraholka/buy/templates',)
release_template_dirs = ('/vint/data/host/42b.ru/shop/buy/templates',)

TEMPLATE_DIRS = dev_template_dirs if is_development else release_template_dirs

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.markup',
    'django.contrib.sessions',
    'django.contrib.sites',
    'pagination',
    'buy.ads',
    'postman',
    'haystack',
)


static_release = ('/vint/data/host/42b.ru/shop/buy/static',)
static_dev = ("/home/rocker/djcode/baraholka/buy/static/",)
STATICFILES_DIRS = static_dev if is_development else static_release

if is_development:
    STATIC_URL = "/static/"
