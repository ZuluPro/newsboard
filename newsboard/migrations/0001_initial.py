# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dj_web_rich_object', '0006_auto_20161219_1809'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('webrichobject_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dj_web_rich_object.WebRichObject')),
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
                ('type', models.CharField(max_length=20, verbose_name='type', choices=[(b'rss', 'RSS'), (b'facebook', 'Facebook')])),
                ('remote_id', models.CharField(max_length=200, verbose_name='remote ID')),
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
