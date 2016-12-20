from time import mktime
from datetime import datetime
try:
    from urllib import HTTPError
except ImportError:
    from urllib2 import HTTPError
import feedparser
from django.utils.module_loading import import_string
from newsboard import settings


def get_feed(stream_type):
    for addr, key, _ in settings.STREAM_TYPES:
        if stream_type == key:
            return import_string(addr)
    else:
        raise Exception("Feed system not found")


class BaseFeed(object):
    def __init__(self, stream):
        self.stream = stream

    def update(self):
        entries = self._get_entries()
        for entry in entries:
            try:
                self._create_or_update_post(entry)
            except HTTPError:
                pass
            except Exception as err:
                url = self._get_entry_url(entry)
                print err, url,


class RssFeed(BaseFeed):
    def _get_entries(self):
        feed = feedparser.parse(self.stream.remote_id)
        return feed['entries']

    def _get_entry_url(self, entry):
        return entry['link']

    def _get_post_attrs(self, entry):
        # XXX: Do not take description from RSS
        attrs = {
            'title': entry['title'],
            # 'tags': [t['term'] for t in entry['tags']],
        }
        if entry.get('updated_parsed'):
            attrs['modified_time'] = datetime.fromtimestamp(mktime(entry['updated_parsed']))
        if entry.get('published_parsed'):
            attrs['published_time'] = datetime.fromtimestamp(mktime(entry['published_parsed']))
        if entry.get('author'):
            attrs['author'] = entry['author']
        return attrs

    def _create_or_update_post(self, entry):
        from newsboard.models import Post
        url = self._get_entry_url(entry)
        post_attrs = self._get_post_attrs(entry)
        post = Post.objects.create_or_update_from_url(url, **post_attrs)
        post.streams.add(self.stream)
        return post


class FacebookFeed(BaseFeed):
    pass


class SitemapFeed(BaseFeed):
    pass
