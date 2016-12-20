from __future__ import absolute_import
from datetime import timedelta, datetime
import facebook
from newsboard.feeds.base import BaseFeed
from newsboard import settings

FEEDS_Q = '%s?fields=feed.limit(%s){picture,updated_time,description,caption,created_time,permalink_url,from,type,attachments{description,title,type,media,description_tags,url},source,message,message_tags}'


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

    def _get_entries(self):
        api = get_facebook_api()
        url = FEEDS_Q % (self.stream.remote_id, settings.UPDATE_LIMIT)
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
            attrs.update({
                'description': entry['description'],
                # 'url': entry['attachments']['data'][0]['media']['image']['src'],
                'image': entry['attachments']['data'][0]['media']['image']['src'],
            })
        elif entry['type'] == 'status':
            attrs.update({
                'description': entry['message'][:300],
                'title': entry['message'][:100],
            })
        elif entry['type'] == 'link':
            attrs.update({
                'image': entry['attachments']['data'][0]['media']['image']['src'],
            })
        elif entry['type'] == 'photo':
            if 'media' in entry['attachments']['data'][0]:
                attrs['image'] = entry['attachments']['data'][0]['media']['image']['src']
            elif 'link' in entry:
                attrs['image'] = entry['link']
        if entry.get('attachments') and entry['attachments']['data']:
            if 'title' not in attrs:
                if 'title' in entry['attachments']['data'][0]:
                    attrs['title'] = entry['attachments']['data'][0]['title']
                if 'title' not in attrs and 'message' in entry:
                    attrs['title'] = entry['message'][:100]
                if 'title' not in attrs and 'description' in entry:
                    attrs['title'] = entry['description'][:100]
            if 'description' in entry['attachments']['data'][0]:
                attrs['description'] = entry['attachments']['data'][0]['description']
        return attrs
