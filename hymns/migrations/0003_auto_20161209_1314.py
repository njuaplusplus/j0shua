# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hymns', '0002_auto_20161209_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hymn',
            name='hymn_score',
            field=models.ImageField(blank=True, upload_to='scores/%Y/%m/%d', help_text='必须上传', verbose_name='歌谱', null=True),
        ),
    ]
