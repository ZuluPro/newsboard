from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from dj_web_rich_object import models as wro_models

from newsboard import settings
from newsboard import feeds

STREAM_TYPES = [(k, v) for a, k, v in settings.STREAM_TYPES]


@python_2_unicode_compatible
class Stream(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    type = models.CharField(max_length=20, choices=STREAM_TYPES, verbose_name=_('type'))
    remote_id = models.CharField(max_length=200, verbose_name=_("remote ID"))

    # main_url = models.URLField(blank=True, null=True, default=None, verbose_name=_("main URL"))
    # last_updated = models.DateTimeField(blank=True, null=True, default=None, verbose_name=_("last updated"))
    # auto_enabled = models.BooleanField(default=False, verbose_name=_("auto update enabled")

    class Meta:
        app_label = 'newsboard'
        verbose_name = _("stream")
        verbose_name_plural = _("streams")

    def __str__(self):
        return self.name

    @property
    def feed(self):
        if not hasattr(self, '_feed'):
            self._feed = feeds.get_feed(self.type)(self)
        return self._feed

    def update(self):
        self.feed.update()

    def last_posts(self):
        return self.post_set.all()[:10]#.order_by('published_time')


@python_2_unicode_compatible
class Post(wro_models.WebRichObject):
    streams = models.ManyToManyField(Stream, verbose_name=_("streams"))

    objects = wro_models.WebRichObjectManager()

    class Meta:
        app_label = 'newsboard'
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def __str__(self):
        return self.title