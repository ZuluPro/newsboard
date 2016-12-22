from __future__ import unicode_literals

from django.test import TestCase
from web_rich_object import functional_tests as utils
from newsboard import models
from newsboard import settings

TEST_STREAMS = [
    # RSS
    ('sebsauvage', {'name': 'Seb Sauvage', 'type': 'rss', 'remote_id': 'http://sebsauvage.net/links/index.php?do=rss'}),
    ('lehollandaisvolant', {'name': 'Le Hollandais Volant', 'type': 'rss', 'remote_id': 'http://lehollandaisvolant.net/rss.php?mode=links'}),
    ('korben', {'name': 'Korben', 'type': 'rss', 'remote_id': 'http://feeds2.feedburner.com/KorbensBlog-UpgradeYourMind'}),
    ('zataz', {'name': 'Zataz', 'type': 'rss', 'remote_id': 'http://feeds.feedburner.com/ZatazNews'}),
    ('sametmax_rss', {'name': 'Sam et Max RSS', 'type': 'rss', 'remote_id': 'http://sametmax.com/feed/rss/'}),
    # Sitemap
    # ('sametmax_sitemap', {'name': 'Sam et Max Sitemap index', 'type': 'sitemap', 'remote_id': 'http://sametmax.com/sitemap.xml'}),
    ('anthonymonthe', {'name': "Anthony Monthe's blog", 'type': 'sitemap', 'remote_id': 'https://anthony-monthe.me/sitemap-blog.xml'}),
    ('agenceinfolibre', {'name': 'Agence Info Libre', 'type': 'sitemap', 'remote_id': 'http://www.agenceinfolibre.fr/post-sitemap2.xml'}),
    ('django', {'name': 'Django', 'type': 'sitemap', 'remote_id': 'https://www.djangoproject.com/sitemap.xml'}),
    ('djangogirls', {'name': 'Django Girls', 'type': 'sitemap', 'remote_id': 'http://blog.djangogirls.org/sitemap1.xml'}),
    # Facebook
    ('permapourlesnuls', {'name': 'Permaculture pour les nuls', 'type': 'facebook', 'remote_id': '1591830631108492'}),
    ('permaculture', {'name': 'Permaculture', 'type': 'facebook', 'remote_id': '413912175295682'}),
    ('energielibre', {'name': 'Enegergie Libre', 'type': 'facebook', 'remote_id': '787592527964816'}),
    ('fandechampignons', {'name': 'Fan de champignons', 'type': 'facebook', 'remote_id': '945469548856376'}),
    ('quelestcechampignon', {'name': 'Quel est ce champignon', 'type': 'facebook', 'remote_id': '293307764341181'}),
]


def gen_test(stream_attrs):
    def func(self):
        if not settings.FACEBOOK_TOKEN and stream_attrs['type'] == 'facebook':
            self.skipTest("Set env vars NEWSBOARD_FACEBOOK_TOKEN to test.")
        limit = 3
        stream = models.Stream.objects.create(**stream_attrs)
        stream.update_posts(limit=limit)
        # Test attrs
        posts = stream.post_set.all()
        self.assertTrue(posts.exists())
        self.assertLessEqual(posts.count(), limit)
    return func


class MetaFunctionalTest(type):
    def __new__(mcls, name, bases, attrs):
        for key, stream_attrs in TEST_STREAMS:
            func_name = 'test_%s_%s' % (stream_attrs['type'], key)
            func = gen_test(stream_attrs)
            attrs[func_name] = func
        return type.__new__(mcls, name, bases, attrs)


class FunctionalTest(TestCase):
    __metaclass__ = MetaFunctionalTest
    maxDiff = None
