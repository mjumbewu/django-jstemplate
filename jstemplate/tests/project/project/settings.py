import sys
import os

DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(DIR, '..', '..', '..', '..')
sys.path.insert(0, os.path.abspath(BASE_DIR))

DEBUG = True
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'} }

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'w1$8^sjw_=%owwctqsa-czup!37mqv2ok$dw!e(tt2yc(cl&amp;bq'

ROOT_URLCONF = 'project.urls'
MIDDLEWARE_CLASSES = ()

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'project.wsgi.application'

INSTALLED_APPS = (
  'project',
  'jstemplate'
)
