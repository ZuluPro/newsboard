from __future__ import absolute_import
from django.utils.module_loading import import_string
from newsboard import settings
from newsboard.feeds.base import BaseFeed
from newsboard.feeds.rss import RssFeed
from newsboard.feeds.facebookfeed import FacebookFeed


def get_feed(stream_type):
    for addr, key, _ in settings.STREAM_TYPES:
        if stream_type == key:
            return import_string(addr)
    else:
        raise Exception("Feed system not found")
