from __future__ import absolute_import, unicode_literals
import hashlib
from logging import getLogger
from celery import shared_task
from django.core.cache import get_cache as django_get_cache
from newsboard import models
from newsboard import settings

logger = getLogger("newsboard")


@shared_task
def update_stream(stream_id):
    stream = models.Stream.objects.get(id=stream_id)
    lock = Lock('update_stream', stream_id)
    if not lock.is_locked:
        logger.debug('Locked %s' % stream)
        return
    logger.debug('Updating %s' % stream)
    stream.update_posts()
    logger.info('Updated %s' % stream)


@shared_task
def update_streams(stream_ids):
    streams = models.Stream.objects.filter(id__in=stream_ids)
    for stream in streams:
        update_stream.delay(stream.id)


@shared_task
def update_all_streams():
    lock = Lock('update_all_streams')
    if not lock.is_locked:
        return
    streams = models.Stream.objects.filter(auto_enabled=True)
    stream_ids = []
    for stream in streams:
        if stream.need_update():
            stream_ids.append(stream_ids)
    return update_streams(stream_ids)


class Lock(object):
    def __init__(self, name, *args, **kwargs):
        self.key = self._get_key(name, *args, **kwargs)

    def _get_key(self, name, *args, **kwargs):
        args_value = '-'.join([str(v) for v in args if str(v)])
        kwargs_value = '-'.join([str(v) for v in kwargs.itervalues() if str(v)])
        value = '-'.join([name, args_value, kwargs_value])
        if settings.LOCK_SALT:
            value = '%s-%s' % (value, settings.SALT)
        hashed = hashlib.sha256(value).hexdigest()
        return hashed

    @property
    def cache(self):
        return django_get_cache(settings.LOCK_CACHE)

    @property
    def is_locked(self):
        return self.cache.has_key(self.key)

    def lock(self):
        self.cache.add(self.key, True, settings.LOCK_TIMEOUT)

    def unlock(self):
        self.cache.delete(self.key)
