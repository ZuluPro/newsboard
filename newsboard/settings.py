import logging.config
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
import newsboard.log


DEFAULT_STREAM_TYPES = [
    ('newsboard.feeds.rss.RssFeed', 'rss', _("RSS")),
    ('newsboard.feeds.sitemap.SitemapFeed', 'sitemap', _("Sitemap")),
    ('newsboard.feeds.facebookfeed.FacebookFeed', 'facebook', _("Facebook")),
]

# Logging
LOGGING = getattr(settings, 'DBBACKUP_LOGGING', newsboard.log.DEFAULT_LOGGING)
LOG_CONFIGURATOR = logging.config.DictConfigurator(LOGGING)
LOG_CONFIGURATOR.configure()

DEFAULT_USER_AGENT = 'Newsboard Client (https://github.com/ZuluPro/newsboard)'

STREAM_TYPES = getattr(settings, 'NEWSBOARD_STREAM_TYPES', [])
STREAM_TYPES += DEFAULT_STREAM_TYPES

DISPLAY_LIMIT = getattr(settings, 'NEWSBOARD_DISPLAY_LIMIT', 15)
UPDATE_LIMIT = getattr(settings, 'NEWSBOARD_UPDATE_LIMIT', 25)

USER_AGENT = getattr(settings, 'NEWSBOARD_USER_AGENT', DEFAULT_USER_AGENT)

LOCK_CACHE = getattr(settings, 'NEWSGROUP_LOCK_CACHE', 'default')
LOCK_TIMEOUT = getattr(settings, 'NEWSGROUP_LOCK_TIMEOUT', 30)
LOCK_SALT = getattr(settings, 'NEWSGROUP_LOCK_SALT', None)

FACEBOOK_TOKEN = getattr(settings, 'NEWSBOARD_FACEBOOK_TOKEN', None)
