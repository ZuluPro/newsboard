from django.conf import settings
from django.utils.translation import ugettext_lazy as _


DEFAULT_STREAM_TYPES = [
    ('newsboard.feeds.RssFeed', 'rss', _("RSS")),
    ('newsboard.feeds.FacebookFeed', 'facebook', _("Facebook")),
]

STREAM_TYPES = getattr(settings, 'NEWSBOARD_STREAM_TYPES', [])
STREAM_TYPES += DEFAULT_STREAM_TYPES
