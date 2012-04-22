# -*- coding: utf-8 -*-
# Default Django settings for possiblecity

import os.path
import posixpath

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    ('Douglas Meehan', 'dmeehan@gmail.com'),
    )

MANAGERS = ADMINS

SITE_ID = 1

#==============================================================================
# Debugging
#==============================================================================

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
    }

INTERNAL_IPS = [
    "127.0.0.1",
]

#==============================================================================
# Localization
#==============================================================================

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
USE_I18N = False    #internationalization machinery
USE_L10N = False    #format dates, numbers and calendars according to locale


#==============================================================================
# Project URLS and media settings
#==============================================================================

SERVE_MEDIA = DEBUG

ROOT_URLCONF = 'possiblecity.urls'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media", "uploads")
MEDIA_URL = "/media/uploads/"

STATIC_ROOT = os.path.join(PROJECT_ROOT, "media", "static")
STATIC_URL = "/media/static/"

ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static"),
]

STATICFILES_FINDERS = [
    "staticfiles.finders.FileSystemFinder",
    "staticfiles.finders.AppDirectoriesFinder",
    "staticfiles.finders.LegacyAppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

# django-compressor is turned off by default due to deployment overhead for
# most users.
COMPRESS = False
COMPRESS_OUTPUT_DIR = "cache"

#==============================================================================
# Templates
#==============================================================================

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, "templates"),
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",

    "staticfiles.context_processors.static",

    "pinax.core.context_processors.pinax_settings",
]


TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

#==============================================================================
# Middleware
#==============================================================================


MIDDLEWARE_CLASSES = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "pinax.middleware.security.HideSensistiveFieldsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

#==============================================================================
# Fixtures
#==============================================================================

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

#==============================================================================
# Messages
#==============================================================================

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"


#==============================================================================
# Authentication
#==============================================================================



#==============================================================================
# Installed Apps
#==============================================================================

INSTALLED_APPS = (
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.humanize',

    # Third party Pinax apps
    'pinax.templatetags',

    # third party apps
    'staticfiles',
    'compressor',
    'debug_toolbar',

    'haystack', # search
    'south', # database migrations
    'oembed',
    'imagekit',
    'django_markup', # required for blog
    'taggit', # required for blog, float, & lotxlot
    'django_generic_flatblocks',


    # backbeat apps
    'inlines',
    'twittools',
    'images',
    'text',

    # local apps
    'blog',
    'about',

)

#==============================================================================
# Logging
#==============================================================================


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


#==============================================================================
# Email
#==============================================================================


#==============================================================================
# Search
#==============================================================================

# django-haystack
HAYSTACK_SITECONF = 'possiblecity.search_sites'


#==============================================================================
# Notifications
#==============================================================================



#==============================================================================
# Analytics
#==============================================================================



#==============================================================================
# local app settings
#==============================================================================

BLOG_MARKUP_DEFAULT = 'markdown'

#==============================================================================
# local environment settings
#==============================================================================

try:
    from local_settings import *
except ImportError:
    pass