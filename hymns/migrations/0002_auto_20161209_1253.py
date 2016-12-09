# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hymns', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hymn',
            name='hymn_compressed_score_url',
            field=models.CharField(max_length=255, blank=True, verbose_name='1920x的七牛key', help_text='不超过 255 个字符'),
        ),
        migrations.AddField(
            model_name='hymn',
            name='hymn_score_url',
            field=models.CharField(max_length=255, blank=True, verbose_name='原图的七牛key', help_text='不超过 255 个字符'),
        ),
    ]
