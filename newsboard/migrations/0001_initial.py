# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dj_web_rich_object', '0007_webrichobject_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('webrichobject_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dj_web_rich_object.WebRichObject')),
                ('is_removed', models.BooleanField(default=False, verbose_name='removed')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
            },
            bases=('dj_web_rich_object.webrichobject',),
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.CharField(max_length=100, verbose_name='slug')),
                ('description', models.TextField(max_length=2000, null=True, verbose_name='description', blank=True)),
                ('type', models.CharField(max_length=20, verbose_name='type', choices=[(b'rss', 'RSS'), (b'sitemap', 'Sitemap'), (b'facebook', 'Facebook'), (b'dummy', 'Dummy'), (b'rss', 'RSS'), (b'sitemap', 'Sitemap'), (b'facebook', 'Facebook')])),
                ('remote_id', models.CharField(max_length=200, verbose_name='remote ID')),
                ('main_url', models.URLField(default=None, null=True, verbose_name='main URL', blank=True)),
                ('last_updated', models.DateTimeField(default=None, null=True, verbose_name='last updated', blank=True)),
                ('auto_enabled', models.BooleanField(default=False, verbose_name='auto update enabled')),
                ('auto_frequency', models.PositiveIntegerField(default=15, help_text='each x minute', verbose_name='auto update frequency')),
            ],
            options={
                'verbose_name': 'stream',
                'verbose_name_plural': 'streams',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='streams',
            field=models.ManyToManyField(to='newsboard.Stream', verbose_name='streams'),
        ),
    ]
