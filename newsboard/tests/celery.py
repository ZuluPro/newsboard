from __future__ import absolute_import, unicode_literals

import os
import celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsboard.tests.settings')

app = celery.Celery('newsboard_tests')
if celery.__version__ >= (4, 0, 0):
    app.config_from_object('django.conf:settings', namespace='CELERY')
    app.autodiscover_tasks()
else:
    app.config_from_object('django.conf:settings')
    app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
