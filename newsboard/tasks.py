from __future__ import absolute_import, unicode_literals
from logging import getLogger
from celery import shared_task
from newsboard import models

logger = getLogger("newsboard")


@shared_task
def update_stream(stream_id):
    stream = models.Stream.objects.get(id=stream_id)
    logger.debug('Updating %s' % stream)
    stream.update()
    logger.info('Updated %s' % stream)


@shared_task
def update_streams(stream_ids):
    streams = models.Stream.objects.filter(id__in=stream_ids)
    for stream in streams:
        update_stream.delay(stream.id)


@shared_task
def auto_update_stream():
    streams = models.Stream.objects.filter(auto_enabled=True)
    stream_ids = []
    for stream in streams:
        if stream.need_update():
            stream_ids.append(stream_ids)
    return update_streams(stream_ids)
