import sys
import os

DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(DIR, '..', '..', '..', '..'))

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
    }
}

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'w1$8^sjw_=%owwctqsa-czup!37mqv2ok$dw!e(tt2yc(cl&amp;bq'

ROOT_URLCONF = 'project.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'project.wsgi.application'

INSTALLED_APPS = (
  'project',
  'jstemplate'
)
