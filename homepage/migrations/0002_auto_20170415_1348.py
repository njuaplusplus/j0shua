# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='openid',
            field=models.CharField(help_text='开发者可通过OpenID来获取用户基本信息', max_length=255, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user_profile',
            name='unionid',
            field=models.CharField(help_text='同一用户，对同一个微信开放平台下的不同应用，unionid是相同的', max_length=255, default=''),
            preserve_default=False,
        ),
    ]
