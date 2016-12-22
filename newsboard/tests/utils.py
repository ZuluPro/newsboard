from django import db
from web_rich_object.tests import factories as wro_factories
from newsboard import models
from newsboard.feeds.base import BaseFeed


class DummyFeed(BaseFeed):
    entries = []

    def _get_entry_url(self, entry):
        return entry.url

    def _get_entries(self, limit):
        if not self.entries:
            self.entries = wro_factories.WebRichObjectFactory.build_batch(limit)
        return self.entries

    def _get_post_attrs(self, entry):
        attrs = entry.__dict__.copy()
        for name, value in entry.__dict__.iteritems():
            if name.startswith('_') or name == 'url':
                del attrs[name]
                continue
            try:
                models.Post._meta.get_field(name)
            except db.models.FieldDoesNotExist:
                del attrs[name]
        return attrs
