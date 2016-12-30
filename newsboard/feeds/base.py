try:
    from urllib import HTTPError
except ImportError:
    from urllib2 import HTTPError
from django.template import defaultfilters
from newsboard import settings


class BaseFeed(object):
    def __init__(self, stream):
        self.stream = stream

    def _get_entries(self, limit):
        """Return entries in asc order and limited in number"""
        raise NotImplementedError()

    def _get_post_attrs(self, entry):
        """Return Post attrs from an entry."""
        raise NotImplementedError()

    def update(self, limit=None):
        limit = limit or settings.UPDATE_LIMIT
        entries = self._get_entries(limit=limit)
        for index, entry in enumerate(entries):
            if index > limit:
                break
            try:
                self._create_or_update_post(entry)
            except HTTPError:
                pass

    def _create_or_update_post(self, entry):
        from newsboard.models import Post
        url = self._get_entry_url(entry)
        post_attrs = self._get_post_attrs(entry)
        post_attrs = self._clean_attrs(post_attrs)
        post = Post.objects.create_or_update_from_url(url, **post_attrs)
        post.streams.add(self.stream)
        return post

    def _clean_attrs(self, attrs):
        if 'title' in attrs:
            attrs['title'] = defaultfilters.truncatechars(attrs['title'], 300)
        return attrs
