from datetime import timedelta

from django.test import TestCase
from django.utils.timezone import now

from web_rich_object.tests import utils as wro_utils

from newsboard import settings
from newsboard import models
from newsboard.feeds.rss import RssFeed
from newsboard.feeds.facebook import FacebookFeed
from newsboard.feeds.sitemap import SitemapFeed
from newsboard.tests import factories, utils


class StreamTest(wro_utils.BaseWebRichObjectTestCase, TestCase):
    def test_update_posts(self):
        stream = factories.StreamFactory(type='dummy')
        stream.update_posts()
        self.assertTrue(models.Stream.objects.exists())
    test_update_posts.mock_attrs = {
        'return_value.read.return_value': '',
        'return_value.info.return_value.__dict__': wro_utils.HTML_RESPONSE_INFO
    }

    def test_feed(self):
        stream = factories.StreamFactory(type='rss')
        self.assertIsInstance(stream.feed, RssFeed)
        stream = factories.StreamFactory(type='facebook')
        self.assertIsInstance(stream.feed, FacebookFeed)
        stream = factories.StreamFactory(type='sitemap')
        self.assertIsInstance(stream.feed, SitemapFeed)
        stream = factories.StreamFactory(type='dummy')
        self.assertIsInstance(stream.feed, utils.DummyFeed)

    def test_last_posts(self):
        stream = factories.StreamFactory()
        old_posts = factories.PostFactory.create_batch(settings.DISPLAY_LIMIT,
                                                       streams=[stream])
        old_last_posts = stream.last_posts()
        for post in old_posts:
            self.assertIn(post, old_last_posts)
        # Test if not in new
        new_posts = factories.PostFactory.create_batch(settings.DISPLAY_LIMIT,
                                                       streams=[stream])
        new_last_posts = stream.last_posts()
        for post in new_posts:
            self.assertNotIn(post, old_last_posts)
            self.assertIn(post, new_last_posts)

    def test_need_update(self):
        # Test not need
        yesterday = now() - timedelta(days=1)
        stream = factories.StreamFactory(last_updated=yesterday, auto_frequency=2)
        self.assertTrue(stream.need_update())
        # test need
        stream.last_updated = now()
        self.assertFalse(stream.need_update())
