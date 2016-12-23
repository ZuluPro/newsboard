from __future__ import absolute_import, unicode_literals
import hashlib
from logging import getLogger
from celery import shared_task
from django.core.cache import caches
from newsboard import models
from newsboard import settings

logger = getLogger("newsboard")


@shared_task
def update_stream(stream_id):
    stream = models.Stream.objects.get(id=stream_id)
    lock = Lock('update_stream', stream_id)
    if lock.is_locked:
        logger.info("Task '%s' for %s is locked: %s", lock.name, stream.name, lock.key)
        return
    lock.lock()
    try:
        logger.debug('Updating %s' % stream)
        stream.update_posts()
        logger.info('Updated %s' % stream)
    finally:
        lock.unlock()


@shared_task
def update_streams(stream_ids):
    streams = models.Stream.objects.filter(id__in=stream_ids)
    for stream in streams:
        update_stream.delay(stream.id)


@shared_task
def update_all_streams(auto_enabled=True):
    lock = Lock('update_all_streams')
    if lock.is_locked:
        logger.info("Task '%s' is locked: %s", lock.name, lock.key)
        return
    lock.lock()
    try:
        streams = models.Stream.objects.filter(auto_enabled=auto_enabled)
        stream_ids = []
        for stream in streams:
            if stream.need_update():
                stream_ids.append(stream.id)
        return update_streams(stream_ids)
    finally:
        lock.unlock()


class Lock(object):
    def __init__(self, name, *args, **kwargs):
        self.name = name
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
        return caches[settings.LOCK_CACHE]

    @property
    def is_locked(self):
        return self.cache.has_key(self.key)

    def lock(self):
        self.cache.add(self.key, True, settings.LOCK_TIMEOUT)

    def unlock(self):
        self.cache.delete(self.key)
