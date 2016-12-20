"""
Configuration and launcher for Django Web Rich Object tests.
"""
import os
import tempfile
import dj_database_url

DEBUG = TEMPLATE_DEBUG = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TESTAPP_DIR = os.path.join(BASE_DIR, 'testapp/')

ADMINS = (
    ('ham', 'foo@bar'),
)
ALLOWED_HOSTS = ['*']
MIDDLEWARE_CLASSES = MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
ROOT_URLCONF = 'newsboard.tests.urls'
SECRET_KEY = "it's a secret to everyone"
SITE_ID = 1
MEDIA_ROOT = os.environ.get('MEDIA_ROOT') or tempfile.mkdtemp()
INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.admin',
    'dj_web_rich_object',
    'newsboard',
)

DATABASE = dj_database_url.config(default='sqlite:///test.sqlite')
DATABASES = {'default': DATABASE}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

SERVER_EMAIL = 'wro@test.org'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            )
        }
    },
]

STATIC_URL = '/static/'

CELERY_BROKER_URL = os.environ.get('BROKER_URL', 'redis://127.0.0.1:6379/0')
# CELERY_BROKER_TRANSPORT = os.environ.get('BROKER_TRANSPORT', 'djkombu.transport.DatabaseTransport')
# CELERY_RESULT_BACKEND = os.environ.get('BROKER_TRANSPORT', )
CELERY_ALWAYS_EAGER = True

NEWSBOARD_FACEBOOK_TOKEN = os.environ.get('NEWSBOARD_FACEBOOK_TOKEN')
