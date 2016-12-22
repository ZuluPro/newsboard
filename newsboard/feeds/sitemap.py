try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
from bs4 import BeautifulSoup
from newsboard.feeds.base import BaseFeed
from newsboard import settings


class SitemapFeed(BaseFeed):
    def _get_entry_url(self, entry):
        return entry.find('loc').text

    def _get_entries(self, limit):
        url = self.stream.remote_id
        headers = {
            'User-Agent': settings.USER_AGENT,
        }
        req = Request(url.encode('utf-8'), headers=headers)
        xml = urlopen(req).read()
        soup = BeautifulSoup(xml, "lxml")
        entries = soup.findAll("url")[:limit]
        return entries

    def _get_post_attrs(self, entry):
        attrs = {}
        return attrs
