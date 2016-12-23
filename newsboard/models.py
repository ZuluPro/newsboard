from __future__ import unicode_literals

from datetime import timedelta

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.core.urlresolvers import reverse

from dj_web_rich_object import models as wro_models

from newsboard import settings
from newsboard import feeds

STREAM_TYPES = [(k, v) for a, k, v in settings.STREAM_TYPES]


@python_2_unicode_compatible
class Stream(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    slug = models.CharField(max_length=100, verbose_name=_("slug"))
    description = models.TextField(max_length=2000, blank=True, null=True, verbose_name=_("description"))
    type = models.CharField(max_length=20, choices=STREAM_TYPES, verbose_name=_('type'))
    remote_id = models.CharField(max_length=200, verbose_name=_("remote ID"))

    main_url = models.URLField(blank=True, null=True, default=None, verbose_name=_("main URL"))
    last_updated = models.DateTimeField(blank=True, null=True, default=None, verbose_name=_("last updated"))

    auto_enabled = models.BooleanField(default=False, verbose_name=_("auto update enabled"))
    auto_frequency = models.PositiveIntegerField(default=15, verbose_name=_("auto update frequency"), help_text=_("each x minute"))

    # is_public = models.BooleanField(default=False, verbose_name=_("public")
    # is_hidden = models.BooleanField(default=False, verbose_name=_("hidden")

    class Meta:
        app_label = 'newsboard'
        verbose_name = _("stream")
        verbose_name_plural = _("streams")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('stream-detail', kwargs={'slug': self.slug})

    @property
    def feed(self):
        if not hasattr(self, '_feed'):
            self._feed = feeds.get_feed(self.type)(self)
        return self._feed

    def update_posts(self, limit=None):
        self.feed.update(limit=limit)
        self.last_updated = now()
        self.save()

    def last_posts(self):
        return self.post_set\
            .filter(is_removed=False)\
            .order_by('-updated_at')[:settings.DISPLAY_LIMIT]

    def need_update(self):
        if self.last_updated is None:
            return True
        expiration = self.last_updated + timedelta(seconds=self.auto_frequency*60)
        return now() > expiration


@python_2_unicode_compatible
class Post(wro_models.WebRichObject):
    streams = models.ManyToManyField(Stream, verbose_name=_("streams"))
    is_removed = models.BooleanField(default=False, verbose_name=_("removed"))

    objects = wro_models.WebRichObjectManager()

    class Meta:
        app_label = 'newsboard'
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'id': self.id})

    def get_remove_url(self):
        return reverse('post-remove', kwargs={'pk': self.id})
