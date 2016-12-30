from __future__ import absolute_import

from datetime import timedelta, datetime
try:
    from urllib import quote
except ImportError:
    from urllib2 import quote

import facebook

from django.template import defaultfilters

from newsboard.feeds.base import BaseFeed
from newsboard import settings

FEEDS_Q = '%s?fields=feed.limit(%s){picture,updated_time,description,caption,created_time,permalink_url,from,type,attachments{description,title,type,media,description_tags,url},source,message,message_tags,full_picture}'


def get_facebook_api(token=None):
    token = token or settings.FACEBOOK_TOKEN
    return facebook.GraphAPI(token)


def parse_facebook_time(date_str):
    date = datetime.strptime(date_str[:-5], '%Y-%m-%dT%H:%M:%S')
    offset = int(date_str[-5:-2])
    utc_offset = timedelta(seconds=offset*3600)
    return date + utc_offset


class FacebookFeed(BaseFeed):
    def _get_entry_url(self, entry):
        return entry['permalink_url']

    def _get_entries(self, limit):
        api = get_facebook_api()
        url = FEEDS_Q % (self.stream.remote_id, limit)
        return api.get_object(url)['feed']['data']

    def _get_post_attrs(self, entry):
        attrs = {
            'author': entry['from']['name'],
            'type': entry['type'],
            'created_time': parse_facebook_time(entry['created_time']),
            'published_time': parse_facebook_time(entry['created_time']),
            'modified_time': parse_facebook_time(entry['updated_time']),
            'base_url': entry['permalink_url'],
        }
        if entry['type'].startswith('video'):
            embed_video = 'https://www.facebook.com/plugins/video.php?href='
            embed_video += quote(entry['attachments']['data'][0]['url'])
            attrs.update({
                'video': embed_video,
                'description': None,
            })
            if entry.get('description'):
                attrs['title'] = defaultfilters.truncatechars(entry['description'], 300)
            if entry['attachments']['data'][0].get('media'):
                if 'image' in entry['attachments']['data'][0]['media']:
                    attrs['image'] = entry['attachments']['data'][0]['media']['image']['src']
        elif entry['type'] == 'status':
            attrs['description'] = None
            if entry.get('message'):
                attrs['title'] = defaultfilters.truncatechars(entry['message'], 300)
        elif entry['type'] == 'link':
            if entry.get('description'):
                attrs['title'] = entry['description']
                attrs['description'] = None
            if entry.get('attachments'):
                if 'media' in entry['attachments']['data'][0]:
                    if 'image' in entry['attachments']['data'][0]['media']:
                        attrs['image'] = entry['attachments']['data'][0]['media']['image']['src']
        elif entry['type'] == 'photo':
            # Guess image
            if entry.get('full_picture'):
                attrs['image'] = entry['full_picture']
            elif 'media' in entry['attachments']['data'][0]:
                attrs['image'] = entry['attachments']['data'][0]['media']['image']['src']
            # Guess from obj
            if entry.get('message'):
                attrs['title'] = defaultfilters.truncatechars(entry['message'], 300)
            if entry.get('description'):
                if attrs.get('title'):
                    attrs['description'] = entry['description']
                else:
                    attrs['description'] = None
            # Guess link
            elif 'link' in entry:
                if entry['attachments']['data'][0]['media'].get('title'):
                    attrs['title'] = defaultfilters.truncatechars(entry['attachments']['data'][0]['media']['title'], 300)
                if entry.get('message'):
                    if 'title' not in attrs:
                        attrs['title'] = defaultfilters.truncatechars(entry['message'], 300)
                        attrs['description'] = None
                    else:
                        attrs['description'] = entry['message']

            # Guess description
            if 'description' in entry:
                if attrs.get('title') != entry['description']:
                    attrs['description'] = entry['description']
        return attrs
